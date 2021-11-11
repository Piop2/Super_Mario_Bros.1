import pygame
from pygame.surface import Surface
from .core_fuc import *


def load_font_img(path, target_color, color):
    bg_color = (147, 187, 236)
    font_img = pygame.image.load(path)
    font_img = swap_color(font_img, target_color, color)
    
    last_x = 0
    letters = []
    letter_spacing = []
    for x in range(font_img.get_width()):
        if font_img.get_at((x, 0))[0] == 255:
            letters.append(clip(font_img, last_x, 0, x - last_x, font_img.get_height()))
            letter_spacing.append(x - last_x)
            last_x = x + 1
    
    for letter in letters:
        letter.set_colorkey(bg_color)
    return letters, letter_spacing, font_img.get_height()

class Font:
    def __init__(self, path, target_color, color, font_order):
        self.letters, self.letter_spacing, self.line_height = load_font_img(path, target_color, color)
        self.font_order = font_order
        self.space_width = self.letter_spacing[0]
        self.base_spacing = 1
    
    def width(self, text):
        text_width = 0
        for char in text:
            if char == ' ':
                text_width += self.space_width + self.base_spacing
            elif char == '\n':
                pass
            else:
                text_width += self.letter_spacing[self.font_order.index(char)] + self.base_spacing
        return text_width
    
    def render(self, surf, text:str, pos):
        x_offset = 0
        y_offset = 0
        
        for char in text:
            if char not in ['\n', ' ']:
                surf.blit(self.letters[self.font_order.index(char)], (pos[0] + x_offset, pos[1] + y_offset))
                x_offset += self.letter_spacing[self.font_order.index(char)] + self.base_spacing
            elif char == ' ':
                x_offset += self.space_width + self.base_spacing
            else:
                y_offset += self.line_height
                x_offset = 0
