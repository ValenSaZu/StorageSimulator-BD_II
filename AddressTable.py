class Registro:
    def __init__(self, id_registro, pista, sector, offset, tamaño, datos):
        self.id_registro = id_registro
        self.pista = pista
        self.sector = sector
        self.offset = offset
        self.tamaño = tamaño
        self.datos = datos

class TablaDeDirecciones:
    def __init__(self):
        self.tabla = []

    def insertar_registro(self, id_registro, pista, sector, offset, tamaño, datos):
        nuevo_registro = Registro(id_registro, pista, sector, offset, tamaño, datos)
        self.tabla.append(nuevo_registro)

    def leer_registro(self, id_registro):
        for registro in self.tabla:
            if registro.id_registro == id_registro:
                return vars(registro)
        return None
