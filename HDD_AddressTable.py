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

    def guardar_tabla(self):
        with open(self.archivo_tabla, "w") as archivo:
            json.dump(self.direcciones, archivo)

    def agregar_direccion(self, direccion_logica, direccion_fisica):
        if direccion_logica in self.direcciones:
            raise ValueError(f"La dirección lógica {direccion_logica} ya existe.")
        self.direcciones[direccion_logica] = direccion_fisica
        self.guardar_tabla()

    def eliminar_direccion(self, direccion_logica):
        if direccion_logica in self.direcciones:
            del self.direcciones[direccion_logica]
            self.guardar_tabla()

    def obtener_direccion(self, direccion_logica):
        return self.direcciones.get(direccion_logica, None)
    
    def listar_direcciones(self):
        return self.direcciones.items()