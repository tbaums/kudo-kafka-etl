kubectl delete deploy/kafka-pacman-consumer


docker build . -t tbaums/kafka-pacman-consumer
docker push tbaums/kafka-pacman-consumer

sleep 2



kubectl apply -f kafka-pacman-consumer.yaml

sleep 8
kubectl logs -f -l app=kafka-pacman-consumer 

