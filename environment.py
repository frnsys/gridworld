from render import Renderer

class Environment():
    def __init__(self, grid):
        # fill in missing cells
        max_width = max(len(row) for row in grid)
        for row in grid:
            row += [None for _ in range(max_width - len(row))] 
        self.grid = grid
        self.n_rows = len(grid)
        self.n_cols = len(grid[0])
        self.positions = self._positions()
        self.renderer = Renderer(self.grid)

    def actions(self, pos):
        """possible actions for a state (position)"""
        r, c = pos
        actions = ['stay']
        if r > 0 and self.grid[r-1][c] is not None:
            actions.append('up')
        if r < self.n_rows - 1 and self.grid[r+1][c] is not None:
            actions.append('down')
        if c > 0 and self.grid[r][c-1] is not None:
            actions.append('left')
        if c < self.n_cols - 1 and self.grid[r][c+1] is not None:
            actions.append('right')
        return actions

    def value(self, pos):
        r, c = pos
        return self.grid[r][c]

    def render(self, pos=None):
        return self.renderer.render(pos)

    def _positions(self):
        """all valid positions"""
        positions = []
        for r, row in enumerate(self.grid):
            for c, _ in enumerate(row):
                if self.grid[r][c] is not None:
                    positions.append((r,c))
        return positions
