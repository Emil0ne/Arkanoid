import pygame
import random
from ball import Ball
WIDEN_SHRINK_RESET = pygame.USEREVENT + 1
SPEED_RESET = pygame.USEREVENT + 2

class PowerUp:
    COLORS = {
        'widen': (255, 255, 0),   # żółty
        'shrink': (255, 165, 0),  # pomarańczowy
        'slow': (0, 255, 255),    # cyjan
        'fast': (0, 0, 255),      # niebieski
        'multi': (0, 255, 0),     # zielony
        'extra': (255, 0, 0),     # czerwony
        'laser': (255, 0, 255)    # fioletowy - DODANY laser
    }

    def __init__(self, x, y, kind):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.kind = kind
        self.speed = 3
       
    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        color = self.COLORS.get(self.kind, (255, 255, 255))
       
        glow_surf = pygame.Surface((self.rect.width + 10, self.rect.height + 10), pygame.SRCALPHA)
        glow_color = (*color, 80)
        pygame.draw.ellipse(glow_surf, glow_color, glow_surf.get_rect())
        screen.blit(glow_surf, (self.rect.x - 5, self.rect.y - 5))

        pygame.draw.rect(screen, color, self.rect, border_radius=15)

        label = self.kind[:2].upper() if self.kind != 'extra' else '+L'
        font = pygame.font.SysFont(None, 26, bold=True)
        text = font.render(label, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
    
    @staticmethod 
    def random_kind():
        return random.choice(['widen', 'shrink', 'slow', 'fast', 'multi', 'extra', 'laser'])

    
def apply_effect(powerup, paddle, balls, SCREEN_WIDTH, SCREEN_HEIGHT, ball_sound, lives):
    if powerup.kind == 'widen':
        paddle.rect.width = 200
        pygame.time.set_timer(WIDEN_SHRINK_RESET, 10000)
    elif powerup.kind == 'shrink':
        paddle.rect.width = 80
        pygame.time.set_timer(WIDEN_SHRINK_RESET, 10000)
    elif powerup.kind == 'slow':
        for ball in balls:
            ball.speed *= 0.7
        pygame.time.set_timer(SPEED_RESET, 10000)
    elif powerup.kind == 'fast':
        for ball in balls:
            ball.speed *= 1.3
        pygame.time.set_timer(SPEED_RESET, 10000)
    elif powerup.kind == "multi":
        new_balls = []
        for ball in balls:
            clones = random.randint(3, 10)
            for _ in range(clones):
                speed_x = random.choice([-1, 1]) * random.randint(4, 7)
                speed_y = random.choice([-1, 1]) * random.randint(4, 7)
                new_ball = Ball(ball.rect.centerx, ball.rect.centery, ball.radius, speed_x, speed_y, SCREEN_WIDTH, SCREEN_HEIGHT, ball_sound)
                new_balls.append(new_ball)
        balls.extend(new_balls)
    elif powerup.kind == "laser":
        laser_enabled = True
        laser_timer = pygame.time.get_ticks()
        return lives, laser_enabled, laser_timer

    elif powerup.kind == 'extra':
        lives = min(6, lives + 1)
    return lives
