from HDD_AddressTable import TablaDirecciones_HDD

class Sector:
    
    def __init__(self):
        self.datos = ""
        self.ocupado = False
        self.offset = 0

class Pista:
    
    def __init__(self, num_sectores):
        self.sectores = [Sector() for _ in range(num_sectores)]

class Plato:
 
    def __init__(self, num_pistas, num_sectores_por_pista):
        self.pistas = [Pista(num_sectores_por_pista) for _ in range(num_pistas)]

class HDD:
    
    def __init__(self, num_platos, num_pistas_por_plato, num_sectores_por_pista):
        self.platos = [Plato(num_pistas_por_plato, num_sectores_por_pista) for _ in range(num_platos)]
        self.tabla_direcciones = TablaDirecciones_HDD()

    def _traducir_direccion(self, direccion_logica):
        direccion_fisica = self.tabla_direcciones.obtener_direccion(direccion_logica)
        if direccion_fisica:
            return map(int, direccion_fisica.split("-"))
        raise ValueError("La dirección lógica no está mapeada a ninguna dirección física.")

    def escribir_dato(self, direccion_logica, datos):
        try:
            plato_index, pista_index, sector_index = self._traducir_direccion(direccion_logica)
            plato = self.platos[plato_index]
            sector = plato.pistas[pista_index].sectores[sector_index]

            if sector.ocupado:
                sector.offset += len(sector.datos)
                sector.datos += f" | {datos}"
            else:
                sector.datos = datos
                sector.ocupado = True
                sector.offset = len(datos)
            self.asignar_direccion(direccion_logica, plato_index, pista_index, sector_index)
        except ValueError as e:
            print(e)

    def leer_dato(self, direccion_logica):
        try:
            plato_index, pista_index, sector_index = self._traducir_direccion(direccion_logica)
            plato = self.platos[plato_index]
            sector = plato.pistas[pista_index].sectores[sector_index]

            return sector.datos if sector.ocupado else "Sector vacío"
        except ValueError:
            return f"Error: Dirección lógica {direccion_logica} no válida."

    def asignar_direccion(self, direccion_logica, plato_index, pista_index, sector_index):
        direccion_fisica = f"{plato_index}-{pista_index}-{sector_index}"
        self.tabla_direcciones.agregar_direccion(direccion_logica, direccion_fisica)