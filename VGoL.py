import pygame
import numpy as np
import random

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)

display_width = 750
display_height = 750

cell_side = 25
state_array = np.empty((30, 30, 1), dtype=bool)
neighbour_array = np.empty((30, 30, 8), dtype=list)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Vinex' Game of Life")

clock = pygame.time.Clock()


def check_neighbour(x, y):
    neighbour_counter = 0
    for i in neighbour_array[x, y]:
        if i[0] in range(30) and i[1] in range(30):
            if state_array[i[0], i[1]]:
                neighbour_counter += 1

    return neighbour_counter


for x in range(30):
    for y in range(30):
        state_array[x, y] = random.choice([True, False])


for x in range(30):
   for y in range(30):
        neighbour_array[x, y, 0] = [x - 1, y]
        neighbour_array[x, y, 1] = [x + 1, y]
        neighbour_array[x, y, 2] = [x, y - 1]
        neighbour_array[x, y, 3] = [x, y + 1]
        neighbour_array[x, y, 4] = [x - 1, y - 1]
        neighbour_array[x, y, 5] = [x + 1, y - 1]
        neighbour_array[x, y, 6] = [x - 1, y + 1]
        neighbour_array[x, y, 7] = [x + 1, y + 1]


while True:
    for event in pygame.event.get():
         if event.type == pygame.QUIT:
             pygame.quit()
             quit()

    gameDisplay.fill(white)
    for x in range(30):
        for y in range(30):
            if state_array[x, y]:
                pygame.draw.rect(gameDisplay, black, [x * 25, y * 25, cell_side, cell_side])
            if state_array[x, y] and check_neighbour(x, y) < 2:
                state_array[x, y] = False
            elif state_array[x, y] and (check_neighbour(x, y) == 2 or check_neighbour(x, y) == 3):
                state_array[x, y] = True
            elif state_array[x, y] and check_neighbour(x, y) > 3:
                state_array[x, y] = False
            elif not state_array[x, y] and check_neighbour(x, y) == 3:
                state_array[x, y] = True

    pygame.display.update()
    clock.tick(5)