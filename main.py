#solo es una prueba
from HDDStructure import HDD
from HDD_AddressTable import TablaDirecciones_HDD
from database_manager import SQLProcessor

if __name__ == "__main__":
    hdd = HDD(num_platos=2, num_pistas_por_plato=10, num_sectores_por_pista=20, tamano_bytes=512)
    sql_processor = SQLProcessor(hdd)
    print("Disco duro virtual inicializado correctamente.")

    try:
        try:
            sql_processor.procesar_query("DROP TABLE PRODUCTO;")
        except ValueError:
            pass

        sql_processor.procesar_query("CREATE TABLE PRODUCTO (index INTEGER PRIMARY KEY, item VARCHAR(40) NOT NULL, cost DECIMAL(10, 2) NOT NULL, tax DECIMAL(10, 2) NOT NULL, total DECIMAL(10, 2) NOT NULL);")
        print("Tabla PRODUCTO creada exitosamente.")

        sql_processor.procesar_query("INSERT INTO PRODUCTO VALUES (1, 'Producto A', 10.00, 1.50, 11.50);")
        print("Datos insertados exitosamente.")

        sql_processor.procesar_query("SELECT * FROM PRODUCTO;")

    except Exception as e:
        print(f"Error: {str(e)}")