import glob
import importlib.resources
import os

import yaml

from .console import console
from .game_c64 import game_c64


class console_c64(console):
    def __init__(self, ren, config, maxX, maxY):
        super(console_c64, self).__init__(ren, config, maxX, maxY)

        # Load any games which aren't explicitly definied in the config, with default settings.
        gameDir = config.get("gameDir", [])
        pathToGames = importlib.resources.files('emulatorui').joinpath('consoles').joinpath(gameDir)
        for gamefile in glob.glob(os.path.join(pathToGames.__str__(), '*'), recursive=True):

            # We're only interested in these file extensions.
            if gamefile[-4:].lower() not in game_c64.fileExtensions:
                continue

            # If a '.yaml' file is present, it will contain further information, so load using that. If not, then just
            # construct the game from the filename.
            yamlFilename = f"{gamefile}.yaml"
            if os.path.exists(yamlFilename):
                with open(yamlFilename, 'r') as f:
                    gameConfig = yaml.safe_load(f)
                newGame = game_c64(str(gamefile), gameConfig)
            else:
                newGame = game_c64(str(gamefile))

            # If no snapshot is present, look for one in our snapshot directory.
            if newGame.snapshotFilename is None:
                snapshotName = f"{gamefile}.png"
                if os.path.exists(snapshotName):
                    newGame.snapshotFilename = snapshotName

            self.games.append(newGame)
