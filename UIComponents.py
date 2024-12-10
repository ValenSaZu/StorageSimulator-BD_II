import pygame

class InputBox:
    def __init__(self, x, y, w, h, text='', font=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = (200, 200, 200)
        self.color_active = (100, 100, 255)
        self.color = self.color_inactive
        self.text = text
        self.active = False
        self.font = font if font else pygame.font.Font(None, 32)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        txt_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(txt_surface, (self.rect.x + 10, self.rect.y + (self.rect.height - txt_surface.get_height()) // 2))

    def get_text(self):
        return self.text


def draw_button(screen, text, rect, color, text_color=(0, 0, 0), border_radius=15, font=None):
    pygame.draw.rect(screen, color, rect, border_radius=border_radius)
    font = font if font else pygame.font.Font(None, 36)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def draw_label(screen, text, x, y, font=None, color=(0, 0, 0)):
    font = font if font else pygame.font.Font(None, 28)
    label_surface = font.render(text, True, color)
    screen.blit(label_surface, (x, y))
