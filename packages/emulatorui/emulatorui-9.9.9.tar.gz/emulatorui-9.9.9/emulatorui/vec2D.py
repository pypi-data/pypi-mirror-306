class vec2D:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        if x.__class__ is float:
            x = int(x)
        if y.__class__ is float:
            y = int(y)
        self.x = x
        self.y = y