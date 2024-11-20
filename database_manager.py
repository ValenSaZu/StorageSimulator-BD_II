# database_manager.py

from SSDStructure import SSD
from HDDStructure import HDD

class DatabaseManager:
    def __init__(self, tipo_disco, tipo_bd, num_bloques=10, num_paginas_por_bloque=4, num_pistas_por_plato=4, num_sectores_por_pista=4):
        self.tipo_disco = tipo_disco.lower()
        self.tipo_bd = tipo_bd.lower()
        
        if self.tipo_disco == 'ssd':
            self.storage = SSD(num_bloques, num_paginas_por_bloque)
        elif self.tipo_disco == 'hdd':
            self.storage = HDD(num_bloques, num_pistas_por_plato, num_sectores_por_pista)
        else:
            raise ValueError("Tipo de disco no soportado: debe ser 'SSD' o 'HDD'.")

    def escribir_dato(self, direccion_logica, datos):
        """Escribe datos en la dirección lógica especificada."""
        try:
            self.storage.escribir_dato(direccion_logica, datos)
            return f"Dato '{datos}' escrito en la dirección lógica '{direccion_logica}'."
        except ValueError as e:
            return f"Error al escribir dato: {str(e)}"

    def leer_dato(self, direccion_logica):
        """Lee datos de la dirección lógica especificada."""
        try:
            return self.storage.leer_dato(direccion_logica)
        except ValueError:
            return f"Error: Dirección lógica '{direccion_logica}' no encontrada."

    def borrar_dato(self, direccion_logica):
        """Borra los datos en la dirección lógica especificada."""
        if self.tipo_disco == 'ssd':
            raise NotImplementedError("El método de borrado específico no está implementado para SSD.")
        elif self.tipo_disco == 'hdd':
            # Para HDD, se podría implementar la lógica de borrado
            raise NotImplementedError("El método de borrado específico no está implementado para HDD.")

    def realizar_query(self, consulta):
        """Ejecuta una consulta en la base de datos."""
        if self.tipo_bd == 'sql':
            return self._ejecutar_query_sql(consulta)
        elif self.tipo_bd == 'nosql':
            return self._ejecutar_query_nosql(consulta)
        else:
            return "Error: Tipo de base de datos no soportado."

    def _ejecutar_query_sql(self, consulta):
        """Ejecuta una consulta SQL."""
        # Implementar la lógica de consulta SQL
        return f"Consulta SQL ejecutada: {consulta}"

    def _ejecutar_query_nosql(self, consulta):
        """Ejecuta una consulta NoSQL."""
        # Implementar la lógica de consulta NoSQL
        return f"Consulta NoSQL ejecutada: {consulta}"

    def listar_datos(self):
        """Lista todos los datos almacenados en el disco."""
        datos = {}
        for bloque in self.storage.bloques:
            for pagina in bloque.paginas:
                if pagina.ocupado:
                    datos[pagina.datos] = pagina.ocupado
        return datos