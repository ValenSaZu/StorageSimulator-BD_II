import json

class TablaDirecciones_HDD:
    
    def __init__(self, archivo_tabla="tabla_direcciones_hdd.json"):
        self.archivo_tabla = archivo_tabla
        self.direcciones = self._cargar_tabla()

    def _cargar_tabla(self):
        try:
            with open(self.archivo_tabla, "r") as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            print("Error: El archivo de tabla de direcciones está corrupto.")
            return {}

    def guardar_tabla(self):
        with open(self.archivo_tabla, "w") as archivo:
            json.dump(self.direcciones, archivo)

    def agregar_direccion(self, direccion_logica, direccion_fisica):
        if direccion_logica in self.direcciones:
            raise ValueError(f"La dirección lógica {direccion_logica} ya existe.")
        
        # Validación del formato de direccion_fisica
        parts = direccion_fisica.split("-")
        if len(parts) != 3:
            raise ValueError(f"Formato de direccion_fisica inválido: '{direccion_fisica}'. Debe ser 'plato-pista-sector'.")
        try:
            plato, pista, sector = map(int, parts)
        except ValueError:
            raise ValueError(f"direccion_fisica contiene valores no enteros: '{direccion_fisica}'.")

        self.direcciones[direccion_logica] = direccion_fisica
        self.guardar_tabla()

    def obtener_direccion(self, direccion_logica):
        return self.direcciones.get(direccion_logica, None)
    
    def listar_direcciones(self):
        return self.direcciones.items()
