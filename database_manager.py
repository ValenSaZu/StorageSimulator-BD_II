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
        elif query.startswith("DELETE"):
            return self.eliminar_datos(query)
        elif query.startswith("DROP TABLE"):
            return self.eliminar_tabla(query)
        else:
            raise ValueError("Consulta SQL no válida.")

    def calcular_tamano(self, datos):
        return sum(sys.getsizeof(dato) for dato in datos)

    def crear_tabla(self, query):
        match = re.match(r"CREATE TABLE\s+(\w+)\s*\((.+?)\);\s*$", query)
        if not match:
            raise ValueError("Consulta CREATE TABLE no válida.")
        
        nombre_tabla = match.group(1)
        columnas_definidas = match.group(2)
        columnas = [col.strip() for col in re.split(r',\s*(?![^()]*\))', columnas_definidas)]

        if nombre_tabla in self.estructuras_tablas:
            raise ValueError(f"La tabla '{nombre_tabla}' ya existe.")

        try:
            self._buscar_tabla(nombre_tabla)
            raise ValueError(f"La tabla '{nombre_tabla}' ya existe en almacenamiento.")
        except ValueError:
            pass

        self.estructuras_tablas[nombre_tabla] = columnas
        
        datos_tabla = json.dumps({
            "nombre": nombre_tabla,
            "columnas": columnas,
            "filas": []
        })
        direccion_logica = self.hdd.escribir_dato(datos_tabla, prefijo=f"tabla_{nombre_tabla}")
        print(f"Tabla '{nombre_tabla}' creada con columnas: {columnas}, dirección lógica: {direccion_logica}")
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

        direccion_logica_tabla, tabla_data = self._buscar_tabla(nombre_tabla)
        
        direccion_fila = self.hdd.escribir_dato(json.dumps(datos), prefijo=f"fila_{nombre_tabla}")
        tabla_data["filas"].append(direccion_fila)

        self.hdd.escribir_dato(json.dumps(tabla_data), direccion_logica_tabla)
        print(f"Datos insertados en '{nombre_tabla}': {datos}")
        return True

    def seleccionar_datos(self, query):
        match = re.match(r"SELECT \* FROM (\w+);", query)
        if not match:
            raise ValueError("Consulta SELECT no válida.")
        
        nombre_tabla = match.group(1)
        if nombre_tabla not in self.estructuras_tablas:
            raise ValueError(f"La tabla '{nombre_tabla}' no existe.")

        direccion_logica_tabla, tabla_data = self._buscar_tabla(nombre_tabla)

        filas = []
        for direccion_fila in tabla_data["filas"]:
            datos = self.hdd.leer_dato(direccion_fila)
            filas.append(json.loads(datos))

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

        direccion_logica_tabla, tabla_data = self._buscar_tabla(nombre_tabla)
        
        filas_actualizadas = []
        encontrado = False
        for direccion_fila in tabla_data["filas"]:
            datos = json.loads(self.hdd.leer_dato(direccion_fila))
            if int(datos[0]) == id_a_eliminar:
                encontrado = True
                self.hdd.tabla_direcciones.eliminar_direccion(direccion_fila)
            else:
                filas_actualizadas.append(direccion_fila)

        if not encontrado:
            print(f"No se encontró el ID={id_a_eliminar} en '{nombre_tabla}'.")
            return False

        tabla_data["filas"] = filas_actualizadas
        self.hdd.escribir_dato(json.dumps(tabla_data), direccion_logica_tabla)
        print(f"Datos con id={id_a_eliminar} eliminados de '{nombre_tabla}'.")
        return True

    def eliminar_tabla(self, query):
        match = re.match(r"DROP TABLE\s+(\w+)\s*;?\s*$", query)
        if not match:
            raise ValueError("Consulta DROP TABLE no válida.")
        
        nombre_tabla = match.group(1)
        
        if nombre_tabla in self.estructuras_tablas:
            del self.estructuras_tablas[nombre_tabla]
        
        try:
            direccion = None
            for dir_logica in self.hdd.tabla_direcciones.direcciones.copy():
                if dir_logica.startswith(f"tabla_{nombre_tabla}"):
                    direccion = dir_logica
                    break
            
            if direccion:
                self.hdd.tabla_direcciones.eliminar_direccion(direccion)
                print(f"Tabla '{nombre_tabla}' eliminada correctamente.")
                return True
            else:
                raise ValueError(f"La tabla '{nombre_tabla}' no existe.")
        except Exception as e:
            raise ValueError(f"Error al eliminar la tabla: {str(e)}")

    def _buscar_tabla(self, nombre_tabla):
        """Busca una tabla en el almacenamiento por su nombre."""
        for dir_logica in self.hdd.tabla_direcciones.direcciones:
            if dir_logica.startswith(f"tabla_{nombre_tabla}"):
                datos = json.loads(self.hdd.leer_dato(dir_logica))
                if datos.get("nombre") == nombre_tabla:
                    return dir_logica, datos
        raise ValueError(f"Tabla '{nombre_tabla}' no encontrada.")
