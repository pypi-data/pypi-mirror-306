import socket
import ssl
import json

class ElectrumClient:
    def __init__(self, host, port, proto):
        self.host = host
        self.port = port
        self.proto = proto.lower()
        self.sock = None
        self.connect()  # Asegúrate de conectar al inicializar la instancia

    def connect(self):
        try:
            if self.proto == 'tcp':
                self.sock = socket.create_connection((self.host, self.port))
            elif self.proto == 'ssl':
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                self.sock = context.wrap_socket(socket.create_connection((self.host, self.port)), server_hostname=self.host)
            else:
                raise ValueError("Protocolo no soportado. Usa 'tcp' o 'ssl'.")
        except (socket.error, ssl.SSLError) as e:
            raise ConnectionError(f"Error al conectar al servidor Electrum: {e}")

    def send_request(self, method, params=None):
        if self.sock is None:
            raise ConnectionError("No hay conexión establecida.")

        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params if params else [],
            "id": 0
        }

        try:
            self.sock.sendall(json.dumps(request).encode('utf-8') + b'\n')
            response = self.sock.recv(8192).decode('utf-8')
            return json.loads(response)
        except (socket.error, json.JSONDecodeError) as e:
            raise RuntimeError(f"Error al enviar la solicitud: {e}")

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except socket.error as e:
                raise RuntimeError(f"Error al cerrar la conexión: {e}")
            finally:
                self.sock = None  # Asegurarse de que el socket no esté referenciado
        else:
            raise ConnectionError("No hay conexión para cerrar.")

    def __del__(self):
        try:
            self.close()  # Asegurar que la conexión se cierra cuando la instancia se destruye
        except Exception as e:
            print(f"Error en el destructor al cerrar la conexión: {e}")