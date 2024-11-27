from HDD_AddressTable import TablaDirecciones_HDD

class Sector:
    def __init__(self, tamano_bytes):
        self.datos = ""
        self.ocupado = False
        self.offset = 0
        self.tamano_bytes = tamano_bytes

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
        self.contador_direcciones = 0

    def generar_direccion_logica(self, prefijo):
        self.contador_direcciones += 1
        return f"{prefijo}:{self.contador_direcciones}"

    def escribir_dato(self, datos, prefijo="dato"):
        direccion_logica = self.generar_direccion_logica(prefijo)
        for plato_index, plato in enumerate(self.platos):
            for pista_index, pista in enumerate(plato.pistas):
                for sector_index, sector in enumerate(pista.sectores):
                    if not sector.ocupado:
                        sector.datos = datos
                        sector.ocupado = True
                        sector.offset = len(datos)
                        self.tabla_direcciones.agregar_direccion(direccion_logica, f"{plato_index}-{pista_index}-{sector_index}")
                        return direccion_logica
        raise ValueError("No hay espacio disponible en el HDD.")

    def leer_dato(self, direccion_logica):
        plato_index, pista_index, sector_index = self._traducir_direccion(direccion_logica)
        plato = self.platos[plato_index]
        sector = plato.pistas[pista_index].sectores[sector_index]
        return sector.datos if sector.ocupado else "Sector vacío"

    def _traducir_direccion(self, direccion_logica):
        direccion_fisica = self.tabla_direcciones.obtener_direccion(direccion_logica)
        if direccion_fisica:
            print(f"Traduciendo {direccion_logica} -> {direccion_fisica}")
            return map(int, direccion_fisica.split("-"))
        raise ValueError(f"La dirección lógica {direccion_logica} no está mapeada a ninguna dirección física.")
