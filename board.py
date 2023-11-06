import pygame
from tile import Tile, BLACK, GREY

pygame.init()

class Board:
    def __init__(self, screen, board_size: int = 600, num_tiles: int = 3, board: list|None = None):
        self.board_size = board_size
        self.num_tiles = num_tiles
        self.tile_size = self.board_size // self.num_tiles
        self.selected_value = None
        self.screen = screen

        if board is None:
            self.board = [[[-1, -1] for _ in range(self.num_tiles)] for _ in range(self.num_tiles)]
        else:
            self.board = board

        self.tiles_list = self._generate_tiles()

    def _generate_tiles(self) -> list[Tile]:
        """ Creates a list of tiles for the board with the piece on the tiles according to self.board initialization """
        tiles_list = []
        for i in range(self.num_tiles):
            for j in range(self.num_tiles):
                new_tile = Tile(i, j, self.tile_size, self.screen)
                new_tile.value = self.board[i][j]
                """ if (val := self.board[i][j]) != -1:
                    new_tile.piece.value = val """
                tiles_list.append(new_tile)
        return tiles_list


    def draw(self, display) -> None:
        """ Draws the board with the tiles and the piece one the tiles """
        for tile in self.tiles_list:
            tile.draw(display)
    


    def get_tile_from_pos(self, x: int, y: int) -> Tile|None:
        """ Expects parameters: x/col, y/row 
            Returns the tile at position (row, col)"""
        for tile in self.tiles_list:
            if (tile.x_index, tile.y_index) == (x, y):
                return tile

    
    def handle_click(self, x: int, y: int, click_type) -> None:
        """ Highlights clicked tile, selects the piece on clicked tile if applicable, moves piece if applicable """
        x = x // self.tile_size
        y = y // self.tile_size
        clicked_tile = self.get_tile_from_pos(x, y)

        """
        1 - left click
        2 - middle click
        3 - right click
        4 - scroll up
        5 - scroll down
        """

        # TODO: think up a better way to assign values to the two sides of the tiles
        if self.selected_value is None and clicked_tile.value is not None:
            if click_type == 1:
                clicked_tile.value[0] = (clicked_tile.value[0] + 1) % 10
                self.board[y][x][0] = (self.board[y][x][0] + 1) % 10
            elif click_type == 2:
                if clicked_tile.draw_color == GREY:
                    clicked_tile.draw_color = (92, 75, 75) if (y + x)%2 else (220, 189, 194)
                else:
                    clicked_tile.draw_color = GREY
                clicked_tile.value = (-1, -1)
            elif click_type == 3:
                clicked_tile.value[1] = (clicked_tile.value[1] + 1) % 10
                self.board[y][x][1] = (self.board[y][x][1] + 1) % 10

        for tile in self.tiles_list:
            tile.highlight = False
        clicked_tile.highlight = False