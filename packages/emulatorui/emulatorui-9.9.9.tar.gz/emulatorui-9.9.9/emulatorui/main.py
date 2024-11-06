import ctypes
import importlib.resources
import time

from sdl2 import *
from sdl2.sdlttf import *

from .consoleScroller import consoleScroller
from .gameSelectMenu import gameSelectMenu
from .glowingText import glowingText
from .textures import textures
from .buttonWithAlphaHighlight import buttonWithAlphaHighlight
from .console import console
from .vec2D import vec2D

def doSelectFade(ren, fade, toRender, selectedConsole, screenSize, rectMiddle):
    SDL_RenderClear(ren)
    # Render everything except the current selection
    for tex, texrect in toRender:
        SDL_SetTextureAlphaMod(tex, int(255 - fade))
        if tex != selectedConsole.tex:
            SDL_RenderCopy(ren, tex, None, texrect)
    # Now render the current console, which is zooming to the top-right of the screen.
    selectedRect = SDL_Rect()
    # FIXME: there's an x offset here which doesn't look good.
    selectedRect.w = int((rectMiddle.w * ((255 - fade) / 255) / 2) + rectMiddle.w / 2)
    selectedRect.h = int((rectMiddle.h * ((255 - fade) / 255) / 2) + rectMiddle.h / 2)
    selectedRect.x = int((screenSize.x - selectedRect.w) - rectMiddle.x * ((255 - fade) / 255))
    selectedRect.y = int(rectMiddle.y * ((255 - fade) / 255))
    SDL_SetTextureAlphaMod(selectedConsole.tex, 255)
    SDL_RenderCopy(ren, selectedConsole.tex, None, selectedRect)
    SDL_RenderPresent(ren)


class main:
    windowSize: vec2D
    borderSize: vec2D
    viewportSize: vec2D

    def __init__(self):
        self.imgAnimProgress = 0
        self.windowSize = vec2D(960, 540)
        self.borderSize = vec2D(10, 10)
        self.fullscreen = False

        SDL_Init(SDL_INIT_VIDEO)
        SDL_SetHint(SDL_HINT_RENDER_SCALE_QUALITY, b"1")
        TTF_Init()

        self.window = SDL_CreateWindow(b"Game UI!", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, self.windowSize.x, self.windowSize.y, SDL_WINDOW_SHOWN)
        if self.fullscreen:
            SDL_SetWindowFullscreen(self.window, SDL_WINDOW_FULLSCREEN_DESKTOP)
            winX = ctypes.c_int()
            winY = ctypes.c_int()
            SDL_GetWindowSize(self.window, winX, winY)
            self.windowSize = vec2D(winX.value, winY.value)
        self.ren = SDL_CreateRenderer(self.window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)

        self.viewportSize = vec2D(
            self.windowSize.x - (self.borderSize.x * 2),
            self.windowSize.y - (self.borderSize.y * 2)
        )

        # Load up consoles and their images
        consoleImages = []
        for filename in importlib.resources.files('emulatorui').joinpath('consoles').iterdir():
            if filename.name.endswith(".yaml"):
                consoleImages.append(console.fromYamlFile(self.ren, self.viewportSize.x / 3, self.viewportSize.y, filename.__str__()))

        # Create child elements
        statusBarH   = int(self.viewportSize.y / 5)
        statusBarTop = self.windowSize.y - self.borderSize.y - statusBarH
        self.leftButton = buttonWithAlphaHighlight(self.ren, "assets/left.png", SDL_Rect(self.borderSize.x, statusBarTop, int(self.viewportSize.x / 10), statusBarH))
        self.rightButton = buttonWithAlphaHighlight(self.ren, "assets/right.png", SDL_Rect(self.windowSize.x - self.borderSize.x - int(self.viewportSize.x / 10), statusBarTop, int(self.viewportSize.x / 10), statusBarH))
        self.consoleCaption = glowingText(self.ren, "hello", int(self.windowSize.x/2), int(self.borderSize.y))
        self.consoles = consoleScroller(SDL_Rect(self.borderSize.x, self.borderSize.y, int(self.viewportSize.x / 3), self.viewportSize.y), consoleImages)

        self.selectConsole(0)

    def run(self):
        with importlib.resources.as_file(importlib.resources.files('emulatorui').joinpath('assets/background.png')) as bg:
            tex_background = textures.loadTexture(self.ren, bg.__str__())
        rectBackground = SDL_Rect(0, 0, self.windowSize.x, self.windowSize.y)

        while True:
            # Let our child elements know that time has passed
            self.leftButton.timeTick()
            self.rightButton.timeTick()
            self.consoleCaption.timeTick()
            self.consoles.timeTick()

            # Render the screen
            toRender = ( (tex_background, rectBackground),
                         self.leftButton.render(),
                         self.rightButton.render(),
                         self.consoleCaption.render())
            toRender += self.consoles.render()
            SDL_RenderClear(self.ren)
            for tex, texrect in toRender:
                SDL_RenderCopy(self.ren, tex, None, texrect)
            SDL_RenderPresent(self.ren)

            # Handle any inputs from the user
            event = SDL_Event()
            if SDL_PollEvent(ctypes.byref(event)) == 0:
                continue
            if event.type == SDL_QUIT:
                break
            elif event.type == SDL_KEYDOWN:
                key = event.key.keysym.sym
                if key == SDLK_ESCAPE:
                    break
                elif key == SDLK_LEFT:
                    self.consoles.scrollToPrevious()
                    self.consoleCaption.caption = self.consoles.selectedConsole.name
                elif key == SDLK_RIGHT:
                    self.consoles.scrollToNext()
                    self.consoleCaption.caption = self.consoles.selectedConsole.name
                elif key == SDLK_RETURN:
                    # Fade out everything except the currently-selected console
                    fadeLenSecs = 0.5
                    for fade in range(0, 255, 25):
                        doSelectFade(self.ren, fade, toRender, self.consoles.selectedConsole, self.viewportSize, self.consoles.findMiddleRect())
                        time.sleep(fadeLenSecs / 10)
                    newMenu = gameSelectMenu(self.ren, self.windowSize, self.borderSize, self.consoles.selectedConsole)
                    newMenu.doMenu()
                    for fade in range(255, 0, -25):
                        doSelectFade(self.ren, fade, toRender, self.consoles.selectedConsole, self.viewportSize, self.consoles.findMiddleRect())
                        time.sleep(fadeLenSecs / 10)
            elif event.type == SDL_MOUSEMOTION:
                # Propogate mouse position to child elements
                self.leftButton.onMouseMove(event.motion)
                self.rightButton.onMouseMove(event.motion)
            elif event.type == SDL_MOUSEBUTTONDOWN:
                # See what's clicked
                if self.leftButton.isHovered:
                    self.consoles.scrollToPrevious()
                elif self.rightButton.isHovered:
                    self.consoles.scrollToNext()
                # Update the caption at the top of the screen
                self.consoleCaption.caption = self.consoles.selectedConsole.name

        SDL_DestroyRenderer(self.ren)
        SDL_DestroyWindow(self.window)
        SDL_Quit()

    def selectConsole(self, newIndex):
        self.consoles.scrollToConsole(newIndex)
        self.consoleCaption.caption = self.consoles.selectedConsole.name

def consoleEntryPoint():
    main().run()

if __name__ == "__main__":
    main().run()

