import pygame
import numpy as np
import random

black = (0, 0, 0)
white = (255, 255, 255)
green = (46, 204, 113)

display_width = 750
display_height = 750

cell_side = 25
state_array = np.full((30, 30, 1), False, dtype=bool)
neighbour_array = np.empty((30, 30, 8), dtype=list)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Vinex' Game of Life")
clock = pygame.time.Clock()
speed = 5


def check_neighbour(x, y):
    neighbour_counter = 0
    for i in neighbour_array[x, y]:
        if i[0] in range(30) and i[1] in range(30):
            if state_array[i[0], i[1]]:
                neighbour_counter += 1

    return neighbour_counter


def choose_randomly():
    for x in range(30):
        for y in range(30):
            state_array[x, y] = random.choice([True, False])


def text(font, content, size, pos, colour):
    sys_font = pygame.font.SysFont(str(font), size)
    text_surface = sys_font.render(str(content), False, colour)
    gameDisplay.blit(text_surface, pos)


def button(x, y, w, h, ic, ac, font, font_size, content, action, action2):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button_font = pygame.font.SysFont(str(font), font_size)
    button_text_object = button_font.render(str(content), False, black)

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x - 1, y - 1, w + 2, h + 2))
        gameDisplay.blit(button_text_object, (x + ((w - button_text_object.get_rect()[2]) / 2), y + ((h - button_text_object.get_rect()[3]) / 2)))

        if click[0] == 1 and action is not None:
            action()
            if action2 is not None:
                action2()

    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))
        gameDisplay.blit(button_text_object, (x + ((w - button_text_object.get_rect()[2]) / 2), y + ((h - button_text_object.get_rect()[3]) / 2)))


def set_speed_intro():
    global speed
    user_input = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key).isdigit():
                    user_input += pygame.key.name(event.key)
                if event.key == pygame.K_RETURN and user_input.isdigit():
                    speed = int(user_input)
                    intro()


def set_speed_main():
    global speed
    user_input = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key).isdigit():
                    user_input += pygame.key.name(event.key)
                if event.key == pygame.K_RETURN and user_input.isdigit():
                    speed = int(user_input)
                    main_loop()


def count_cells():
    counter = 0
    for x in range(30):
        for y in range(30):
            if state_array[x, y]:
                counter += 1
    return counter


def intro():
    pygame.init()
    pygame.font.init()
    intro_font = pygame.font.SysFont("Times New Roman", 55)
    intro_text_object = intro_font.render("Vinex' Game of Life", False, black)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        gameDisplay.blit(intro_text_object, (0 + ((display_width - (intro_text_object.get_rect()[2])) / 2), 100))
        button(display_width * 0.25, display_height * 0.75, 175, 75, (75, 75, 75), (100, 100, 100), "Times New Roman", 40, "Random", choose_randomly, main_loop)
        button(display_width * 0.5, display_height * 0.75, 175, 75, (75, 75, 75), (100, 100, 100), "Times New Roman", 40, "Draw", draw, None)
        button(display_width * 0.25, display_height * 0.9, 175, 75, (75, 75, 75), (100, 100, 100), "Times New Roman", 40, "Speed:", set_speed_intro, None)
        text("Times New Roman", str(speed), 40, (display_width * 0.5, display_height * 0.9), black)

        pygame.display.update()


def draw():
    eraser = False
    while True:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main_loop()
                if event.key == pygame.K_SPACE:
                    eraser = not eraser
        gameDisplay.fill(white)
        for x in range(30):
            for y in range(30):
                if state_array[x, y]:
                    pygame.draw.rect(gameDisplay, black, [x * 25, y * 25, cell_side, cell_side])
        text("Times New Roman", "Press Space to toggle the eraser", 15, (0, 0), green)
        text("Times New Roman", "Press Enter to continue", 15, (0, 15), green)
        if click[0] == 1 and not eraser:
            state_array[mouse[0] // 25, mouse[1] // 25] = True
        elif click[0] == 1 and eraser:
            state_array[mouse[0] // 25, mouse[1] // 25] = False

        pygame.display.update()


def main_loop():
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
        living_cells = str(count_cells())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    draw()
                elif event.key == pygame.K_r:
                    for x in range(30):
                        for y in range(30):
                            state_array[x, y] = False
                    intro()
                elif event.key == pygame.K_s:
                    set_speed_main()
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

        text("Times New Roman", "Press D to go back to drawing mode", 15, (0, 0), green)
        text("Times New Roman", "Press R to return to the main menu", 15, (0, 15), green)
        text("Times New Roman", "Press S to change the speed", 15, (0, 30), green)
        text("Times New Roman", "Living Cells: " + living_cells, 15, (650, 0), green)
        text("Times New Roman", "Speed: " + str(speed), 15, (650, 15), green)

        pygame.display.update()
        clock.tick(speed)


intro()
