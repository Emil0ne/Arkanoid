import random, os

def apply_difficulty_settings(difficulty, paddle):
    if difficulty in ['easy', 'łatwy']:
        initial_ball_speed_x = 5
        initial_ball_speed_y = -5
        paddle.rect.width = 160
        powerup_chance = 0.3
    elif difficulty in ['normal', 'normalny']:
        initial_ball_speed_x = 6
        initial_ball_speed_y = -6
        paddle.rect.width = 140
        powerup_chance = 0.2
    elif difficulty in ['hard', 'trudny']:
        initial_ball_speed_x = 8
        initial_ball_speed_y = -8
        paddle.rect.width = 120
        powerup_chance = 0.1

    base_paddle_width = paddle.rect.width
    return initial_ball_speed_x, initial_ball_speed_y, base_paddle_width, powerup_chance

def get_randomized_ball_speed(initial_ball_speed_x, initial_ball_speed_y):
    start_speed_x = initial_ball_speed_x * random.choice([-1, 1])
    start_speed_y = initial_ball_speed_y
    return start_speed_x, start_speed_y

def save_score(player_name, score, difficulty):
    filename = f'scores_{difficulty}.txt'
    scores = []

    # Wczytaj istniejące wyniki
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                if ':' in line:
                    parts = line.strip().split(':')
                    if len(parts) == 2:
                        name = parts[0].strip()
                        try:
                            old_score = int(parts[1].strip())
                            scores.append((name, old_score))
                        except ValueError:
                            pass

    # Dodaj nowy wynik
    scores.append((player_name, score))

    # Posortuj malejąco
    scores.sort(key=lambda x: x[1], reverse=True)

    # Zapisz tylko TOP 10
    with open(filename, 'w', encoding='utf-8') as f:
        for name, s in scores[:10]:
            f.write(f'{name}: {s}\n')

def show_level_transition(screen, SCREEN_WIDTH, SCREEN_HEIGHT, background_image, level_number):
    import pygame  # lokalny import żeby helpers nie wymagał pygame przy importowaniu helpers

    font_big = pygame.font.SysFont(None, 100)
    level_text = font_big.render(f"LEVEL {level_number}", True, (255, 255, 255))

    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill((0, 0, 0))

    # FADE IN
    for alpha in range(0, 256, 15):
        overlay.set_alpha(alpha)
        screen.blit(background_image, (0, 0))  # możesz dać czarne tło
        screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, SCREEN_HEIGHT // 2 - level_text.get_height() // 2))
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)

    # krótkie zatrzymanie (pełny czarny + napis)
    pygame.time.delay(1000)

    # FADE OUT
    for alpha in range(255, -1, -15):
        overlay.set_alpha(alpha)
        screen.blit(background_image, (0, 0))  # albo czarne tło
        screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, SCREEN_HEIGHT // 2 - level_text.get_height() // 2))
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)

def reset_game_state(level_keys, difficulty, paddle, SCREEN_WIDTH, SCREEN_HEIGHT, LEVELS, ball_sound):
    import pygame
    import math
    from levels import load_level
    from helpers import apply_difficulty_settings, get_randomized_ball_speed
    from ball import Ball

    current_level_index = 0
    brick_width = SCREEN_WIDTH // len(LEVELS[level_keys[current_level_index]][0])
    brick_height = 30
    bricks = load_level(level_keys[current_level_index], brick_width, brick_height, LEVELS)

    initial_ball_speed_x, initial_ball_speed_y, base_paddle_width, powerup_chance = apply_difficulty_settings(difficulty, paddle)
    angle = math.atan2(initial_ball_speed_y, initial_ball_speed_x)
    speed = math.hypot(initial_ball_speed_x, initial_ball_speed_y)
    balls = [Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, math.cos(angle) * speed, math.sin(angle) * speed, SCREEN_WIDTH, SCREEN_HEIGHT, ball_sound)]
    ball_active = False

    score = 0
    lives = 5
    powerups = []
    paused = False
    particles = []
    lost_life_animation_timer = 0
    lost_life_animation_duration = 3000
    waiting_for_respawn = False
    lasers = []
    laser_enabled = False
    laser_timer = 0

    paddle.rect.width = base_paddle_width
    paddle.rect.centerx = SCREEN_WIDTH // 2
    pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # WIDEN_SHRINK_RESET
    pygame.time.set_timer(pygame.USEREVENT + 2, 0)  # SPEED_RESET

    # zwracamy wszystkie zmienne które były globalne:
    return (current_level_index, brick_width, brick_height, bricks,
            initial_ball_speed_x, initial_ball_speed_y, base_paddle_width, powerup_chance,
            angle, speed, balls, ball_active, score, lives, powerups,
            paused, particles, lost_life_animation_timer, lost_life_animation_duration,
            waiting_for_respawn, lasers, laser_enabled, laser_timer)