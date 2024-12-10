class Tabla:
    def __init__(self, nombre):
        self.nombre = nombre
        self.columnas = []  
        self.datos = []     

    def agregar_columna(self, nombre, tipo, tamano=None):
        if tipo not in ["int", "float", "varchar"]:
            raise ValueError(f"Tipo de dato '{tipo}' no soportado.")
        if tipo == "varchar" and (tamano is None or tamano <= 0):
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
            elif tipo == "float":
                if not isinstance(valor, float):
                    raise ValueError(f"El valor para '{nombre}' debe ser un flotante.")
            elif tipo == "varchar":
                if not isinstance(valor, str):
                    raise ValueError(f"El valor para '{nombre}' debe ser una cadena.")
                if len(valor) > tamano:
                    raise ValueError(f"El valor para '{nombre}' excede el tamaño máximo de {tamano}.")
            registro[nombre] = valor

        self.datos.append(registro)
        print(f"Dato insertado en la tabla '{self.nombre}': {registro}")

    def buscar_dato(self, clave, valor):
        for dato in self.datos:
            if dato.get(clave) == valor:
                return dato
        return None


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
