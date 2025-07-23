argocd installation:
kubectl apply -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/crds.yaml
kubectl apply -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

helm upgrade --install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=aip3-cluster \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller \
  --set vpcId=vpc-0a5e30813d32f424b \
  --set region=us-east-1 \
  --version 1.13.0

aws dynamodb create-table \
  --table-name ideas-table \
  --attribute-definitions \
      AttributeName=user_id,AttributeType=S \
      AttributeName=session_id,AttributeType=S \
  --key-schema \
      AttributeName=user_id,KeyType=HASH \
      AttributeName=session_id,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1