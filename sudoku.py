"""
Created on Tue Feb 16 13:37:30 2021

@author: Sule
@name: sudoku.py
@description: ->
    DOCSTRING:
"""
#!/usr/bin/env python3


import pygame
import sys
from customs import Text, Button, ImageButton, InputBox
import database
from datetime import datetime, timedelta

"""
class Grid():
    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, value):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(value)
            self.update_model()

            if valid(self.model, value, (row, col)) and self.solve():
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, value):
        row, col = self.selected
        self.cubes[row][col].set_temp(value)

    def draw(self):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.win, (0,0,0), (i*gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        :param: pos
        :return: (row, col)
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def solve(self):
        empty = find_empty(self.model)
        if not empty:
            return True
        else:
            row, col = empty

        for number in range(1, 10):
            if valid(self.model, number, (row, col)):
                self.model[row][col] = number

                if self.solve():
                    return True

                self.model[row][col] = 0

        return False

    def solve_gui(self):
        self.update_model()
        empty = find_empty(self.model)
        if not empty:
            return True
        else:
            row, col = empty

        for number in range(1, 10):
            if valid(self.model, number, (row, col)):
                self.model[row][col] = number
                self.cubes[row][col].set(number)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(50)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(50)

        return False




def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col

    return None


def valid(board, number, pos):
    # Check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == number and pos[1] != i:
            return False

    # Check column
    for i in range(len(board)):
        if board[i][pos[1]] == number and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if board[i][j] == number and (i,j) != pos:
                return False

    return True


def redraw_window(win, board, time, strikes):
    win.fill((255,255,255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (540 - 160, 560))
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    # Draw grid and board
    board.draw()

def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540, win)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:
        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

                if event.key == pygame.K_SPACE:
                    board.solve_gui()

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()

"""

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (74, 74, 74)
RED = (244, 0, 38)
GREEN = (74, 145, 35)
BLUE = (45, 77, 109)
YELLOW = (242, 209, 17)
ORANGE = (242, 118, 9)

pygame.font.init()
pygame.init()
clock = pygame.time.Clock()

class Cube():
    def __init__(self, screen, value, row, col, pos, gap):
        self.screen = screen
        self.value = value
        self.temp = ''
        self.row = row
        self.col = col
        self.pos = pos
        self.gap = gap
        self.selected = False

    def draw(self):
        x, y = self.pos

        if self.value != 0:
            Text(self.screen, str(self.value), (x + self.gap/2, y + self.gap/2), GREY, center=True)
        elif self.temp != '':
            Text(self.screen, str(self.temp), (x + 8, y + 8), GREY, text_size=14)

        if self.selected:
            pygame.draw.rect(self.screen, RED, (x, y, self.gap, self.gap), 3)

    def add_temp(self, value):
        self.temp += str(value)
        self.draw()

    def click(self, click_pos):
        x1, y1 = click_pos
        x, y = self.pos
        if x <= x1 <= x + self.gap and y <= y1 <= y + self.gap:
            return True
        return False

    def __repr__(self):
        return f'{self.row},{self.col}'

    def __str__(self):
        return f'{self.row},{self.col}'

class Grid():
    """
    DOCSTRING:

    """
    def __init__(self, screen, size, pos, grid_size=(9,9)):
        super(Grid, self).__init__()
        self.screen = screen
        self.size = size
        self.pos = pos
        self.grid_size = grid_size

        # Unpack values
        width, height = size
        x, y = pos
        rows, cols = grid_size
        gap = width / 9

        # Create grid
        self.grid = []
        for i in range(rows):
            self.grid.append([])
            for j in range(cols):
                cube_x = x + i*gap
                cube_y = y + j*gap
                cube = Cube(self.screen, 0, i, j, (cube_x, cube_y), gap)
                self.grid[i].append(cube)

    def clear(self):
        for row in self.grid:
            for cube in row:
                cube.value = 0

    def draw(self):
        # Unpack values
        width, height = self.size
        x, y = self.pos
        rows, cols = self.grid_size
        gap = width / 9

        # Draw Grid Lines
        for i in range(rows + 1):
            if i == 0 or i == 3 or i == 6 or i == 9:
                thick = 3
            else:
                thick = 1

            pygame.draw.line(self.screen, GREY, (x, y + i*gap), (x+width, y + i*gap), thick)
            pygame.draw.line(self.screen, GREY, (x + i*gap, y), (x + i * gap, y+height), thick)

        # Draw values for cubes
        for row in self.grid:
            for cube in row:
                cube.draw()

    def use_number(self, selected_cube, number, finish_grid, mistakes):
        i, j = selected_cube
        cube = self.grid[i][j]
        cube.selected = False

        if finish_grid[i][j] == number:
            cube.value = number
            cube.temp = ''
        else:
            cube.temp = ''
            mistakes += 1
        return mistakes

