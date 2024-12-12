# main.py

import pygame
import sys
import csv
from tkinter import Tk, filedialog
from HDDStructure import HDD
from UIComponents import InputBox, draw_button, draw_label, draw_disk, display_error
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

def search_data_interface(hdd, admin_tablas):
    tablas = admin_tablas.listar_tablas()
    if not tablas:
        print("No hay tablas disponibles.")
        display_error(screen, "No hay tablas disponibles.")
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

                        if not search_value:
                            display_error(screen, "Por favor, ingrese un valor para buscar.")
                            continue

                        try:
                            # Obtener el nombre de la clave primaria
                            primary_key = table.primary_key
                            if not primary_key:
                                raise ValueError(f"La tabla '{selected_table}' no tiene una clave primaria definida.")

                            # No convertir a int o float, ya que la clave primaria podría ser una cadena
                            result = table.buscar_dato(primary_key, search_value)
                            if result:
                                print(f"Dato encontrado en la tabla: {result}")
                                hdd_data = hdd.obtener_datos_completos(search_value)
                                if hdd_data:
                                    print(f"Datos guardados en el HDD: {hdd_data['datos']}")
                                    print(f"Ubicaciones en el HDD (plato, pista, sector): {hdd_data['ubicaciones']}")
                                    display_error(screen, f"Dato encontrado:\n{hdd_data['datos']}")
                                else:
                                    print("Dato encontrado en la tabla, pero no ubicado en el HDD.")
                                    display_error(screen, "Dato encontrado en la tabla, pero no ubicado en el HDD.")
                            else:
                                print("Dato no encontrado en la tabla.")
                                display_error(screen, "Dato no encontrado en la tabla.")
                        except ValueError as ve:
                            print(f"Error al buscar el dato: {ve}")
                            display_error(screen, f"Error al buscar el dato: {ve}")
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
            draw_label(screen, "Clave Primaria del Dato:", WIDTH // 2 - 300, HEIGHT // 2 - 140)
            search_box.draw(screen)
            draw_button(screen, "Buscar", search_button, LIGHT_BLUE, BLACK)

        draw_button(screen, "Cancelar", cancel_button, LIGHT_BLUE, BLACK)

        draw_disk_and_buttons(hdd, 0)
        pygame.display.flip()

def create_table_from_txt(filepath, admin_tablas):
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()

        create_statement = [line.strip() for line in lines if line.strip()]

        if not create_statement[0].upper().startswith("CREATE TABLE"):
            raise ValueError("El archivo no contiene una declaración válida de 'CREATE TABLE'.")

        match_table = re.match(r'CREATE TABLE\s+(\w+)\s*\(', create_statement[0], re.IGNORECASE)
        if not match_table:
            raise ValueError("Formato de 'CREATE TABLE' inválido.")

        table_name = match_table.group(1)

        column_definitions = []
        table_constraints = []
        for line in create_statement[1:]:
            if line.startswith(")"):
                break
            line = line.rstrip(',').strip()
            if line:
                if re.match(r'PRIMARY KEY\s*\(', line, re.IGNORECASE) or re.match(r'FOREIGN KEY\s*\(', line, re.IGNORECASE):
                    table_constraints.append(line)
                else:
                    column_definitions.append(line)

        new_table = Tabla(table_name)

        for column_def in column_definitions:
            match_column = re.match(r'([\w\.]+)\s+(\w+(?:\([^\)]+\))?)\s*(.*)', column_def, re.IGNORECASE)
            if not match_column:
                raise ValueError(f"Formato de columna inválido: '{column_def}'")

            column_name = match_column.group(1)
            column_type_raw = match_column.group(2).lower()
            constraints = match_column.group(3).upper()

            type_match = re.match(r'(\w+)(?:\(([^)]+)\))?', column_type_raw)
            if not type_match:
                raise ValueError(f"Tipo de dato inválido para la columna '{column_name}': '{column_type_raw}'")

            base_type = type_match.group(1)
            type_params = type_match.group(2)

            es_primary_key = False
            no_null = False

            if "PRIMARY KEY" in constraints:
                es_primary_key = True
            if "NOT NULL" in constraints:
                no_null = True

            if base_type in ["varchar"]:
                if not type_params:
                    raise ValueError(f"El tipo '{base_type}' requiere un tamaño especificado.")
                size = int(type_params)
                new_table.agregar_columna(column_name, "varchar", size, es_primary_key=es_primary_key, no_null=no_null)

            elif base_type in ["integer", "int"]:
                new_table.agregar_columna(column_name, "int", tamano=None, es_primary_key=es_primary_key, no_null=no_null)

            elif base_type in ["float"]:
                new_table.agregar_columna(column_name, "float", tamano=None, es_primary_key=es_primary_key, no_null=no_null)

            elif base_type == "decimal":
                if not type_params:
                    raise ValueError(f"El tipo '{base_type}' requiere precisión y escala especificadas.")
                params = [param.strip() for param in type_params.split(',')]
                if len(params) != 2:
                    raise ValueError(f"El tipo '{base_type}' requiere dos parámetros: precisión y escala.")
                precision, scale = map(int, params)
                new_table.agregar_columna(column_name, "decimal", (precision, scale), es_primary_key=es_primary_key, no_null=no_null)

            elif base_type == "boolean":
                new_table.agregar_columna(column_name, "boolean", tamano=None, es_primary_key=es_primary_key, no_null=no_null)

            elif base_type == "date":
                new_table.agregar_columna(column_name, "date", tamano=None, es_primary_key=es_primary_key, no_null=no_null)

            else:
                raise ValueError(f"Tipo de columna desconocido: '{base_type}'")

            print(f"Columna '{column_name}' agregada con tipo '{base_type}' y tamaño '{type_params}'.")

        for constraint in table_constraints:
            if constraint.upper().startswith("PRIMARY KEY"):
                match_pk = re.match(r'PRIMARY KEY\s*\(([\w\.]+)\)', constraint, re.IGNORECASE)
                if not match_pk:
                    raise ValueError(f"Formato de PRIMARY KEY inválido: '{constraint}'")
                pk_column = match_pk.group(1)
                if not any(col[0] == pk_column for col in new_table.columnas):
                    raise ValueError(f"Clave primaria especificada para columna inexistente: '{pk_column}'")
                new_table.primary_key = pk_column
                print(f"Clave primaria establecida en la columna '{pk_column}'.")

        admin_tablas.tablas[table_name] = new_table
        print(f"Tabla '{table_name}' creada con éxito desde el archivo {filepath}.")

    except Exception as e:
        print(f"Error al procesar el archivo '{filepath}': {e}")
        display_error(screen, f"Error al procesar el archivo '{filepath}': {e}")

def upload_csv_interface(hdd, admin_tablas):
    tablas = admin_tablas.listar_tablas()
    if not tablas:
        print("No hay tablas disponibles.")
        display_error(screen, "No hay tablas disponibles.")
        return

    selected_table = None
    Tk().withdraw()
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not filepath:
        print("No se seleccionó ningún archivo.")
        display_error(screen, "No se seleccionó ningún archivo.")
        return

    try:
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            # Asumimos delimitador coma y comillas dobles, ajusta si es necesario.
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')

            if reader.fieldnames is None:
                raise ValueError("El archivo CSV no tiene encabezados.")

            # Limpiar encabezados
            csv_headers = [header.strip().strip('"').strip(';') for header in reader.fieldnames]
            print(f"Encabezados del archivo CSV (limpiados): {csv_headers}")

            tablas_disponibles = admin_tablas.listar_tablas()
            if not tablas_disponibles:
                print("No hay tablas disponibles para insertar datos. Crea primero una tabla.")
                display_error(screen, "No hay tablas disponibles para insertar datos. Crea primero una tabla.")
                return

            # Aquí debes asegurar que INVENTORY ya se haya creado y tenga primary_key
            selected_table = "INVENTORY"  # Ajusta según tu lógica
            table = admin_tablas.obtener_tabla(selected_table)
            if not table:
                raise ValueError(f"No se encontró la tabla '{selected_table}' en el AdministradorTablas.")

            table_columns = [col[0] for col in table.columnas]

            missing_columns = [col for col in table_columns if col not in csv_headers]
            if missing_columns:
                raise ValueError(f"Faltan las siguientes columnas en el archivo CSV: {', '.join(missing_columns)}")

            primary_key = table.primary_key
            if not primary_key:
                raise ValueError(f"La tabla '{selected_table}' no tiene una clave primaria definida.")

            for row_number, row in enumerate(reader, start=1):
                try:
                    cleaned_row = {
                        k.strip().strip('"'): (v.strip().strip('"') if isinstance(v, str) and v else None)
                        for k, v in row.items()
                    }
                    print(f"Fila {row_number} procesada: {cleaned_row}")

                    data = {}
                    # Aquí se asume que cada columna es una tupla (nombre, tipo, tamano, es_primary_key, no_null)
                    for (column_name, column_type, column_size, es_primary_key, no_null) in table.columnas:
                        value = cleaned_row.get(column_name)

                        if no_null and (value is None or (isinstance(value, str) and value.strip() == "")):
                            raise ValueError(f"Columna {column_name} faltante o vacía en la fila {row_number}.")

                        # Validación y conversión de tipos
                        if column_type in ["int", "bigint"]:
                            try:
                                value = int(value.strip()) if value is not None else None
                            except (ValueError, TypeError):
                                raise ValueError(f"El valor para '{column_name}' debe ser un entero.")
                        elif column_type == "float":
                            try:
                                value = float(value.strip()) if value is not None else None
                            except (ValueError, TypeError):
                                raise ValueError(f"El valor para '{column_name}' debe ser un flotante.")
                        elif column_type == "decimal":
                            from decimal import Decimal, InvalidOperation
                            try:
                                value = Decimal(value.strip()) if value is not None else None
                            except (InvalidOperation, TypeError):
                                raise ValueError(f"El valor para '{column_name}' debe ser un número decimal.")
                            if column_size is not None and value is not None:
                                precision, scale = column_size
                                partes = str(value).split('.')
                                integer_part = partes[0]
                                decimal_part = partes[1] if len(partes) > 1 else ''
                                if len(integer_part) > (precision - scale) or len(decimal_part) > scale:
                                    raise ValueError(f"El valor para '{column_name}' excede la precisión/escala.")
                        elif column_type in ["varchar", "text"]:
                            if not isinstance(value, str):
                                raise ValueError(f"El valor para '{column_name}' debe ser una cadena.")
                            if column_type == "varchar" and value and len(value.strip()) > column_size:
                                raise ValueError(f"El valor para '{column_name}' excede el tamaño máximo de {column_size}.")
                        elif column_type == "date":
                            from datetime import datetime
                            if not isinstance(value, str):
                                raise ValueError(f"El valor para '{column_name}' debe ser una cadena (YYYY-MM-DD).")
                            try:
                                datetime.strptime(value.strip(), "%Y-%m-%d")
                            except (ValueError, TypeError):
                                raise ValueError(f"El valor para '{column_name}' debe ser una fecha válida (YYYY-MM-DD).")
                        elif column_type == "datetime":
                            from datetime import datetime
                            if not isinstance(value, str):
                                raise ValueError(f"El valor para '{column_name}' debe ser una cadena (YYYY-MM-DD HH:MM:SS).")
                            try:
                                datetime.strptime(value.strip(), "%Y-%m-%d %H:%M:%S")
                            except (ValueError, TypeError):
                                raise ValueError(f"El valor para '{column_name}' debe ser una fecha/hora válida (YYYY-MM-DD HH:MM:SS).")
                        elif column_type == "boolean":
                            if isinstance(value, str):
                                val_lower = value.lower()
                                if val_lower == "true":
                                    value = True
                                elif val_lower == "false":
                                    value = False
                                else:
                                    raise ValueError(f"El valor para '{column_name}' debe ser 'true' o 'false'.")
                            elif not isinstance(value, bool):
                                raise ValueError(f"El valor para '{column_name}' debe ser booleano (true/false).")

                        data[column_name] = value

                    row_values = [data[col[0]] for col in table.columnas]
                    table.insertar_dato(row_values)

                    direcciones_fragmentos = hdd.escribir_dato(str(data), prefijo=selected_table)

                    if primary_key not in data:
                        raise ValueError(f"La clave primaria '{primary_key}' no se encuentra en la fila {row_number}.")
                    index_value = data[primary_key]
                    if index_value is None:
                        raise ValueError(f"El valor de la clave primaria '{primary_key}' no puede ser None en la fila {row_number}.")

                    hdd.guardar_mapeo_index(index_value, direcciones_fragmentos)

                except Exception as e:
                    print(f"Error al procesar la fila {row_number}: {e}")
                    display_error(screen, f"Error al procesar la fila {row_number}: {e}")

    except Exception as e:
        print(f"Error al procesar el archivo CSV: {e}")
        display_error(screen, f"Error al procesar el archivo CSV: {e}")

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
        
def main():
    show_start_screen()
    hdd = create_disk_interface()
    admin_tablas = AdministradorTablas()
    main_menu(hdd, admin_tablas)

if __name__ == "__main__":
    main()