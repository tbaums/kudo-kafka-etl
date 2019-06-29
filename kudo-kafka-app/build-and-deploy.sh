docker build . -t tbaums/kudo-kafka-app
docker push tbaums/kudo-kafka-app

sleep 2

kubectl delete deploy/kafka-app

kubectl apply -f kafka-app.yaml
kubectl apply -f kafka-app-ingress.yaml