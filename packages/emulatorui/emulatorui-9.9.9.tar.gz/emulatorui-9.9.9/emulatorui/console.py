import ctypes
import importlib.resources

import yaml
from sdl2 import SDL_QueryTexture, SDL_SetTextureBlendMode, SDL_BLENDMODE_BLEND
from sdl2.sdlimage import IMG_LoadTexture

from .game import game

from typing import List

class console:
    tex: object
    name: str
    games: List[game]

    def __init__(self, ren, config, maxX, maxY):
        self.games = []
        self.name = config['name'].upper()

        with importlib.resources.as_file(importlib.resources.files('emulatorui').joinpath('consoles').joinpath(config['image'])) as f:
            filepath = f.__str__()
            self.tex = IMG_LoadTexture(ren, filepath.encode("UTF-8"))
            if self.tex is None:
                raise Exception("Failed to load console image '%s'" % filepath)
            SDL_SetTextureBlendMode(self.tex, SDL_BLENDMODE_BLEND)
            sizeX = ctypes.c_int()
            sizeY = ctypes.c_int()
            SDL_QueryTexture(self.tex, None, None, sizeX, sizeY)
            if sizeX.value == 0 or sizeY.value == 0:
                raise Exception("Failed to load console image '%s'" % filepath)
        aspect = sizeY.value / sizeX.value
        # Clamp or stretch until we fill horizontal space
        self.sizeX = maxX
        self.sizeY = maxX * aspect
        # Ensure we centre the image Y-wise
        self.posY = (maxY / 2) - (self.sizeY / 2)

        self.scartPortID = None

        # Change types as appropriate
        self.posY = int(self.posY)
        self.sizeX = int(self.sizeX)
        self.sizeY = int(self.sizeY)

    @staticmethod
    def fromYamlFile(parentRenderer, sizeX, sizeY, configFileName):
        with open(configFileName, 'r') as configHnd:
            config = yaml.safe_load(configHnd)

        requiredKeys = ('image', 'name', 'type')
        for req in requiredKeys:
            if not req in config.keys():
                raise Exception("File '%s' does not specify required key '%s'" % (configFileName, req))

        if config['type'].lower() == 'c64':
            from .console_c64 import console_c64
            return console_c64(parentRenderer, config, sizeX, sizeY)
        else:
            # Unknown type, just return the base class for now.
            return console(parentRenderer, config, sizeX, sizeY)
