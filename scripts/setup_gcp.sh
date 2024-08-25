#!/bin/bash

# Set up GCP project
gcloud projects create your-project-id --name="Your Project Name"
gcloud config set project your-project-id

# Enable necessary APIs
gcloud services enable compute.googleapis.com container.googleapis.com aiplatform.googleapis.com bigquery.googleapis.com pubsub.googleapis.com securitycenter.googleapis.com spanner.googleapis.com

# Set up Cloud Spanner
gcloud spanner instances create cbr-instance --config=regional-us-central1 --description="CBR System Instance" --nodes=1
gcloud spanner databases create cbr-database --instance=cbr-instance

# Set up BigQuery
bq mk --dataset your-project-id:siem_logs
bq mk --table your-project-id:siem_logs.security_logs timestamp:TIMESTAMP,log_type:STRING,source_ip:STRING,destination_ip:STRING,event:STRING

# Set up Pub/Sub
gcloud pubsub topics create siem-logs-topic

# Create GKE cluster
gcloud container clusters create cybersecurity-ai-cluster --num-nodes=3 --zone=us-central1-a