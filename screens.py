import pygame
import sys
import os

# Kolory
DARK_BLUE = (10, 10, 50)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 150, 255)

# Czcionka
def get_font(size, bold=False):
    if bold:
        font_path = os.path.join("fonts", "Lato-Bold.ttf")
    else:
        font_path = os.path.join("fonts", "Lato-Regular.ttf")
    return pygame.font.Font(font_path, size)

# Ekran startowy
def show_start_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, select_sound):
    options = [('Graj', 'play'), ('Wyniki', 'show_highscores'), ('Instrukcje', 'show_instructions'), ('Wyjście', 'quit')]
    selected = 0

    font = get_font(48, bold=True)

    theme_path = os.path.join('sounds', 'theme-song.mp3')
    try:
        pygame.mixer.music.load(theme_path)
        pygame.mixer.music.play(-1)
    except pygame.error:
        pass

    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill(DARK_BLUE)
    fade_alpha = 255
    fade_done = False
    waiting = True
    while waiting:
        screen.fill(DARK_BLUE)
        if not fade_done:
            fade_alpha = max(0, fade_alpha - 10)
            fade_surface.set_alpha(fade_alpha)
        logo = pygame.image.load('img/arkanoid_logo.png')
        logo = pygame.transform.scale(logo, (500, 150))
        screen.blit(logo, (SCREEN_WIDTH // 2 - logo.get_width() // 2, 100))

        for i, (label, value) in enumerate(options):
            color = YELLOW if i == selected else WHITE
            text = font.render(label, True, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 300 + i * 60))

        prompt_font = get_font(28)
        prompt = prompt_font.render("Użyj STRZAŁEK GÓRA/DÓŁ, ENTER aby wybrać", True, WHITE)
        prompt_y = 300 + len(options) * 60 + 30
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, prompt_y))
        if fade_alpha > 0:
            screen.blit(fade_surface, (0, 0))
        else:
            fade_done = True
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                    select_sound.play()
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                    select_sound.play()
                if event.key == pygame.K_RETURN:
                    value = options[selected][1]
                    if value == "show_highscores":
                        show_highscores(screen, SCREEN_WIDTH, SCREEN_HEIGHT, 'normal', select_sound)
                    elif value == "show_instructions":
                        show_instructions(screen, SCREEN_WIDTH, SCREEN_HEIGHT, select_sound)
                    elif value == "quit":
                        pygame.quit()
                        sys.exit()
                    else:
                        pygame.mixer.music.stop()
                        return value

#Ekran wyboru trudnośći
def show_difficulty_selection_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, select_sound):
    difficulties = [('Łatwy', 'easy'), ('Normalny', 'normal'), ('Trudny', 'hard')]
    selected = 1  # domyślnie normal

    font_title = get_font(48, bold=True)
    font = get_font(36)

    waiting = True
    while waiting:
        screen.fill(DARK_BLUE)

        title = font_title.render("WYBIERZ TRUDNOŚĆ", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        total_width = sum(font.render(label, True, WHITE).get_width() + 60 for label, value in difficulties) - 60
        start_x = SCREEN_WIDTH // 2 - total_width // 2
        x = start_x
        y = SCREEN_HEIGHT // 2

        for i, (label, value) in enumerate(difficulties):
            color = YELLOW if i == selected else WHITE
            text = font.render(label, True, color)
            screen.blit(text, (x, y))
            x += text.get_width() + 60

        prompt = font.render("<-/-> wybierz, ENTER - start", True, WHITE)
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, SCREEN_HEIGHT - 80))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected = (selected - 1) % len(difficulties)
                    select_sound.play()
                elif event.key == pygame.K_RIGHT:
                    selected = (selected + 1) % len(difficulties)
                    select_sound.play()
                elif event.key == pygame.K_RETURN:
                    select_sound.play()
                    return difficulties[selected][1]
                elif event.key == pygame.K_ESCAPE:
                    select_sound.play()
                    return None


