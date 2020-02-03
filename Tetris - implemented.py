import pygame, sys, time, random
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_a, K_d

window_size = (640*2,480*2)
blue = (0,0,155)
box_size = 20*2
screen_height = 100*2
screen_width = 50*2
white_color = (255,255,255)
grey_color = (150,150,150)
green = (102,255,0)
s_shape_template = [['.','.','.','.','.'],['.','.','.','.','.'],['.','.','c','c','.'],['.','c','c','.','.'],['.','.','.','.','.']]
s2_shape_template = [['.','.','.','.','.'],['.','.','c','.','.'],['.','c','c','.','.'],['.','c','.','.','.'],['.','.','.','.','.']]
o_shape_template = [['.','.','.','.','.'],['.','.','.','.','.'],['.','c','c','.','.'],['.','c','c','.','.'],['.','.','.','.','.']]
i_shape_template = [['.','.','c','.','.'],['.','.','c','.','.'],['.','.','c','.','.'],['.','.','c','.','.'],['.','.','.','.','.']]
i2_shape_template = [['.','.','.','.','.'],['.','.','.','.','.'],['c','c','c','c','.'],['.','.','.','.','.'],['.','.','.','.','.']]
t1_shape_template = [['.','.','.','.','.'],['.','.','c','.','.'],['.','.','c','c','.'],['.','.','c','.','.'],['.','.','.','.','.']]
t2_shape_template = [['.','.','.','.','.'],['.','.','.','.','.'],['.','c','c','c','.'],['.','.','c','.','.'],['.','.','.','.','.']]
t3_shape_template = [['.','.','.','.','.'],['.','.','c','.','.'],['.','c','c','.','.'],['.','.','c','.','.'],['.','.','.','.','.']]
t4_shape_template = [['.','.','.','.','.'],['.','.','c','.','.'],['.','c','c','c','.'],['.','.','.','.','.'],['.','.','.','.','.']]

def run_tetris_game():
    pygame.init()
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('TETRIS')
    game_matrix = create_game_matrix()
    last_time_piece_moved = time.time()
    piece_arrived_at_bottom = 0
    piece = create_piece()
    score = 0
    game_speed_start = .4
    max_game_speed = 0.15
    game_speed = game_speed_start
    crashed = False
    while not crashed:

        # DRAWS THE BOARD
        screen.fill((0,0,0))
        draw_moving_piece(screen, piece, white_color, grey_color)
        draw_board(screen, game_matrix, white_color, grey_color)
        draw_score(screen, score, game_speed)
        pygame.draw.rect(screen,blue,[screen_height, screen_width, 10*box_size + 10, 20*box_size + 10],5)
        pygame.display.update()

        listen_to_user_input(game_matrix, piece)
        if game_speed > max_game_speed:
            game_speed = (1 - score*.05)*game_speed_start

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                crashed = True
        for event in pygame.event.get(QUIT):
            pygame.display.quit()
            pygame.quit()
            sys.exit()


        # MAKES PIECE FALL
        if (time.time() - last_time_piece_moved > game_speed) and (is_valid_position_to_move(game_matrix, piece, adj_row=1)):
            piece['row'] += 1
            last_time_piece_moved = time.time()
            # print(piece['row'])

        # RESETS THE TIME THE PIECE TOUCHED THE FLOOR IN CASE THERE STILL IS FREE SPACE FOR MOVEMENT
        if is_valid_position_to_move(game_matrix, piece, adj_row=1):
            piece_arrived_at_bottom = 0

        # MARKS THE TIME THE PIECE TOUCHED A FLOOR
        if (is_valid_position_to_move(game_matrix, piece, adj_row=1) == False) and (piece_arrived_at_bottom == 0):
            piece_arrived_at_bottom = time.time()

        # UPDATES THE GAME BOARD AND CREATES NEW PIECE
        if (is_valid_position_to_move(game_matrix, piece, adj_row=1) == False) and (time.time() - piece_arrived_at_bottom > game_speed):
            # game_matrix[piece['row']][piece['column']] = 'c'
            game_matrix = update_game_matrix(game_matrix, piece)
            piece = create_piece()
            piece_arrived_at_bottom = 0

        # CLEAR COMPLETED LINES AND UPDATES THE SCORE
        for row in range(20):
            if line_is_complete(game_matrix, row):
                eliminate_row(game_matrix, row)
                score += 1

def starting_pieces():
    return {'s': s_shape_template, 'i': i_shape_template, 'o': o_shape_template, 't1': t1_shape_template }

def avaiable_pieces():
    return {'s': s_shape_template, 'i': i_shape_template, 'o': o_shape_template, 's2': s2_shape_template, 'i2': i2_shape_template, 't1': t1_shape_template, 't2': t2_shape_template, 't3': t3_shape_template, 't4': t4_shape_template}


def is_valid_position_to_move(matrix, piece, adj_row=0, adj_col=0):
    piece_matrix = avaiable_pieces()[piece['shape']]
    for row in range(5):
        for col in range(5):
            if piece_matrix[row][col] == '.':
                continue
            if is_on_board(piece['row'] + row + adj_row, piece['column'] + col + adj_col) == False or piece['column'] + col + adj_col < 0:
                return False
            if matrix[piece['row'] + row + adj_row][piece['column'] + col + adj_col] == 'c':
                return False
    return True

