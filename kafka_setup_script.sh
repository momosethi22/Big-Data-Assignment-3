#!/bin/bash

# Start Zookeeper in a new terminal
gnome-terminal -- bash -c '/home/momo/kafka/bin/zookeeper-server-start.sh config/zookeeper.properties; exec bash'

# Start Kafka Server in a new terminal
gnome-terminal -- bash -c '/home/momo/kafka/bin/kafka-server-start.sh config/server.properties; exec bash'

# Wait for Kafka to start (adjust sleep time as needed)
sleep 10

# Start the producer in a new terminal
gnome-terminal -- bash -c 'python3 /home/momo/kafka/producer.py; exec bash'

# Start Apriori consumer in a new terminal
gnome-terminal -- bash -c 'python3 /home/momo/kafka/consumerapriori.py; exec bash'

# Start PCY consumer in a new terminal
gnome-terminal -- bash -c 'python3 /home/momo/kafka/consumerpcy.py; exec bash'

# Start PCY consumer in a new terminal
gnome-terminal -- bash -c 'python3 /home/momo/kafka/consumerSON.py; exec bash'

# Wait for the consumers to finish (adjust sleep time as needed)
echo "Waiting for consumers to finish..."
sleep 10  # Adjust as needed

# Optional: Close all terminals after consumers finish
# gnome-terminal -- bash -c 'killall gnome-terminal'

