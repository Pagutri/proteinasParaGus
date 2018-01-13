"""
This code calculates the optimum tertiary
structure of a very simplified model of
protein.
"""

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
L = 17 # Lado de la matriz con las soluciones. Podria ser menor

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

# 2. INItIAL POPULATION
# Each element of the population
# is a list of 0, -1 and 1, desig-
# nating the direction of folding.
# Constraint: The protein cannot
# intersect itself. This is cha-
# llenge number one.
print("Initial population:")

for i in range(number_of_proteins):
	protein = Protein(protein_size)
	temp = []

	for j in range(protein_size - 1):
		direction = random.randint(-1,1)		
		temp.append(direction)

	protein.folding = temp
	proteins.append(protein)
	print(protein)

# 4. COMPUTATE FITNESS
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

# 3. REPRODUCTION AND MUTATION
def selection(population):
	valuated = [ (calc_fitness(make_matrix(i.folding), i.folding), i) for i in population]
	valuated = [i[1] for i in sorted(valuated)] #Aqui me quedo solo con las mejores instancias.Ya no guardo el fitness
	population = valuated  
	selected = valuated[:pressure] #Me interesan los de menor energia
	return selected

# No me gusta este metodo. Preferiria conservar algunos
# individuos de la poblacion vieja
def reproduction(selected):
	for i in range(number_of_proteins):
		cross_point = random.randint(1, protein_size - 2)
		parent = []
		parent.append(Protein(folding = random.choice(selected).folding))
		parent.append(Protein(folding = random.choice(selected).folding))
		proteins[i].folding[:cross_point] = parent[0].folding[:cross_point]
		proteins[i].folding[cross_point:] = parent[1].folding[cross_point:]

def mutation(population):
	#Solo quiero mutar los ultimos
    for i in range(pressure, number_of_proteins):
        if random.random() <= mutation_chance:
            point = random.randint(0, protein_size - 2)
            new_value = random.randint(-1, 1)

            while new_value == population[i].folding[point]:
                new_value = random.randint(-1, 1)

            population[i].folding[point] = new_value
  
    return population

#Poner ya hasta aca el main. Arriba solo las funciones
for i in range(number_of_generations):
	reproduction(selection(proteins))
	proteins = mutation(proteins)

print("Final generation:")

for i in proteins:
	print(i)

# 5. (EXTRA) VISUALIZING THE RE-
# SULTS WITH PYGAME
(screen_width, screen_height) = (400, 400)
white = (255,255,255)
black = (0, 0, 0)
bond_len = 20

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

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			
	draw_solution(primary_strc, proteins[0].folding)

	pygame.display.flip()
