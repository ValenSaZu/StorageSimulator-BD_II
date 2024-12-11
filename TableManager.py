class Tabla:
    def __init__(self, nombre):
        self.nombre = nombre
        self.columnas = []
        self.datos = []

    def agregar_columna(self, nombre, tipo, tamano=None):
        tipos_validos = ["int", "bigint", "float", "decimal", "varchar", "text", "date", "datetime", "boolean"]
        if tipo not in tipos_validos:
            raise ValueError(f"Tipo de dato '{tipo}' no soportado.")
        if tipo in ["varchar", "decimal"] and (tamano is None or tamano <= 0):
            raise ValueError(f"El tipo '{tipo}' requiere un tamaño mayor a 0.")
        self.columnas.append((nombre, tipo, tamano))
        print(f"Columna '{nombre}' agregada con tipo '{tipo}' y tamaño '{tamano}'.")

    def insertar_dato(self, datos):
        if len(datos) != len(self.columnas):
            raise ValueError("La cantidad de datos no coincide con las columnas.")
        
        registro = {}
        for (nombre, tipo, tamano), valor in zip(self.columnas, datos):
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
                    p, s = divmod(tamano, 10)
                    partes = str(valor).split('.')
                    if len(partes[0]) > p or len(partes[1]) > s:
                        raise ValueError(f"El valor para '{nombre}' excede el tamaño máximo de precisión {tamano}.")
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

        self.datos.append(registro)
        print(f"Dato insertado en la tabla '{self.nombre}': {registro}")

    def buscar_dato(self, clave, valor):
        for dato in self.datos:
            if dato.get(clave) == valor:
                return dato
        return None

    @staticmethod
    def _validar_fecha(valor):
        from datetime import datetime
        try:
            datetime.strptime(valor, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def _validar_datetime(valor):
        from datetime import datetime
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