def draw_score(screen, score, speed):
    font = pygame.font.Font('freesansbold.ttf', 36)
    scoreSurf = font.render('Score: %s' % score, True, (255,255,255))
    screen.blit(scoreSurf, (640*2 - 150*2, 20))
    scoreSurf = font.render('Speed: %s seg' % speed, True, (255,255,255))
    screen.blit(scoreSurf, (640*2 - 150*2, 65))
    pygame.draw.rect(screen,green,[970, 12, 280, 95],5)

def eliminate_row(matrix, row):
    for line in range(1, row):
        matrix[row- line + 1] = matrix[row - line]

def line_is_complete(matrix, row):
    if matrix[row] == ['c','c','c','c','c','c','c','c','c','c']:
        return True
    else:
        return False

def next_block_down_free(matrix, piece):
    if piece['row'] >= 19:
        return False
    elif matrix[piece['row'] + 1][piece['column']] == 'c':
        return False
    else:
        return True

def create_game_matrix():
	game_matrix_columns = 10
	game_matrix_rows = 20
	matrix = []
	for row in range(game_matrix_rows):
		new_row = []
		for column in range(game_matrix_columns):
			new_row.append('.')
		matrix.append(new_row)
	return matrix

def create_piece():
    piece = {}
    random_shape = random.choice(list(starting_pieces().keys()))
    piece['shape'] = random_shape
    piece['row'] = 0
    piece['column'] = 4
    return piece

def update_game_matrix(matrix, piece):
    for row in range(5):
        for col in range(5):
            if avaiable_pieces()[piece['shape']][row][col] != '.':
                matrix[piece['row'] + row][piece['column'] + col] = 'c'
    return matrix

def is_on_board(row, column):
    if row > 19 or column > 9:
        return False
    if (column >= 0) and (column < 10) and (row < 20):
        return True

def draw_moving_piece(screen, piece, color, shadow):
    shape_to_draw = avaiable_pieces()[piece['shape']]
    for row in range(5):
        for col in range(5):
            if shape_to_draw[row][col] != '.':
                draw_single_box(screen, piece['column'] + col, piece['row'] + row, color, shadow)

def draw_single_box(screen, column, row, color, shadow):
	origin_x = screen_height + 5 + column*box_size + 1
	origin_y = screen_width + 5 + row*box_size + 1
	pygame.draw.rect(screen, shadow, [origin_x, origin_y, box_size, box_size])
	pygame.draw.rect(screen, color, [origin_x, origin_y, box_size-4, box_size-4])

def draw_board(screen, matrix, color, shadow):
    game_matrix_columns = 10
    game_matrix_rows = 20
    for column in range(game_matrix_columns):
        for row in range(game_matrix_rows):
            if matrix[row][column] != '.':
                draw_single_box(screen, column, row, color, shadow)

def listen_to_user_input(matrix, piece):
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT and is_valid_position_to_move(matrix, piece, adj_col=-1):
                piece['column'] -= 1
            if event.key == K_RIGHT and is_valid_position_to_move(matrix, piece, adj_col=+1):
                piece['column'] += 1
            if event.key == K_UP:
                # old_shape = piece['shape']
                if piece['shape'] == 's':
                    piece['shape'] = 's2'
                    if not is_valid_position_to_move(matrix, piece):
                        piece['shape'] = 's'

                elif piece['shape'] == 's2':
                    piece['shape'] = 's'
                    if not is_valid_position_to_move(matrix, piece):
                        piece['shape'] = 's2'

                elif piece['shape'] == 'i':
                    piece['shape'] = 'i2'
                    if not is_valid_position_to_move(matrix, piece):
                        piece['shape'] = 'i'

                elif piece['shape'] == 'i2':
                    piece['shape'] = 'i'
                    if not is_valid_position_to_move(matrix, piece):
                        piece['shape'] = 'i2'

                elif piece['shape'] == 't1':
                    piece['shape'] = 't2'
                    if not is_valid_position_to_move(matrix, piece):
                        piece['shape'] = 't1'

                elif piece['shape'] == 't2':
                    piece['shape'] = 't3'
                    if not is_valid_position_to_move(matrix, piece):
                        piece['shape'] = 't2'

                elif piece['shape'] == 't3':
                    piece['shape'] = 't4'
                    if not is_valid_position_to_move(matrix, piece):
                        piece['shape'] = 't3'

                elif piece['shape'] == 't4':
                    piece['shape'] = 't1'
                    if not is_valid_position_to_move(matrix, piece):
                        piece['shape'] = 't4'


def valid_move(matrix, piece, d):
    if piece['column'] == 0 and d == -1:
        return False
    elif piece['column'] == 9 and d == +1:
        return False
    elif matrix[piece['row']][piece['column'] + d] == 'c':
        return False
    else:
        return True



run_tetris_game()
