# VPN-GODIN
📌 Información General
Materia: Análisis de algoritmos
Profesor: Jorge Ernesto López Arce Delgado
Sección: D25
Calendario: 2025 A
Actividad: 06 - Optimización de Transferencia de Archivos en una VPN con Algoritmos Voraces

👥 Integrantes del Equipo
Erick Abraham Chavarin Morales (218557215)
Fernando Luna De La Peña (223379341)
Yael Ivan Garcia Mercado (218769492)
David Arreola Araiza (219625419)

🚀 Parte 1: Configuración de la VPN
📋 Descripción de la Tarea
-Crear una VPN entre los dispositivos de los integrantes usando herramientas como WireGuard, OpenVPN o Tailscale.
-Asignar IPs estáticas a cada nodo.
-Diseñar e implementar un protocolo para enviar archivos por una ruta específica.

🔧 Elección de VPN
Se eligió Tailscale por su facilidad de uso:
-Solo requiere crear una cuenta, instalar la aplicación y generar una red compartida.
-Permite invitar a otros usuarios a unirse a la red.

🌐 Asignación de IPs Estáticas
Tailscale asigna automáticamente una IP estática a cada nodo. No se modificaron las IPs ya que la conexión funcionaba correctamente.

📡 Protocolo de Transferencia de Archivos
Se desarrolló un programa con una GUI sencilla que permite:
-Modo escucha en el puerto 5001.
-Enviar archivos a un nodo específico.
-Medir ping y ancho de banda durante la transferencia.

🔄 Protocolo Utilizado: TCP
-Ventaja: Garantiza la entrega confiable de datos mediante verificación.
-Desventaja: Más lento que UDP, pero más seguro para transferencias críticas.

🖼️ Capturas de Interfaz
-Interfaz de Tailscale con las IPs asignadas.
-Programa en modo escucha.
-Transferencia exitosa entre nodos.

🛠️ Cómo Usar el Programa
🔧 Requisitos Previos
-Tener Python 3.8+ instalado
-Tener Tailscale configurado y funcionando
-Instalar las dependencias:
-bash
-pip install tkinter networkx matplotlib

🖥️ Interfaz Gráfica (GUI)
El programa ofrece una interfaz intuitiva con dos modos principales:
-Modo Receptor
-Al ejecutar el programa, inicia automáticamente en modo receptor
-Escucha en el puerto 5001 esperando conexiones entrantes
-Muestra el progreso de las transferencias con:
-Barra de progreso
-Porcentaje completado
-Velocidad de transferencia en MB/s
-Modo Emisor
-Hacer clic en "Enviar archivo"
-Seleccionar el archivo a transferir
-Elegir el nodo destino del menú desplegable
-El sistema calculará automáticamente la ruta óptima usando Dijkstra
-Hacer clic en "Iniciar transferencia"

📊 Métricas Mostradas
Durante la transferencia se muestran:
-Ruta óptima calculada
-Tiempo de transferencia (ruta óptima vs ruta directa)
-Velocidad promedio de transferencia
-Gráfico de la topología de red

📂 Estructura del Repositorio
.
├── Grado ponderado Actividad 6.py    # Script principal de análisis de red
├── PROYECTO 3 AdA.py                 # Implementación completa del proyecto
├── dijkstra.py                       # Algoritmo de Dijkstra para rutas óptimas
├── kruskal.py                        # Algoritmo de Kruskal para MST
├── mediciones.py                     # Herramientas de medición de red
└── README.md                         # Documentación del proyecto
🚀 Cómo Ejecutar el Proyecto
Requisitos:
bash
pip install networkx matplotlib tkinter
Ejecutar la aplicación principal:

bash
python "PROYECTO 3 AdA.py"
Ejecutar análisis individuales:

bash
python "Grado ponderado Actividad 6.py"  # Análisis de red
python dijkstra.py                       # Pruebas de ruteo
python kruskal.py                        # Generación de MST
🛠️ Componentes Clave
1. Grado ponderado Actividad 6.py
Analiza las métricas de red (latencia/ancho de banda)

Genera grafos ponderados para visualización

2. PROYECTO 3 AdA.py
Aplicación principal con GUI
Integra todas las funcionalidades:
Transferencia de archivos
Cálculo de rutas óptimas
Visualización de red

3. dijkstra.py
python
def calcular_ruta_optima(grafo, inicio):
    # Implementación del algoritmo
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    # ... resto de la implementación
4. kruskal.py
python
def generar_mst(grafo):
    # Implementación del algoritmo
    arbol = nx.Graph()
    # ... resto de la implementación
5. mediciones.py
Herramientas para:
Medición de ping
Pruebas de ancho de banda
Monitoreo de transferencias

📊 Métricas de Red
Conexión	Latencia (ms)	Ancho de Banda (Mbps)
NodoA ↔ NodoB	85	68
NodoA ↔ NodoC	78	73.6
NodoB ↔ NodoC	91	68

📌 Uso Recomendado
Configurar Tailscale/VPN
Ejecutar PROYECTO 3 AdA.py en todos los nodos
Seleccionar archivos y nodos destino en la GUI
Monitorear las transferencias en tiempo real

📜 Licencia
MIT License - Libre uso y modificación

🛠️ Desarrollado por:
Erick Abraham Chavarin Morales
Fernando Luna De La Peña
Yael Ivan Garcia Mercado
David Arreola Araiza

🎯 Tecnologías: Python, Tailscale, Algoritmos Voraces
Este proyecto está bajo la licencia MIT.

🛠️ Desarrollado con Python, Tailscale y Algoritmos Voraces 🎯
