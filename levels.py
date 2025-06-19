from brick import Brick
import random
LEVELS = {
   'level1':[
       [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
       [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
       [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
       [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
       [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
       [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
       [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
       [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    ],
    'level2':[
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
    ],
    'level3':[
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 1, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0],
        [0, 2, 1, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0],
        [0, 2, 0, 0, 2, 1, 0, 2, 0, 0, 2, 0, 0],
        [0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0],
        [0, 2, 0, 1, 2, 0, 0, 2, 0, 1, 2, 0, 0],
        [0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0],
        [0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0],
        [0, 2, 0, 0, 2, 0, 1, 2, 0, 0, 2, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
        [0, 2, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1],
        [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    ],
    'level4':[
        [0, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 2, 0],
        [0, 1, 2, 1, 1, 1, 0, 1, 1, 1, 2, 1, 0],
        [0, 2, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 0, 2, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 2, 0, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 2, 0],
        [0, 1, 2, 1, 1, 1, 0, 1, 1, 1, 2, 1, 0],
        [0, 2, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 0, 2, 1, 1, 1, 1, 0]
    ],
    'level5':[
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 2, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]
    ],
    'level6':[
        [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 0],
        [0, 0, 2, 2, 0, 0, 3, 0, 0, 2, 2, 0, 0],
        [2, 2, 0, 0, 1, 1, 0, 1, 1, 0, 0, 2, 2],
        [0, 0, 1, 1, 0, 0, 3, 0, 0, 1, 1, 0, 0],
        [1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1],
        [0, 0, 1, 1, 0, 0, 3, 0, 0, 1, 1, 0, 0],
        [1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1],
        [0, 0, 1, 1, 0, 0, 3, 0, 0, 1, 1, 0, 0],
        [1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1],
        [0, 0, 1, 1, 0, 0, 3, 0, 0, 1, 1, 0, 0],
        [1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1],
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    ], 
    'level7':[
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [3, 3, 3, 3, 3, 2, 2, 2, 3, 3, 3, 3, 3],
        [3, 1, 1, 1, 3, 0, 0, 0, 3, 1, 1, 1, 3],
        [3, 1, 1, 1, 3, 0, 0, 0, 3, 1, 1, 1, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [3, 0, 0, 0, 3, 1, 1, 1, 3, 0, 0, 0, 3],
        [3, 0, 0, 0, 3, 1, 1, 1, 3, 0, 0, 0, 3],
        [3, 2, 2, 2, 3, 3, 3, 3, 3, 2, 2, 2, 3]
    ],
}

def load_level(level_key, brick_width, brick_height, LEVELS):
    bricks = []
    level_data = LEVELS[level_key]

    predefined_colors = [
        (255, 255, 255),  # white
        (255, 165, 0),    # orange
        (255, 255, 0),    # yellow
        (0, 255, 0),      # green
        (255, 0, 0),      # red
        (0, 0, 255),      # blue
        (255, 99, 71),    # tomato
        (0, 191, 255),    # deep sky blue
        (124, 252, 0),    # lawn green
        (255, 215, 0),    # gold
        (138, 43, 226),   # blue violet
        (255, 105, 180),  # hot pink
        (244, 164, 96),   # sandy brown
        (0, 255, 127),    # spring green
        (70, 130, 180),   # steel blue
        (255, 140, 0),    # dark orange
        (255, 0, 255),    # magenta
        (0, 255, 255),    # cyan
        (128, 0, 0),      # maroon
        (0, 128, 0),      # dark green
        (0, 0, 128)       # navy
    ]

    row_colors = []
    diagonal_colors = {}
    layer_colors = {}
    tile_color_map = {}

    # Ustawienia kolorów zależnie od poziomu
    if level_key in ['level1', 'level5']:  # kolumny
        for _ in range(len(level_data)):
            row_colors.append(predefined_colors[0])
    elif level_key == 'level2':  # rzędy, każdy inny kolor
        available_colors = predefined_colors.copy()
        random.shuffle(available_colors)
        row_colors = available_colors[:len(level_data)]
    elif level_key == 'level4':  # skośne przekątne
        available_colors = predefined_colors.copy()
        random.shuffle(available_colors)
        color_index = 0
        diag_set = set()
        for row_index, row in enumerate(level_data):
            for col_index, cell in enumerate(row):
                if cell == 1:
                    diag_set.add(col_index + row_index)
        for diag in sorted(diag_set):
            diagonal_colors[diag] = available_colors[color_index % len(available_colors)]
            color_index += 1
    elif level_key == 'level6':  # łuki liczone względem dolnego klocka w kolumnie
        center_col = len(level_data[0]) // 2

        # Obliczamy lowest_row[col_index]
        lowest_row = {}
        for col_index in range(len(level_data[0])):
            lowest_row[col_index] = None
            for row_index in reversed(range(len(level_data))):
                if level_data[row_index][col_index] == 1:
                    lowest_row[col_index] = row_index
                    break

        # Zbieramy layer_set
        layer_set = set()
        for row_index, row in enumerate(level_data):
            for col_index, cell in enumerate(row):
                if cell == 1 and lowest_row[col_index] is not None:
                    layer = row_index - lowest_row[col_index]
                    layer_set.add(layer)

        # Przypisujemy kolory do layerów
        available_colors = predefined_colors.copy()
        random.shuffle(available_colors)
        for layer in sorted(layer_set):
            layer_colors[layer] = available_colors.pop()

    elif level_key == 'level7':  # SZTYWNE przypisanie (row, col) → kolor
        tile_color_map = {
            # pełne rzędy u góry
            **{(0, c): (255, 0, 0) for c in range(13)},
            **{(1, c): (0, 255, 0) for c in range(13)},
            **{(2, c): (0, 0, 255) for c in range(13)},
            
            # lewa wyspa wiersz 4-5 → zielona
            **{(4, c): (0, 255, 0) for c in range(1, 5)},
            **{(5, c): (0, 255, 0) for c in range(1, 5)},
            
            # prawa wyspa wiersz 4-5 → czerwona
            **{(4, c): (255, 0, 0) for c in range(8, 12)},
            **{(5, c): (255, 0, 0) for c in range(8, 12)},
            
            # dolna wyspa wiersz 8-9 → niebieska
            **{(8, c): (0, 0, 255) for c in range(5, 8)},
            **{(9, c): (0, 0, 255) for c in range(5, 8)},
        }

    else:
        for _ in level_data:
            row_colors.append(random.choice(predefined_colors))

    # Tworzenie cegiełek
    for row_index, row in enumerate(level_data):
        for col_index, cell in enumerate(row):
            x = col_index * brick_width
            y = row_index * brick_height + 50

            if cell == 1:
                if level_key in ['level1', 'level5']:
                    color = predefined_colors[col_index % len(predefined_colors)]
                elif level_key == 'level2':
                    color = row_colors[row_index]
                elif level_key == 'level3':
                    color = random.choice(predefined_colors)
                elif level_key == 'level4':
                    diag = col_index + row_index
                    color = diagonal_colors[diag]
                elif level_key == 'level6':
                    if lowest_row[col_index] is not None:
                        layer = row_index - lowest_row[col_index]
                        color = layer_colors[layer]
                    else:
                        color = (255, 255, 255)  # fallback
                elif level_key == 'level7':
                    color = tile_color_map.get((row_index, col_index), (255, 255, 255))  # default white
                else:
                    color = row_colors[row_index]
                bricks.append(Brick(x, y, brick_width, brick_height, color))

            elif cell == 2:
                silver_color = (192, 192, 192)
                bricks.append(Brick(x, y, brick_width, brick_height, silver_color, indestructible=True))

            elif cell == 3:
                color = (60, 60, 60)  # ciemny szary
                bricks.append(Brick(x, y, brick_width, brick_height, color, hits_remaining=2))

    return bricks


