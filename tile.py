import pygame

pygame.init() 
BLACK = (0, 0, 0)
LIGHT = (220, 189, 194)
DARK = (31, 12, 8)
WHITE = (255, 255, 255)
GREY = (40, 40, 40)

class Tile:
    def __init__(self, row:int, col:int, tile_size:int, screen):
        self.tile_size = tile_size
        self.font = pygame.font.Font('freesansbold.ttf', self.tile_size // 2)
        self.x_abs = col * self.tile_size # absolute x position
        self.y_abs = row * self.tile_size # absolute y position

        self.screen = screen

        self.x_index = col # column index
        self.y_index = row # row index

        self.color = 'light'
        self.draw_color = LIGHT if self.color == 'light' else DARK
        self.highlight_color = (100, 249, 83) if self.color == 'light' else (0, 200, 10)
        self.highlight = False

        self.value = [-1, -1]

        self.rect = pygame.Rect(
            self.x_abs,
            self.y_abs,
            self.tile_size,
            self.tile_size
        )

    def __repr__(self):
        return f'Tile at position {self.x_abs, self.y_abs}'

    def draw(self, display):
        """ Draws a rectangle for each tile and renders the image of a piece on top of the tile if applicable """
        if self.highlight:
            pygame.draw.rect(display, self.highlight_color, self.rect)
        else:
            pygame.draw.rect(display, self.draw_color, self.rect)

        if self.value[0] != -1 or self.value[1] != -1:
            if self.value[0] != -1:
                number = self.font.render(str(self.value[0]), True, LIGHT)
                number_rect = number.get_rect(center=(self.rect.centerx - self.rect.height//4, self.rect.centery + self.rect.width//4))
                self.screen.blit(number, number_rect)
            if self.value[1] != -1:
                number = self.font.render(str(self.value[1]), True, LIGHT)
                number_rect = number.get_rect(center=(self.rect.centerx + self.rect.height//4, self.rect.centery - self.rect.width//4))
                self.screen.blit(number, number_rect)
            line = pygame.draw.line(self.screen, LIGHT, (self.rect.left, self.rect.top), (self.rect.right, self.rect.bottom), 2)