# Ekran gratulacji
def show_congratulations_screen(score, screen, SCREEN_WIDTH, SCREEN_HEIGHT, select_sound):
    options = [('Następny poziom', 'next_level'), ('Wyjście', 'quit')]
    selected = 0

    font = get_font(48, bold=True)
    font_small = get_font(36)

    waiting = True
    result = None

    while waiting:
        screen.fill(DARK_BLUE)
        congrats = font.render("GRATULACJE!", True, GREEN)
        screen.blit(congrats, (SCREEN_WIDTH // 2 - congrats.get_width() // 2, 100))

        score_text = font_small.render(f"Wynik: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 200))

        button_rects = []
        for i, (label, value) in enumerate(options):
            color = YELLOW if i == selected else WHITE
            text = font_small.render(label, True, color)
            rect = text.get_rect()
            rect.topleft = (SCREEN_WIDTH // 2 - text.get_width() // 2, 300 + i * 50)
            button_rects.append(rect)
            screen.blit(text, rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                    select_sound.play()
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                    select_sound.play()
                if event.key == pygame.K_RETURN:
                    result = options[selected][1]
                    waiting = False
                    select_sound.play()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(mouse_x, mouse_y):
                        selected = i
                        result = options[selected][1]
                        waiting = False
                        select_sound.play()

    return result

# Ekran game over
def show_game_over_screen(score, screen, SCREEN_WIDTH, SCREEN_HEIGHT, select_sound):
    options = [
        ('Menu główne', 'main_menu'),
    ]
    selected = 0

    font = get_font(48, bold=True)
    font_small = get_font(36)

    waiting = True
    result = None

    while waiting:
        screen.fill(DARK_BLUE)
        game_over = font.render("KONIEC GRY", True, RED)
        screen.blit(game_over, (SCREEN_WIDTH // 2 - game_over.get_width() // 2, 100))

        score_text = font_small.render(f"Wynik: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 200))

        button_rects = []
        for i, (label, value) in enumerate(options):
            color = YELLOW if i == selected else WHITE
            text = font_small.render(label, True, color)
            rect = text.get_rect()
            rect.topleft = (SCREEN_WIDTH // 2 - text.get_width() // 2, 300 + i * 50)
            button_rects.append(rect)
            screen.blit(text, rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                    select_sound.play()
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                    select_sound.play()
                if event.key == pygame.K_RETURN:
                    result = options[selected][1]
                    select_sound.play()
                    waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(mouse_x, mouse_y):
                        selected = i
                        select_sound.play()
                        result = options[selected][1]
                        waiting = False

    return result

# Ekran wyników
def show_highscores(screen, SCREEN_WIDTH, SCREEN_HEIGHT, difficulty, select_sound):
    font_title = get_font(50, bold=True)
    font = get_font(36)

    difficulties = ['easy', 'normal', 'hard']
    selected_difficulty_index = difficulties.index(difficulty)

    def load_scores(filename):
        scores = []
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    if ':' in line:
                        parts = line.strip().split(':')
                        if len(parts) == 2:
                            name = parts[0].strip()
                            try:
                                score = int(parts[1].strip())
                                scores.append((name, score))
                            except ValueError:
                                pass
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    waiting = True
    while waiting:
        screen.fill(DARK_BLUE)
        current_diff = difficulties[selected_difficulty_index]
        title = font_title.render(f"WYNIKI - {current_diff.upper()}", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        filename = f'scores_{current_diff}.txt'
        highscores = load_scores(filename)

        for i, (name, score) in enumerate(highscores[:10]):
            entry = font.render(f"{i+1}. {name} - {score}", True, WHITE)
            screen.blit(entry, (SCREEN_WIDTH // 2 - entry.get_width() // 2, 200 + i * 40))

        prompt = font.render("ESC - powrót    <-/-> - zmiana poziomu", True, WHITE)
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, SCREEN_HEIGHT - 80))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    select_sound.play()
                    waiting = False
                elif event.key == pygame.K_RIGHT:
                    selected_difficulty_index = (selected_difficulty_index + 1) % len(difficulties)
                    select_sound.play()
                elif event.key == pygame.K_LEFT:
                    selected_difficulty_index = (selected_difficulty_index - 1) % len(difficulties)
                    select_sound.play()

# Ekran instrukcji
def show_instructions(screen, SCREEN_WIDTH, SCREEN_HEIGHT, select_sound):
    font_title = get_font(50, bold=True)
    font = get_font(28)

    instructions = [
        "INSTRUKCJE:",
        "",
        "Sterowanie:",
        "- Strzałki LEWO/PRAWO: poruszanie paletką",
        "- SPACJA: start / wypuszczenie piłki",
        "- P: pauza",
        "",
        "Cel gry:",
        "- Zniszcz wszystkie niszczalne cegiełki",
        "- Zbieraj bonusy",
        "",
        "Punktacja:",
        "- Zniszczenie cegiełki: +10 punktów",
        "- Odbicie piłki: -1 punkt",
        "",
        "Bonusy:",
        "- WI: poszerzenie paletki",
        "- SH: zwężenie paletki",
        "- SL: spowolnienie piłki",
        "- FA: przyspieszenie piłki",
        "- MU: multi-ball",
        "- LA: laser",
        "",
        "ESC - powrót do menu",
        "",
        "Strzałki GÓRA/DÓŁ - przewijanie"
    ]

    scroll_offset = 0
    max_offset = max(0, len(instructions) * 40 - SCREEN_HEIGHT + 100)
    line_height = 40

    waiting = True
    while waiting:
        screen.fill(DARK_BLUE)
        y = 50 - scroll_offset

        for line in instructions:
            if line == "INSTRUKCJE:":
                text = font_title.render(line, True, YELLOW)
            else:
                text = font.render(line, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y))
            y += line_height

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    select_sound.play()
                    waiting = False
                elif event.key == pygame.K_DOWN:
                    scroll_offset = min(scroll_offset + 20, max_offset)
                elif event.key == pygame.K_UP:
                    scroll_offset = max(scroll_offset - 20, 0)

# Ekran wpisywania imienia
def ask_player_name(screen, SCREEN_WIDTH, SCREEN_HEIGHT, select_sound):
    font = get_font(48, bold=True)
    font_small = get_font(32)

    name = ""
    entering = True

    error_message = ""
    error_timer = 0

    while entering:
        screen.fill(DARK_BLUE)
        title = font.render("PODAJ SWOJE IMIĘ", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))

        name_surface = font.render(name, True, WHITE)
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - 200, 300, 400, 60), 2)
        input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 300, 400, 60)
        text_rect = name_surface.get_rect(center=input_rect.center)
        screen.blit(name_surface, text_rect)

        prompt = font_small.render("ENTER - potwierdź, BACKSPACE - usuń, ESC - wyjdź", True, WHITE)
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 400))

        # Wyświetl komunikat błędu jeśli jest
        if error_message and pygame.time.get_ticks() - error_timer < 2000:
            error_font = font_small
            error_text = error_font.render(error_message, True, RED)
            screen.blit(error_text, (SCREEN_WIDTH // 2 - error_text.get_width() // 2, 450))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name.strip() == "":
                        select_sound.play()
                        error_message = "Imię nie może być puste!"
                        error_timer = pygame.time.get_ticks()
                        continue
                    else:
                        select_sound.play()
                        return name
                elif event.key == pygame.K_ESCAPE:
                    select_sound.play()
                    return None  
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 12 and event.unicode.isprintable():
                        name += event.unicode

def show_game_complete_screen(score, screen, SCREEN_WIDTH, SCREEN_HEIGHT, select_sound):
    options = [
        ('Menu główne', 'main_menu'),
    ]
    selected = 0

    font = get_font(48, bold=True)
    font_small = get_font(36)

    waiting = True
    result = None

    while waiting:
        screen.fill(DARK_BLUE)
        complete_text = font.render("UKOŃCZYŁEŚ GRĘ!", True, GREEN)
        screen.blit(complete_text, (SCREEN_WIDTH // 2 - complete_text.get_width() // 2, 100))

        score_text = font_small.render(f"Twój wynik: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 200))

        button_rects = []
        for i, (label, value) in enumerate(options):
            color = YELLOW if i == selected else WHITE
            text = font_small.render(label, True, color)
            rect = text.get_rect()
            rect.topleft = (SCREEN_WIDTH // 2 - text.get_width() // 2, 300 + i * 50)
            button_rects.append(rect)
            screen.blit(text, rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                    select_sound.play()
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                    select_sound.play()
                if event.key == pygame.K_RETURN:
                    result = options[selected][1]
                    select_sound.play()
                    waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(mouse_x, mouse_y):
                        selected = i
                        select_sound.play()
                        result = options[selected][1]
                        waiting = False

    return result

