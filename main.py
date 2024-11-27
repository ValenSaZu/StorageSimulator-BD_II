import pygame
import math
import sys

pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Base de Datos")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
LIGHT_BLUE = (100, 200, 255)
DARK_BLUE = (0, 100, 200)

center = (WIDTH // 2 + 150, HEIGHT // 2)
radio_base = 50
incremento_radio = 30
num_pistas = 0
num_sectores = 0

class HDD:
    def __init__(self, num_pistas, num_sectores):
        self.num_pistas = num_pistas
        self.num_sectores = num_sectores

def draw_disk():
    for pista in range(num_pistas):
        radio = radio_base + incremento_radio * pista
        pygame.draw.circle(screen, WHITE, center, radio, 1)
        for sector in range(num_sectores):
            angle = (2 * math.pi / num_sectores) * sector
            x = center[0] + radio * math.cos(angle)
            y = center[1] - radio * math.sin(angle)
            pygame.draw.line(screen, WHITE, center, (x, y), 1)

def show_start_screen():
    font = pygame.font.Font(None, 74)
    text = font.render("Simulador de Base de Datos", True, WHITE)
    screen.fill(BLACK)
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

    # Título
    title_font = pygame.font.Font(None, 48)
    title_surface = title_font.render("Crear Disco Duro", True, WHITE)

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

        screen.fill(BLACK)
        screen.blit(title_surface, (50, 50))
        pygame.draw.rect(screen, color, input_box, 2)
        txt_surface = font.render(text, True, color)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.display.flip()

def query_interface():
    global num_pistas, num_sectores
    font = pygame.font.Font(None, 32)
    query_text = ""
    input_box = pygame.Rect(50, HEIGHT - 100, 700, 40)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(f"Ejecutar consulta: {query_text}")
                    query_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    query_text = query_text[:-1]
                else:
                    query_text += event.unicode

        screen.fill(BLACK)
        draw_disk()
        
        title_surface = font.render("Ingrese su consulta SQL:", True, WHITE)
        screen.blit(title_surface, (50, HEIGHT - 150))

        txt_surface = font.render(query_text, True, WHITE)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, WHITE, input_box, 2)
        pygame.display.flip()

show_start_screen()
create_disk_interface()
hdd = HDD(num_pistas, num_sectores)

while True:
    query_interface()