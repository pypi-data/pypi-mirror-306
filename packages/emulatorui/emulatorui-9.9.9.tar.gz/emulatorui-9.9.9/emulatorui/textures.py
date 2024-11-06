import ctypes
from typing import Any, Dict

import importlib.resources
from sdl2 import *
from sdl2.sdlimage import *
from sdl2.sdlttf import *

class textures:
    loadedTextures: Dict[str, Any]
    _defaultFont: Dict[int, Any]
    _inst = None # type: textures

    def __init__(self):
        self._defaultFont = {}
        self.loadedTextures = {}

    @staticmethod
    def _getInst():
        if hasattr(textures, 'inst') is False:
            textures._inst = textures()
        return textures._inst

    @staticmethod
    def loadTexture(ren: object, filename: str):
        assert isinstance(filename, str)

        inst = textures._getInst()
        if filename not in inst.loadedTextures:
            inst.loadedTextures[filename] = IMG_LoadTexture(ren, filename.encode('utf-8'))
            SDL_SetTextureBlendMode(inst.loadedTextures[filename], SDL_BLENDMODE_BLEND)
        return inst.loadedTextures[filename]

    @staticmethod
    def makeSolid(ren, b: int, g: int, r: int, a: int) -> object:
        solidTexture = SDL_CreateTexture(ren, SDL_PIXELFORMAT_ARGB32, SDL_TEXTUREACCESS_STATIC, 1, 1)
        SDL_SetTextureBlendMode(solidTexture, SDL_BLENDMODE_BLEND)
        pixelInt = b | (g << 8) | (r << 16) | (a << 24)
        solidPixels = ctypes.c_char_p(pixelInt.to_bytes(4, 'big'))
        SDL_UpdateTexture(solidTexture, None, solidPixels, 4)
        return solidTexture

    @staticmethod
    def getDefaultFont(sizePts):
        inst = textures._getInst()
        if sizePts not in inst._defaultFont:
            with importlib.resources.files('emulatorui').joinpath('assets').joinpath('fixedsys.ttf') as fontfile:
                inst._defaultFont[sizePts] = TTF_OpenFont(str(fontfile).encode('ascii'), sizePts)
        return inst._defaultFont[sizePts]
