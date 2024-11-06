import enum
import os.path
import subprocess

from .game import game


class controlMode_64(enum.Enum):
    JOY1 = 1
    JOY2 = 2

class game_c64(game):
    fileExtensions = ('.d64', '.prg', '.t64', '.tap')

    # noinspection PyDefaultArgument
    def __init__(self, filename: str, yamlInfo = {}):
        displayName = yamlInfo.get('displayname', None)
        controlModeStr = yamlInfo.get('controlMode', 'JOY2')

        self.filename = filename
        self.controlMode = controlMode_64[controlModeStr]

        self.gameOpts = {
            'VICIIdscan': '-',
            'VICIIdsize' : '-',
            '-Fullscreen' : '-',
            '-VICIIfilter' : 2
        }

        # If no display name is present, then trim the file extension from the file name and use that.
        if displayName is None:
            displayName = os.path.basename(filename)
            for fileExt in game_c64.fileExtensions:
                if displayName.lower().endswith(fileExt):
                    displayName = displayName[:-len(fileExt)]

        super().__init__(displayName)

    def start(self):
        # Assume the emulator is in the system path.
        emuPath = "x64.exe"

        args = [emuPath]
        for k,v in self.gameOpts.items():
            if v == '-' or v == '+':
                args.append(f"{v}{k}")
            else:
                args.extend((k, str(v)))
        if self.controlMode == controlMode_64.JOY1:
            args.extend(("-joydev1", "2"))
        elif self.controlMode == controlMode_64.JOY2:
            args.extend(("-joydev2", "2"))
        else:
            raise Exception("Unrecognised control mode")

        args.append(os.path.abspath(self.filename))

        p = subprocess.Popen(args)
        # TODO: don't let the SDL window hang
        p.wait()
