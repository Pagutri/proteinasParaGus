"""
This code calculates the optimum tertiary
structure of a very simplified model of
protein.
"""

import random
import pygame

# 1. INITIAL DATA
protein_size = 10
primary_strc = [0, 0, 0, 1, 1, 0, 1, 1, 1, 0]
number_of_proteins = 10
pressure = 3 # Number of proteins for reproduction in each generation
mutation_chance = 0.2
number_of_generations = 15
proteins = []

class Protein():
	def __init__(self, size):
		self.size = size
		self.primary = primary_strc
		self.folding = []

	def __str__(self):
		return str(self.folding)

# 2. INICIAL POPULATION
# Each element of the population
# is a list of 0, -1 and 1, desig-
# nating the direction of folding.
# Constraint: The protein cannot
# intersect itself. This is cha-
# llenge number one.
for i in range(number_of_proteins):
	protein = Protein(protein_size)

	for j in range(protein_size - 1):
		direction = random.randint(-1,1)
		protein.folding.append(direction)

	proteins.append(protein)
	print(protein)

def fitness(folding): # Ahorita no mas pa' que haga algo
	energy = 0
	for direction in folding:
		energy += direction
	return energy

# 3. REPRODUCTION AND MUTATION
def selection(population):
	valuated = [ (fitness(i), i) for i in population]
	valuated = [i[1] for i in sorted(valuated)]
	population = valuated  
	selected =  valuated[(len(valuated)-pressure):]
	return selected

# No me gusta este metodo. Preferiria conservar algunos
# individuos de la poblacion vieja
def reproduction(selected):
	for i in selected:
		cross_point = random.randint(1, protein_size - 2)
		parent = random.sample(selected, 2)
		population[i][:cross_point] = parent[0][:cross_point]
		population[i][cross_point:] = parent[1][cross_point:]

	return population

def mutation(population):
    for i in range(len(population)-pressure):
        if random.random() <= mutation_chance:
            point = random.randint(0, protein_size - 2)
            new_value = random.randint(-1, 1)

            while new_value == population[i][point]:
                new_value = random.randint(-1, 1)

            population[i][point] = new_value
  
    return population
      
  
# 4. FITNESS COMPUTATION
# The fitness is computed adding
# the values from two topological
# neighbours. A perfect pointing
# on these neighbours is challenge
# number two.

#Poner ya hasta aca el main. Arriba solo las funciones
for i in range(number_of_generations):
    proteins = selection(proteins)
    proteins = reproduction(proteins)
    proteins = mutation(proteins)

print(proteins)

# 5. (EXTRA) VISUALIZING THE RE-
# SULTS WITH PYGAME
(screen_width, screen_height) = (400, 400)
white = (255,255,255)
black = (0, 0, 0)

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
	pass

def nueva_coord(mov_ant, direction):
	pass

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			
	draw_aminoacid(1, 200, 200)
	draw_aminoacid(0, 220, 200)

	pygame.display.flip()