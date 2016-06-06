import math
import textwrap
from PIL import Image, ImageDraw, ImageFont
from images2gif import writeGif


font_size = 18
# font_path = '/usr/share/fonts/truetype/calibre/calibre-regular.ttf'
# font = ImageFont.truetype(font_path, size=font_size)
font = ImageFont.load_default()


class Renderer():
    """renders a grid with values (for the gridworld)"""
    def __init__(self, grid, cell_size=60):
        self.grid = grid
        self.cell_size = cell_size

        grid_h = len(grid)
        grid_w = max(len(row) for row in grid)
        self.size = (grid_w * self.cell_size, grid_h * self.cell_size)

    def _draw_cell(self, x, y, fill, color, value, pos, text_padding=10):
        self.draw.rectangle([(x, y), (x+self.cell_size, y+self.cell_size)], fill=fill)

        # render text
        y_mid = math.floor(self.cell_size/2)
        lines = textwrap.wrap(str(value), width=15)
        _, line_height = self.draw.textsize(lines[0], font=font)
        height = len(lines) * line_height + (len(lines) - 1) * text_padding
        current_height = y_mid - height/2

        for line in lines:
            w, h = self.draw.textsize(line, font=font)
            self.draw.text((x + (self.cell_size - w)/2, y + current_height), line, font=font, fill=color)
            current_height += h + text_padding

    def render(self, pos=None):
        """renders the grid,
        highlighting the specified position if there is one"""
        self.img = Image.new('RGBA', self.size, color=(255,255,255,0))
        self.draw = ImageDraw.Draw(self.img)

        for r, row in enumerate(self.grid):
            for c, val in enumerate(row):
                if val is None:
                    continue
                fill = (220,220,220,255) if (r + c) % 2 == 0 else (225,225,225,255)

                # current position
                if pos is not None and pos == (r, c):
                    fill = (255,255,150,255)
                self._draw_cell(c * self.cell_size, r * self.cell_size, fill, (0,0,0,255), val, (r,c))

        return self.img


def annotate_image(img, text, padding=20, color=(0,0,0,255)):
    """adds a line of text underneath an image"""
    w, h = img.size
    size = (w, h + padding + font_size)
    _img = Image.new('RGBA', size, color=(255,255,255,0))
    draw = ImageDraw.Draw(_img)
    draw.text((0, h + padding), text, font=font, fill=color)
    _img.paste(img, (0,0))
    return _img


def save_gif(output, images):
    writeGif(output,
            images,
            duration=0.1,
            repeat=True,

            # if True, reduces file size by minimally
            # re-drawing parts of the image
            # but it can conflict with disposing frames
            # (can cause parts to not be rendered)
            subRectangles=False,

            # 1 -> leave each frame
            # 2 -> restore background color
            # 3 -> restore previous frame
            dispose=2)


if __name__ == '__main__':
    grid = [
        [100, 0, 100],
        [20,5,-10]
    ]
    renderer = Renderer(grid)
    images = [annotate_image(renderer.render((i,i)), 'hello_{}'.format(i)) for i in range(2)]
    save_gif('test.gif', images)