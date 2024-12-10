import pygame
import math
import sys
from HDDStructure import HDD

pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Base de Datos")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
LIGHT_BLUE = (100, 200, 255)
DARK_BLUE = (0, 100, 200)

ubi = (WIDTH // 2 + 320 , HEIGHT // 2 - 130)
radio_base = 50
incremento_radio = 30
num_pistas = 0
num_sectores = 0


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
    inputs = {"platos": "", "pistas": "", "sectores": "", "bytes": ""}
    active_input = None
    colors = {"platos": LIGHT_BLUE, "pistas": LIGHT_BLUE, "sectores": LIGHT_BLUE, "bytes": LIGHT_BLUE}
    
    font = pygame.font.Font(None, 32)
    title_font = pygame.font.Font(None, 48)
    label_font = pygame.font.Font(None, 28)

    labels = {
        "platos": label_font.render("Número de Platos:", True, BLACK),
        "pistas": label_font.render("Número de Pistas:", True, BLACK),
        "sectores": label_font.render("Número de Sectores:", True, BLACK),
        "bytes": label_font.render("Tamaño (bytes/sector):", True, BLACK)
    }

    input_boxes = {
        "platos": pygame.Rect(0, 0, 250, 40),
        "pistas": pygame.Rect(0, 0, 250, 40),
        "sectores": pygame.Rect(0, 0, 250, 40),
        "bytes": pygame.Rect(0, 0, 250, 40),
    }
    configure_button = pygame.Rect(0, 0, 200, 50)

    center_x = WIDTH // 2
    spacing_y = 70
    start_y = HEIGHT // 2 - len(input_boxes) * spacing_y // 2 - 50

    y_positions = [start_y + i * spacing_y for i in range(len(input_boxes))]
    for i, key in enumerate(input_boxes):
        input_boxes[key].center = (center_x, y_positions[i])
    configure_button.center = (center_x, y_positions[-1] + 80)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for key, box in input_boxes.items():
                    if box.collidepoint(event.pos):
                        active_input = key
                        colors[key] = DARK_BLUE
                    else:
                        colors[key] = LIGHT_BLUE
                if configure_button.collidepoint(event.pos):
                    try:
                        num_platos = int(inputs["platos"])
                        num_pistas = int(inputs["pistas"])
                        num_sectores = int(inputs["sectores"])
                        tamano_bytes = int(inputs["bytes"])
                        return HDD(num_platos, num_pistas, num_sectores, tamano_bytes)
                    except ValueError:
                        print("Error: Todos los valores deben ser enteros positivos.")
            if event.type == pygame.KEYDOWN and active_input:
                if event.key == pygame.K_BACKSPACE:
                    inputs[active_input] = inputs[active_input][:-1]
                else:
                    inputs[active_input] += event.unicode

        screen.fill(WHITE)

        title_surface = title_font.render("Crear Disco Duro", True, BLACK)
        screen.blit(title_surface, (center_x - title_surface.get_width() // 2, start_y - 100))

        for i, (key, box) in enumerate(input_boxes.items()):
            pygame.draw.rect(screen, colors[key], box, border_radius=10)
            txt_surface = font.render(inputs[key], True, BLACK)
            label_surface = labels[key]
            screen.blit(label_surface, (center_x - box.width // 2 - label_surface.get_width() - 10, box.y + 10))
            screen.blit(txt_surface, (box.x + 10, box.y + 5))

        pygame.draw.rect(screen, LIGHT_BLUE, configure_button, border_radius=15)
        configure_text = font.render("Configurar", True, BLACK)
        screen.blit(configure_text, (configure_button.x + configure_button.width // 2 - configure_text.get_width() // 2,
                                     configure_button.y + configure_button.height // 2 - configure_text.get_height() // 2))

        pygame.display.flip()

show_start_screen()
create_disk_interface()