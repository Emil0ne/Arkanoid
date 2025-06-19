import pygame
import math
import random

class Ball:
    def __init__(self, x, y, radius, speed_x, speed_y, screen_width, screen_height, bounce_sound):
        self.x = x
        self.y = y
        self.radius = radius
        self.angle = math.atan2(speed_y, speed_x)
        self.speed = math.hypot(speed_x, speed_y)
        self.base_speed = self.speed
        self.top_speed = 15
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bounce_sound = bounce_sound
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)

    def move(self, collidables=None, play_bounce_sound = True):
        hit_bricks = []

        if self.speed < self.base_speed:
            self.speed += 0.02
        elif self.speed > self.base_speed:
            self.speed -= 0.02

        dx = math.cos(self.angle) * self.speed
        dy = math.sin(self.angle) * self.speed

        # Ruch w osi X
        self.x += dx
        self.rect.centerx = int(self.x)
        if collidables:
            for obj in collidables:
                if self.rect.colliderect(obj.rect):
                    hit_bricks.append(obj)
                    self.x -= dx
                    self.rect.centerx = int(self.x)
                    self.bounce_horizontal(play_sound=play_bounce_sound)
                    break

        # Ruch w osi Y
        self.y += dy
        self.rect.centery = int(self.y)
        if collidables:
            for obj in collidables:
                if self.rect.colliderect(obj.rect):
                    hit_bricks.append(obj)
                    self.y -= dy
                    self.rect.centery = int(self.y)
                    self.bounce_vertical(play_sound=play_bounce_sound)
                    break

        # Ściany
        bounced = False
        if self.rect.left <= 0:
            self.rect.left = 0
            self.x = self.rect.centerx
            self.angle = math.pi - self.angle + random.uniform(-0.1, 0.1)
            bounced = True
        elif self.rect.right >= self.screen_width:
            self.rect.right = self.screen_width
            self.x = self.rect.centerx
            self.angle = math.pi - self.angle + random.uniform(-0.1, 0.1)
            bounced = True

        if self.rect.top <= 0:
            self.rect.top = 0
            self.y = self.rect.centery
            self.angle = -self.angle + random.uniform(-0.1, 0.1)
            bounced = True

        if bounced:
            self.bounce_sound.play()

        if self.rect.bottom >= self.screen_height:
            self.reset()

        return hit_bricks

    def bounce_horizontal(self, play_sound=True):
        self.angle = math.pi - self.angle + random.uniform(-0.05, 0.05)
        if play_sound:
            self.bounce_sound.play()

    def bounce_vertical(self, play_sound=True):
        self.angle = -self.angle + random.uniform(-0.05, 0.05)
        if play_sound:
            self.bounce_sound.play()

    def set_angle_from_offset(self, offset):
        max_offset = 1
        normalized_offset = max(-max_offset, min(offset, max_offset))
        self.angle = -math.pi / 2 + normalized_offset * (math.pi / 4)

    def reset(self):
        self.speed = 0

    def draw(self, screen):
        pygame.draw.ellipse(screen, (255, 255, 255), self.rect)