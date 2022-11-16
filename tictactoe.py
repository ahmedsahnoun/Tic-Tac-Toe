# MODULES
import pygame
from sys import exit
from numpy import zeros
from algorithme import *
from time import time

# constants
WIDTH = 600
HEIGHT = 600
EXTRA = 180
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55
# rgb: red green blue
RED = (255, 0, 0)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# initialisation de board
board = zeros( (BOARD_ROWS, BOARD_COLS) )

# foncitons
# ecrire un texte dans l'ecran
def printText(text,dest):
	font = pygame.font.SysFont("Arial",25,True,False)
	surface = font.render(text, True, (220,220,220))
	screen.blit(surface, dest)

# ecrire les infos relatives à l'execution
def displayInfo():
	screen.fill(BG_COLOR, (0, HEIGHT + 10, WIDTH, EXTRA))
	printText("p1 vs p2: a", (20, HEIGHT + 15))
	printText("p1 vs minimax: z", (20, HEIGHT + 15 + EXTRA//4))
	printText("p1 vs AlphaBeta: e", (20, HEIGHT + 15 + 2 * EXTRA//4))
	printText("Hauteur(+/-): "+ str(hauteur), (20, HEIGHT + 15 + 3 * EXTRA//4))
	printText("Adversaire: " + adversaire, (20 + WIDTH//2, HEIGHT + 15))
	printText("H(n): " + str(H), (20 + WIDTH//2, HEIGHT + 15 + EXTRA//4))
	printText("Noeuds: " + str(noeuds), (20 + WIDTH//2, HEIGHT + 15 + 2 *EXTRA//4))
	printText("time: " + "{:.2f}".format(temps*1000)+" ms", (20 + WIDTH//2, HEIGHT + 15 + 3 *EXTRA//4))
	pygame.draw.line( screen, LINE_COLOR, (WIDTH//2, 3 * SQUARE_SIZE), (WIDTH//2, HEIGHT+EXTRA), LINE_WIDTH )

# dessiner les lignes limitants les cases
def draw_lines():
	# 1 horizontal
	pygame.draw.line( screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH )
	# 2 horizontal
	pygame.draw.line( screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH )
	# 3 horizontal
	pygame.draw.line( screen, LINE_COLOR, (0, 3 * SQUARE_SIZE), (WIDTH, 3 * SQUARE_SIZE), LINE_WIDTH )

	# 1 vertical
	pygame.draw.line( screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH )
	# 2 vertical
	pygame.draw.line( screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH )

# dessiner les symboles X et O selon leur contenu
def draw_figures():
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == 1:
				#draw O
				pygame.draw.circle( screen, CIRCLE_COLOR, (int( col * SQUARE_SIZE + SQUARE_SIZE//2 ), int( row * SQUARE_SIZE + SQUARE_SIZE//2 )), CIRCLE_RADIUS, CIRCLE_WIDTH )
			elif board[row][col] == 2:
				#draw X
				pygame.draw.line( screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH )	
				pygame.draw.line( screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH )

# remplir la case convenable par l'id du joueur
def mark_square(row, col, player):
	board[row][col] = player

# verifier si une case est vide
def available_square(row, col):
	return board[row][col] == 0

# verifier si la matrice est remplie
def is_board_full():
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == 0:
				return False

	return True

# verifier si un certain joueur a gagné
def check_win(player):
	# vertical win check
	for col in range(BOARD_COLS):
		if board[0][col] == player and board[1][col] == player and board[2][col] == player:
			draw_vertical_winning_line(col, player)
			return True

	# horizontal win check
	for row in range(BOARD_ROWS):
		if board[row][0] == player and board[row][1] == player and board[row][2] == player:
			draw_horizontal_winning_line(row, player)
			return True

	# asc diagonal win check
	if board[2][0] == player and board[1][1] == player and board[0][2] == player:
		draw_asc_diagonal(player)
		return True

	# desc diagonal win chek
	if board[0][0] == player and board[1][1] == player and board[2][2] == player:
		draw_desc_diagonal(player)
		return True

	return False

# fonctions pour dessiner une ligne pour la combinaison qui gagne:

def draw_vertical_winning_line(col, player):
	posX = col * SQUARE_SIZE + SQUARE_SIZE//2

	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( screen, color, (posX, 15), (posX, HEIGHT - 15), LINE_WIDTH )

def draw_horizontal_winning_line(row, player):
	posY = row * SQUARE_SIZE + SQUARE_SIZE//2

	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( screen, color, (15, posY), (WIDTH - 15, posY), WIN_LINE_WIDTH )

def draw_asc_diagonal(player):
	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), WIN_LINE_WIDTH )

def draw_desc_diagonal(player):
	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), WIN_LINE_WIDTH )


# rafraichir l'ecran de jeu
def restart():
	screen.fill( BG_COLOR )
	draw_lines()
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			board[row][col] = 0

# ecran
screen = pygame.display.set_mode( (WIDTH, HEIGHT + EXTRA) )
pygame.display.set_caption( 'TIC TAC TOE' )
screen.fill( BG_COLOR )
draw_lines()

# Initialisation
player = 1
game_over = False
adversaire = "p2"
hauteur = 3
H = 0
noeuds = 0
temps = 0
pygame.init()

# Boucle main
while True:
	for event in pygame.event.get():
		# quitter le jeu
		if event.type == pygame.QUIT:
			exit()

		# clicker avec le souris
		if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

			mouseX = event.pos[0] # x
			mouseY = event.pos[1] # y

			if mouseY > HEIGHT:
				pass
			else:
				clicked_row = int(mouseY // SQUARE_SIZE)
				clicked_col = int(mouseX // SQUARE_SIZE)

				if available_square( clicked_row, clicked_col ):

					mark_square( clicked_row, clicked_col, player )
					if check_win( player ):
						game_over = True

					# changer le joueur
					player = 3 - player

					# action selon l'adversaire
					if adversaire == "p2" or game_over:
						pass
					else:
						if adversaire == "minimax":
							start = time()
							x=minimax(board,hauteur,False)
							end = time()
							temps = (end - start)
						else:
							start = time()
							x=AlphaBeta(board,hauteur,-20,20,False)
							end = time()
							temps = (end - start)
						H = x[0]
						noeuds = x[1]
						if x[2]:
							mark_square(x[2][0], x[2][1], player)
						if check_win( player ):
							game_over = True
						player = 3 - player

					draw_figures()

		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
				if hauteur<8:
					hauteur += 1

			if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
				if hauteur>1:
					hauteur -= 1

			if event.key == pygame.K_a:
				temps = 0
				player = 1
				game_over = False
				H = 0
				noeuds = 0
				restart()
				adversaire = "p2"

			if event.key == pygame.K_z:
				temps = 0
				player = 1
				game_over = False
				H = 0
				noeuds = 0
				restart()
				adversaire = "minimax"
				
			if event.key == pygame.K_e:
				temps = 0
				player = 1
				game_over = False
				H = 0
				noeuds = 0
				restart()
				adversaire = "alphabeta"

	# visualisation
	displayInfo()
	pygame.display.update()