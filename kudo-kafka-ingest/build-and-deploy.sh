docker build . -t tbaums/kudo-kafka-ingest
docker push tbaums/kudo-kafka-ingest

sleep 2

kubectl delete deploy/kafka-ingest

kubectl apply -f ingest.yaml