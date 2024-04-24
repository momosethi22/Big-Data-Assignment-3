# Big-Data-Assignment-3

# Amazon Sample Meta.json Frequent Itemset Mining

This repository contains the implementation of frequent itemset mining algorithms (Apriori, PCY, and SON) applied to the Amazon Sample Meta.json dataset. The goal was to extract insights from the dataset using Kafka and streaming processing techniques.

## Dataset Preprocessing
The dataset preprocessing involved selecting relevant columns (`asin`, `also_buy`, `also_view`) and discarding the rest. Only the `also_buy` column was utilized for frequent itemset mining.

## Streaming Pipeline Setup
A streaming pipeline was established using Kafka, consisting of one topic, one producer, and three consumers. The producer continuously streamed live data to the consumers.

## Frequent Itemset Mining Algorithms
### 1. Apriori
The first consumer applied the Apriori algorithm, which involved finding frequent individual items, frequent pairs, and frequent triples within each batch of data.

### 2. PCY (Park-Chan-Yu)
The second consumer applied the PCY algorithm, which utilized hash-based techniques to find frequent pairs within the dataset.

### 3. SON (Savasere, Omiecinski, and Navathe)
The third consumer implemented the SON algorithm, which divided the data into chunks and found frequent items and pairs in each chunk. The frequent items and pairs were then combined and checked against the overall threshold.

## Incremental Processing
All consumers operated in an incremental manner, processing batches of 50 data points at a time. Once a batch was received, the respective algorithm was applied to the accumulated data.

## Findings
The frequent itemset mining algorithms revealed patterns and associations within the Amazon Sample Meta dataset. These insights can be utilized for various purposes, such as market basket analysis, recommendation systems, and customer behavior analysis.

## Notes
- Further optimizations and parameter tuning can be explored to enhance the efficiency and accuracy of the algorithms.
- Additional analyses, such as association rule mining, can be performed to extract deeper insights from the dataset.

- Certainly! Here's the updated section for your README:

## Team Members
This project was completed collaboratively by a group of three individuals:

- **Abdul Mohaiman** (22i-1882)
- **Abdullah Arif** (22i-1938)
- **Tayyab Kamran** (22i-2076)

Each team member contributed to various aspects of the project, including dataset preprocessing, algorithm implementation, Kafka setup, and result analysis. Working together, they successfully applied frequent itemset mining algorithms to extract valuable insights from the Amazon Sample Meta.json dataset.


