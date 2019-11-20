# Retail-Banking-Microservices-Demo

## Quickstart

1. Install requirements

   - [skaffold](https://skaffold.dev/docs/install/)

   - [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
   - [Docker](https://docs.docker.com/v17.12/install/)
2. Generate kubeconfig for your kubernetes cluster. The services will be deployed to this cluster
   - For local development you can use k8s with Docker Desktop
   - You can also configure kubeconfig for a remote cluster. With gcloud, `gcloud container clusters get-credentials [$CLUSTER_NAME] --project [$PROJECT_NAME] --[region/zone] [$REGION/ZONE]`
3. Configure service account secret for the services to use.
   - Run `kubectl create secret generic svc-key --from-file [$ABSOLUTE_PATH_TO_KEY]/service-acc.json` to make a k8s secret to store credentials
4. Configure project id as a configmap for the services to use.
   - Run `kubectl create configmap env-vars --from-literal=env.project-id=[$PROJECT_ID] -o yaml --dry-run | kubectl apply -f -` to make a k8s configmap with project id
5. Build and run services by following any one of the steps below.
   - Run `skaffold run` for running locally
   - Run `skaffold run --default-repo=gcr.io/[$PROJECT_ID]` for getting images from remote registry
   - RUN `skaffold run -p gcb --default-repo=gcr.io/[$PROJECT_ID]` for remotely building docker images
   - Run `skaffold dev --default-repo=gcr.io/[$PROJECT_ID]` for constantly watching code changes locally and rebuilding locally
   - Run `skaffold dev -p gcb --default-repo=gcr.io/[$PROJECT_ID]` for constantly watching code changes locally and rebuilding remotely

6. Application should be available at service external IP or localhost
   - Frontend: localhost/svc-external-ip:80
   - ProfileService: localhost/svc-external-ip:8080

## frontend

## frontendservice

## profileservice

## transactionservice

## transferservice