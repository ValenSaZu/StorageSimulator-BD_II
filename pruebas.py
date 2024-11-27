from HDDStructure import HDD
from database_manager import SQLProcessor

def main():
    hdd = HDD(num_platos=1, num_pistas_por_plato=10, num_sectores_por_pista=4, tamano_bytes=128)

    sql_processor = SQLProcessor(hdd)

    create_table_query = "CREATE TABLE usuarios (id, nombre, edad);"
    try:
        sql_processor.procesar_query(create_table_query)
        print("Tabla 'usuarios' creada exitosamente.")
    except ValueError as e:
        print(f"Error al crear la tabla: {e}")

    insert_data_query = "INSERT INTO usuarios VALUES (1, 'Juan', 25);"
    try:
        sql_processor.procesar_query(insert_data_query)
        print("Datos insertados correctamente en la tabla 'usuarios'.")
    except ValueError as e:
        print(f"Error al insertar datos: {e}")

    select_query = "SELECT * FROM usuarios;"
    try:
        resultados = sql_processor.procesar_query(select_query)
        print("Datos seleccionados de la tabla 'usuarios':")
        for fila in resultados:
            print(fila)
    except ValueError as e:
        print(f"Error al seleccionar datos: {e}")

if __name__ == "__main__":
    main()
