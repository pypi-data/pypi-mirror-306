import ctypes

from sdl2 import *
from sdl2.sdlttf import *


class text:
    def __init__(self, ren, font, caption : str, pos, size, colour):
        s = TTF_RenderText_Solid(font, caption.encode('utf-8'), colour)
        self.text = SDL_CreateTextureFromSurface(ren, s)

        textX = ctypes.c_long()
        textY = ctypes.c_long()
        SDL_QueryTexture(self.text, None, None, textX, textY)
        self.rect = SDL_Rect(pos[0], pos[1], size[0], size[1])

    def render(self):
        return self.text, self.rect