class App():
    """
    DOCSTRING:

    """
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.screen = pygame.display.set_mode((width, height))
        icon = pygame.image.load("images/logo.png")
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Sudoku')

    def main_menu(self):
        click = False
        
        play = Button(self.screen, 'PLAY', (self.width/2 - 130, 100), (260, 30), WHITE, text_color=GREY, border=2, border_color=GREY)
        new_level = Button(self.screen, 'NEW LEVEL', (self.width/2 - 130, 140), (260, 30), WHITE, text_color=GREY, border=2, border_color=GREY)
        custom_level = Button(self.screen, 'PLAY CUSTOM', (self.width/2 - 130, 180), (140, 30), WHITE, text_color=GREY, border=2, border_color=GREY)
        custom_id = InputBox(self.screen, (self.width/2 + 20, 180), (110, 29), '', BLACK, GREY)
        exit = Button(self.screen, 'EXIT', (self.width/2 - 130, self.height-60), (260, 30), WHITE, text_color=GREY, border=2, border_color=GREY)
        while True:
            mx, my = pygame.mouse.get_pos()
            pygame.display.set_caption('Sudoku (Main Menu)')

            self.screen.fill(BLACK)
            bg = pygame.image.load("images/background.jpg")
            bg = pygame.transform.scale(bg, (self.width, self.height))
            self.screen.blit(bg, (0, 0))

            Text(self.screen, 'SUDOKU', (self.width/2, 40), GREY, text_size=64, center=True)

            play.draw()
            new_level.draw()
            custom_level.draw()
            custom_id.draw()
            exit.draw()

            if click:
                if play.rect.collidepoint((mx, my)):
                    self.game_screen()
                if new_level.rect.collidepoint((mx, my)):
                    self.add_level()
                if custom_level.rect.collidepoint((mx, my)):
                    if custom_id.text != '':
                        try:
                            game_id = int(custom_id.text)
                            self.game_screen(game_id)
                        except ValueError:
                            Text(self.screen, 'You did not enter ID from database.', (self.width / 2, self.height - 15), GREY, center=True)
                            pygame.display.update()
                            pygame.time.delay(1500)
                    else:
                        Text(self.screen, 'You did not enter ID from database.', (self.width / 2, self.height - 15), GREY, center=True)
                        pygame.display.update()
                        pygame.time.delay(1500)

                if exit.rect.collidepoint((mx, my)):
                    pygame.quit()
                    sys.exit()

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        click = True

                custom_id.handle_event(event)
            custom_id.update()

            pygame.display.update()
            clock.tick(60)

    def game_screen(self, game_id = 0):

        if game_id == 0:
            game_id = database.get_random()

        start_grid, finish_grid = database.get_level(game_id)
        if not start_grid: 
            return False

        run = True
        click = False

        show_grid = False
        selected_cube = (-1, -1)
        time_started = datetime.now()
        mistakes = 0
        notes_on = False
        grid_solved = False

        grid = Grid(self.screen, (self.width-140, self.height-140), (70, 30), (9,9))
        for i, row in enumerate(grid.grid):
            for j, col in enumerate(row):
                cube = grid.grid[i][j]
                cube.value = start_grid[i][j]

        notes = Button(self.screen, 'N', (25, 29), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)

        hint = Button(self.screen, 'H', (25, 65), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)
        clear = Button(self.screen, 'C', (25, 101), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)
        reset = Button(self.screen, 'R', (25, 137), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)
        solve = Button(self.screen, 'S', (25, 173), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)
        info = Button(self.screen, '?', (25, 209), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)

        player = InputBox(self.screen, (25, self.height - 100), (140, 30), '', BLACK, GREY)
        exit = Button(self.screen, 'EXIT', (25, self.height - 60), (self.width-50, 30), WHITE, text_color=GREY, border=2, border_color=GREY)

        while run:
            mx, my = pygame.mouse.get_pos()
            pygame.display.set_caption('Sudoku (Game)')

            if mistakes >= 3:
                self.game_over()
                run = False

            self.screen.fill(BLACK)
            bg = pygame.image.load("images/background.jpg")
            bg = pygame.transform.scale(bg, (self.width, self.height))
            self.screen.blit(bg, (0, 0))
            Text(self.screen, f'SUDOKU GAME (ID: {game_id})', (self.width/2, 15), GREY, text_size=22, center=True)

            if notes_on:
                notes.border = 2
                notes.border_color = GREEN
            else:
                notes.border = 1
                notes.border_color = GREY

            if grid_solved:
                solve.border = 2
                solve.border_color = GREEN
            else:
                solve.border = 1
                solve.border_color = GREY

            notes.draw()
            hint.draw()
            clear.draw()
            reset.draw()
            solve.draw()
            info.draw()

            y = 29
            numbers = []
            for i in range(1, 10):
                btn = Button(self.screen, str(i), (self.width-52, y), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)
                btn.draw()
                numbers.append(btn)
                y += 36

            if show_grid:
                grid.draw()

                if click:
                    if selected_cube[0] != -1:
                        for num, btn in enumerate(numbers):
                            if btn.rect.collidepoint((mx, my)):
                                if not notes_on:
                                    mistakes = grid.use_number(selected_cube, num+1, finish_grid, mistakes)
                                else:
                                    i, j = selected_cube
                                    cube = grid.grid[i][j]
                                    cube.add_temp(num+1)
                                
                                selected_cube = (-1, -1)

                    for i, row in enumerate(grid.grid):
                        for j, cube in enumerate(row):
                            cube.selected = False
                            if cube.click((mx, my)):
                                cube.selected = True
                                selected_cube = (i, j)
            else:
                Text(self.screen, 'Toggle taking notes', (60, 41), GREY, text_size=22)
                Text(self.screen, 'Take a hint', (60, 77), GREY, text_size=22)
                Text(self.screen, 'Clear selected cube', (60, 113), GREY, text_size=22)
                Text(self.screen, 'Reset grid', (60, 149), GREY, text_size=22)
                Text(self.screen, 'Solve grid', (60, 185), GREY, text_size=22)
                Text(self.screen, 'Hide / show more information', (60, 221), GREY, text_size=22)

            duration = int((datetime.now() - time_started).total_seconds())
            Text(self.screen, f'{timedelta(seconds=duration)}', (self.width-27, self.height-85), GREY, text_size=22, right=True)
            Text(self.screen, f'Mistakes: {mistakes} / 3', (185, self.height-85), GREY, text_size=22)
            player.draw()
            exit.draw()

            if click:
                if notes.rect.collidepoint((mx, my)):
                    if notes_on:
                        notes_on = False
                    else:
                        notes_on = True

                if hint.rect.collidepoint((mx, my)):
                    if selected_cube[0] != -1:
                        i, j = selected_cube
                        grid.grid[i][j].value = finish_grid[i][j]
                        selected_cube = (-1, -1)

                if clear.rect.collidepoint((mx, my)):
                    if selected_cube[0] != -1:
                        i, j = selected_cube
                        grid.grid[i][j].value = 0
                        grid.grid[i][j].temp = ''
                        selected_cube = (-1, -1)

                if reset.rect.collidepoint((mx, my)):
                    selected_cube = (-1, -1)
                    grid.clear()

                    for i, row in enumerate(grid.grid):
                        for j, col in enumerate(row):
                            grid.grid[i][j].value = start_grid[i][j]

                    time_started = datetime.now()
                    mistakes = 0
                    grid_solved = False

                if solve.rect.collidepoint((mx, my)):
                    for i, row in enumerate(grid.grid):
                        for j, col in enumerate(row):
                            grid.grid[i][j].value = finish_grid[i][j]

                    grid_solved = True

                if info.rect.collidepoint((mx, my)):
                    if show_grid:
                        show_grid = False
                    else:
                        show_grid = True

                if exit.rect.collidepoint((mx, my)):
                    run = False


            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

                    number = 0
                    if event.key == pygame.K_1:
                        number = 1
                    if event.key == pygame.K_2:
                        number = 2
                    if event.key == pygame.K_3:
                        number = 3
                    if event.key == pygame.K_4:
                        number = 4
                    if event.key == pygame.K_5:
                        number = 5
                    if event.key == pygame.K_6:
                        number = 6
                    if event.key == pygame.K_7:
                        number = 7
                    if event.key == pygame.K_8:
                        number = 8
                    if event.key == pygame.K_9:
                        number = 9
                    if event.key == pygame.K_0:
                        number = 0

                    if selected_cube[0] != -1 and number != 0:
                        if not notes_on:
                            mistakes = grid.use_number(selected_cube, number, finish_grid, mistakes)
                        else:
                            i, j = selected_cube
                            cube = grid.grid[i][j]
                            cube.add_temp(number)
                        
                        selected_cube = (-1, -1)

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        click = True

                player.handle_event(event)
            player.update()

            pygame.display.update()
            clock.tick(60)


    def game_over(self):
        click = False
        run = True
        while run:
            mx, my = pygame.mouse.get_pos()
            pygame.display.set_caption('Sudoku (Game Over)')

            self.screen.fill(BLACK)
            bg = pygame.image.load("images/background.jpg")
            bg = pygame.transform.scale(bg, (self.width, self.height))
            self.screen.blit(bg, (0, 0))

            Text(self.screen, 'GAME OVER', (self.width/2, 40), GREY, text_size=64, center=True)

            if click:
                pass

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        click = True

            pygame.display.update()
            clock.tick(60)


    def add_level(self):
        run = True
        click = False

        show_grid = True
        selected_cube = (-1, -1)
        start_pos_grid = []
        finish_pos_grid = []

        grid = Grid(self.screen, (self.width-140, self.height-140), (70, 30), (9,9))
        
        start_pos = Button(self.screen, 'S', (25, 30), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)
        finish_pos = Button(self.screen, 'F', (25, 65), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)
        delete = Button(self.screen, 'D', (25, 100), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)
        clear = Button(self.screen, 'C', (25, 135), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)
        info = Button(self.screen, '?', (25, 170), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)

        creator = InputBox(self.screen, (70, self.height - 100), (140, 30), '', BLACK, GREY)
        save = Button(self.screen, 'SAVE', (240, self.height - 100), (140, 30), WHITE, text_color=GREY, border=2, border_color=GREY)
        exit = Button(self.screen, 'EXIT', (70, self.height - 60), (self.width-140, 30), WHITE, text_color=GREY, border=2, border_color=GREY)

        while run:
            mx, my = pygame.mouse.get_pos()
            pygame.display.set_caption('Sudoku (Create Level)')

            self.screen.fill(BLACK)
            bg = pygame.image.load("images/background.jpg")
            bg = pygame.transform.scale(bg, (self.width, self.height))
            self.screen.blit(bg, (0, 0))
            Text(self.screen, 'LEVEL CREATOR', (self.width/2, 15), GREY, text_size=22, center=True)

            start_pos.draw()
            finish_pos.draw()
            delete.draw()
            clear.draw()
            info.draw()

            y = 29
            numbers = []
            for i in range(1, 10):
                btn = Button(self.screen, str(i), (self.width-50, y), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)
                btn.draw()
                numbers.append(btn)
                y += 36

            if show_grid:
                grid.draw()

                if click:
                    if selected_cube[0] != -1:
                        for num, btn in enumerate(numbers):
                            if btn.rect.collidepoint((mx, my)):
                                i, j = selected_cube
                                cube = grid.grid[i][j]
                                cube.value = num + 1
                                cube.selected = False
                                selected_cube = (-1, -1)
                                
                    for i, row in enumerate(grid.grid):
                        for j, cube in enumerate(row):
                            cube.selected = False
                            if cube.click((mx, my)):
                                cube.selected = True
                                selected_cube = (i, j)

            else:
                Text(self.screen, 'Starting grid', (60, 42), GREY, text_size=22)
                Text(self.screen, 'Finishing grid', (60, 77), GREY, text_size=22)
                Text(self.screen, 'Delete selected', (60, 112), GREY, text_size=22)
                Text(self.screen, 'Clear grid', (60, 147), GREY, text_size=22)
                Text(self.screen, 'Hide / show more information', (60, 182), GREY, text_size=22)

            creator.draw()
            save.draw()
            exit.draw()

            if click:
                if start_pos.rect.collidepoint((mx, my)):
                    start_pos_grid = []
                    selected_cube = (-1, -1)
                    for i, row in enumerate(grid.grid):
                        start_pos_grid.append([])
                        for j, cube in enumerate(row):
                            start_pos_grid[i].append(cube.value)
                    print(start_pos_grid)

                if finish_pos.rect.collidepoint((mx, my)):
                    finish_pos_grid = []
                    selected_cube = (-1, -1)
                    cant_save = False
                    for i, row in enumerate(grid.grid):
                        finish_pos_grid.append([])
                        for j, cube in enumerate(row):

                            if cube.value == 0:
                                cant_save = True
                            else:
                                finish_pos_grid[i].append(cube.value)

                    if cant_save:
                        finish_pos_grid = []
                        Text(self.screen, 'Finishing grid can not have zeros.', (self.width / 2, self.height - 15), GREY, center=True)
                        pygame.display.update()
                        pygame.time.delay(1500)
                    else:
                        print(finish_pos_grid)

                if delete.rect.collidepoint((mx, my)):
                    if selected_cube[0] != -1:
                        grid.grid[selected_cube[0]][selected_cube[1]].value = 0
                    selected_cube = (-1, -1)

                if clear.rect.collidepoint((mx, my)): 
                    selected_cube = (-1, -1)
                    grid.clear()

                if info.rect.collidepoint((mx, my)):
                    if show_grid:
                        show_grid = False
                    else:
                        show_grid = True
       
                if save.rect.collidepoint((mx, my)):
                    if not start_pos_grid:
                        Text(self.screen, 'You did not save start grid.', (self.width / 2, self.height - 15), GREY, center=True)
                        pygame.display.update()
                        pygame.time.delay(1500)

                    elif not finish_pos_grid:
                        Text(self.screen, 'You did not save finish grid.', (self.width / 2, self.height - 15), GREY, center=True)
                        pygame.display.update()
                        pygame.time.delay(1500)

                    elif creator == '':
                        Text(self.screen, 'You did not enter creator name.', (self.width / 2, self.height - 15), GREY, center=True)
                        pygame.display.update()
                        pygame.time.delay(1500)

                    else:
                        if database.new_grid(creator.text, start_pos_grid, finish_pos_grid):
                            grid.clear()
                        else:
                            Text(self.screen, 'Can not save new level in database.', (self.width / 2, self.height - 15), GREY, center=True)
                            pygame.display.update()
                            pygame.time.delay(1500)


                if exit.rect.collidepoint((mx, my)):
                    run = False


            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

                    number = 0
                    if event.key == pygame.K_1:
                        number = 1
                    if event.key == pygame.K_2:
                        number = 2
                    if event.key == pygame.K_3:
                        number = 3
                    if event.key == pygame.K_4:
                        number = 4
                    if event.key == pygame.K_5:
                        number = 5
                    if event.key == pygame.K_6:
                        number = 6
                    if event.key == pygame.K_7:
                        number = 7
                    if event.key == pygame.K_8:
                        number = 8
                    if event.key == pygame.K_9:
                        number = 9
                    if event.key == pygame.K_0:
                        number = 0

                    if selected_cube[0] != -1 and number != 0:
                        i, j = selected_cube
                        cube = grid.grid[i][j]
                        cube.value = key
                        cube.selected = False
                        selected_cube = (-1, -1)

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        click = True

                creator.handle_event(event)
            creator.update()

            pygame.display.update()
            clock.tick(60)

if __name__ == '__main__':
    app = App(450, 450)
    app.main_menu() 
