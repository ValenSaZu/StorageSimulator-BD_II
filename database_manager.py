import re
import json
import sys
from HDDStructure import HDD
from HDD_AddressTable import TablaDirecciones_HDD

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
        elif query.startswith("DELETE"):
            return self.eliminar_datos(query)
        else:
            raise ValueError("Consulta SQL no válida.")

    def calcular_tamano(self, datos):
        return sum(sys.getsizeof(dato) for dato in datos)

    def crear_tabla(self, query):
        match = re.match(r"CREATE TABLE (\w+)\((.+)\);", query)
        if not match:
            raise ValueError("Consulta CREATE TABLE no válida.")
        
        nombre_tabla = match.group(1)
        columnas = [col.strip() for col in match.group(2).split(",")]

        if nombre_tabla in self.estructuras_tablas:
            raise ValueError(f"La tabla '{nombre_tabla}' ya existe.")

        self.estructuras_tablas[nombre_tabla] = columnas
        
        direccion_logica = f"tabla:{nombre_tabla}"
        self.hdd.escribir_dato(direccion_logica, json.dumps({"columnas": columnas, "filas": []}))
        print(f"Tabla '{nombre_tabla}' creada con columnas: {columnas}")
        return True

    def insertar_datos(self, query):
        match = re.match(r"INSERT INTO (\w+) VALUES \((.+)\);", query)
        if not match:
            raise ValueError("Consulta INSERT no válida.")
        
        nombre_tabla = match.group(1)
        datos = [dato.strip() for dato in match.group(2).split(",")]

        if nombre_tabla not in self.estructuras_tablas:
            raise ValueError(f"La tabla '{nombre_tabla}' no existe.")

        columnas = self.estructuras_tablas[nombre_tabla]
        if len(columnas) != len(datos):
            raise ValueError(f"El número de valores no coincide con las columnas de la tabla '{nombre_tabla}'.")

        tamano_datos = self.calcular_tamano(datos)
        sectores_necesarios = -(-tamano_datos // self.hdd.platos[0].pistas[0].sectores[0].tamano_bytes)

        datos_divididos = []
        offset = 0
        for _ in range(sectores_necesarios):
            tamano_sector = self.hdd.platos[0].pistas[0].sectores[0].tamano_bytes
            datos_divididos.append(json.dumps(datos)[offset:offset + tamano_sector])
            offset += tamano_sector

        fila_direccion_logica = []
        for fragmento in datos_divididos:
            direccion = self.hdd.tabla_direcciones.agregar_datos(fragmento)
            fila_direccion_logica.append(direccion)

        direccion_logica = f"tabla:{nombre_tabla}"
        tabla_data = json.loads(self.hdd.leer_dato(direccion_logica))
        tabla_data["filas"].append(fila_direccion_logica)
        self.hdd.escribir_dato(direccion_logica, json.dumps(tabla_data))
        
        print(f"Datos insertados en '{nombre_tabla}': {datos}")
        return True

    def seleccionar_datos(self, query):
        match = re.match(r"SELECT \* FROM (\w+);", query)
        if not match:
            raise ValueError("Consulta SELECT no válida.")
        
        nombre_tabla = match.group(1)
        if nombre_tabla not in self.estructuras_tablas:
            raise ValueError(f"La tabla '{nombre_tabla}' no existe.")

        direccion_logica = f"tabla:{nombre_tabla}"
        tabla_data = json.loads(self.hdd.leer_dato(direccion_logica))

        filas = []
        for fila_direccion_logica in tabla_data["filas"]:
            datos_completos = ""
            for fragmento_direccion in fila_direccion_logica:
                datos_completos += self.hdd.leer_dato(fragmento_direccion)
            filas.append(json.loads(datos_completos))

        print(f"Datos seleccionados de '{nombre_tabla}': {filas}")
        return filas

    def eliminar_datos(self, query):
        match = re.match(r"DELETE FROM (\w+) WHERE id=(\d+);", query)
        if not match:
            raise ValueError("Consulta DELETE no válida.")
        
        nombre_tabla = match.group(1)
        id_a_eliminar = int(match.group(2))
        
        if nombre_tabla not in self.estructuras_tablas:
            raise ValueError(f"La tabla '{nombre_tabla}' no existe.")
        
        direccion_logica = f"tabla:{nombre_tabla}"
        tabla_data = json.loads(self.hdd.leer_dato(direccion_logica))
        
        filas_actualizadas = []
        for fila in tabla_data["filas"]:
            datos_completos = ""
            for fragmento_direccion in fila:
                datos_completos += self.hdd.leer_dato(fragmento_direccion)
            
            datos_json = json.loads(datos_completos)
            if datos_json[0] == id_a_eliminar:
                for fragmento_direccion in fila:
                    self.hdd.tabla_direcciones.liberar_direccion(fragmento_direccion)
            else:
                filas_actualizadas.append(fila)
        
        tabla_data["filas"] = filas_actualizadas
        self.hdd.escribir_dato(direccion_logica, json.dumps(tabla_data))
        print(f"Datos con id={id_a_eliminar} eliminados de '{nombre_tabla}'.")
        return True
