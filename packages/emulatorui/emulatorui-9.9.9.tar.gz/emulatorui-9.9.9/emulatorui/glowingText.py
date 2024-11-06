import ctypes

from sdl2 import SDL_CreateTextureFromSurface, SDL_QueryTexture, SDL_Color, SDL_Rect
from sdl2.sdlttf import TTF_RenderText_Solid

from .textures import textures


class glowingText:
    def __init__(self, ren, caption, centerX, centerY):
        self.ren = ren
        self.caption = caption
        self.font = textures.getDefaultFont(48)
        self.glowingTextCounter = 0
        self.glowingTextDir = False
        self.centerX = centerX
        self.centerY = centerY

    def render(self):
        s = TTF_RenderText_Solid(self.font, self.caption.encode("utf-8"), SDL_Color(self.glowingTextCounter, self.glowingTextCounter, self.glowingTextCounter, 0))
        # FIXME: does this leak textures?
        textTexture = SDL_CreateTextureFromSurface(self.ren, s)
        textX = ctypes.c_long()
        textY = ctypes.c_long()
        SDL_QueryTexture(textTexture, None, None, textX, textY)
        # FIXME: does this draw with centerY in the center?
        return textTexture, SDL_Rect(
                            int(self.centerX - textX.value/2),
                            self.centerY,
                            textX.value,
                            textY.value)

    def timeTick(self):
        if self.glowingTextDir:
            self.glowingTextCounter = self.glowingTextCounter + 10
        else:
            self.glowingTextCounter = self.glowingTextCounter - 10
        if self.glowingTextCounter > 200:
            self.glowingTextDir = False
        elif self.glowingTextCounter < 100:
            self.glowingTextDir = True

