import pygame
import sys
import os
import random
import math

os.chdir(os.path.dirname(__file__))

from paddle import Paddle
from ball import Ball
from brick import Brick
from powerup import PowerUp, apply_effect
from levels import LEVELS, load_level
from screens import show_start_screen, show_difficulty_selection_screen, show_game_over_screen, show_congratulations_screen, ask_player_name, show_highscores, show_game_complete_screen
from helpers import apply_difficulty_settings, get_randomized_ball_speed, save_score
from particle import Particle
from laser import Laser

WIDEN_SHRINK_RESET = pygame.USEREVENT + 1
SPEED_RESET = pygame.USEREVENT + 2

pygame.init()
heart_image = pygame.image.load('img/heart_life.png')
heart_image = pygame.transform.scale(heart_image, (30, 30))

select_sound = pygame.mixer.Sound('sounds/select.mp3')
ball_sound = pygame.mixer.Sound('sounds/ball.mp3')
lose_life_sound = pygame.mixer.Sound('sounds/lose-life.mp3')
sound_2 = pygame.mixer.Sound('sounds/2-sound.mp3')
sound_3 = pygame.mixer.Sound('sounds/3-sound.mp3')
powerup_sound = pygame.mixer.Sound('sounds/powerup.mp3')
laser_sound = pygame.mixer.Sound('sounds/laser.mp3')

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arkanoid")
background_image = pygame.image.load('img/background.png').convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

BLACK = (0, 0, 0)
clock = pygame.time.Clock()
FPS = 60

level_keys = list(LEVELS.keys())

