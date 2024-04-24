import json
from kafka import KafkaConsumer
from collections import Counter, defaultdict
from itertools import combinations

# Initialize Kafka consumer
consumer = KafkaConsumer('topic1', bootstrap_servers='localhost:9092')

def pcy(rows, threshold, hash_table_size):
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
    
    # Step 3: Create hash table (buckets) and count frequent pairs in each bucket
    buckets = defaultdict(list)
    for pair in frequent_pairs:
        hash_value = hash(str(pair)) % hash_table_size
        buckets[hash_value].append(pair)
    
    return buckets

def write_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write(data)

if __name__ == "__main__":
    batch_count = 0
    items_accumulated = []
    threshold = 5
    hash_table_size = 100
    
    for message in consumer:
        data = json.loads(message.value.decode('utf-8'))
        items_accumulated.append(data)  # Append each received row as a list
        
        batch_count += 1
        if batch_count == 50:
            print("Applying PCY algorithm...")
            frequent_itemsets = pcy(items_accumulated, threshold, hash_table_size)
            
            # Write frequent itemsets to file
            with open('frequent_itemsets_pcy.txt', 'w') as file:
                file.write("Frequent Pairs and Counts:\n")
                for bucket, items in frequent_itemsets.items():
                    file.write(f"Bucket {bucket}:\n")
                    for pair, count in items:
                        file.write(f"Pair: {pair}, Count: {count}\n")
            
            batch_count = 0

