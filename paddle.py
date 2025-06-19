import pygame

class Paddle:
    def __init__(self, x, y, width, height, speed, screen_width):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.screen_width = screen_width        
    
    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        #Uniemożliwienie wyjścia paletki poza ekran
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)