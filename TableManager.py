import json
from datetime import datetime
from decimal import Decimal

class Tabla:
    def __init__(self, nombre):
        self.nombre = nombre
        self.columnas = []
        self.datos = []
        self.primary_key = None

    def agregar_columna(self, nombre, tipo, tamano=None, es_primary_key=False, no_null=False):
        tipos_validos = ["int", "bigint", "float", "decimal", "varchar", "text", "date", "datetime", "boolean"]
        if tipo not in tipos_validos:
            raise ValueError(f"Tipo de dato '{tipo}' no soportado.")
        if tipo in ["varchar", "decimal"]:
            if tipo == "varchar" and (tamano is None or tamano <= 0):
                raise ValueError(f"El tipo '{tipo}' requiere un tamaño mayor a 0.")
            if tipo == "decimal" and (not isinstance(tamano, tuple) or len(tamano) != 2):
                raise ValueError(f"El tipo '{tipo}' requiere una tupla (precision, scale).")
        self.columnas.append((nombre, tipo, tamano, es_primary_key, no_null))
        if es_primary_key:
            if self.primary_key is not None:
                raise ValueError("Ya existe una clave primaria en la tabla.")
            self.primary_key = nombre
        print(f"Columna '{nombre}' agregada con tipo '{tipo}' y tamaño '{tamano}'.")

    def insertar_dato(self, datos):
        if len(datos) != len(self.columnas):
            raise ValueError("La cantidad de datos no coincide con las columnas.")
        
        registro = {}
        for (nombre, tipo, tamano, es_primary_key, no_null), valor in zip(self.columnas, datos):
            if no_null and (valor is None or (isinstance(valor, str) and valor.strip() == "")):
                raise ValueError(f"La columna '{nombre}' no puede ser nula.")
            
            if tipo in ["int", "bigint"]:
                if not isinstance(valor, int):
                    raise ValueError(f"El valor para '{nombre}' debe ser un entero.")
            elif tipo == "float":
                if not isinstance(valor, float):
                    raise ValueError(f"El valor para '{nombre}' debe ser un número flotante.")
            elif tipo == "decimal":
                if not isinstance(valor, float):
                    raise ValueError(f"El valor para '{nombre}' debe ser un número decimal.")
                if tamano is not None:
                    precision, scale = tamano
                    partes = str(valor).split('.')
                    integer_part = partes[0]
                    decimal_part = partes[1] if len(partes) > 1 else ''
                    if len(integer_part) > (precision - scale) or len(decimal_part) > scale:
                        raise ValueError(f"El valor para '{nombre}' excede la precisión o escala especificada. Precisión: {precision}, Escala: {scale}.")
            elif tipo in ["varchar", "text"]:
                if not isinstance(valor, str):
                    raise ValueError(f"El valor para '{nombre}' debe ser una cadena.")
                if tipo == "varchar" and len(valor) > tamano:
                    raise ValueError(f"El valor para '{nombre}' excede el tamaño máximo de {tamano}.")
            elif tipo == "date":
                if not isinstance(valor, str) or not self._validar_fecha(valor):
                    raise ValueError(f"El valor para '{nombre}' debe ser una fecha en formato YYYY-MM-DD.")
            elif tipo == "datetime":
                if not isinstance(valor, str) or not self._validar_datetime(valor):
                    raise ValueError(f"El valor para '{nombre}' debe ser una fecha y hora en formato YYYY-MM-DD HH:MM:SS.")
            elif tipo == "boolean":
                if not isinstance(valor, bool):
                    raise ValueError(f"El valor para '{nombre}' debe ser un booleano (True o False).")
            registro[nombre] = valor

        # Verificar clave primaria
        if self.primary_key:
            pk_valor = registro[self.primary_key]
            if self.buscar_dato(self.primary_key, pk_valor):
                raise ValueError(f"Valor duplicado para la clave primaria '{self.primary_key}': {pk_valor}")

        self.datos.append(registro)
        print(f"Dato insertado en la tabla '{self.nombre}': {registro}")

    def buscar_dato(self, clave, valor):
        for dato in self.datos:
            if dato.get(clave) == valor:
                return dato
        return None

    @staticmethod
    def _validar_fecha(valor):
        try:
            datetime.strptime(valor, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def _validar_datetime(valor):
        try:
            datetime.strptime(valor, "%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            return False


class AdministradorTablas:
    def __init__(self):
        self.tablas = {}

    def crear_tabla(self, nombre):
        if nombre in self.tablas:
            raise ValueError(f"Ya existe una tabla con el nombre '{nombre}'.")
        self.tablas[nombre] = Tabla(nombre)
        print(f"Tabla '{nombre}' creada con éxito.")

    def obtener_tabla(self, nombre):
        return self.tablas.get(nombre, None)

    def listar_tablas(self):
        return list(self.tablas.keys())
