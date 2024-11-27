import pygame
import math
import sys
from HDDStructure import HDD
from database_manager import SQLProcessor
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
    global num_pistas, num_sectores
    input_box = pygame.Rect(50, 100, 200, 40)
    color_inactive = LIGHT_BLUE
    color_active = DARK_BLUE
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 32)

    title_font = pygame.font.Font(None, 48)
    title_surface = title_font.render("Crear Disco Duro", True, BLACK)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        try:
                            num_pistas, num_sectores = map(int, text.split(","))
                            if num_pistas <= 0 or num_sectores <= 0:
                                raise ValueError("Los números deben ser mayores que cero.")
                            return
                        except Exception as e:
                            print(f"Error: {e}")
                            text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(WHITE)
        screen.blit(title_surface, (50, 50))
        pygame.draw.rect(screen, color, input_box, 2)
        txt_surface = font.render(text, True, color)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.display.flip()

def query_interface(hdd, sql_processor):
    global num_pistas, num_sectores
    font = pygame.font.Font(None, 32)
    query_text = ""
    input_box = pygame.Rect(50, 100, 600, 400)
    output_box = pygame.Rect(50, 600, 600, 100)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        result = sql_processor.procesar_query(query_text)
                        query_text = ''
                    except Exception as e:
                        print(f"Error procesando consulta: {e}")
                        query_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    query_text = query_text[:-1]
                else:
                    query_text += event.unicode

        screen.fill(WHITE)
        draw_disk(num_pistas, num_sectores)

        title_surface = font.render("Ingrese su consulta SQL:", True, BLACK)
        screen.blit(title_surface, (50, 50))
        txt_surface = font.render(query_text, True, BLACK)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, BLACK, input_box, 2)

        output_surface = font.render("Salida:", True, BLACK)
        screen.blit(output_surface, (50, 550))
        result_surface = font.render(result if 'result' in locals() else "", True, BLACK)
        screen.blit(result_surface, (output_box.x + 5, output_box.y + 5))
        pygame.draw.rect(screen, BLACK, output_box, 2)

        pygame.display.flip()

show_start_screen()
create_disk_interface()
hdd = HDD(num_platos=1, num_pistas_por_plato=num_pistas, num_sectores_por_pista=num_sectores, tamano_bytes=1024)
sql_processor = SQLProcessor(hdd)

while True:
    query_interface(hdd, sql_processor)