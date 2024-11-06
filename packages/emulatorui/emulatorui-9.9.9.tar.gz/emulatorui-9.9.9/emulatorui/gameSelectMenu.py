import ctypes
import math
import time
from typing import List

import importlib.resources
from sdl2 import *
from sdl2.sdlimage import *

from .text import text
from .textures import textures
from .vec2D import vec2D
from .console import console
from .game import game

class snapshotTextureCache:
    def __init__(self, ren):
        self.textures = {}
        self.ren = ren

    def getTextureForGame(self, toLoad: game):
        if self.textures.get(toLoad.snapshotFilename, None) is None:
            self.textures[toLoad.snapshotFilename] = IMG_LoadTexture(self.ren, toLoad.snapshotFilename.encode('utf-8'))
        return self.textures[toLoad.snapshotFilename]

class snapshotBox:
    def __init__(self, ren, displayRect: SDL_Rect, games: List[game]):
        self.ren = ren
        self.displayRect = displayRect
        self.games = games
        self.selectedGameIndex = 0
        self.fadePos = 0
        self.previousSnapshotTexture = None

        self.snapshotTextures = snapshotTextureCache(ren)

    def render(self):
        # Show the screenshot, if one is present
        selectedGame = self.games[self.selectedGameIndex]

        if selectedGame.snapshotFilename is not None:
            texture = self.snapshotTextures.getTextureForGame(selectedGame)
            if self.previousSnapshotTexture is not None and self.fadePos > 0:
                SDL_SetTextureAlphaMod(texture, 255 - self.fadePos)
                SDL_SetTextureAlphaMod(self.previousSnapshotTexture, 255 - self.fadePos)

                return (self.previousSnapshotTexture, self.displayRect), (texture, self.displayRect)
            else:
                SDL_SetTextureAlphaMod(texture, 255)
                return [(texture, self.displayRect)]

        return [(None, None)]

    def setGameIndex(self, newPos):
        if self.selectedGameIndex != newPos:
            self.fadePos = 255
            selectedGame = self.games[self.selectedGameIndex]
            if selectedGame.snapshotFilename is not None:
                self.previousSnapshotTexture = self.snapshotTextures.getTextureForGame(selectedGame)
            else:
                self.previousSnapshotTexture = None
        self.selectedGameIndex = newPos

    def timeTick(self):
        if self.fadePos > 0:
            self.fadePos = self.fadePos - 20
        if self.fadePos < 0:
            self.previousSnapshotTexture = None
            self.fadePos = 0


class gameSelectionBar:
    games: List[game]
    solidTexture: object

    def __init__(self, ren, menuRect : SDL_Rect, games, numberOfGamesToShowAtATime):
        self.rect = menuRect
        # Create a solid white texture we can use for highlighting the current selection
        self.solidTexture = textures.makeSolid(ren, 0xff, 0xff, 0xff, 0xff)
        self.gamePos = 0
        self.numberOfGamesToShowAtATime = numberOfGamesToShowAtATime
        self.games = games

    def render(self):
        # Fade alpha based on wall time
        alphatime = abs(int(math.sin(time.time() % math.pi * 2 ) * 128)) + 128
        SDL_SetTextureAlphaMod(self.solidTexture, alphatime)

        selectedGame = self.games[self.gamePos]
        gameName = selectedGame.displayname

        barSizeX = len(gameName) * 20 + 10
        barSizeY = int(self.rect.h / self.numberOfGamesToShowAtATime)

        if self.gamePos < self.numberOfGamesToShowAtATime / 2:
            # If we're in the bottom few games, we must draw the bar here.
            barIdx = self.gamePos
        elif self.gamePos > len(self.games) - int(self.numberOfGamesToShowAtATime / 2):
            # And in the top few, here..
            offsetFromTop = len(self.games) - self.gamePos
            barIdx = self.numberOfGamesToShowAtATime - offsetFromTop
        else:
            # Otherwise, the bar is always in the middle position.
            barIdx = int(self.numberOfGamesToShowAtATime / 2)

        return self.solidTexture, SDL_Rect(self.rect.x, self.rect.y + (barIdx * barSizeY), barSizeX, barSizeY)

    def setGameIndex(self, newPos):
        self.gamePos = newPos

    def timeTick(self):
        pass

