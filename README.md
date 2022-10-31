# Vertex AI Pipelines CI/CD Introduction

An introduction to CI/CD workflow on Vertex AI through example. 

## Setup 

### Enable APIs 

1.  [In the GCP Cloud Shell](https://console.cloud.google.com/home/dashboard?cloudshell=true), run the commands below. 

```sh
export PROJECT=$DEVSHELL_PROJECT_ID

gcloud services enable aiplatform.googleapis.com --project $PROJECT_ID
gcloud services enable artifactregistry.googleapis.com --project $PROJECT_ID
gcloud services enable bigquerystorage.googleapis.com --project $PROJECT_ID
gcloud services enable cloudbuild.googleapis.com --project $PROJECT_ID
gcloud services enable clouddeploy.googleapis.com --project $PROJECT_ID
gcloud services enable container.googleapis.com --project $PROJECT_ID
gcloud services enable containerregistry.googleapis.com --project $PROJECT_ID
gcloud services enable monitoring.googleapis.com --project $PROJECT_ID
gcloud services enable notebooks.googleapis.com --project $PROJECT_ID
gcloud services enable run.googleapis.com --project $PROJECT_ID
```

### Create Workbench Notebook Instance

2.  Navigate to [Vertex Workbench User Managed Notebooks](https://console.cloud.google.com/ai-platform/notebooks) and create a python notebook instance (or use the cloud shell command below)
    1.  At the top of the screen, click "NEW NOTEBOOK"
    2.  Use the first option for a notebook "Python 3"
    3.  For the Region, select the first option "us-central1" 
    4.  Click "Create"
    ```sh
    gcloud notebooks instances create vertex-ai-pipelines-cicd-intro \
        --vm-image-project=deeplearning-platform-release \
        --vm-image-family=common-cpu-notebooks \
        --machine-type=n1-standard-4 \
        --location=us-central1-a \
        --post-startup-script=https://raw.githubusercontent.com/justinjm/vertex-pipelines-ci-cd-intro/main/notebook_startup.sh
    ```

**Optional** You can also work from the [Cloud Shell Editor](https://cloud.google.com/shell/docs/editor-overview) and click the button below to clone and open this repository in your own Cloud Shell instance:  

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://ssh.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https://github.com/justinjm/vertex-pipelines-ci-cd-intro.git)

3.a Complete workbench notebook instance setup by installing dependencies and restarting kernel

See notebook `00_setup.ipynb` 

### Create Cloud Storage Bucket

4. Create a cloud storage bucket 

create bucket and save the name for use later

```sh
BUCKET_NAME=gs://$GOOGLE_CLOUD_PROJECT-aip-pipeline-cicd
gsutil mb -l us-central1 $BUCKET_NAME
```

Now give our compute service account access to this bucket. This will ensure that Vertex Pipelines has the necessary permissions to write files to this bucket. Run the following command to add this permission: 

```sh
gcloud projects describe $GOOGLE_CLOUD_PROJECT > project-info.txt
PROJECT_NUM=$(cat project-info.txt | sed -nre 's:.*projectNumber\: (.*):\1:p')
SVC_ACCOUNT="${PROJECT_NUM//\'/}-compute@developer.gserviceaccount.com"
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT --member serviceAccount:$SVC_ACCOUNT --role roles/storage.objectAdmin
```

### Create Artifact Registry 

6. Create artifact registry 

See notebook `02_image_build.ipynb`

### 7. Setup Cloud Build Trigger

7.a. Create cloudbuild.yaml 

See `cloudbuild.yaml` for pre-built one, update with your constants as needed

7.b Setup GitHub Build trigger 

Setup a Cloud Build trigger to execute the vertex pipeline execution whenever a commit is made to the `main` branch in the repository 

First, [Connect to a GitHub repository](https://cloud.google.com/build/docs/automating-builds/github/connect-repo-github)

Then, setup a cloud build trigger from the connected GitHub repo via the Google Cloud Console: [Building repositories from GitHub  |  Cloud Build Documentation  |  Google Cloud](https://cloud.google.com/build/docs/automating-builds/github/build-repos-from-github)

Console:

* name: automl-beans
* region: us-central1
* description: Trigger for implementing CI/CD workflow for Vertex Pipelines 
* event: "push to a new branch"
* source: 
    * repository: select repository from dropdown
    * branch: `^main$`
* Configuration: Autodetected 

### Grant Vertex AI access to Cloud Build 

8. Grant permissions to vertex AI service agents 

Grant the following roles to the Cloud Build service account `{PROJECT-NUMBER}@cloudbuild.gserviceaccount.com`: 

* `Vertex AI Service Agent` (roles/aiplatform.serviceAgent)

You can do this in the console or via gclound: 

Console: 

1. Goto [IAM & Admin page](https://console.cloud.google.com/iam-admin/iam), select your project from the top dropdown 
2. Check the box on the right: "Include Google-provided role grants" 
3. Find Cloud Build default service account `{PROJECT-NUMBER}@cloudbuild.gserviceaccount.com`
4. Add role `Vertex AI Service Agent` (roles/aiplatform.serviceAgent)


gcloud: 

```sh
gcloud projects describe $GOOGLE_CLOUD_PROJECT > project-info.txt
PROJECT_NUM=$(cat project-info.txt | sed -nre 's:.*projectNumber\: (.*):\1:p')
SVC_ACCOUNT="${PROJECT_NUM//\'/}@cloudbuild.gserviceaccount.com"
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT --member serviceAccount:$SVC_ACCOUNT --role roles/aiplatform.serviceAgent
```
#### Resources 

* [IAM permissions  |  Vertex AI  |  Google Cloud](https://cloud.google.com/vertex-ai/docs/general/iam-permissions)
* [Access control with IAM  |  Vertex AI  |  Google Cloud](https://cloud.google.com/vertex-ai/docs/general/access-control#predefined-roles)
* [Troubleshooting Vertex AI  |  Google Cloud](https://cloud.google.com/vertex-ai/docs/general/troubleshooting#custom-trained_models)


## Workflow 

General workflow is as follows: 

1. Setup GCP environment: 
    * `README.md` (this document) - setup GCP environment
    * `00_setup.ipynb`  - setup notebook instabce
    * `02_image_build.ipynb` - create artifact registry 
2. write code to train and deploy pipeline 
    * `01_pipeline_build.ipynb` code here and generates file  `src/pipelines/train_pipeline.py` to be used in pipeline
    * `src/build_and_deploy.py` - main function for building and deploying Vertex Pipeline
    * `src/components/classification_eval_model_v2.py` - custom component for model evaluation 
    * `src/component_specs/classification_eval_model_v2.yaml` - create based on `src/components/classification_eval_model_v2.py`
3. create Dockerfile and build image (to containerize for CI/CD)
    * `02_image_build.ipynb`
4. manually run pipeline to test 
    * `03_pipeline_run.ipynb`
5. commit/push code to the linked repository 
6. Pipeline job submitted to Vertex AI

## Resources 

* GCP official [Notebook examples](https://cloud.google.com/vertex-ai/docs/pipelines/notebooks)
* Codelabs:
  * [Intro to Vertex Pipelines](https://codelabs.developers.google.com/vertex-pipelines-intro)  
  * [Using Vertex ML Metadata with Pipelines](https://codelabs.developers.google.com/vertex-mlmd-pipelines)  
* [Schedule pipeline execution with Cloud Scheduler](https://cloud.google.com/vertex-ai/docs/pipelines/schedule-cloud-scheduler)  
* [Python reference](https://cloud.google.com/python/docs/reference/aiplatform/latest/google.cloud.aiplatform)
* [vertex-ai-labs/vertex\_ai\_pipelines\_r\_model.ipynb at main · RajeshThallam/vertex-ai-labs](https://github.com/RajeshThallam/vertex-ai-labs/blob/main/06-vertex-train-deploy-r-model/vertex_ai_pipelines_r_model.ipynb) - example with R 
* Vertex Pipelines Setup 
  * [Configure your Google Cloud project for Vertex AI Pipelines](https://cloud.google.com/vertex-ai/docs/pipelines/configure-project#service-account)
  * [Use a custom service account  |  Vertex AI  |  Google Cloud](https://cloud.google.com/vertex-ai/docs/general/custom-service-account)