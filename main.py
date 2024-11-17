from DiskStructure import Disco
from AddressTable import TablaDeDirecciones

disco = Disco(num_pistas=3, num_sectores_por_pista=4)
tabla = TablaDeDirecciones()

datos_a_escribir = []

for id_registro, pista, sector, datos in datos_a_escribir:
    disco.escribir_dato_con_offset(pista, sector, datos)
    sector_actual = disco.pistas[pista].sectores[sector]
    tabla.insertar_registro(id_registro, pista, sector, sector_actual.offset, len(datos), datos)

print("Contenido de la Tabla de Direcciones:")
for registro in tabla.tabla:
    print(tabla.leer_registro(registro.id_registro))

print("\nDatos en el Disco:")
for pista_index in range(len(disco.pistas)):
    for sector_index, sector in enumerate(disco.pistas[pista_index].sectores):
        print(f"Pista {pista_index}, Sector {sector_index}: {sector.datos}")