class gameSelectMenu:
    def __init__(self, ren, windowSize : vec2D, borderSize : vec2D, currentConsole : console):
        self.ren = ren
        self.windowSize = windowSize
        self.borderSize = borderSize
        self.console = currentConsole

        self.fadeCounter = 255
        self.fadeDirection = False

        self.gamePos = 0
        self.font = textures.getDefaultFont(24)
        with importlib.resources.files('emulatorui').joinpath('assets').joinpath('background.png') as bg:
            self.tex_background = textures.loadTexture(ren, str(bg))
        self.rectBackground = SDL_Rect(0, 0, windowSize.x, windowSize.y)

        # The size of our menu, in games. Keep this even for best results.
        self.numberOfGamesToShow = 6

        # The rectangle the game snapshot will be drawn in
        snapSizeX = int(self.windowSize.x/2) - self.borderSize.x
        snapSizeY = int(self.windowSize.y/2) - self.borderSize.y
        self.snapshotRect = SDL_Rect(int(self.windowSize.x/4), self.windowSize.y - self.borderSize.y - snapSizeY, snapSizeX, snapSizeY)
        # And the game snapshot widget itself
        self.snapshot = snapshotBox(ren, self.snapshotRect, self.console.games)

        # The rectangle where our list of games sits
        self.gameListRect = SDL_Rect(self.borderSize.x, self.borderSize.y, int(self.windowSize.x/2) - self.borderSize.x, int(self.windowSize.y/2) - self.borderSize.y)

        # The glowy rectangle drawn underneath the current game
        self.gameCursor = gameSelectionBar(ren, self.gameListRect, self.console.games, self.numberOfGamesToShow)

    def doMenu(self):
        while True:
            event = SDL_Event()

            self.gameCursor.timeTick()
            self.snapshot.timeTick()

            toRender = [
                (self.tex_background, self.rectBackground),
                (self.console.tex, SDL_Rect(int(self.windowSize.x - self.console.sizeX/2), 0, int(self.console.sizeX/2), int(self.console.sizeY/2))),
                # Draw a rectangle under the currently-selected game
                self.gameCursor.render()
            ]
            toRender.extend(self.snapshot.render())

            # Draw the list of games
            gameIdx = self.gamePos
            if gameIdx < self.numberOfGamesToShow / 2:
                gameIdx = 0
            elif gameIdx > len(self.console.games) - self.numberOfGamesToShow / 2:
                gameIdx = len(self.console.games) - self.numberOfGamesToShow
            else:
                gameIdx = gameIdx - int(self.numberOfGamesToShow / 2)
            gameIdxThisScreen = 0
            while gameIdx < len(self.console.games) and gameIdxThisScreen < self.numberOfGamesToShow:
                gameTitle = self.console.games[gameIdx].displayname
                titleHeight = int(self.gameListRect.h / self.numberOfGamesToShow)
                titlePos = self.gameListRect.x, self.gameListRect.y + (gameIdxThisScreen * titleHeight)
                titleSize = int(20 * len(self.console.games[gameIdx].displayname)), titleHeight

                t = text(self.ren, self.font, gameTitle, titlePos, titleSize, SDL_Color(128, 0, 128))
                toRender.append(t.render())

                gameIdx = gameIdx + 1
                gameIdxThisScreen = gameIdxThisScreen + 1

            # Do the rendering
            SDL_RenderClear(self.ren)
            for tex, r in toRender:
                if tex == self.console.tex and self.fadeDirection == False:
                    # The console image (in the top-left) is not faded in when we are first showing this menu..
                    SDL_SetTextureAlphaMod(tex, 255)
                else:
                    if self.fadeCounter > 0:
                        if self.fadeDirection == True:
                            SDL_SetTextureAlphaMod(tex, self.fadeCounter)
                        else:
                            SDL_SetTextureAlphaMod(tex, 255 - self.fadeCounter)
                SDL_RenderCopy(self.ren, tex, None, r)
            SDL_RenderPresent(self.ren)

            if self.fadeCounter > 0:
                self.fadeCounter = self.fadeCounter - 10
                if self.fadeCounter < 0:
                    if self.fadeDirection == True:
                        self.startGame()
                    for tex, _ in toRender:
                        SDL_SetTextureAlphaMod(tex, 255)
                    self.fadeCounter = 0
                continue

            if SDL_PollEvent(ctypes.byref(event)) == 0:
                continue
            if event.type == SDL_QUIT:
                break
            elif event.type == SDL_KEYDOWN:
                key = event.key.keysym.sym
                if key == SDLK_ESCAPE:
                    return
                elif key == SDLK_RETURN:
                    self.fadeDirection = True
                    self.fadeCounter = 255
                elif key == SDLK_DOWN:
                    self.gamePos = self.gamePos + 1
                elif key == SDLK_UP:
                    self.gamePos = self.gamePos - 1
                elif key == SDLK_HOME:
                    self.gamePos = 0
                elif key == SDLK_END:
                    self.gamePos = len(self.console.games) - 1
                elif key == SDLK_PAGEUP or key == SDLK_LEFT:
                    self.gamePos = self.gamePos - self.numberOfGamesToShow
                elif key == SDLK_PAGEDOWN or key == SDLK_RIGHT:
                    self.gamePos = self.gamePos + self.numberOfGamesToShow
                else:
                    # An unrecognised key was pressed. Perhaps the user wants to search for a game by first character?
                    keyNameBytes = SDL_GetKeyName(key)
                    keyName = str(keyNameBytes, 'ascii')
                    if len(keyName) == 1 and keyName[0] >= 'A' and keyName[0] <= 'Z':
                        # Jump to the first occurance of this character.
                        posIdx = 0
                        for gameToTest in self.console.games:
                            if gameToTest.displayname[0] == keyName[0]:
                                self.gamePos = posIdx
                                break
                            posIdx = posIdx + 1

                if self.gamePos > len(self.console.games) - 1:
                    self.gamePos = len(self.console.games) - 1
                if self.gamePos < 0:
                    self.gamePos = 0

            self.gameCursor.setGameIndex(self.gamePos)
            self.snapshot.setGameIndex(self.gamePos)

    def startGame(self):
        self.gameCursor.games[self.gameCursor.gamePos].start()

