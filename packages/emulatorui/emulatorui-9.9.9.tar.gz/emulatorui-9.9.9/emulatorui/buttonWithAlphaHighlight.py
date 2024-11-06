import importlib.resources

from sdl2 import SDL_Rect, SDL_SetTextureAlphaMod

from .textures import textures


class buttonWithAlphaHighlight:
    texture: object
    rect: SDL_Rect
    ren: object

    isHovered: bool
    hoverDir: bool
    _hoverCounter: int

    def __init__(self, ren, imagename : str, rect : SDL_Rect):
        self.ren = ren
        self.rect = rect
        with importlib.resources.files('emulatorui').joinpath(imagename) as f:
            self.texture = textures.loadTexture(self.ren, str(f))
        self.hoverDir = True
        self.isHovered = False
        self._hoverCounter = 0

    def onMouseMove(self, mousePos):
        if mousePos.x < self.rect.x or mousePos.x > self.rect.x + self.rect.w:
            self.isHovered = False
        elif mousePos.y < self.rect.y or mousePos.y > self.rect.y + self.rect.h:
            self.isHovered = False
        else:
            self.isHovered = True

    def timeTick(self):
        if self.isHovered:
            SDL_SetTextureAlphaMod(self.texture, self._hoverCounter)
        else:
            SDL_SetTextureAlphaMod(self.texture, 255)
            self._hoverCounter = 0

        if self.hoverDir:
            self._hoverCounter = self._hoverCounter + 10
        else:
            self._hoverCounter = self._hoverCounter - 10
        if self._hoverCounter > 200:
            self.hoverDir = False
        elif self._hoverCounter < 100:
            self.hoverDir = True

    def render(self):
        return self.texture, self.rect
