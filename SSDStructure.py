from SSD_AdressTable import TablaDirecciones_SSD

class Pagina:
    def __init__(self):
        self.datos = ""
        self.ocupado = False

class Bloque:
    def __init__(self, num_paginas):
        self.paginas = [Pagina() for _ in range(num_paginas)]
        self.borrado = False

    def borrar_bloque(self):
        for pagina in self.paginas:
            pagina.datos = ""
            pagina.ocupado = False
        self.borrado = True

class SSD:
    
    def __init__(self, num_bloques, num_paginas_por_bloque):
        self.bloques = [Bloque(num_paginas_por_bloque) for _ in range(num_bloques)]
        self.tabla_direcciones = TablaDirecciones_SSD()

    def escribir_dato(self, direccion_logica, datos):
        for indice_bloque, bloque in enumerate(self.bloques):
            for indice_pagina, pagina in enumerate(bloque.paginas):
                if not pagina.ocupado:
                    pagina.datos = datos
                    pagina.ocupado = True
                    direccion_fisica = (indice_bloque, indice_pagina)
                    self.tabla_direcciones.agregar_direccion(direccion_logica, direccion_fisica)
                    return
        raise ValueError("Error: No hay espacio disponible para escribir.")

    def leer_dato(self, direccion_logica):
        direccion_fisica = self.tabla_direcciones.obtener_direccion(direccion_logica)
        if direccion_fisica:
            indice_bloque, indice_pagina = direccion_fisica
            pagina = self.bloques[indice_bloque].paginas[indice_pagina]
            return pagina.datos
        return "Error: Dirección lógica no encontrada."

    def borrar_bloque(self, indice_bloque):
        bloque = self.bloques[indice_bloque]
        bloque.borrar_bloque()
        direcciones_a_eliminar = [
            logica for logica, (b, _) in self.tabla_direcciones.direcciones.items() if b == indice_bloque
        ]
        for direccion in direcciones_a_eliminar:
            self.tabla_direcciones.eliminar_direccion(direccion)