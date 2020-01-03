#~/bin/sh
export PROJECT_ID="meganzhao-test"
# gcloud config set account meganzhao@premium-cloud-support.com
# gcloud config set project meganzhao-test
export GOOGLE_APPLICATION_CREDENTIALS_PATH="/Users/meganzhao/Downloads/retail-api-svc/service-acc.json"
kubectl create secret generic svc-key --from-file $GOOGLE_APPLICATION_CREDENTIALS_PATH
kubectl create configmap env-vars --from-literal=env.project-id=$PROJECT_ID -o yaml --dry-run | kubectl apply -f -