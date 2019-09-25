# Text drawing and handling utilities.


def draw_string(screen, s, **kwargs):
    screen.draw.text(s, owidth=0.5, ocolor=(255, 255, 255), color=(0, 64, 255),
                     fontsize=60, **kwargs)


def draw_center_text(screen, t, screen_width, top=300):
    draw_string(screen, t, center=(screen_width/2, top))


# We need a way to show text screens between levels, for credits, etc.
class TextScreen():
    rows = []
    centered = False
    left = 0
    top = 0
    line_height = 0
    screen_width = None

    def __init__(self, screen, centered=False, screen_width=None, left=100, top=300, line_height=60, rows=[]):
        self.screen = screen
        self.centered = centered
        self.left = left
        self.top = top
        self.line_height = line_height
        if screen_width is None:
            raise AssertionError("Must pass screen_width if centered")
        self.screen_width = screen_width
        self.rows = [str(s) for s in rows]

    def add_row(self, s):
        self.rows.append(str(s))

    def clear_rows(self):
        self.rows = []

    # TODO: handle color, style, font, etc.
    def draw(self):
        top = self.top
        for row in self.rows:
            if self.centered:
                draw_string(self.screen, row, midtop=(self.screen_width/2,top))
            else:
                draw_string(self.screen, row, left=self.left, top=top)
            top += self.line_height
