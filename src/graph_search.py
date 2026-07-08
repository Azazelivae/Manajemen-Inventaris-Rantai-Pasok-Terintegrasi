import csv
import math

def load_data():
    nodes = {}
    with open('data/kopdesnodes.csv', mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            nodes[row['name']] = (float(row['latitude']), float(row['longitude']))
    
    adj = {n: [] for n in nodes}
    with open('data/kopdesjalur.csv', mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Karena undirected graph, masukkan dua arah
            adj[row['source']].append(row['destination'])
            adj[row['destination']].append(row['source'])
    return nodes, adj

# Panggil fungsi ini untuk mengisi variabel global
NODES, ADJACENCY = load_data()