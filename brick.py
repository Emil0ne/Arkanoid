import pygame
import time

class Brick:
    def __init__(self, x, y, width, height, color, indestructible=False, hits_remaining=1):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.alive = True
        self.indestructible = indestructible
        self.last_blink = time.time()
        self.is_blinking = False
        self.hits_remaining = hits_remaining
        self.cracked = False

    def draw(self, screen):
        if self.alive:
            draw_color = self.color

            # obsługa błysku dla silverów
            if self.indestructible:
                current_time = time.time()
                if current_time - self.last_blink > 2:
                    self.is_blinking = True
                    self.last_blink = current_time
                if self.is_blinking:
                    draw_color = (220, 220, 220)
                    if current_time - self.last_blink > 0.2:
                        self.is_blinking = False

            # główny prostokąt
            pygame.draw.rect(screen, draw_color, self.rect)

            # gradient: jaśniejsza góra
            highlight = (
                min(draw_color[0] + 50, 255),
                min(draw_color[1] + 50, 255),
                min(draw_color[2] + 50, 255),
            )
            pygame.draw.rect(
                screen,
                highlight,
                (self.rect.x, self.rect.y, self.rect.width, self.rect.height // 3),
            )

            # gradient: ciemniejszy dół
            shadow = (
                max(draw_color[0] - 50, 0),
                max(draw_color[1] - 50, 0),
                max(draw_color[2] - 50, 0),
            )
            pygame.draw.rect(
                screen,
                shadow,
                (
                    self.rect.x,
                    self.rect.y + 2 * self.rect.height // 3,
                    self.rect.width,
                    self.rect.height // 3,
                ),
            )

            # obramowanie
            pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

            # efekt popękania
            if self.cracked:
                # przykładowe pęknięcie — 2 linie
                pygame.draw.line(screen, (255, 255, 255), (self.rect.left + 5, self.rect.top + 5),
                                 (self.rect.right - 5, self.rect.bottom - 5), 2)
                pygame.draw.line(screen, (255, 255, 255), (self.rect.right - 5, self.rect.top + 5),
                                 (self.rect.left + 5, self.rect.bottom - 5), 2)

    def hit(self):
        if not self.indestructible:
            self.hits_remaining -= 1
            if self.hits_remaining == 1:
                self.cracked = True  # po pierwszym uderzeniu
            if self.hits_remaining <= 0:
                self.alive = False
