#####################################################################
#
# setup
#
#####################################################################


# imports for this notebook to run
import sys, json
from datetime import datetime
from typing import NamedTuple

from google.cloud import aiplatform as vertex
from google_cloud_pipeline_components.experimental import vertex_notification_email as gcc_exp

import kfp
from kfp.v2 import dsl, compiler
from kfp.v2.dsl import (Artifact, Dataset, Input, InputPath, Model, Metrics, Output, OutputPath, component)


# specify parameters
PROJECT_ID = "your-project"
REGION = "us-central1"
BUCKET_NAME = f"bkt-{PROJECT_ID}-vpipelines"
BUCKET_PATH = f"gs://{BUCKET_NAME}"
PIPELINE_ROOT = f"{BUCKET_PATH}/pipeline_root"
PIPELINE_DATA = f"{BUCKET_PATH}/data"
TIMESTAMP = datetime.now().strftime("%Y%m%d%H%M%S")


#####################################################################
#
# create individual pipeline components, then specify the pipeline
#
#####################################################################


# Download BigQuery data and convert to CSV
@component(
    packages_to_install=["google-cloud-bigquery", "pandas", "pyarrow", "db-dtypes"],
    base_image="python:3.9",
    output_component_file="component_create_dataset.yaml"
)
def get_dataframe(
    bq_table: str,
    output_data_path: OutputPath("Dataset")
):
    from google.cloud import bigquery
    import pandas as pd
    import os

    project_number = os.environ["CLOUD_ML_PROJECT_ID"]
    bqclient = bigquery.Client(project=project_number)
    table = bigquery.TableReference.from_string(
        bq_table
    )
    rows = bqclient.list_rows(
        table
    )
    dataframe = rows.to_dataframe(
        create_bqstorage_client=True,
    )
    dataframe = dataframe.sample(frac=1, random_state=2)
    dataframe.to_csv(output_data_path)

# score data using a custom sklearn model
@component(
    packages_to_install=["sklearn", "pandas", "numpy"]
    , base_image="python:3.9"
    , output_component_file="component_score_data.yaml"
)
def score_data(
    # inputs
    model: Input[Model]
    , to_score_data: Input[Dataset]
    # outputs
    , scored_data: Output[Dataset]
):

    import pickle
    import pandas as pd
    import numpy as np
    
    # load the model
    skmodel = pickle.load(open(model.path , 'rb'))
    
    # load the data
    df = pd.read_csv(to_score_data.path)
    labels = df.pop("label").tolist()
    data = df.values.tolist()
    
    # score data
    predictions = skmodel.predict_proba(data)
    
    # write predictions    
    predictions_file = 'predictions.csv'
    num_cols = predictions.shape[1]
    col_names = ','.join([f"prob_{i}" for i in range(num_cols)])
    np.savetxt(  predictions_file
               , predictions
               , delimiter=','
               , fmt='%f'
               , header=col_names
               , comments="")
    # metadata
    scored_data.uri = scored_data.uri  + ".csv"

pipeline_name = "python-batch-predict-sklearn"
pipeline_description = "my pipeline description"

# define a pipeline
@dsl.pipeline(name=pipeline_name, description=pipeline_description)

# specify all the inputs the pipeline needs to run
def my_pipeline(
    bq_table: str = "",
    output_data_path: str = "data.csv",
    project_id: str = PROJECT_ID,
    region: str = REGION
):
    # pipeline graph
    
    # import model from GCS location
    importer_task = dsl.importer(
        artifact_uri = 'gs://path-to-champion-model/model.pkl',
        artifact_class = dsl.Model,
        reimport = True,
        metadata = {'model_name': "sklearn GradientBoostingClassifier"}
    )
    
    # import data to score
    dataset_task = get_dataframe(bq_table)
    
    # apply model to data
    score_data_task = score_data(importer_task.output, dataset_task.output)    

# compile the pipeline
my_package_path = 'my_vertex_pipeline_specification_file.json'
compiler.Compiler().compile(pipeline_func=my_pipeline, package_path=my_package_path)

# runtime parameters to pass to pipeline
pipeline_params = {"bq_table": "your-project.your-ds.your-table"}

# run the pipeline
vertex.init(project=PROJECT_ID)

job = vertex.PipelineJob(
    display_name = pipeline_name
    , template_path = my_package_path
    , pipeline_root = PIPELINE_ROOT
    , parameter_values = pipeline_params
    , enable_caching = False
)

job.submit()
