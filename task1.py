import pygame
import sys
from pygame.locals import *
import random

# Function to move the ant in a straight line
def straight(ant, matrix, play_time, pheromone, p):
	if p == "a" and play_time >= 0.01:
		pheromone[ant[1]][ant[0]] = 5
	elif p == "b" and play_time >= 0.01:
		pheromone[ant[1]][ant[0]] = -5

	if matrix[ant[1]][ant[0]] == 0 and play_time >= 0.01:
		matrix[ant[1]][ant[0]] = 1
		move_ant(ant)
	elif matrix[ant[1]][ant[0]] == 1 and play_time >= 0.01:
		matrix[ant[1]][ant[0]] = 0
		move_ant(ant)

# Function to move the ant in a normal pattern (turning left or right)
def normal(ant, matrix, play_time, pheromone, p):
	if p == "a" and play_time >= 0.01:
		pheromone[ant[1]][ant[0]] = 5
	elif p == "b" and play_time >= 0.01:
		pheromone[ant[1]][ant[0]] = -5

	if matrix[ant[1]][ant[0]] == 0 and play_time >= 0.01:
		matrix[ant[1]][ant[0]] = 1
		ant[2] = (ant[2] + 1) % 4  # Turn right
		move_ant(ant)
	elif matrix[ant[1]][ant[0]] == 1 and play_time >= 0.01:
		matrix[ant[1]][ant[0]] = 0
		ant[2] = (ant[2] - 1) % 4  # Turn left
		move_ant(ant)

# Function to move the ant based on its direction
def move_ant(ant):
	if ant[2] == 0:
		ant[0] -= 1  # Move left
	elif ant[2] == 1:
		ant[1] += 1  # Move down
	elif ant[2] == 2:
		ant[0] += 1  # Move right
	elif ant[2] == 3:
		ant[1] -= 1  # Move up

# Function to draw the grid on the background
def draw_grid(background):
	for i in range(128):
		pygame.draw.line(background, (92, 51, 23), (i * 8, 0), (i * 8, 768))
	for i in range(96):
		pygame.draw.line(background, (92, 51, 23), (0, i * 8), (1024, i * 8))

# Function to draw the matrix and pheromone levels on the background
def draw_matrix(background, matrix, pheromone):
	for i in range(96):
		for j in range(128):
			if pheromone[j][i] != 0:
				pheromone[j][i] -= 1 if pheromone[j][i] > 0 else -1
			color = (255, 255, 255) if matrix[j][i] == 0 else (0, 0, 0)
			if pheromone[j][i] != 0:
				color = (144, 238, 144)
			pygame.draw.rect(background, color, Rect((j * 8, i * 8), (8, 8)))

# Initialize pygame and font system for displaying the counter
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 20)

screen = pygame.display.set_mode((1024, 768))
matrix = [[0 for _ in range(96)] for _ in range(128)]
pheromone = [[0 for _ in range(96)] for _ in range(128)]
clock = pygame.time.Clock()
FPS = 60
playtime = 0.0

# Global step counter
step_counter = 0

# Set the ants' starting points randomly
# ant[0] = x-coordinate (0 to 95), ant[1] = y-coordinate (0 to 127), ant[2] = direction
ant1 = [random.randint(40, 65), random.randint(50, 100), 1]
ant2 = [random.randint(30, 75), random.randint(40, 90), 1]

# Main game loop
while True:
	background = pygame.Surface(screen.get_size())
	background.fill((255, 255, 255))

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	milliseconds = clock.tick(FPS)
	playtime += milliseconds / 1000.0

	# Increment and display the step counter
	step_counter += 1
	counter_text = font.render("Steps: " + str(step_counter), True, (0, 0, 0))
	background.blit(counter_text, (10, 10))

	screen.lock()
	draw_matrix(background, matrix, pheromone)
	draw_grid(background)

	# Update and draw ant1
	pygame.draw.rect(background, (139, 0, 0), Rect((ant1[1] * 8, ant1[0] * 8), (8, 8)))
	if pheromone[ant1[1]][ant1[0]] == 0:
		normal(ant1, matrix, playtime, pheromone, "a")
	elif pheromone[ant1[1]][ant1[0]] > 0:
		if random.random() <= 0.8:
			straight(ant1, matrix, playtime, pheromone, "a")
		else:
			normal(ant1, matrix, playtime, pheromone, "a")
	else:
		if random.random() <= 0.8:
			normal(ant1, matrix, playtime, pheromone, "a")
		else:
			straight(ant1, matrix, playtime, pheromone, "a")
	pygame.draw.rect(background, (255, 102, 102), Rect((ant1[1] * 8, ant1[0] * 8), (8, 8)))

	# Update and draw ant2
	pygame.draw.rect(background, (0, 0, 139), Rect((ant2[1] * 8, ant2[0] * 8), (8, 8)))
	if pheromone[ant2[1]][ant2[0]] == 0:
		normal(ant2, matrix, playtime, pheromone, "b")
	elif pheromone[ant2[1]][ant2[0]] < 0:
		if random.random() <= 0.8:
			straight(ant2, matrix, playtime, pheromone, "b")
		else:
			normal(ant2, matrix, playtime, pheromone, "b")
	else:
		if random.random() <= 0.8:
			normal(ant2, matrix, playtime, pheromone, "b")
		else:
			straight(ant2, matrix, playtime, pheromone, "b")
	pygame.draw.rect(background, (173, 216, 230), Rect((ant2[1] * 8, ant2[0] * 8), (8, 8)))

	playtime = 0.0

	screen.unlock()
	screen.blit(background, (0, 0))
	pygame.display.update()