while True:
    paddle = Paddle(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT - 30, 120, 15, 10, SCREEN_WIDTH)
    current_level_index = 0
    brick_width = SCREEN_WIDTH // len(LEVELS[level_keys[current_level_index]][0])
    brick_height = 30
    bricks = load_level(level_keys[current_level_index], brick_width, brick_height, LEVELS)

    while True:
        difficulty = show_start_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, select_sound)
        if difficulty == 'play':
            difficulty = show_difficulty_selection_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, select_sound)
            if difficulty is None:
                continue
        else:
            continue

        player_name = ask_player_name(screen, SCREEN_WIDTH, SCREEN_HEIGHT, select_sound)
        if player_name is None:
            continue
        break

    initial_ball_speed_x, initial_ball_speed_y, base_paddle_width, powerup_chance = apply_difficulty_settings(difficulty, paddle)
    angle = math.atan2(initial_ball_speed_y, initial_ball_speed_x)
    speed = math.hypot(initial_ball_speed_x, initial_ball_speed_y)
    balls = [Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, math.cos(angle) * speed, math.sin(angle) * speed, SCREEN_WIDTH, SCREEN_HEIGHT, ball_sound)]
    ball_active = False
    score = 0
    lives = 5
    score_saved = False

    powerups = []
    paused = False
    particles = []
    lost_life_animation_timer = 0
    lost_life_animation_duration = 3000
    waiting_for_respawn = False
    lasers = []
    laser_enabled = False
    laser_timer = 0

    restart_to_menu = False

    while True:
        level_cleared = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if laser_enabled:
                            laser1 = Laser(paddle.rect.left + 10, paddle.rect.top)
                            laser2 = Laser(paddle.rect.right - 10, paddle.rect.top)
                            lasers.append(laser1)
                            lasers.append(laser2)
                            laser_sound.play()

                        elif not ball_active:
                            ball_active = True
                            for ball in balls:
                                random_offset = random.uniform(-1, 1)
                                ball.set_angle_from_offset(random_offset)
                    if event.key == pygame.K_p:
                        paused = not paused
                if event.type == WIDEN_SHRINK_RESET:
                    paddle.rect.width = 120
                    pygame.time.set_timer(WIDEN_SHRINK_RESET, 0)
                if event.type == SPEED_RESET:
                    for ball in balls:
                        ball.speed = 7
                    pygame.time.set_timer(SPEED_RESET, 0)

            if paused:
                font = pygame.font.SysFont(None, 72)
                pause_text = font.render("PAUSED", True, (255, 255, 255))
                screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
                font_small = pygame.font.SysFont(None, 36)
                resume_text = font_small.render("Press P to resume", True, (255, 255, 255))
                screen.blit(resume_text, (SCREEN_WIDTH // 2 - resume_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
                pygame.display.flip()
                clock.tick(FPS)
                continue

            keys = pygame.key.get_pressed()
            paddle.move(keys)

            if not ball_active:
                for ball in balls:
                    ball.x = paddle.rect.centerx
                    ball.y = paddle.rect.top - ball.radius
                    ball.rect.center = (int(ball.x), int(ball.y))
            else:
                for ball in balls[:]:
                    hit_bricks = ball.move(bricks, play_bounce_sound=False)
                    for brick in hit_bricks:
                        try:
                            if brick.indestructible:
                                sound_2.play()
                            elif hasattr(brick, 'hits_remaining') and brick.hits_remaining == 2:
                                sound_3.play()
                            else:
                                ball.bounce_sound.play()
                            brick.hit()
                            if not brick.alive:
                                bricks.remove(brick)
                                score += 10
                                for _ in range(10):
                                    particles.append(Particle(brick.rect.centerx, brick.rect.centery, brick.color))
                                if random.random() < powerup_chance:
                                    kind = PowerUp.random_kind()
                                    powerups.append(PowerUp(brick.rect.centerx, brick.rect.centery, kind))
                        except ValueError:
                            pass
                    if ball.rect.bottom >= SCREEN_HEIGHT:
                        balls.remove(ball)
                if not balls and not waiting_for_respawn:
                    lives -= 1
                    if lives > 0:
                        lose_life_sound.play()
                        lost_life_animation_timer = pygame.time.get_ticks()
                        waiting_for_respawn = True
                    else:
                        running = False

            for ball in balls:
                if ball.rect.colliderect(paddle.rect):
                    offset = (ball.rect.centerx - paddle.rect.centerx) / (paddle.rect.width / 2)
                    ball.set_angle_from_offset(offset)
                    ball.bounce_sound.play()
                    score = max(0, score - 1)
                    ball.y = paddle.rect.top - ball.radius
                    ball.rect.centery = int(ball.y)

            if not any(brick.alive for brick in bricks if not brick.indestructible):
                running = False
                level_cleared = True

            for laser in lasers[:]:
                laser.move()
                if laser.rect.bottom < 0:
                    lasers.remove(laser)
                else:
                    for brick in bricks[:]:
                        if laser.rect.colliderect(brick.rect):
                            while not brick.indestructible and brick.hits_remaining > 0:
                                brick.hit()
                            if not brick.alive:
                                bricks.remove(brick)
                                score += 10
                                for _ in range(10):
                                    particles.append(Particle(brick.rect.centerx, brick.rect.centery, brick.color))
                                if random.random() < powerup_chance:
                                    kind = PowerUp.random_kind()
                                    powerups.append(PowerUp(brick.rect.centerx, brick.rect.centery, kind))
                            if laser in lasers:
                                lasers.remove(laser)
                            break

            if laser_enabled and pygame.time.get_ticks() - laser_timer > 10000:
                laser_enabled = False

            screen.blit(background_image, (0, 0))
            font = pygame.font.SysFont(None, 36)
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            paddle.draw(screen)
            for ball in balls:
                ball.draw(screen)
            for brick in bricks:
                brick.draw(screen)
            for laser in lasers:
                laser.draw(screen)

            for i in range(lives):
                screen.blit(heart_image, (SCREEN_WIDTH - (i + 1) * 40, 10))

            if lost_life_animation_timer > 0:
                elapsed = pygame.time.get_ticks() - lost_life_animation_timer
                if elapsed < lost_life_animation_duration:
                    screen.fill((0, 0, 0))
                    scale = 3 - 2 * (elapsed / lost_life_animation_duration)
                    heart_scaled = pygame.transform.scale(heart_image, (int(30 * scale), int(30 * scale)))
                    screen.blit(heart_scaled, (SCREEN_WIDTH // 2 - heart_scaled.get_width() // 2, SCREEN_HEIGHT // 2 - heart_scaled.get_height() // 2))
                    pygame.display.flip()
                    continue
                else:
                    lost_life_animation_timer = 0
                    waiting_for_respawn = False
                    start_speed_x, start_speed_y = get_randomized_ball_speed(initial_ball_speed_x, initial_ball_speed_y)
                    angle = math.atan2(start_speed_y, start_speed_x)
                    speed = math.hypot(start_speed_x, start_speed_y)
                    balls = [Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, math.cos(angle) * speed, math.sin(angle) * speed, SCREEN_WIDTH, SCREEN_HEIGHT, ball_sound)]
                    ball_active = False
                    paddle.rect.centerx = SCREEN_WIDTH // 2
                    paddle.rect.width = base_paddle_width
                    powerups.clear()
                    lasers.clear()
                    laser_enabled = False
                    pygame.time.set_timer(WIDEN_SHRINK_RESET, 0)
                    pygame.time.set_timer(SPEED_RESET, 0)

            for powerup in powerups[:]:
                powerup.move()
                powerup.draw(screen)
                if powerup.rect.colliderect(paddle.rect):
                    result = apply_effect(powerup, paddle, balls, SCREEN_WIDTH, SCREEN_HEIGHT, ball_sound, lives)
                    if isinstance(result, tuple):
                        lives, laser_enabled, laser_timer = result
                    else:
                        lives = result
                    powerup_sound.play()
                    powerups.remove(powerup)
                elif powerup.rect.top > SCREEN_HEIGHT:
                    powerups.remove(powerup)

            for particle in particles[:]:
                particle.update()
                if particle.lifetime <= 0:
                    particles.remove(particle)
                else:
                    particle.draw(screen)

            pygame.display.flip()
            clock.tick(FPS)

        if lives <= 0 and not score_saved:
            save_score(player_name, score, difficulty)
            score_saved = True
            choice = show_game_over_screen(score, screen, SCREEN_WIDTH, SCREEN_HEIGHT, select_sound)
            if choice == 'main_menu':
                restart_to_menu = True
            if restart_to_menu:
                break

        if level_cleared:
            score += lives * 10
            if current_level_index + 1 < len(level_keys):
                result = show_congratulations_screen(score, screen, SCREEN_WIDTH, SCREEN_HEIGHT, select_sound)
                if result == 'next_level':
                    current_level_index += 1
                    brick_width = SCREEN_WIDTH // len(LEVELS[level_keys[current_level_index]][0])
                    brick_height = 30
                    bricks = load_level(level_keys[current_level_index], brick_width, brick_height, LEVELS)
                    start_speed_x, start_speed_y = get_randomized_ball_speed(initial_ball_speed_x, initial_ball_speed_y)
                    angle = math.atan2(start_speed_y, start_speed_x)
                    speed = math.hypot(start_speed_x, start_speed_y)
                    balls = [Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10,
                                math.cos(angle) * speed, math.sin(angle) * speed,
                                SCREEN_WIDTH, SCREEN_HEIGHT, ball_sound)]
                    ball_active = False
                    paddle.rect.width = base_paddle_width
                    paddle.rect.centerx = SCREEN_WIDTH // 2
                    powerups.clear()
                    lasers.clear()
                    laser_enabled = False
                    pygame.time.set_timer(WIDEN_SHRINK_RESET, 0)
                    pygame.time.set_timer(SPEED_RESET, 0)
                elif result == 'quit':
                    if not score_saved:
                        save_score(player_name, score, difficulty)
                        score_saved = True
                    restart_to_menu = True
                    break
            else:
                if not score_saved:
                    save_score(player_name, score, difficulty)
                    score_saved = True
                while True:
                    final_choice = show_game_complete_screen(score, screen, SCREEN_WIDTH, SCREEN_HEIGHT, select_sound)
                    if final_choice == 'show_highscores':
                        show_highscores(screen, SCREEN_WIDTH, SCREEN_HEIGHT, difficulty, select_sound)
                    elif final_choice == 'main_menu':
                        restart_to_menu = True
                        break
                    elif final_choice == 'quit':
                        pygame.quit()
                        sys.exit()
                    else:
                        break
                if restart_to_menu:
                    break