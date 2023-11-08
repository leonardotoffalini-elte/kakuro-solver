import pygame
from board import Board


def kakuro_to_ampl(board: list[list[list[int]]]):
    # helper dictionary to conert indeces to strings
    index_to_string = {0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine'}

    # creating the output file
    with open('output.txt', 'w') as f:
        f.write(f'# Note: There is a -1st row and column, and a {len(board)}th row and column.\n')
        f.write('# These rows and collumns function as 0 paddings so that the indices will not be out of bounds\n\n')
        f.write(f'set I = -1 .. {len(board)};\n\n')
        f.write('set N = 1 .. 9;\n\n')
        # creates sets for each length
        for i in range(1, len(board)):
            f.write(f'set {index_to_string[i]}_long_interval = 1 .. {i};\n')
        f.write('set R = -1 .. 1;\n\n')
        f.write('var X {I, I, N}, binary;\n\n')
        f.write('# paddings must be zeros\n')
        f.write(f's.t. firstRow: sum {{n in N}}sum {{i in I}} X[-1, i, n] = 0;\n')
        f.write(f's.t. lastRow: sum {{n in N}}sum {{i in I}} X[{len(board)}, i, n] = 0;\n')
        f.write(f's.t. firstCol: sum {{n in N}}sum {{i in I}} X[i, -1, n] = 0;\n')
        f.write(f's.t. lastCol: sum {{n in N}}sum {{i in I}} X[i, {len(board)}, n] = 0;\n\n')
        f.write('# each row and column most have only one of each number at most\n')
        f.write(f's.t. row_unique {{i in I, n in N}}: sum {{j in I}} X[i, j, n] <= 1;\n')
        f.write(f's.t. col_unique {{j in I, n in N}}: sum {{i in I}} X[i, j, n] <= 1;\n')
        f.write('\n# actual conditions for the game\n')
        f.write('# (the first part of the statement reflects the row, the second part of the statement reflects the column)\n')
        
        for i in range(len(board)):
            for j in range(len(board[0])):
                # sum of the tiles vertically down equals the number in the tile
                if (num := board[i][j][0]) > 0:
                    name = index_to_string[i] + '_' + index_to_string[j]
                    # check how far until the next wall or edge of the board
                    walker = i+1
                    while walker < len(board):
                        if board[walker][j][0] > -1 or board[walker][j][1] > -1:
                            break
                        walker += 1
                    f.write(f's.t. {name}_down: sum {{n in N}} sum {{i in {index_to_string[walker-1]}_long_interval}} X[{i}+i, {j}, n] = {num};\n')

                # sum of the tiles horizontally to the right equals the number in the tile
                if (num := board[i][j][1]) > 0:
                    name = index_to_string[i] + '_' + index_to_string[j]
                    # check how far until the nexxt wall or edge of the board
                    walker = j+1
                    while walker < len(board[0]):
                        if board[i][walker][0] > -1 or board[i][walker][1] > -1:
                            break
                        walker += 1
                    f.write(f's.t. {name}_right: sum {{n in N}} sum {{j in {index_to_string[walker-1]}_long_interval}} X[{i}, {j}+j, n] = {num};\n')


def main():
    num_tiles = int(input('Enter the number of tiles (for example, 5): '))
    screen = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
    board_size = screen.get_width()
    board = Board(screen, board_size=board_size, num_tiles=num_tiles)

    running = True

    while running:
        for event in pygame.event.get():
            # quit the game
            if event.type == pygame.QUIT:
                running = False

            # change color of tile when clicked in outline mode, select a tile and side in value mode
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.handle_click(event.pos[0], event.pos[1], event.button)
            
            # change the mode by pressing Shift and Enter at the same time
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LSHIFT] and keys[pygame.K_RETURN]:
                board.mode = 'outline' if board.mode == 'value' else 'value'

            # takes input and assigns value to the selected side of the selected tile
            if board.selected_tile is not None and board.mode == 'value':
                # board.highlight_triangle()
                number_input = int(input('Enter a numerical value for the selected tile: '))
                board.assign_value(number_input)

            # resize the screen
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.w), pygame.RESIZABLE)
                board.board_size = screen.get_width()
                board.tile_size = board.board_size // board.num_tiles
                board.tiles_list = board._generate_tiles()
        
        board.draw(screen)
        pygame.display.update()

    kakuro_to_ampl(board.board)
    pygame.quit()

if __name__ == '__main__':
    main()