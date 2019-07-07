kubectl delete deploy/kafka-pacman-producer


docker build . -t tbaums/kafka-pacman-producer
docker push tbaums/kafka-pacman-producer

sleep 2



kubectl apply -f kafka-pacman-producer.yaml

sleep 1
watch kubectl logs -l app=kafka-pacman-producer

