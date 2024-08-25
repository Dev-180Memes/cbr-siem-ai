#!/bin/bash

# Build and push Docker image
docker build -t gcr.io/cbr-siem-ai/cybersecurity-ai-app:v1 .
docker push gcr.io/cbr-siem-ai/cybersecurity-ai-app:v1

# Apply Kubernetes configurations
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml