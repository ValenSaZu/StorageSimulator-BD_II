from HDD_AddressTable import TablaDirecciones_HDD
import json

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
        self.num_platos = num_platos
        self.num_pistas_por_plato = num_pistas_por_plato
        self.num_sectores_por_pista = num_sectores_por_pista
        self.tamano_bytes = tamano_bytes
        self.platos = [Plato(num_pistas_por_plato, num_sectores_por_pista, tamano_bytes) for _ in range(num_platos)]
        self.tabla_direcciones = TablaDirecciones_HDD()
        self.contador_direcciones = 0

    def generar_direccion_logica(self, prefijo):
        self.contador_direcciones += 1
        return f"{prefijo}:{self.contador_direcciones}"

    def escribir_dato(self, datos, prefijo="dato"):
        datos_bytes = datos.encode('utf-8')
        tamano_datos = len(datos_bytes)
        tamano_sector = self.platos[0].pistas[0].sectores[0].tamano_bytes

        fragmentos = [datos_bytes[i:i + tamano_sector] for i in range(0, tamano_datos, tamano_sector)]
        direcciones_fragmentos = []

        for fragmento in fragmentos:
            direccion_logica = self.generar_direccion_logica(prefijo)
            espacio_asignado = False
            for plato_index, plato in enumerate(self.platos):
                for pista_index, pista in enumerate(plato.pistas):
                    for sector_index, sector in enumerate(pista.sectores):
                        if not sector.ocupado:
                            sector.datos = fragmento.decode('utf-8', errors='replace')
                            sector.ocupado = True
                            sector.offset = len(fragmento)
                            self.tabla_direcciones.agregar_direccion(direccion_logica, f"{plato_index}-{pista_index}-{sector_index}")
                            direcciones_fragmentos.append(direccion_logica)
                            espacio_asignado = True
                            break
                    if espacio_asignado:
                        break
                if espacio_asignado:
                    break
            if not espacio_asignado:
                raise ValueError("No hay espacio disponible en el HDD para guardar todos los fragmentos del dato.")
        return direcciones_fragmentos

    def leer_dato(self, direcciones_logicas):
        datos = b""
        for direccion_logica in direcciones_logicas:
            try:
                plato_index, pista_index, sector_index = self._traducir_direccion(direccion_logica)
            except ValueError as e:
                raise ValueError(f"Error en la dirección lógica {direccion_logica}: {e}")

            plato = self.platos[plato_index]
            sector = plato.pistas[pista_index].sectores[sector_index]
            if sector.ocupado:
                datos += sector.datos.encode('utf-8')
            else:
                raise ValueError(f"Sector {direccion_logica} vacío o no asignado.")
        return datos.decode('utf-8', errors='replace')

    def _traducir_direccion(self, direccion_logica):
        direccion_fisica = self.tabla_direcciones.obtener_direccion(direccion_logica)
        if direccion_fisica:
            return map(int, direccion_fisica.split("-"))
        raise ValueError(f"La dirección lógica {direccion_logica} no está mapeada a ninguna dirección física.")

    def obtener_direccion_fisica(self, dato):
        dato_str = str(dato)
        for plato_index, plato in enumerate(self.platos):
            for pista_index, pista in enumerate(plato.pistas):
                for sector_index, sector in enumerate(pista.sectores):
                    if sector.datos == dato_str:
                        print(f"Dato encontrado en Plato: {plato_index}, Pista: {pista_index}, Sector: {sector_index}")
                        return plato_index, pista_index, sector_index
        print("Dato no encontrado en ningún sector.")
        return None

    def obtener_datos_completos(self, dato_id):
        datos_encontrados = {"datos": [], "ubicaciones": []}
        dato_id_str = str(dato_id)

        for plato_index, plato in enumerate(self.platos):
            for pista_index, pista in enumerate(plato.pistas):
                for sector_index, sector in enumerate(pista.sectores):
                    if sector.ocupado:
                        try:
                            dato = eval(sector.datos)
                            if isinstance(dato, dict) and dato.get("Index") == dato_id:
                                datos_encontrados["datos"].append(dato)
                                datos_encontrados["ubicaciones"].append((plato_index, pista_index, sector_index))
                        except (SyntaxError, ValueError):
                            continue

        return datos_encontrados if datos_encontrados["datos"] else None