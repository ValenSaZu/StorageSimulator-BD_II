import pygame
import sys
import csv
from tkinter import Tk, filedialog
from HDDStructure import HDD
from UIComponents import InputBox, draw_button, draw_label, draw_disk
from TableManager import AdministradorTablas, Tabla
import re

pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Base de Datos")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (100, 200, 255)

plato_actual = 0

def show_start_screen():
    font = pygame.font.Font(None, 74)
    text = font.render("Simulador de Base de Datos", True, BLACK)
    screen.fill(WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

def draw_disk_and_buttons(hdd, plato_actual):
    draw_disk(screen, hdd.platos[plato_actual], WIDTH // 2 + 300, HEIGHT // 2, 200)

    prev_plato_button = pygame.Rect(WIDTH // 2 + 100, HEIGHT // 2 + 280, 150, 40)
    next_plato_button = pygame.Rect(WIDTH // 2 + 350, HEIGHT // 2 + 280, 150, 40)

    draw_button(screen, "Plato Anterior", prev_plato_button, LIGHT_BLUE, BLACK)
    draw_button(screen, "Siguiente Plato", next_plato_button, LIGHT_BLUE, BLACK)

    return prev_plato_button, next_plato_button

def create_disk_interface():
    platos_box = InputBox(WIDTH // 2 - 125, HEIGHT // 2 - 150, 250, 40)
    pistas_box = InputBox(WIDTH // 2 - 125, HEIGHT // 2 - 90, 250, 40)
    sectores_box = InputBox(WIDTH // 2 - 125, HEIGHT // 2 - 30, 250, 40)
    bytes_box = InputBox(WIDTH // 2 - 125, HEIGHT // 2 + 30, 250, 40)

    configure_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            platos_box.handle_event(event)
            pistas_box.handle_event(event)
            sectores_box.handle_event(event)
            bytes_box.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if configure_button.collidepoint(event.pos):
                    try:
                        num_platos = int(platos_box.get_text())
                        num_pistas = int(pistas_box.get_text())
                        num_sectores = int(sectores_box.get_text())
                        tamano_bytes = int(bytes_box.get_text())
                        return HDD(num_platos, num_pistas, num_sectores, tamano_bytes)
                    except ValueError:
                        print("Error: Todos los valores deben ser enteros positivos.")

        screen.fill(WHITE)

        draw_label(screen, "Configuración del Disco Duro", WIDTH // 2 - 300, HEIGHT // 2 - 220, font=pygame.font.Font(None, 48))
        draw_label(screen, "Número de Platos:", WIDTH // 2 - 350, HEIGHT // 2 - 140)
        draw_label(screen, "Número de Pistas:", WIDTH // 2 - 350, HEIGHT // 2 - 80)
        draw_label(screen, "Número de Sectores:", WIDTH // 2 - 350, HEIGHT // 2 - 20)
        draw_label(screen, "Tamaño (bytes/sector):", WIDTH // 2 - 350, HEIGHT // 2 + 40)

        platos_box.draw(screen)
        pistas_box.draw(screen)
        sectores_box.draw(screen)
        bytes_box.draw(screen)

        draw_button(screen, "Configurar", configure_button, LIGHT_BLUE, BLACK)

        pygame.display.flip()

def main_menu(hdd, admin_tablas):
    global plato_actual

    add_data_button = pygame.Rect(WIDTH // 2 - 300, HEIGHT // 2 - 100, 200, 50)
    search_data_button = pygame.Rect(WIDTH // 2 - 300, HEIGHT // 2, 200, 50)
    load_table_button = pygame.Rect(WIDTH // 2 - 300, HEIGHT // 2 + 100, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                prev_plato_button, next_plato_button = draw_disk_and_buttons(hdd, plato_actual)

                if add_data_button.collidepoint(event.pos):
                    upload_csv_interface(hdd, admin_tablas)
                elif search_data_button.collidepoint(event.pos):
                    search_data_interface(hdd, admin_tablas)
                elif load_table_button.collidepoint(event.pos):
                    Tk().withdraw()
                    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
                    if filepath:
                        create_table_from_txt(filepath, admin_tablas)
                elif prev_plato_button.collidepoint(event.pos):
                    plato_actual = (plato_actual - 1) % hdd.num_platos
                elif next_plato_button.collidepoint(event.pos):
                    plato_actual = (plato_actual + 1) % hdd.num_platos

        screen.fill(WHITE)

        draw_button(screen, "Añadir Datos", add_data_button, LIGHT_BLUE, BLACK)
        draw_button(screen, "Buscar Dato", search_data_button, LIGHT_BLUE, BLACK)
        draw_button(screen, "Cargar Tabla", load_table_button, LIGHT_BLUE, BLACK)

        prev_plato_button, next_plato_button = draw_disk_and_buttons(hdd, plato_actual)

        draw_label(screen, f"Plato Actual: {plato_actual + 1} / {hdd.num_platos}", WIDTH // 2 + 200, HEIGHT // 2 + 240)

        pygame.display.flip()

def create_table_from_txt(filepath, admin_tablas):
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()
        
        create_statement = [line.strip() for line in lines if line.strip()]
        
        if not create_statement[0].startswith("CREATE TABLE"):
            raise ValueError("El archivo no contiene una declaración válida de 'CREATE TABLE'.")

        table_name = create_statement[0].split("CREATE TABLE")[1].strip().split("(")[0].strip()
        column_definitions = create_statement[1:-1]
        column_definitions = [col.replace(",", "").strip() for col in column_definitions]
        
        new_table = Tabla(table_name)
        for column_def in column_definitions:
            parts = column_def.split()
            column_name = parts[0]
            column_type = parts[1].lower()
            constraints = parts[2:]
            
            if "varchar" in column_type:
                size = int(column_type.split("(")[1].replace(")", ""))
                new_table.agregar_columna(column_name, "varchar", size)
            elif "integer" in column_type or column_type == "int":
                new_table.agregar_columna(column_name, "int")
            elif "float" in column_type or "decimal" in column_type:
                if "decimal" in column_type:
                    precision, scale = map(int, column_type.split("(")[1].replace(")", "").split(","))
                    new_table.agregar_columna(column_name, "decimal", (precision, scale))
                else:
                    new_table.agregar_columna(column_name, "float")
            elif "boolean" in column_type:
                new_table.agregar_columna(column_name, "boolean")
            elif "date" in column_type:
                new_table.agregar_columna(column_name, "date")
            else:
                raise ValueError(f"Tipo de columna desconocido: {column_type}")
        
        admin_tablas.tablas[table_name] = new_table
        print(f"Tabla '{table_name}' creada con éxito desde el archivo {filepath}.")

    except Exception as e:
        print(f"Error al procesar el archivo '{filepath}': {e}")

def upload_csv_interface(hdd, admin_tablas):
    tablas = admin_tablas.listar_tablas()
    if not tablas:
        print("No hay tablas disponibles.")
        return

    selected_table = None
    Tk().withdraw()
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not filepath:
        print("No se seleccionó ningún archivo.")
        return

    try:
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            try:
                sniffer = csv.Sniffer()
                dialect = sniffer.sniff(csvfile.read(1024))
                csvfile.seek(0)
            except csv.Error:
                print("No se pudo detectar el delimitador, usando coma por defecto.")
                dialect = csv.excel
                dialect.delimiter = ','

            reader = csv.DictReader(csvfile, dialect=dialect)

            csv_headers = [header.strip().strip('"').strip(';') for header in reader.fieldnames]
            print(f"Encabezados del archivo CSV (limpiados): {csv_headers}")

            if not selected_table:
                selected_table = tablas[0]

            table = admin_tablas.obtener_tabla(selected_table)
            table_columns = [column[0] for column in table.columnas]

            missing_columns = [col for col in table_columns if col not in csv_headers]
            if missing_columns:
                raise ValueError(f"Faltan las siguientes columnas en el archivo CSV: {', '.join(missing_columns)}")

            for row_number, row in enumerate(reader, start=1):
                try:
                    cleaned_row = {
                        k.strip().strip('"'): v.strip().strip('"') if isinstance(v, str) and v else None
                        for k, v in row.items()
                    }
                    print(f"Fila {row_number} procesada: {cleaned_row}")

                    data = {}
                    for column_name, column_type, column_size in table.columnas:
                        value = cleaned_row.get(column_name)

                        if value is None or value == "":
                            raise ValueError(f"Columna {column_name} faltante o vacía en la fila {row_number}.")
                        if column_type == "int":
                            try:
                                value = int(value)
                            except ValueError:
                                raise ValueError(f"El valor para '{column_name}' debe ser un entero.")
                        elif column_type == "float":
                            try:
                                value = float(value)
                            except ValueError:
                                raise ValueError(f"El valor para '{column_name}' debe ser un flotante.")
                        elif column_type == "varchar":
                            if len(value) > column_size:
                                raise ValueError(f"El valor en {column_name} excede el tamaño permitido de {column_size}.")
                        elif column_type == "date":
                            from datetime import datetime
                            try:
                                datetime.strptime(value, "%Y-%m-%d")
                            except ValueError:
                                raise ValueError(f"El valor para '{column_name}' debe ser una fecha válida (YYYY-MM-DD).")
                        elif column_type == "boolean":
                            if value.lower() not in ["true", "false"]:
                                raise ValueError(f"El valor para '{column_name}' debe ser 'true' o 'false'.")
                            value = (value.lower() == "true")

                        data[column_name] = value

                    row_values = [data[col[0]] for col in table.columnas]
                    table.insertar_dato(row_values)
                    direcciones_fragmentos = hdd.escribir_dato(str(data), prefijo=selected_table)
                    index_value = data["Index"]
                    hdd.guardar_mapeo_index(index_value, direcciones_fragmentos)

                except Exception as e:
                    print(f"Error al procesar la fila {row_number}: {e}")
    except Exception as e:
        print(f"Error al procesar el archivo CSV: {e}")

def search_data_interface(hdd, admin_tablas):
    tablas = admin_tablas.listar_tablas()
    if not tablas:
        print("No hay tablas disponibles.")
        return

    selected_table = None
    table_buttons = [
        pygame.Rect(WIDTH // 2 - 125, HEIGHT // 2 - 150 + i * 50, 250, 40)
        for i in range(len(tablas))
    ]

    search_box = InputBox(WIDTH // 2 - 125, HEIGHT // 2 - 100, 250, 40)
    search_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    cancel_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            search_box.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not selected_table:
                    for i, button in enumerate(table_buttons):
                        if button.collidepoint(event.pos):
                            selected_table = tablas[i]

                if search_button.collidepoint(event.pos):
                    if selected_table:
                        table = admin_tablas.obtener_tabla(selected_table)
                        search_value = search_box.get_text()

                        try:
                            search_value = int(search_value)
                            result = table.buscar_dato("Index", search_value)
                            if result:
                                print(f"Dato encontrado en la tabla: {result}")
                                hdd_data = hdd.obtener_datos_completos(search_value)
                                if hdd_data:
                                    print(f"Datos guardados en el HDD: {hdd_data['datos']}")
                                    print(f"Ubicaciones en el HDD (plato, pista, sector): {hdd_data['ubicaciones']}")
                                else:
                                    print("Dato encontrado en la tabla, pero no ubicado en el HDD.")
                            else:
                                print("Dato no encontrado en la tabla.")
                        except ValueError:
                            print("Por favor, ingrese un ID válido (debe ser un número entero).")
                        return

                if cancel_button.collidepoint(event.pos):
                    return

        screen.fill(WHITE)

        if not selected_table:
            draw_label(screen, "Seleccionar Tabla:", WIDTH // 2 - 300, HEIGHT // 2 - 220)
            for i, button in enumerate(table_buttons):
                draw_button(screen, tablas[i], button, LIGHT_BLUE, BLACK)
        else:
            draw_label(screen, f"Buscar Dato en: {selected_table}", WIDTH // 2 - 300, HEIGHT // 2 - 220)
            draw_label(screen, "ID del Dato:", WIDTH // 2 - 300, HEIGHT // 2 - 140)
            search_box.draw(screen)
            draw_button(screen, "Buscar", search_button, LIGHT_BLUE, BLACK)

        draw_button(screen, "Cancelar", cancel_button, LIGHT_BLUE, BLACK)

        draw_disk_and_buttons(hdd, 0)
        pygame.display.flip()

def main():
    show_start_screen()
    hdd = create_disk_interface()
    admin_tablas = AdministradorTablas()
    main_menu(hdd, admin_tablas)

if __name__ == "__main__":
    main()