import json
from kafka import KafkaConsumer
from collections import Counter, defaultdict
from itertools import combinations

# Initialize Kafka consumer
consumer = KafkaConsumer('topic1', bootstrap_servers='localhost:9092')

def chunk_data(rows, num_chunks):
    chunk_size = len(rows) // num_chunks
    chunks = [rows[i:i + chunk_size] for i in range(0, len(rows), chunk_size)]
    return chunks

def find_frequent_items(chunk, threshold):
    item_counts = Counter(item for row in chunk for item in row)
    frequent_items = {item for item, count in item_counts.items() if count >= threshold}
    
    frequent_pairs = set()
    for pair in combinations(frequent_items, 2):
        pair_count = sum(1 for row in chunk if set(pair).issubset(set(row)))
        if pair_count >= threshold:
            frequent_pairs.add(pair)
    
    return frequent_items, frequent_pairs

def write_to_file(filename, data):
    with open(filename, 'w') as file:  # Open file in write mode to overwrite existing content
        file.write(data)

def process_messages(threshold):
    rows_accumulated = []
    batch_count = 0
    all_frequent_items = set()
    all_frequent_pairs = set()
    
    for message in consumer:
        data = json.loads(message.value.decode('utf-8'))
        rows_accumulated.append(data)  # Append each received row as a list
        batch_count += 1
        
        if batch_count >= 50:  # Check if at least 50 rows received
            output_data = "Creating chunks...\n"
            num_chunks = 4  # Number of chunks
            chunks = chunk_data(rows_accumulated, num_chunks)
            chunk_threshold = threshold // num_chunks  # Calculate threshold for each chunk
            
            for i, chunk in enumerate(chunks):
                frequent_items, frequent_pairs = find_frequent_items(chunk, chunk_threshold)
                all_frequent_items.update(frequent_items)
                all_frequent_pairs.update(frequent_pairs)
                
            # Write data to file
            write_to_file("output.txt", "Frequent Items:\n")
            write_to_file("output.txt", str(all_frequent_items))
            write_to_file("output.txt", "\nFrequent Pairs:\n")
            write_to_file("output.txt", str(all_frequent_pairs))
            
            # Reset accumulated rows

            batch_count = 0  # Reset batch count

if __name__ == "__main__":
    threshold = 10  # Set the threshold for frequent itemsets
    process_messages(threshold)

