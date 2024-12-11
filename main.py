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

def show_start_screen():
    font = pygame.font.Font(None, 74)
    text = font.render("Simulador de Base de Datos", True, BLACK)
    screen.fill(WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

def draw_disk_and_buttons(hdd):
    draw_disk(screen, hdd, WIDTH // 2 + 300, HEIGHT // 2 + 50, 200)

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
    create_table_button = pygame.Rect(WIDTH // 2 - 300, HEIGHT // 2 - 100, 200, 50)
    add_data_button = pygame.Rect(WIDTH // 2 - 300, HEIGHT // 2, 200, 50)
    search_data_button = pygame.Rect(WIDTH // 2 - 300, HEIGHT // 2 + 100, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if create_table_button.collidepoint(event.pos):
                    create_table_interface(hdd, admin_tablas)
                elif add_data_button.collidepoint(event.pos):
                    upload_csv_interface(hdd, admin_tablas)
                elif search_data_button.collidepoint(event.pos):
                    search_data_interface(hdd, admin_tablas)

        screen.fill(WHITE)

        draw_button(screen, "Crear Tabla", create_table_button, LIGHT_BLUE, BLACK)
        draw_button(screen, "Añadir Datos", add_data_button, LIGHT_BLUE, BLACK)
        draw_button(screen, "Buscar Dato", search_data_button, LIGHT_BLUE, BLACK)

        draw_disk_and_buttons(hdd)

        pygame.display.flip()

def create_table_interface(hdd, admin_tablas):
    table_name_box = InputBox(WIDTH // 2 - 125, HEIGHT // 2 - 200, 250, 40)
    column_name_box = InputBox(WIDTH // 2 - 125, HEIGHT // 2 - 140, 250, 40)
    varchar_length_box = InputBox(WIDTH // 2 - 125, HEIGHT // 2, 250, 40)

    tipos_datos = ["int", "float", "varchar"]
    tipo_buttons = [
        pygame.Rect(WIDTH // 2 - 125, HEIGHT // 2 - 70 + i * 50, 250, 40)
        for i in range(len(tipos_datos))
    ]

    add_column_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50)
    finalize_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 160, 200, 50)

    column_list = []
    selected_tipo = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            table_name_box.handle_event(event)
            column_name_box.handle_event(event)
            varchar_length_box.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(tipo_buttons):
                    if button.collidepoint(event.pos):
                        selected_tipo = tipos_datos[i]

                if add_column_button.collidepoint(event.pos):
                    column_name = column_name_box.get_text()
                    if column_name and selected_tipo:
                        if selected_tipo == "varchar":
                            try:
                                varchar_length = int(varchar_length_box.get_text())
                                if varchar_length > 0:
                                    column_list.append((column_name, (selected_tipo, varchar_length)))
                                    column_name_box.text = ""
                                    varchar_length_box.text = ""
                                    selected_tipo = None
                                else:
                                    print("El tamaño de 'varchar' debe ser mayor a 0.")
                            except ValueError:
                                print("El tamaño de 'varchar' debe ser un número entero válido.")
                        else:
                            column_list.append((column_name, selected_tipo))
                            column_name_box.text = ""
                            selected_tipo = None

                if finalize_button.collidepoint(event.pos):
                    table_name = table_name_box.get_text()
                    if table_name and column_list:
                        new_table = Tabla(table_name)
                        for column_name, column_type in column_list:
                            if isinstance(column_type, tuple):
                                new_table.agregar_columna(column_name, column_type[0], column_type[1])
                            else:
                                new_table.agregar_columna(column_name, column_type)
                        admin_tablas.tablas[table_name] = new_table
                        return

        screen.fill(WHITE)
        draw_label(screen, "Creación de Tablas", WIDTH // 2 - 300, HEIGHT // 2 - 220)
        draw_label(screen, "Nombre de la Tabla:", WIDTH // 2 - 350, HEIGHT // 2 - 190)
        draw_label(screen, "Nombre de la Columna:", WIDTH // 2 - 350, HEIGHT // 2 - 130)
        draw_label(screen, "Tipo de la Columna:", WIDTH // 2 - 350, HEIGHT // 2 - 90)

        table_name_box.draw(screen)
        column_name_box.draw(screen)

        for i, button in enumerate(tipo_buttons):
            color = LIGHT_BLUE if tipos_datos[i] == selected_tipo else WHITE
            draw_button(screen, tipos_datos[i], button, color, BLACK)

        if selected_tipo == "varchar":
            draw_label(screen, "Tamaño de Varchar:", WIDTH // 2 - 350, HEIGHT // 2 - 20)
            varchar_length_box.draw(screen)

        draw_button(screen, "Agregar Columna", add_column_button, LIGHT_BLUE, BLACK)
        draw_button(screen, "Finalizar", finalize_button, LIGHT_BLUE, BLACK)

        y_offset = HEIGHT // 2 + 220
        for column_name, column_type in column_list:
            if isinstance(column_type, tuple):
                draw_label(screen, f"{column_name} ({column_type[0]}[{column_type[1]}])", WIDTH // 2 - 300, y_offset)
            else:
                draw_label(screen, f"{column_name} ({column_type})", WIDTH // 2 - 300, y_offset)
            y_offset += 30

        draw_disk_and_buttons(hdd)
        pygame.display.flip()



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

            # Si no se ha seleccionado una tabla, tomamos la primera disponible
            if not selected_table:
                selected_table = tablas[0]

            table = admin_tablas.obtener_tabla(selected_table)
            table_columns = [column[0] for column in table.columnas]

            missing_columns = [col for col in table_columns if col not in csv_headers]
            if missing_columns:
                raise ValueError(f"Faltan las siguientes columnas en el archivo CSV: {', '.join(missing_columns)}")

            for row_number, row in enumerate(reader, start=1):
                try:
                    # Limpieza inicial de la fila
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

                        # Limpia el valor
                        if isinstance(value, str):
                            value = value.strip()

                        if column_type == "int":
                            cleaned_value = "".join(ch for ch in value if ch.isdigit() or ch == '-')
                            if cleaned_value == "":
                                raise ValueError(f"El valor para '{column_name}' debe ser un entero. Valor recibido: '{value}' en la fila {row_number}.")
                            try:
                                value = int(cleaned_value)
                            except ValueError:
                                raise ValueError(f"El valor para '{column_name}' debe ser un entero. Valor recibido: '{value}' en la fila {row_number}.")

                        elif column_type == "float":
                            cleaned_value = value.replace(",", "").strip()
                            try:
                                value = float(cleaned_value)
                            except ValueError:
                                raise ValueError(f"El valor para '{column_name}' debe ser un flotante. Valor recibido: '{value}' en la fila {row_number}.")

                        elif column_type == "varchar":
                            if len(value) > column_size:
                                raise ValueError(f"El valor en {column_name} excede el tamaño permitido de {column_size}.")

                        data[column_name] = value

                    # Convertir el diccionario data en una lista en el orden de las columnas
                    row_values = []
                    for (col_name, col_type, col_size) in table.columnas:
                        row_values.append(data[col_name])

                    # Inserta los datos en la tabla como una lista
                    table.insertar_dato(row_values)

                    # Escribe los datos en el HDD
                    hdd.escribir_dato(str(data), prefijo=selected_table)
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
                            result = table.buscar_dato("ID", search_value)
                            if result:
                                print(f"Dato encontrado: {result}")
                                hdd_address = hdd.obtener_direccion_fisica(result)
                                if hdd_address:
                                    print(f"Ubicación en HDD: Plato {hdd_address[0]}, Pista {hdd_address[1]}, Sector {hdd_address[2]}")
                                    draw_label(screen, f"Ubicación: Plato {hdd_address[0]}, Pista {hdd_address[1]}, Sector {hdd_address[2]}", WIDTH // 2 - 300, HEIGHT // 2 + 100)
                                else:
                                    print("Dato no encontrado en el HDD.")
                            else:
                                print("Dato no encontrado.")
                        except ValueError:
                            print("Por favor, ingrese un ID válido.")
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

        draw_disk_and_buttons(hdd)

        pygame.display.flip()

def main():
    show_start_screen()
    hdd = create_disk_interface()
    admin_tablas = AdministradorTablas()
    main_menu(hdd, admin_tablas)

if __name__ == "__main__":
    main()
