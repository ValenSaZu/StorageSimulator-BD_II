from DiskStructure import Disco
from AddressTable import TablaDeDirecciones

disco = Disco(num_platos=4, num_pistas_por_plato=3, num_sectores_por_pista=4)
tabla = TablaDeDirecciones()

datos_a_escribir = []

for id_registro, plato, pista, sector, datos in datos_a_escribir:
    disco.escribir_dato_con_offset(plato, pista, sector, datos)
    sector_actual = disco.platos[plato].pistas[pista].sectores[sector]
    tabla.insertar_registro(id_registro, plato, pista, sector, sector_actual.offset, len(datos), datos)

print("Contenido de la Tabla de Direcciones:")
for registro in tabla.tabla:
    print(tabla.leer_registro(registro.id_registro))

print("\nDatos en el Disco:")
for plato_index in range(len(disco.platos)):
    for pista_index in range(len(disco.platos[plato_index].pistas)):
        for sector_index, sector in enumerate(disco.platos[plato_index].pistas[pista_index].sectores):
            print(f"Plato {plato_index}, Pista {pista_index}, Sector {sector_index}: {sector.datos}")
