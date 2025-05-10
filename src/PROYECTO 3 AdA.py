import socket
import os
import sys
import threading
import time
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import platform
import heapq

# ---------------------- NODOS DEFINIDOS ----------------------

NODOS_DEFINIDOS = {
    "Erick": "100.72.129.51",
    "Fernando": "100.78.56.18",
    "David": "100.103.73.22",
    "Yael": "100.80.62.115"
}

# ---------------------- FUNCIONES DE RED ----------------------

def hacer_ping(ip):
    try:
        param = "-n" if platform.system().lower() == "windows" else "-c"
        resultado = subprocess.run(["ping", param, "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if resultado.returncode == 0:
            for linea in resultado.stdout.splitlines():
                if "time=" in linea.lower() or "tiempo=" in linea.lower():
                    partes = linea.replace("=", " = ").split()
                    for i, p in enumerate(partes):
                        if p.startswith("time") or p.startswith("tiempo"):
                            valor = partes[i + 2].replace("ms", "").replace(",", ".")
                            return float(valor)
        return None
    except Exception as e:
        print(f"[PING ERROR] {e}")
        return None

# ---------------------- GRAFO Y DIJKSTRA ----------------------

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

# ---------------------- RECEPTOR ----------------------

class FileReceiver:
    def __init__(self, port=5001):
        self.host = '0.0.0.0'
        self.port = port
        self.running = True
        self.thread = threading.Thread(target=self.listen)
        self.thread.daemon = True

    def print_progress(self, received, total, speed_mbps):
        percent = received / total
        bar = '=' * int(50 * percent)
        sys.stdout.write(f"\r[RECEPCION] [{bar:<50}] {percent*100:.2f}% - {speed_mbps:.2f} MB/s")
        sys.stdout.flush()

    def listen(self):
        with socket.socket() as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(1)
            print(f"[INFO] Esperando conexion en el puerto {self.port}...")

            while self.running:
                try:
                    server_socket.settimeout(1.0)
                    conn, addr = server_socket.accept()
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"[ERROR] {e}")
                    break

                with conn:
                    print(f"\n[INFO] Conectado desde {addr}")

                    filename = conn.recv(1024).decode()
                    conn.send(b"OK")
                    filesize = int(conn.recv(1024).decode())
                    conn.send(b"OK")

                    with open("recibido_" + filename, "wb") as f:
                        bytes_received = 0
                        start_time = time.time()
                        last_time = start_time
                        last_received = 0

                        while bytes_received < filesize:
                            bytes_read = conn.recv(4096)
                            if not bytes_read:
                                break
                            f.write(bytes_read)
                            bytes_received += len(bytes_read)

                            current_time = time.time()
                            elapsed = current_time - last_time
                            if elapsed >= 0.5:
                                delta_bytes = bytes_received - last_received
                                speed = delta_bytes / 1024 / 1024 / elapsed
                                self.print_progress(bytes_received, filesize, speed)
                                last_time = current_time
                                last_received = bytes_received

                        total_time = time.time() - start_time
                        avg_speed = (bytes_received / 1024 / 1024) / total_time
                        self.print_progress(bytes_received, filesize, avg_speed)
                        print(f"\n[BANDA] Archivo recibido: {bytes_received / 1024:.2f} KB en {total_time:.2f} s → {avg_speed:.2f} MB/s")

                    conn.send(b"RECIBIDO")
                    print(f"[INFO] Archivo recibido exitosamente en {total_time:.2f} s")

    def start(self):
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join(timeout=2)
        print("[INFO] Servidor detenido.")

# ---------------------- ENVÍO ----------------------

def medir_tiempo_transferencia(ip_destino, filename, dummy=False):
    try:
        filesize = os.path.getsize(filename)
        s = socket.socket()
        s.connect((ip_destino, 5001))
        s.send(os.path.basename(filename).encode())
        s.recv(1024)
        s.send(str(filesize).encode())
        s.recv(1024)

        sent = 0
        start_time = time.time()
        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(4096)
                if not bytes_read:
                    break
                s.sendall(bytes_read)
                sent += len(bytes_read)
        s.send(b"EOF")
        recibido = s.recv(1024)
        s.close()
        total_time = time.time() - start_time
        return total_time
    except Exception as e:
        print(f"[ERROR] {e}")
        return None

def send_file(filename, ip_destino, progress_bar, ruta_optima, label_info):
    try:
        tiempo_ruta_directa = medir_tiempo_transferencia(ip_destino, filename)
        tiempo_ruta_optima = tiempo_ruta_directa  # Aquí podrías simular cambios si hubiese redirección

        filesize = os.path.getsize(filename)
        s = socket.socket()
        s.connect((ip_destino, 5001))

        s.send(os.path.basename(filename).encode())
        s.recv(1024)
        s.send(str(filesize).encode())
        s.recv(1024)

        sent = 0
        start_time = time.time()
        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(4096)
                if not bytes_read:
                    break
                s.sendall(bytes_read)
                sent += len(bytes_read)
                progress = int((sent / filesize) * 100)
                progress_bar["value"] = progress

        s.send(b"EOF")
        confirm = s.recv(1024)
        s.close()

        total_time = time.time() - start_time
        speed = (filesize / 1024 / 1024) / total_time
        label_info.config(text=f"Ruta óptima: {' → '.join(ruta_optima)}\n"
                               f"Tiempo (óptima): {total_time:.2f}s\n"
                               f"Tiempo (directa): {tiempo_ruta_directa:.2f}s")

        messagebox.showinfo("Éxito", f"Archivo enviado correctamente.\nVelocidad media: {speed:.2f} MB/s")
    except Exception as e:
        print(f"[ERROR] {e}")
        messagebox.showerror("Error", f"Falló la transferencia:\n{e}")

# ---------------------- GUI ----------------------

class FileTransferApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Transferencia de Archivos con Dijkstra")

        self.receiver = FileReceiver()
        self.receiver.start()

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=20, pady=20)

        tk.Label(self.main_frame, text="Esperando archivos entrantes...").pack(pady=10)
        tk.Button(self.main_frame, text="Enviar archivo", command=self.abrir_cliente).pack(pady=20)

    def abrir_cliente(self):
        self.receiver.stop()
        self.main_frame.destroy()

        self.client_frame = tk.Frame(self.root)
        self.client_frame.pack(padx=20, pady=20)

        tk.Label(self.client_frame, text="Archivo a transferir:").pack()
        self.entry_file = tk.Entry(self.client_frame, width=50)
        self.entry_file.pack()
        tk.Button(self.client_frame, text="Seleccionar", command=self.seleccionar_archivo).pack()

        tk.Label(self.client_frame, text="Destino:").pack(pady=5)
        self.nodos = list(NODOS_DEFINIDOS.keys())
        self.combo = ttk.Combobox(self.client_frame, values=self.nodos)
        self.combo.pack()

        self.progress = ttk.Progressbar(self.client_frame, length=300)
        self.progress.pack(pady=10)

        self.label_info = tk.Label(self.client_frame, text="")
        self.label_info.pack()

        tk.Button(self.client_frame, text="Iniciar transferencia", command=self.iniciar_transferencia).pack(pady=10)

    def seleccionar_archivo(self):
        file = filedialog.askopenfilename()
        if file:
            self.entry_file.delete(0, tk.END)
            self.entry_file.insert(0, file)

    def iniciar_transferencia(self):
        destino = self.combo.get()
        archivo = self.entry_file.get()
        if not archivo or not destino:
            messagebox.showwarning("Faltan datos", "Elige un archivo y un destino.")
            return

        grafo = construir_grafo_latencias(NODOS_DEFINIDOS)
        dist, prev = dijkstra(grafo, self.obtener_nombre_local())
        ruta = reconstruir_ruta(prev, destino)
        ip_destino = NODOS_DEFINIDOS[destino]

        threading.Thread(target=send_file,
                         args=(archivo, ip_destino, self.progress, ruta, self.label_info),
                         daemon=True).start()

    def obtener_nombre_local(self):
        ip_local = socket.gethostbyname(socket.gethostname())
        for nombre, ip in NODOS_DEFINIDOS.items():
            if ip == ip_local:
                return nombre
        return list(NODOS_DEFINIDOS.keys())[0]  # Por defecto

# ---------------------- EJECUCIÓN ----------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = FileTransferApp(root)
    root.mainloop()
