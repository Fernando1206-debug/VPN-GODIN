import networkx as nx
import matplotlib.pyplot as plt
from collections.abc import Mapping


# Datos de conexiones: (dispositivo1, dispositivo2, latencia en segundos, ancho de banda en Mbps)
conexiones = [
    ("Fernando", "David", 0.19, 68),
    ("Fernando", "Yael", 2.2, 47.2),
    ("Fernando", "Erick", 0.96, 68),
    ("David", "Yael", 1.2, 59.7),
    ("David", "Erick", 0.41, 73.6),
    ("Erick", "Yael", 1.25, 68)
]

# Crear grafo
G = nx.Graph()

# Añadir nodos y aristas con pesos calculados
for d1, d2, latencia, banda in conexiones:
    peso = latencia / banda
    G.add_edge(d1, d2, weight=peso, latencia=latencia, banda=banda)

# Posiciones para graficar
pos = nx.spring_layout(G, seed=42)

# Dibujar nodos y bordes
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=10, font_weight='bold')
nx.draw_networkx_edges(G, pos)

# Etiquetas con peso (latencia/ancho de banda)
edge_labels = {
    (u, v): f"{d['latencia']}s / {d['banda']}Mbps\n= {d['weight']:.4f}"
    for u, v, d in G.edges(data=True)
}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

plt.title("Grafo Ponderado (Latencia / Ancho de Banda)")
plt.tight_layout()
plt.show()
