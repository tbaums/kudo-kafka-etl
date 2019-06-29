kubectl delete deploy/kafka-app


docker build . -t tbaums/kudo-kafka-app
docker push tbaums/kudo-kafka-app

sleep 2



kubectl apply -f kafka-app.yaml
kubectl apply -f kafka-app-ingress.yaml

sleep 15
kubectl logs -f -l app=kafka-app 

