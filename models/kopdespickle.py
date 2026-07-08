import pickle
from src.graph_search import GRAPH

# Simpan state graph sebagai representasi "model" ruang pencarian
with open("models/graph_state.pkl", "wb") as f:
    pickle.dump(GRAPH, f)