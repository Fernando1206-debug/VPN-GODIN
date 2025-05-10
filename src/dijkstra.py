import heapq

def construir_grafo_latencias(nodos):
    grafo = {nodo: {} for nodo in nodos}
    for nombre1, ip1 in nodos.items():
        for nombre2, ip2 in nodos.items():
            if nombre1 != nombre2:
                latencia = hacer_ping(ip2)
                if latencia:
                    grafo[nombre1][nombre2] = latencia
    return grafo

def dijkstra(grafo, inicio):
    dist = {nodo: float('inf') for nodo in grafo}
    dist[inicio] = 0
    prev = {nodo: None for nodo in grafo}
    heap = [(0, inicio)]

    while heap:
        actual_dist, actual = heapq.heappop(heap)
        if actual_dist > dist[actual]:
            continue
        for vecino, peso in grafo[actual].items():
            distancia = actual_dist + peso
            if distancia < dist[vecino]:
                dist[vecino] = distancia
                prev[vecino] = actual
                heapq.heappush(heap, (distancia, vecino))
    return dist, prev

def reconstruir_ruta(prev, destino):
    ruta = []
    while destino:
        ruta.insert(0, destino)
        destino = prev[destino]
    return ruta
