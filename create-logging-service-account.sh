#!/bin/sh 
PROJECT=$(gcloud config get-value project)

gcloud iam service-accounts create logging-service-account --display-name "logging-service-account"

gcloud projects add-iam-policy-binding $PROJECT \
  --member serviceAccount:logging-service-account@${PROJECT}.iam.gserviceaccount.com \
  --role roles/logging.logWriter

gcloud projects add-iam-policy-binding $PROJECT \
  --member serviceAccount:logging-service-account@${PROJECT}.iam.gserviceaccount.com \
  --role roles/editor

gcloud iam service-accounts keys create \
  logging-service-account.json \
  --iam-account logging-service-account@${PROJECT}.iam.gserviceaccount.com
