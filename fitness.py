#http://www.phys.ens.fr/~wiese/highlights/lerw.html

import random
import pygame
import numpy as np

# 1. INITIAL DATA
protein_size = 10
primary_strc = [0, 0, 0, 1, 1, 0, 1, 1, 1, 0]
number_of_proteins = 10
pressure = 3 # Number of proteins for reproduction in each generation
mutation_chance = 0.1
number_of_generations = 100
proteins = []

# Mejorar esto de que variables hay que pedir y cuales no
class Protein():
	def __init__(self, size = 10, folding = [] ):
		self.size = size
		self.primary = primary_strc
		self.folding = folding

	def __str__(self):
		return str(self.folding)

	def __lt__(self, other):
		return True
  
# 5. (EXTRA) VISUALIZING THE RE-
# SULTS WITH PYGAME
(screen_width, screen_height) = (400, 400)
white = (255,255,255)
black = (0, 0, 0)
bond_len = 20
L = 17 # Lado de la matriz con las soluciones. Podria ser menor

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Protein')
screen.fill(white)

def draw_aminoacid(style, x, y):
	if style == 0:
		thickness = 1
	else:
		thickness = 5
	pygame.draw.circle(screen, black, (x, y), 5, thickness)

def draw_bond(xi, yi, xf, yf):
	pygame.draw.line(screen, black, (xi, yi), (xf, yf))

def new_coord_x(move, old_x, step):
	new_x = old_x*np.ones(4)
	new_x[1] += step
	new_x[3] -= step
	return new_x[move]

def new_coord_y(move, old_y, step):
	new_y = old_y*np.ones(4)
	new_y[0] -= step
	new_y[2] += step
	return new_y[move]

def make_matrix(folding):
	matrix = np.zeros((L,L))
	act_coord_x = (L-1)/2
	act_coord_y = (L-1)/2
	matrix[act_coord_y][act_coord_x] = 1
	prev_move = 0

	for i in range(len(folding)):
		act_move = (prev_move + folding[i])%4
		next_coord_x = new_coord_x(act_move, act_coord_x, 1)
		next_coord_y = new_coord_y(act_move, act_coord_y, 1)
		matrix[int(next_coord_y)][int(next_coord_x)] = i + 2

		prev_move = act_move
		act_coord_x = next_coord_x
		act_coord_y = next_coord_y

	return matrix

def calc_fitness(matrix, folding):
	act_coord_x = (L-1)/2
	act_coord_y = (L-1)/2
	prev_move = 0
	energy = 0
	neighbours = np.zeros((4,2))

	for i in range(len(folding)):
		#check_neighbours(matrix, coordinates)
		# Coordenadas de los vecinos
		neighbours[0][0] = act_coord_x + 1
		neighbours[0][1] = act_coord_y
		neighbours[1][0] = act_coord_x
		neighbours[1][1] = act_coord_y - 1
		neighbours[2][0] = act_coord_x - 1
		neighbours[2][1] = act_coord_y
		neighbours[3][0] = act_coord_x
		neighbours[3][1] = act_coord_y + 1

		for j in range(4):
			vx = int(neighbours[j][0])
			vy = int(neighbours[j][1])
			if (matrix[vy][vx] != 0.0) and (abs(matrix[vy][vx] - matrix[int(act_coord_y)][int(act_coord_x)]) != 1.0):
				energy += 2*primary_strc[i] - 1

		act_move = (prev_move + folding[i])%4
		next_coord_x = new_coord_x(act_move, act_coord_x, 1)
		next_coord_y = new_coord_y(act_move, act_coord_y, 1)

		prev_move = act_move
		act_coord_x = next_coord_x
		act_coord_y = next_coord_y

	return energy

def draw_solution(primary, folding):
	#Dibujar el primer amino
	act_coord_x = screen_width//2
	act_coord_y = screen_height//2
	prev_move = 0
	draw_aminoacid(primary[0], act_coord_x, act_coord_y)

	for i in range(len(folding)):
		act_move = (prev_move + folding[i])%4
		next_coord_x = new_coord_x(act_move, act_coord_x, bond_len)
		next_coord_y = new_coord_y(act_move, act_coord_y, bond_len)

		draw_bond(act_coord_x, act_coord_y, next_coord_x, next_coord_y)
		draw_aminoacid(primary[i+1], int(next_coord_x), int(next_coord_y))

		prev_move = act_move
		act_coord_x = next_coord_x
		act_coord_y = next_coord_y

last_protein = Protein(protein_size)
temp = [0,0,0,0,0,0,0,0,0]

last_protein.folding = temp
print("Primary structure:\n" + str(primary_strc))

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			
	draw_solution(primary_strc, last_protein.folding)

	pygame.display.flip()
