#datos de NeuroSky a TouchDesigner bien normalizados y clasificados pero muy variados 
import socket
import json

# Conexión con NeuroSky
def conectar_neurosky():
    host = '127.0.0.1'
    port = 13854
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.sendall('{"enableRawOutput": true, "format": "Json"}\n'.encode('utf-8'))
    print("Conectado a NeuroSky")
    return sock

# Normalización entre 0-100
def normalizar(valor, min_val, max_val):
    valor = max(min(valor, max_val), min_val)
    return int(((valor - min_val) / (max_val - min_val)) * 100)

# Clasificación emociones Russell
def clasificar_emociones(eeg_data):
    delta = eeg_data.get('delta', 0)
    theta = eeg_data.get('theta', 0)
    alpha = eeg_data.get('lowAlpha', 0) + eeg_data.get('highAlpha', 0)
    beta = eeg_data.get('lowBeta', 0) + eeg_data.get('highBeta', 0)
    gamma = eeg_data.get('lowGamma', 0) + eeg_data.get('highGamma', 0)

    # Clasificación basada en los rangos de la tabla
    return {
        # Asociaciones directas con Russell (ver tabla)
        "tristeza": normalizar(delta, 0, 300000),        # Delta alta = tristeza
        "depresion": normalizar(theta + delta, 0, 380000),# Theta+Delta = depresión
        "calma": normalizar(alpha, 0, 50000),            # Alpha = calma
        "serenidad": normalizar(alpha + theta, 0, 130000), # Alpha+Theta = serenidad
        "felicidad": normalizar(beta, 0, 30000),         # Beta alta = felicidad
        "excitacion": normalizar(beta + gamma, 0, 45000),# Beta + Gamma = excitación
        "preocupacion": normalizar(gamma, 0, 15000),     # Gamma alta = preocupación
        "enfado": normalizar(gamma + beta, 0, 45000)     # Gamma + Beta = enfado
    }

    

# Enviar datos por UDP a TouchDesigner
def enviar_udp():
    sock_neuro = conectar_neurosky()
    sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    udp_ip = "127.0.0.1"
    udp_port = 7000
    buffer = ""

    try:
        while True:
            data = sock_neuro.recv(1024)
            try:
                buffer += data.decode('utf-8', errors='ignore')  # <- clave para evitar errores de byte
                while '\r' in buffer:
                    mensaje, buffer = buffer.split('\r', 1)
                    try:
                        json_data = json.loads(mensaje)
                        if "eSense" in json_data or "eegPower" in json_data:
                            emociones = clasificar_emociones(json_data.get("eegPower", {}))
                            json_data["eSense"].update(emociones)

                            mensaje_udp = json.dumps(json_data) + '\n'  # importante el salto de línea
                            sock_udp.sendto(mensaje_udp.encode('utf-8'), (udp_ip, udp_port))
                            print(f"📡 Enviado por UDP: {mensaje_udp}")
                    except json.JSONDecodeError:
                        print("JSON inválido, descartado.")
            except Exception as e:
                print(f"⚠️ Error procesando: {e}")
    except KeyboardInterrupt:
        print("Cerrando conexiones...")
        sock_neuro.close()
        sock_udp.close()

enviar_udp()
