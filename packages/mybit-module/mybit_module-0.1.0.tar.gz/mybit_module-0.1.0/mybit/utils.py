import json
import importlib.resources as pkg_resources

def read_json(json_file):
    try:
        with open(json_file, 'r') as file:
            return json.load(file)
    except Exception as e:
        raise FileNotFoundError(f"Error al abrir el archivo .JSON {str(e)}")
    
def read_json_servers():
    try:
        # Usamos importlib.resources para acceder al archivo dentro del paquete
        with pkg_resources.open_text('mybit.network', 'servers.json') as file:
            return json.load(file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error al abrir el archivo .JSON {str(e)}")