import pygame
from board import Board


def mosaic_to_ampl(board: list[list[int]]):
    # helper dictionary to conert indeces to strings
    index_to_string = {0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine'}

    # creating the output file
    with open('output.txt', 'w') as f:
        f.write('# Note: There is a -1st row and column, and a 5th row and column.\n')
        f.write('# These rows and collumns function as 0 paddings so that the indices will not be out of bounds\n\n')
        f.write(f'set I = -1 .. {len(board)};\n\n')
        f.write('set R = -1 .. 1;\n\n')
        f.write('var X {I, I}, binary;\n\n')
        f.write('# paddings must be zeros\n')
        f.write('s.t. firstRow: sum {i in I} X[-1, i] = 0;\n')
        f.write(f's.t. lastRow: sum {{i in I}} X[{len(board)}, i] = 0;\n')
        f.write('s.t. firstCol: sum {i in I} X[i, -1] = 0;\n')
        f.write(f's.t. lastCol: sum {{i in I}} X[i, {len(board)}] = 0;\n\n')
        f.write('# actual conditions for the game\n')
        f.write('# (the first part of the statement reflects the row, the second part of the statement reflects the column)\n')
        for i in range(len(board)):
            for j in range(len(board[0])):
                if (num := board[i][j]) != -1:
                    name = index_to_string[i] + '_' + index_to_string[j]
                    f.write(f's.t. {name}: sum {{i in R}} sum {{j in R}} X[{i}+i, {j}+j] = {num};\n')


def main():
    num_tiles = int(input('Enter the number of tiles (for example, 5): '))
    screen = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
    board_size = screen.get_width()
    board = Board(screen, board_size=board_size, num_tiles=num_tiles)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.handle_click(event.pos[0], event.pos[1], event.button)
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.w), pygame.RESIZABLE)
                board.board_size = screen.get_width()
                board.tile_size = board.board_size // board.num_tiles
                board.tiles_list = board._generate_tiles()
        
        board.draw(screen)
        pygame.display.update()

    mosaic_to_ampl(board.board)
    pygame.quit()

if __name__ == '__main__':
    main()