# Vertex AI Pipelines CI/CD Introduction

An introduction to CI/CD workflow on Vertex AI through example. 


## Setup 

1.  [In the GCP Cloud Shell](https://console.cloud.google.com/home/dashboard?cloudshell=true), run the commands below.  Be sure to replace your project ID in the first line.
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
        --location=us-central1-a 
    ```

3.  Once the notebook instance is created, clone this repository via the GUI or terminal: 
    ```sh
    git clone https://github.com/justinjm/vertex-pipelines-ci-cd-intro.git
    ```

**Optional** You can also work from the Cloud Shell and click the button below to clone and open this repository in your own Cloud Shell instance:  

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://ssh.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https://github.com/justinjm/vertex-pipelines-ci-cd-intro.git)

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


6. Create artifact registry 

```sh 
! gcloud artifacts repositories create $PRIVATE_REPO --repository-format=docker \
    --location=$REGION \
    --description="Docker repository"

! gcloud artifacts repositories list
```

7. Setup GitHub Build trigger 

[Building repositories from GitHub  |  Cloud Build Documentation  |  Google Cloud](https://cloud.google.com/build/docs/automating-builds/github/build-repos-from-github)


### Constants 

```
PROJECT_ID= 
REGION= 
BUCKET_NAME= 
PRIVATE_REPO= 
```

## Workflow 

TODO




## Resources 

* GCP official [Notebook examples](https://cloud.google.com/vertex-ai/docs/pipelines/notebooks)
* Codelabs:
  * [Intro to Vertex Pipelines](https://codelabs.developers.google.com/vertex-pipelines-intro)  
  * [Using Vertex ML Metadata with Pipelines](https://codelabs.developers.google.com/vertex-mlmd-pipelines)  
* [Schedule pipeline execution with Cloud Scheduler](https://cloud.google.com/vertex-ai/docs/pipelines/schedule-cloud-scheduler)  
* [Python reference](https://cloud.google.com/python/docs/reference/aiplatform/latest/google.cloud.aiplatform)
* [vertex-ai-labs/vertex\_ai\_pipelines\_r\_model.ipynb at main · RajeshThallam/vertex-ai-labs](https://github.com/RajeshThallam/vertex-ai-labs/blob/main/06-vertex-train-deploy-r-model/vertex_ai_pipelines_r_model.ipynb) - example with R 