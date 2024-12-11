class Tabla:
    def __init__(self, nombre):
        self.nombre = nombre
        self.columnas = []  
        self.datos = []     

    def agregar_columna(self, nombre, tipo, tamano=None):
        tipos_permitidos = ["int", "bigint", "float", "decimal", "varchar", "text", "date", "datetime", "boolean"]
        if tipo not in tipos_permitidos:
            raise ValueError(f"Tipo de dato '{tipo}' no soportado.")
        if tipo in ["varchar"] and (tamano is None or tamano <= 0):
            raise ValueError("El tipo 'varchar' requiere un tamaño mayor a 0.")
        self.columnas.append((nombre, tipo, tamano))
        print(f"Columna '{nombre}' agregada con tipo '{tipo}' y tamaño '{tamano}'.")

    def insertar_dato(self, datos):
        if len(datos) != len(self.columnas):
            raise ValueError("La cantidad de datos no coincide con las columnas.")

        registro = {}
        for (nombre, tipo, tamano), valor in zip(self.columnas, datos):
            if tipo == "int":
                if not isinstance(valor, int):
                    raise ValueError(f"El valor para '{nombre}' debe ser un entero.")
            elif tipo == "bigint":
                if not isinstance(valor, int):
                    raise ValueError(f"El valor para '{nombre}' debe ser un entero grande.")
            elif tipo == "float":
                if not isinstance(valor, (float, int)):
                    raise ValueError(f"El valor para '{nombre}' debe ser un flotante.")
            elif tipo == "decimal":
                if not re.match(r"^\d+(\.\d+)?$", str(valor)):
                    raise ValueError(f"El valor para '{nombre}' debe ser decimal.")
            elif tipo == "varchar":
                if not isinstance(valor, str) or len(valor) > tamano:
                    raise ValueError(f"El valor para '{nombre}' excede el tamaño máximo de {tamano}.")
            elif tipo == "text":
                if not isinstance(valor, str):
                    raise ValueError(f"El valor para '{nombre}' debe ser texto.")
            elif tipo == "date":
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(valor)):
                    raise ValueError(f"El valor para '{nombre}' debe ser una fecha (YYYY-MM-DD).")
            elif tipo == "datetime":
                if not re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", str(valor)):
                    raise ValueError(f"El valor para '{nombre}' debe ser fecha y hora (YYYY-MM-DD HH:MM:SS).")
            elif tipo == "boolean":
                if not isinstance(valor, bool):
                    raise ValueError(f"El valor para '{nombre}' debe ser booleano (True o False).")
            registro[nombre] = valor

        self.datos.append(registro)
        print(f"Dato insertado en la tabla '{self.nombre}': {registro}")

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
