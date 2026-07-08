import csv
import math
import heapq
import random

# 1. Load Data dari CSV
def load_data():
    nodes = {}
    # Pastikan file CSV Anda ada di folder data/
    with open('data/kopdesnodes.csv', mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            nodes[row['name']] = (float(row['latitude']), float(row['longitude']))
    
    adj = {n: [] for n in nodes}
    with open('data/kopdesjalur.csv', mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            adj[row['source']].append(row['destination'])
            adj[row['destination']].append(row['source'])
    return nodes, adj

NODES, ADJACENCY = load_data()

# 2. Helper untuk Heuristik
def euclidean_h1_km(a, b):
    lat1, lon1 = a
    lat2, lon2 = b
    # Konversi koordinat ke km
    km_per_deg_lat = 110.574
    km_per_deg_lon = 111.320 * math.cos(math.radians((lat1 + lat2) / 2))
    dx = (lon2 - lon1) * km_per_deg_lon
    dy = (lat2 - lat1) * km_per_deg_lat
    return math.sqrt(dx**2 + dy**2)

# 3. Membangun Graf Berbobot (Weighted Graph)
def build_graph():
    graph = {n: {} for n in NODES}
    random.seed(42) # Agar hasil bobot konsisten
    for n, neighbors in ADJACENCY.items():
        for m in neighbors:
            if m not in graph[n]:
                # Menambahkan variasi jarak/winding factor agar realistis
                winding = random.uniform(1.15, 1.40)
                dist_km = euclidean_h1_km(NODES[n], NODES[m]) * winding
                graph[n][m] = round(dist_km, 3)
                graph.setdefault(m, {})[n] = round(dist_km, 3)
    return graph

GRAPH = build_graph()

# 4. Fungsi Utama A* Search
def astar(start, goal):
    if start not in NODES or goal not in NODES:
        raise KeyError(f"Node tidak valid. Start: {start}, Goal: {goal}")
        
    open_set = [(euclidean_h1_km(NODES[start], NODES[goal]), start)]
    g_score = {start: 0}
    came_from = {}
    visited = set()

    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return {"path": path, "cost": round(g_score[goal], 2)}
            
        if current in visited: continue
        visited.add(current)

        for neighbor, w in GRAPH[current].items():
            tentative_g = g_score[current] + w
            if tentative_g < g_score.get(neighbor, math.inf):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + euclidean_h1_km(NODES[neighbor], NODES[goal])
                heapq.heappush(open_set, (f, neighbor))
    return None
