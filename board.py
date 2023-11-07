import pygame
from tile import Tile, BLACK, GREY, LIGHT, DARK

pygame.init()

class Board:
    def __init__(self, screen, board_size: int = 600, num_tiles: int = 3, board: list|None = None):
        self.board_size = board_size
        self.num_tiles = num_tiles
        self.tile_size = self.board_size // self.num_tiles
        self.selected_side = None
        self.selected_tile = None
        self.screen = screen

        self.mode = 'outline' # 'outline 'or 'value'

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
        self.selected_tile = self.get_tile_from_pos(x, y)

        """
        1 - left click
        2 - middle click
        3 - right click
        4 - scroll up
        5 - scroll down
        """

        if self.mode == 'outline':
            if self.selected_tile is not None:
                self.selected_tile.draw_color = LIGHT if self.selected_tile.draw_color == DARK else DARK
                self.selected_tile = None

        if self.mode == 'value':
            if self.selected_side is None:
                if click_type == 1:
                    self.selected_side = 'left'
                elif click_type == 3:
                    self.selected_side = 'right'

    def assign_value(self, value:int):
        if self.selected_tile is None:
            return
        if self.selected_side == 'left':
            self.selected_tile.value[0] = value
        else:
            self.selected_tile.value[1] = value
        self.selected_tile = None
        self.selected_side = None