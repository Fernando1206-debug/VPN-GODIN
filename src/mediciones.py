import subprocess
import platform



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