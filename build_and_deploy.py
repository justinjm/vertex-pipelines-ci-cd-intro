#Initialize pipeline object
from pipelines.train_pipeline import pipeline_controller
import time

PROJECT_ID = "demos-vertex-ai"
REGION="us-central1"

BUCKET_NAME="gs://" + PROJECT_ID + "-aip-pipeline-cicd"
BUCKET_NAME

PIPELINE_ROOT = f"{BUCKET_NAME}/pipeline_root/"
PIPELINE_ROOT

DISPLAY_NAME = 'automl-beans{}'.format(str(int(time.time())))
DISPLAY_NAME

pipe = pipeline_controller(template_path="tab_classif_pipeline.json",
                           display_name="automl-tab-beans-training", 
                           pipeline_root=PIPELINE_ROOT,
                           project_id=PROJECT_ID,
                           region=REGION)

#Build and Compile pipeline
pipe._build_compile_pipeline()

#Submit Job
pipe._submit_job()
# TODO: add `service_account` parameter - https://cloud.google.com/python/docs/reference/aiplatform/latest/google.cloud.aiplatform.PipelineJob#google_cloud_aiplatform_PipelineJob_submit