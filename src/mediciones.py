import subprocess
import platform

NODOS_DEFINIDOS = {
    "Erick": "100.72.129.51",
    "Fernando": "100.78.56.18",
    "David": "100.103.73.22",
    "Yael": "100.80.62.115"
}

def hacer_ping(ip):
    try:
        param = "-n" if platform.system().lower() == "windows" else "-c"
        resultado = subprocess.run(
            ["ping", param, "1", ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
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

print("Resultados de latencia por nodo:")
for nombre, ip in NODOS_DEFINIDOS.items():
    latencia = hacer_ping(ip)
    if latencia is not None:
        print(f"{nombre} ({ip}): {latencia:.2f} ms")
    else:
        print(f"{nombre} ({ip}): No accesible")
