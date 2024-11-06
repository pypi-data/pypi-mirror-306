from sdl2 import SDL_Rect

from .console import console

from typing import List

class consoleScroller:
    rect: SDL_Rect
    consoleImages: List[console]

    selectedConsoleIndex: int
    previousConsole: console
    selectedConsole: console
    nextConsole: console

    imgAnimSpeed: int
    imgAnimProgress: int

    def __init__(self, displayRect : SDL_Rect, consoleList : List[console]):
        self.rect = displayRect
        self.consoleImages = consoleList
        self.imgAnimProgress = 0
        self.imgAnimSpeed = 0

        self.selectedConsoleIndex = 0
        self.previousConsole = self.consoleImages[self.selectedConsoleIndex - 1]
        self.selectedConsole = self.consoleImages[self.selectedConsoleIndex]
        self.nextConsole     = self.consoleImages[(self.selectedConsoleIndex + 1) % len(self.consoleImages)]

    def scrollToConsole(self, newIndex):
        # Clamp the selected console to valid options
        if newIndex < 0:
            newIndex = len(self.consoleImages) - 1
        elif newIndex > len(self.consoleImages) - 1:
            newIndex = 0

        self.selectedConsoleIndex = newIndex
        # And ensure prev/selected/next console images are up to date.
        self.previousConsole = self.consoleImages[self.selectedConsoleIndex - 1]
        self.selectedConsole = self.consoleImages[self.selectedConsoleIndex]
        self.nextConsole     = self.consoleImages[(self.selectedConsoleIndex + 1) % len(self.consoleImages)]

    def timeTick(self):
        # Progress any animations and apply acceleration to animation speed
        if self.imgAnimProgress > 0:
            self.imgAnimProgress = self.imgAnimProgress - self.imgAnimSpeed
            if self.imgAnimProgress < 0:
                self.imgAnimProgress = 0
        elif self.imgAnimProgress < 0:
            self.imgAnimProgress = self.imgAnimProgress + self.imgAnimSpeed
            if self.imgAnimProgress > 0:
                self.imgAnimProgress = 0

        if self.imgAnimProgress == 0:
            self.imgAnimSpeed = 1
        else:
            if self.imgAnimSpeed < 20:
                self.imgAnimSpeed +=1

    def scrollToNext(self):
        self.scrollToConsole(self.selectedConsoleIndex - 1)
        self.imgAnimProgress = +100

    def scrollToPrevious(self):
        self.scrollToConsole(self.selectedConsoleIndex + 1)
        self.imgAnimProgress = -100

    def render(self):
        # Work out where current, previous, and next consoles should be when stationary
        rectMiddle = SDL_Rect(self.rect.x + self.rect.w,
                              self.rect.y + self.selectedConsole.posY,
                              self.selectedConsole.sizeX, self.selectedConsole.sizeY)

        # Draw the previous and next console images.
        rectNext      = SDL_Rect(int((rectMiddle.x / 2) - (self.nextConsole.sizeX / 2)),
                                       self.rect.y + self.nextConsole.posY,
                                       self.nextConsole.sizeX, self.nextConsole.sizeY)
        rectPrevious  = SDL_Rect(int(((self.rect.w * 3) - (rectMiddle.w/2)) - (self.previousConsole.sizeX / 2)),
                                       self.rect.y + self.previousConsole.posY,
                                       self.previousConsole.sizeX, self.previousConsole.sizeY)
        # If we're currently animating a console sliding off/onto the screen, apply that
        imgAnimProgressNormalized = self.imgAnimProgress / 100
        pixelsToSlide = int( imgAnimProgressNormalized * int(self.rect.w ))
        rectPrevious.x += pixelsToSlide
        rectMiddle.x   += pixelsToSlide
        rectNext.x     += pixelsToSlide

        # And likewise, make the prev/next consoles slightly smaller as they slide away from being the current console
        sizeScaling = imgAnimProgressNormalized
        sizeScalingMiddle = (abs(sizeScaling) / 2)
        self.scaleRect(rectMiddle, 1-sizeScalingMiddle)
        # Scale prev/max from 50% to 100% size
        sizeScaling = (sizeScaling / 2) + 0.5
        self.scaleRect(rectNext,  sizeScaling)
        self.scaleRect(rectPrevious,    1-sizeScaling)

        return (
            (self.previousConsole.tex, rectPrevious),
            (self.selectedConsole.tex, rectMiddle),
            (self.nextConsole.tex, rectNext))

    # Scale a rectangle around its center by a factor of 0..1
    def scaleRect(self, rect, scale):
        rect.y += int(rect.h / 2 * (1 - scale))
        rect.x += int(rect.w / 2 * (1 - scale))
        rect.h = int(rect.h * scale)
        rect.w = int(rect.w * scale)

    def findMiddleRect(self):
        # Return a rectangle expressing where the currently-selected console is rendered.
        return SDL_Rect(self.rect.x + self.rect.w,
                        self.rect.y + self.selectedConsole.posY,
                        self.selectedConsole.sizeX, self.selectedConsole.sizeY)
