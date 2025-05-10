import networkx as nx
import matplotlib.pyplot as plt

# Grafo de ancho de banda (cuanto mayor, mejor)
# Formato: (nodo1, nodo2, ancho_de_banda)
enlaces = [
    ("Erick", "Fernando", 68),#----Real
    ("Erick", "David", 73.6), #----Real
    ("Fernando", "David", 68),#----Reañ
    ("Fernando", "Yael", 47.2),#-----
    ("David", "Yael", 59.7),#------Real
    ("Erick", "Yael", 1.72)#---real
]

# Crear grafo original
G = nx.Graph()
for u, v, bw in enlaces:
    G.add_edge(u, v, weight=bw)

# Mostrar grafo original
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=10)
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{d['weight']} Mbps" for u, v, d in G.edges(data=True)})
plt.title("Grafo original")

# Aplicar Kruskal (maximizar ancho de banda => minimizamos el inverso)
G_inv = nx.Graph()
for u, v, bw in enlaces:
    # Para Kruskal en networkx usamos el peso como "costo", así que usamos el inverso del ancho de banda
    G_inv.add_edge(u, v, weight=1 / bw)

# Obtener MST
mst = nx.minimum_spanning_tree(G_inv)

# Mostrar MST
plt.subplot(1, 2, 2)
nx.draw(mst, pos, with_labels=True, node_color='lightgreen', node_size=2000, font_size=10)
nx.draw_networkx_edge_labels(mst, pos, edge_labels={(u, v): f"{int(1 / d['weight'])} Mbps" for u, v, d in mst.edges(data=True)})
plt.title("Árbol de expansión mínima (Kruskal)")

plt.tight_layout()
plt.show()

# También puedes imprimir los enlaces del MST
print("Enlaces seleccionados por Kruskal para MST:")
for u, v, d in mst.edges(data=True):
    print(f"{u} <-> {v}: {int(1 / d['weight'])} Mbps")
