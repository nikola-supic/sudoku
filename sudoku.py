"""
Created on Tue Feb 16 13:37:30 2021

@author: Sule
@name: sudoku.py
@description: ->
    DOCSTRING:
"""
#!/usr/bin/env python3

# Importing the libraries
from threading import Thread
import pygame
import sys
from customs import Text, Button, ImageButton, InputBox
import database
from datetime import datetime, timedelta

# Defining constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (74, 74, 74)
RED = (244, 0, 38)
GREEN = (74, 145, 35)
BLUE = (45, 77, 109)
YELLOW = (242, 209, 17)
ORANGE = (242, 118, 9)

ROWS = 9
COLS = 9

# Pygame initilaization
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
        self.changeable = True

    def draw(self):
        x, y = self.pos

        if self.value != 0:
            if self.changeable:
                Text(self.screen, str(self.value), (x + self.gap/2, y + self.gap/2), GREEN, center=True)
            else:
                Text(self.screen, str(self.value), (x + self.gap/2, y + self.gap/2), GREY, center=True)

        elif self.temp != '':
            Text(self.screen, str(self.temp), (x + 8, y + 8), GREY, text_size=14)

        if self.selected:
            pygame.draw.rect(self.screen, RED, (x, y, self.gap, self.gap), 3)

    def draw_change(self, green):
        x, y = self.pos

        pygame.draw.rect(self.screen, WHITE, (x, y, self.gap, self.gap), 0)
        Text(self.screen, str(self.value), (x + self.gap/2, y + self.gap/2), GREEN, center=True)

        if green:
            pygame.draw.rect(self.screen, GREEN, (x, y, self.gap, self.gap), 3)
        else:
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
    def __init__(self, screen, size, pos):
        super(Grid, self).__init__()
        self.screen = screen
        self.size = size
        self.pos = pos

        # Unpack values
        width, height = size
        x, y = pos
        gap = width / 9

        # Create grid
        self.grid = [[Cube(self.screen, 0, i, j, (x + i*gap, y + j*gap), gap) for j in range(COLS)] for i in range(ROWS)]

    def clear(self):
        for row in self.grid:
            for cube in row:
                cube.value = 0
                cube.changeable = True

    def is_finished(self):
        for row in self.grid:
            for cube in row:
                if cube.value == 0:
                    return False
        return True

    def find_empty(self):
        for i in range(ROWS):
            for j in range(COLS):
                if self.grid[i][j].value == 0:
                    return i, j
        return None

    def valid(self, number, pos):
        pos_x, pos_y = pos
        # Check row
        for i in range(len(self.grid)):
            if self.grid[i][pos_y].value == number and pos_x != i:
                return False

        # Check column
        for i in range(len(self.grid[0])):
            if self.grid[pos_x][i].value == number and pos_y != i:
                return False

        # Check box
        box_x = pos_y // 3
        box_y = pos_x // 3

        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x * 3, box_x*3 + 3):
                if self.grid[i][j].value == number and (i,j) != pos:
                    return False
        return True

    def solve(self):
        empty = self.find_empty()
        if not empty:
            return True
        else:
            row, col = empty

        for number in range(1, 10):
            if self.valid(number, (row, col)):
                self.grid[row][col].value = number

                if self.solve():
                    return True

                self.grid[row][col].value = 0
        return False

    def solve_gui_thread(self):
        solved = False
        while not solved:
            solved = self.solve_gui()
            pygame.time.delay(150)

    def solve_gui(self):
        empty = self.find_empty()
        if not empty:
            return True
        else:
            row, col = empty

        for number in range(1, 10):
            if self.valid(number, (row, col)):
                self.grid[row][col].value = number
                self.grid[row][col].draw_change(True)
                pygame.display.update()

                if self.solve_gui():
                    return True

                self.grid[row][col].value = 0
                self.grid[row][col].draw_change(False)
                pygame.display.update()

        return False        

    def use_number(self, selected_cube, number, finish_grid, mistakes):
        i, j = selected_cube
        cube = self.grid[i][j]
        cube.selected = False

        if cube.changeable:
            if finish_grid[i][j] == number:
                cube.value = number
                cube.temp = ''
            else:
                cube.temp = ''
                mistakes += 1
        return mistakes

    def draw(self):
        # Unpack values
        width, height = self.size
        x, y = self.pos
        gap = width / 9

        # Draw Grid Lines
        for i in range(ROWS + 1):
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

        start_grid, finish_grid = database.get_level_grid(game_id)
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

        grid = Grid(self.screen, (self.width-140, self.height-140), (70, 30))
        for i, row in enumerate(grid.grid):
            for j, col in enumerate(row):
                if start_grid[i][j] != 0:
                    cube = grid.grid[i][j]
                    cube.value = start_grid[i][j]
                    cube.changeable = False

        notes = Button(self.screen, 'N', (25, 29), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)
        hint = Button(self.screen, 'H', (25, 65), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)
        clear = Button(self.screen, 'C', (25, 101), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)
        reset = Button(self.screen, 'R', (25, 137), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)
        solve = Button(self.screen, 'S', (25, 173), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)
        info = Button(self.screen, '?', (25, 209), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)

        y = 29
        numbers = []
        for i in range(1, 10):
            btn = Button(self.screen, str(i), (self.width-52, y), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)
            numbers.append(btn)
            y += 36

        player = InputBox(self.screen, (25, self.height - 100), (140, 30), '', BLACK, GREY)
        exit = Button(self.screen, 'EXIT', (25, self.height - 60), (self.width-50, 30), WHITE, text_color=GREY, border=2, border_color=GREY)

        while run:
            mx, my = pygame.mouse.get_pos()
            pygame.display.set_caption('Sudoku (Game)')

            if mistakes >= 3:
                self.game_over()
                run = False

            if grid.is_finished() and not grid_solved:
                self.game_finished(game_id, player.text, time_started, datetime.now())
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

            if show_grid:
                info.border = 2
                info.border_color = GREEN
            else:
                info.border = 1
                info.border_color = GREY

            notes.draw()
            hint.draw()
            clear.draw()
            reset.draw()
            solve.draw()
            info.draw()

            for btn in numbers:
                btn.draw()

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
                            cube.changeable = False

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


    def game_finished(self, game_id, name, time_started, time_finished):
        click = False
        run = True

        duration = int((time_finished - time_started).total_seconds())
        creator, record, recorder = database.get_level(game_id)
        if duration < record:
            database.update_record(game_id, duration, name)

        pygame.display.set_caption('Sudoku (Game Finished)')
        self.screen.fill(BLACK)
        bg = pygame.image.load("images/background.jpg")
        bg = pygame.transform.scale(bg, (self.width, self.height))
        self.screen.blit(bg, (0, 0))

        Text(self.screen, 'GAME FINISHED', (self.width/2, 40), GREY, text_size=72, center=True)

        if duration < record:
            Text(self.screen, 'New record!', (self.width/2, 80), GREY, text_size=48, center=True)
            Text(self.screen, f'Record: {timedelta(seconds=duration)}', (self.width/2, 110), GREY, text_size=24, center=True)
            Text(self.screen, f'Recorder: {name}', (self.width/2, 130), GREY, text_size=24, center=True)
        else:
            Text(self.screen, f'Your time: {timedelta(seconds=duration)}', (self.width/2, 70), GREY, text_size=24, center=True)
            Text(self.screen, f'Name: {name}', (self.width/2, 90), GREY, text_size=24, center=True)
            Text(self.screen, f'Record: {timedelta(seconds=record)}', (self.width/2, 110), GREY, text_size=24, center=True)
            Text(self.screen, f'Recorder: {recorder}', (self.width/2, 130), GREY, text_size=24, center=True)

        Text(self.screen, f'Level created by: {creator}', (self.width/2, 150), GREY, text_size=24, center=True)
        exit = Button(self.screen, 'EXIT', (25, self.height - 60), (self.width-50, 30), WHITE, text_color=GREY, border=2, border_color=GREY)
        exit.draw()

        while run:
            mx, my = pygame.mouse.get_pos()

            if click:
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
        solve_with_gui = False

        grid = Grid(self.screen, (self.width-140, self.height-140), (70, 30))
        
        start_pos = Button(self.screen, 'S', (25, 29), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)
        finish_pos = Button(self.screen, 'F', (25, 65), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)
        delete = Button(self.screen, 'D', (25, 101), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)
        clear = Button(self.screen, 'C', (25, 137), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)
        gui = Button(self.screen, 'G', (25, 173), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)
        info = Button(self.screen, '?', (25, 209), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)

        y = 29
        numbers = []
        for i in range(1, 10):
            btn = Button(self.screen, str(i), (self.width-52, y), (25, 25), WHITE, text_color=GREY, border=1, border_color=GREY)
            numbers.append(btn)
            y += 36

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
            Text(self.screen, 'LEVEL CREATOR SCREEN', (self.width/2, 15), GREY, text_size=22, center=True)

            if solve_with_gui:
                gui.border = 2
                gui.border_color = GREEN
            else:
                gui.border = 1
                gui.border_color = GREY

            if start_pos_grid:
                start_pos.border = 2
                start_pos.border_color = GREEN
            else:
                start_pos.border = 1
                start_pos.border_color = GREY

            if finish_pos_grid:
                finish_pos.border = 2
                finish_pos.border_color = GREEN
            else:
                finish_pos.border = 1
                finish_pos.border_color = GREY

            if not show_grid:
                info.border = 2
                info.border_color = GREEN
            else:
                info.border = 1
                info.border_color = GREY

            start_pos.draw()
            finish_pos.draw()
            delete.draw()
            clear.draw()
            gui.draw()
            info.draw()

            for btn in numbers:
                btn.draw()

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
                Text(self.screen, 'Starting grid', (60, 41), GREY, text_size=22)
                Text(self.screen, 'Create finishing grid', (60, 77), GREY, text_size=22)
                Text(self.screen, 'Delete selected', (60, 113), GREY, text_size=22)
                Text(self.screen, 'Clear grid', (60, 149), GREY, text_size=22)
                Text(self.screen, 'Solve with visualization', (60, 185), GREY, text_size=22)
                Text(self.screen, 'Hide / show more information', (60, 221), GREY, text_size=22)

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

                if finish_pos.rect.collidepoint((mx, my)):
                    finish_pos_grid = []
                    selected_cube = (-1, -1)
                    cant_save = False

                    for i, row in enumerate(grid.grid):
                        start_pos_grid.append([])
                        for j, cube in enumerate(row):
                            if cube.value != 0:
                                cube.changeable = False

                    if solve_with_gui:
                        thread = Thread(target = grid.solve_gui_thread)
                        thread.daemon = True
                        thread.start()
                    else:
                        grid.solve()

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

                if delete.rect.collidepoint((mx, my)):
                    if selected_cube[0] != -1:
                        grid.grid[selected_cube[0]][selected_cube[1]].value = 0
                    selected_cube = (-1, -1)

                if clear.rect.collidepoint((mx, my)): 
                    finish_pos_grid = []
                    start_pos_grid = []
                    selected_cube = (-1, -1)
                    grid.clear()

                if gui.rect.collidepoint((mx, my)):
                    if solve_with_gui:
                        solve_with_gui = False
                    else:
                        solve_with_gui = True

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
                            finish_pos_grid = []
                            start_pos_grid = []
                            grid.clear()
                            creator.clear()
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
                    match event.key:
                        case pygame.K_1:
                            number = 1
                        case pygame.K_2:
                            number = 2
                        case pygame.K_3:
                            number = 3
                        case pygame.K_4:
                            number = 4
                        case pygame.K_5:
                            number = 5
                        case pygame.K_6:
                            number = 6
                        case pygame.K_7:
                            number = 7
                        case pygame.K_8:
                            number = 8
                        case pygame.K_9:
                            number = 9
                        case pygame.K_0, _:
                            number = 0

                    if selected_cube[0] != -1 and number != 0:
                        i, j = selected_cube
                        cube = grid.grid[i][j]
                        cube.value = number
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
