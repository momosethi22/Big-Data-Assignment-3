import json
from time import sleep
from kafka import KafkaProducer

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Path to preprocessed data file
preprocessed_data_file = '/home/momo/Downloads/subset_Amazon_Meta.json'

# Function to read preprocessed data and send to Kafka topic
def stream_data():
    with open(preprocessed_data_file, 'r') as file:
        for line in file:
            sleep(0.5)
            try:
                data = json.loads(line)
                # Extract 'also_buy' column
                also_buy = data.get('also_buy', [])
                # Send each 'also_buy' item as a separate message to Kafka topic
                
                producer.send('topic1', json.dumps(also_buy).encode('utf-8'))
                print("Sent data to Kafka topic: topic1")
            except Exception as e:
                print(f"Error streaming data: {e}")

if __name__ == "__main__":
    stream_data()

