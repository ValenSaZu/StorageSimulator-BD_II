class Sector:
    def __init__(self):
        self.datos = ""
        self.ocupado = False
        self.offset = 0

class Pista:
    def __init__(self, num_sectores):
        self.sectores = [Sector() for _ in range(num_sectores)]

class Disco:
    def __init__(self, num_pistas, num_sectores_por_pista):
        self.pistas = [Pista(num_sectores_por_pista) for _ in range(num_pistas)]

    def escribir_dato_con_offset(self, pista_index, sector_index, datos):
        sector = self.pistas[pista_index].sectores[sector_index]
        
        if sector.ocupado:
            sector.offset += len(sector.datos)
            sector.datos += f" | {datos}"
        else:
            sector.datos = datos
            sector.ocupado = True
            sector.offset = len(datos)

    def leer_dato(self, pista_index, sector_index):
        sector = self.pistas[pista_index].sectores[sector_index]
        if sector.ocupado:
            return sector.datos
        return "Sector vacío"
