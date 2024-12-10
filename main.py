import pygame
import math
import sys
from HDDStructure import HDD
from UIComponents import InputBox, draw_button, draw_label
from TableManager import AdministradorTablas

pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Base de Datos")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
LIGHT_BLUE = (100, 200, 255)
DARK_BLUE = (0, 100, 200)

ubi = (WIDTH // 2 + 320, HEIGHT // 2 - 130)
radio_base = 50
incremento_radio = 30
num_platos, num_pistas, num_sectores, tamano_bytes = 0, 0, 0, 0

def draw_disk(num_pistas, num_sectores):
    for pista in range(num_pistas):
        radio = radio_base + incremento_radio * pista
        pygame.draw.circle(screen, BLACK, ubi, radio, 1)
        for sector in range(num_sectores):
            angle = (2 * math.pi / num_sectores) * sector
            x = ubi[0] + radio * math.cos(angle)
            y = ubi[1] - radio * math.sin(angle)
            pygame.draw.line(screen, BLACK, ubi, (x, y), 1)

def show_start_screen():
    font = pygame.font.Font(None, 74)
    text = font.render("Simulador de Base de Datos", True, BLACK)
    screen.fill(WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

def create_disk_interface():
    global num_platos, num_pistas, num_sectores, tamano_bytes

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
        draw_label(screen, "Por favor, complete los campos:", WIDTH // 2 - 200, HEIGHT // 2 - 180, font=pygame.font.Font(None, 28))

        label_font = pygame.font.Font(None, 28)
        draw_label(screen, "Número de Platos:", WIDTH // 2 - 350, HEIGHT // 2 - 140, font=label_font)
        draw_label(screen, "Número de Pistas:", WIDTH // 2 - 350, HEIGHT // 2 - 80, font=label_font)
        draw_label(screen, "Número de Sectores:", WIDTH // 2 - 350, HEIGHT // 2 - 20, font=label_font)
        draw_label(screen, "Tamaño (bytes/sector):", WIDTH // 2 - 350, HEIGHT // 2 + 40, font=label_font)

        platos_box.draw(screen)
        pistas_box.draw(screen)
        sectores_box.draw(screen)
        bytes_box.draw(screen)

        draw_button(screen, "Configurar", configure_button, LIGHT_BLUE, BLACK)

        pygame.display.flip()

def manage_tables_interface(hdd):
    admin_tablas = AdministradorTablas()

    tabla_en_creacion = None

    table_name_box = InputBox(WIDTH // 2 - 125, HEIGHT // 2 - 200, 250, 40)
    column_name_box = InputBox(WIDTH // 2 - 125, HEIGHT // 2 - 140, 250, 40)
    length_box = InputBox(WIDTH // 2 + 150, HEIGHT // 2 - 80, 100, 40)
    create_table_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 50)
    add_column_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50)
    finalize_table_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 140, 200, 50)

    tipos_datos = ["int", "float", "varchar"]
    selected_type_index = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            table_name_box.handle_event(event)
            column_name_box.handle_event(event)
            length_box.handle_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_type_index = (selected_type_index - 1) % len(tipos_datos)
                elif event.key == pygame.K_DOWN:
                    selected_type_index = (selected_type_index + 1) % len(tipos_datos)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if create_table_button.collidepoint(event.pos):
                    table_name = table_name_box.get_text()
                    if table_name and not tabla_en_creacion:
                        tabla_en_creacion = Tabla(table_name)
                        print(f"Tabla '{table_name}' en proceso de creación.")

                if add_column_button.collidepoint(event.pos) and tabla_en_creacion:
                    column_name = column_name_box.get_text()
                    column_type = tipos_datos[selected_type_index]
                    try:
                        if column_type == "varchar":
                            length = int(length_box.get_text())
                            tabla_en_creacion.agregar_columna(column_name, (column_type, length))
                        else:
                            tabla_en_creacion.agregar_columna(column_name, column_type)
                        print(f"Columna '{column_name}' de tipo '{column_type}' agregada a la tabla '{tabla_en_creacion.nombre}'.")
                    except Exception as e:
                        print(e)

                if finalize_table_button.collidepoint(event.pos) and tabla_en_creacion:
                    admin_tablas.tablas[tabla_en_creacion.nombre] = tabla_en_creacion
                    print(f"Tabla '{tabla_en_creacion.nombre}' creada con éxito.")
                    tabla_en_creacion = None

        screen.fill(WHITE)

        draw_label(screen, "Creación de Tablas", WIDTH // 2 - 200, HEIGHT // 2 - 260, font=pygame.font.Font(None, 48))
        draw_label(screen, "Nombre de la Tabla:", WIDTH // 2 - 300, HEIGHT // 2 - 190)
        draw_label(screen, "Nombre de la Columna:", WIDTH // 2 - 300, HEIGHT // 2 - 130)
        draw_label(screen, "Tipo de Dato (flechas):", WIDTH // 2 - 300, HEIGHT // 2 - 70)
        draw_label(screen, f"Tipo Seleccionado: {tipos_datos[selected_type_index]}", WIDTH // 2 + 150, HEIGHT // 2 - 70)

        if tipos_datos[selected_type_index] == "varchar":
            draw_label(screen, "Longitud (solo varchar):", WIDTH // 2 - 300, HEIGHT // 2 - 10)

        table_name_box.draw(screen)
        column_name_box.draw(screen)
        if tipos_datos[selected_type_index] == "varchar":
            length_box.draw(screen)

        draw_button(screen, "Crear Tabla", create_table_button, LIGHT_BLUE, BLACK)
        draw_button(screen, "Agregar Columna", add_column_button, LIGHT_BLUE, BLACK)
        draw_button(screen, "Finalizar Tabla", finalize_table_button, LIGHT_BLUE, BLACK)

        pygame.display.flip()

def manage_data_interface(tabla, hdd):
    input_boxes = []
    for i, (columna, tipo, tamano) in enumerate(tabla.columnas):
        input_boxes.append(InputBox(WIDTH // 2 - 125, HEIGHT // 2 - 200 + i * 60, 250, 40))

    insert_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            for box in input_boxes:
                box.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if insert_button.collidepoint(event.pos):
                    try:
                        datos = []
                        for box, (columna, tipo, tamano) in zip(input_boxes, tabla.columnas):
                            if tipo == "varchar":
                                valor = box.get_text()
                                if len(valor) > tamano:
                                    raise ValueError(f"El valor '{valor}' excede la longitud de {tamano} en '{columna}'.")
                                datos.append(valor)
                            elif tipo == "int":
                                datos.append(int(box.get_text()))
                            elif tipo == "float":
                                datos.append(float(box.get_text()))

                        tabla.insertar_dato(datos)
                        hdd.escribir_dato(str(datos), prefijo=tabla.nombre)
                        print(f"Datos insertados correctamente: {datos}")
                    except Exception as e:
                        print(e)

        screen.fill(WHITE)

        draw_label(screen, f"Insertar en la Tabla: {tabla.nombre}", WIDTH // 2 - 200, HEIGHT // 2 - 260)
        for i, (columna, _, _) in enumerate(tabla.columnas):
            draw_label(screen, f"{columna}:", WIDTH // 2 - 300, HEIGHT // 2 - 200 + i * 60)
            input_boxes[i].draw(screen)

        draw_button(screen, "Insertar Datos", insert_button, LIGHT_BLUE, BLACK)
        pygame.display.flip()

show_start_screen()
hdd = create_disk_interface()
manage_tables_interface(hdd)

screen.fill(WHITE)
draw_disk(num_pistas, num_sectores)
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
