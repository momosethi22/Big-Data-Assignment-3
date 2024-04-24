import json
from kafka import KafkaConsumer
from collections import Counter, defaultdict
from itertools import combinations

# Initialize Kafka consumer
consumer = KafkaConsumer('topic1', bootstrap_servers='localhost:9092')


def apriori(rows, threshold):
    # Step 1: Find individual unique items and count occurrences
    item_counts = Counter(item for row in rows for item in set(row))
    
    # Filter items by threshold
    frequent_items = [(item, count) for item, count in item_counts.items() if count >= threshold]
    
    # Step 2: Generate pairs of frequent individual items
    frequent_pairs = []
    for pair in combinations([item for item, _ in frequent_items], 2):
        pair_count = sum(1 for row in rows if set(pair).issubset(set(row)))
        if pair_count >= threshold:
            frequent_pairs.append((pair, pair_count))
    
    # Step 3: Generate triples of frequent individual items
    frequent_triples = []
    for triple in combinations([item for item, _ in frequent_items], 3):
        triple_count = sum(1 for row in rows if set(triple).issubset(set(row)))
        if triple_count >= threshold:
            frequent_triples.append((triple, triple_count))
    
    return frequent_items, frequent_pairs, frequent_triples

        
# Function to process messages from Kafka topic and apply Apriori algorithm
def process_messages(threshold):
    rows_accumulated = []
    batch_count = 0
    
    for message in consumer:
        data = json.loads(message.value.decode('utf-8'))
        rows_accumulated.append(data)  # Append each received row as a list
        batch_count += 1
        
        if batch_count >= 50:  # Check if at least 50 rows received
            frequent_items, frequent_pairs, frequent_triples = apriori(rows_accumulated, threshold)
            
            # Write frequent itemsets to file
            with open('frequent_itemsets.txt', 'w') as file:
                file.write("Frequent Individual Items and Counts:\n")
                for item, count in frequent_items:
                    file.write(f"Item: {item}, Count: {count}\n")
                
                file.write("\nFrequent Pairs and Counts:\n")
                for pair, count in frequent_pairs:
                    file.write(f"Pair: {pair}, Count: {count}\n")
                
                file.write("\nFrequent Triples and Counts:\n")
                for triple, count in frequent_triples:
                    file.write(f"Triple: {triple}, Count: {count}\n")
            
            print("Frequent itemsets written to file.")
            
            # Reset accumulated rows
            
            batch_count = 0  # Reset batch count


if __name__ == "__main__":
    threshold = 5  # Set the threshold for frequent itemsets
    process_messages(threshold)

