# Retail-Banking-Microservices-Demo

## Quickstart

1. Install requirements

   - [skaffold](https://skaffold.dev/docs/install/)
   - [istioctl](https://istio.io/docs/setup/getting-started/#download)
   - [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
   - [Docker](https://docs.docker.com/v17.12/install/)
2. Generate kubeconfig for your kubernetes cluster. The services will be deployed to this cluster
   - For local development you can use k8s with Docker Desktop
   - You can also configure kubeconfig for a remote cluster. 
        - With gcloud, to create cluster `gcloud container clusters create [$CLUSTER_NAME] --project [$PROJECT_NAME] --[region/zone] [$REGION/ZONE]`

        - To generate kubeconfig   `gcloud container clusters get-credentials [$CLUSTER_NAME] --project [$PROJECT_NAME] --[region/zone] [$REGION/ZONE]`
3. (Optional) Apply Istio manifests to cluster for **local** development
   - Run `istioctl manifest apply`
4. Create an fsi namespace and enable istio-injection
   - Run `kubectl create namespace fsi | kubectl label namespace fsi istio-injection=enabled` to create the fsi namespace and enable istio sidecar auto-injection for this namespace
5. Configure service account secret for the services to use.
   - Run `kubectl create secret generic svc-key -n fsi --from-file [$ABSOLUTE_PATH_TO_KEY]/service-acc.json` to make a k8s secret to store credentials
6. Configure project id as a configmap for the services to use.
   - Run `kubectl create configmap env-vars -n fsi --from-literal=env.project-id=[$PROJECT_ID] -o yaml --dry-run | kubectl apply -f -` to make a k8s configmap with project id
7. Build and run services by following any one of the steps below.
   - Run `skaffold run` for running locally
   - Run `skaffold run --default-repo=gcr.io/[$PROJECT_ID]` for getting images from remote registry
   - RUN `skaffold run -p gcb --default-repo=gcr.io/[$PROJECT_ID]` for remotely building docker images
   - Run `skaffold dev --default-repo=gcr.io/[$PROJECT_ID]` for constantly watching code changes locally and rebuilding locally
   - Run `skaffold dev -p gcb --default-repo=gcr.io/[$PROJECT_ID]` for constantly watching code changes locally and rebuilding remotely

8. Application URLs:
   - App URL: 
        - Local: http://localhost/ 
        - Remote: http://{istio-ingressgateway-ip}
   - Views:
        - /home
        - /about
        - /transfer
        - /transactions
   - API Endpoints:
        - /user: GET all users, POST new user
        - /user/{userId}: GET, DELETE, PUT a user
        - /api/transfer/{userId}: GET all user transfers, POST new user transfer
        - /api/transfer/{userId}: {transferId}: GET, PUT, DELETE a transfer
        - /api//transaction/{userId}: GET all user transactions, POST new user transaction
        - /api/transaction/{userId}/{transactionId}: GET, PUT, DELETE a transaction

## frontend

## frontendservice

## profileservice

## transactionservice

## transferservice