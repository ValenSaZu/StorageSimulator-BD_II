class Sector:
    
    def __init__(self, tamano_bytes):
        self.datos = ""
        self.ocupado = False
        self.offset = 0
        self.tamano_bytes = tamano_bytes  # Tamaño en bytes del sector

class Pista:
    
    def __init__(self, num_sectores, tamano_bytes):
        self.sectores = [Sector(tamano_bytes) for _ in range(num_sectores)]

class Plato:
 
    def __init__(self, num_pistas, num_sectores_por_pista, tamano_bytes):
        self.pistas = [Pista(num_sectores_por_pista, tamano_bytes) for _ in range(num_pistas)]

class HDD:
    
    def __init__(self, num_platos, num_pistas_por_plato, num_sectores_por_pista, tamano_bytes):
        self.platos = [Plato(num_pistas_por_plato, num_sectores_por_pista, tamano_bytes) for _ in range(num_platos)]
        self.tabla_direcciones = TablaDirecciones_HDD()

    def escribir_dato(self, direccion_logica, datos):
        try:
            plato_index, pista_index, sector_index = self._traducir_direccion(direccion_logica)
            plato = self.platos[plato_index]
            sector = plato.pistas[pista_index].sectores[sector_index]

            if sector.ocupado:
                if sector.offset + len(datos) <= sector.tamano_bytes:
                    sector.datos += f" | {datos}"
                    sector.offset += len(datos)
                else:
                    raise ValueError("No hay suficiente espacio en el sector para almacenar los datos.")
            else:
                sector.datos = datos
                sector.ocupado = True
                sector.offset = len(datos)
            self.asignar_direccion(direccion_logica, plato_index, pista_index, sector_index)
        except ValueError as e:
            print(e)