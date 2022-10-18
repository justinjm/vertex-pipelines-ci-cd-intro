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
    git clone https://github.com/justinjm/<REPO-NAME>
    ```

TODO - Add correct link above and add button below:  


https://ssh.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https://github.com/justinjm/<REPO-NAME>.git

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)]()



4. Create a cloud storage bucket 


6. Create artifact registry 



7. Setup GitHub Build trigger 

[Building repositories from GitHub  |  Cloud Build Documentation  |  Google Cloud](https://cloud.google.com/build/docs/automating-builds/github/build-repos-from-github)




## Workflow 