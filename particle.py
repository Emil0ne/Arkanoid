import pygame
import random

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radius = random.randint(2, 4)
        self.color = color
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.lifetime = 30
    
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 1
        if self.radius > 0.1:
            self.radius -= 0.1
    
    def draw(self, screen):
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))