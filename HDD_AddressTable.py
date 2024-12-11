import json

class HDD:
    def __init__(self, num_platos, num_pistas_por_plato, num_sectores_por_pista, tamano_bytes):
        self.num_platos = num_platos
        self.num_pistas_por_plato = num_pistas_por_plato
        self.num_sectores_por_pista = num_sectores_por_pista
        self.tamano_bytes = tamano_bytes
        self.sectores = [[[None for _ in range(num_sectores_por_pista)]
                          for _ in range(num_pistas_por_plato)]
                         for _ in range(num_platos)]

    def escribir_dato(self, dato):
        bytes_restantes = len(dato)
        direccion = []
        for plato in range(self.num_platos):
            for pista in range(self.num_pistas_por_plato):
                for sector in range(self.num_sectores_por_pista):
                    if self.sectores[plato][pista][sector] is None:
                        if bytes_restantes > self.tamano_bytes:
                            self.sectores[plato][pista][sector] = dato[:self.tamano_bytes]
                            direccion.append((plato, pista, sector))
                            dato = dato[self.tamano_bytes:]
                            bytes_restantes -= self.tamano_bytes
                        else:
                            self.sectores[plato][pista][sector] = dato
                            direccion.append((plato, pista, sector))
                            return direccion
        raise ValueError("No hay espacio suficiente para almacenar el dato.")

    def leer_dato(self, direccion):
        datos = []
        for (plato, pista, sector) in direccion:
            if self.sectores[plato][pista][sector] is not None:
                datos.append(self.sectores[plato][pista][sector])
        return ''.join(datos)

    def mostrar_sectores(self):
        return self.sectores