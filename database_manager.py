import re
import json
import sys

class SQLProcessor:
    def __init__(self, hdd):
        self.hdd = hdd
        self.estructuras_tablas = {}

    def procesar_query(self, query):
        query = query.strip()
        if query.startswith("CREATE TABLE"):
            return self.crear_tabla(query)
        elif query.startswith("INSERT INTO"):
            return self.insertar_datos(query)
        elif query.startswith("SELECT"):
            return self.seleccionar_datos(query)
        else:
            raise ValueError("Consulta SQL no reconocida.")

    def crear_tabla(self, query):
        match = re.match(r"CREATE TABLE (\w+) \((.+)\)", query)
        if not match:
            raise ValueError("Consulta CREATE TABLE inválida.")
        
        nombre_tabla = match.group(1)
        columnas = [col.strip() for col in match.group(2).split(",")]
        self.estructuras_tablas[nombre_tabla] = columnas

        datos_tabla = json.dumps({"nombre": nombre_tabla, "columnas": columnas, "filas": []})
        direccion_tabla = f"tabla_{nombre_tabla}:1"

        if direccion_tabla in self.hdd.tabla_direcciones.direcciones:
            raise ValueError(f"La dirección lógica {direccion_tabla} ya existe.")
        self.hdd.escribir_dato(datos_tabla, direccion_tabla)
        self.hdd.tabla_direcciones.agregar_direccion(direccion_tabla, "0-0-0")

        print(f"Tabla '{nombre_tabla}' creada con dirección lógica: {direccion_tabla}")

    def insertar_datos(self, query):
        match = re.match(r"INSERT INTO (\w+) VALUES \((.+)\)", query)
        if not match:
            raise ValueError("Consulta INSERT INTO inválida.")
        
        nombre_tabla = match.group(1)
        datos = [dato.strip() for dato in match.group(2).split(",")]

        if nombre_tabla not in self.estructuras_tablas:
            raise ValueError(f"La tabla {nombre_tabla} no existe.")

        direccion_tabla = f"tabla_{nombre_tabla}:1"
        tabla_datos = json.loads(self.hdd.leer_dato([direccion_tabla]))

        direccion_fila = self.hdd.generar_direccion_logica(f"fila_{nombre_tabla}")
        self.hdd.escribir_dato(json.dumps(datos), direccion_fila)
        tabla_datos["filas"].append(direccion_fila)

        self.hdd.escribir_dato(json.dumps(tabla_datos), direccion_tabla)

        print(f"Datos insertados en '{nombre_tabla}': {datos}")

    def seleccionar_datos(self, query):
        match = re.match(r"SELECT \* FROM (\w+)", query)
        if not match:
            raise ValueError("Consulta SELECT inválida.")
        
        nombre_tabla = match.group(1)
        if nombre_tabla not in self.estructuras_tablas:
            raise ValueError(f"La tabla {nombre_tabla} no existe.")

        direccion_tabla = f"tabla_{nombre_tabla}:1"
        tabla_datos = json.loads(self.hdd.leer_dato([direccion_tabla]))

        filas = []
        for direccion_fila in tabla_datos["filas"]:
            datos_fila = self.hdd.leer_dato([direccion_fila])
            filas.append(json.loads(datos_fila))

        print(f"Datos seleccionados de '{nombre_tabla}': {filas}")
        return filas
