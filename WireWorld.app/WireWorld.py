import pyxel

# Cores para cada estado
COLORS = {0: 0, 1: 9, 2: 8, 3: 10}  # Pyxel colors: black, blue, red, yellow

class WireWorld:
    def __init__(self, grid, cell_size=10):
        self.grid = grid
        self.initial_grid = [row[:] for row in grid]  # Backup do estado inicial
        self.cell_size = cell_size
        self.playing = False

    def reset(self):
        self.grid = [row[:] for row in self.initial_grid]
        self.playing = False

    def update(self):
        if self.playing:
            self.step()

    def draw(self):
        pyxel.cls(0)
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                color = COLORS[cell]
                pyxel.rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size, color)

    def step(self):
        new_grid = [row[:] for row in self.grid]
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == 1:  # Cabeça de elétron -> Cauda de elétron
                    new_grid[y][x] = 2
                elif self.grid[y][x] == 2:  # Cauda de elétron -> Fio condutor
                    new_grid[y][x] = 3
                elif self.grid[y][x] == 3:  # Fio condutor -> Depende do vizinho
                    neighbors = self.get_neighbors(x, y)
                    head_count = neighbors.count(1)
                    if head_count == 1 or head_count == 2:
                        new_grid[y][x] = 1
        self.grid = new_grid

    def get_neighbors(self, x, y):
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(self.grid[0]) and 0 <= ny < len(self.grid):
                    neighbors.append(self.grid[ny][nx])
        return neighbors

def read_grid_from_file(filename):
    with open(filename, 'r') as f:
        grid = [[int(char) for char in line.strip()] for line in f]
    return grid

class WireWorldApp:
    def __init__(self, filename):
        self.grid = read_grid_from_file(filename)
        self.automaton = WireWorld(self.grid)
        pyxel.init(len(self.grid[0]) * self.automaton.cell_size, len(self.grid) * self.automaton.cell_size, caption="WireWorld")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_P):
            self.automaton.playing = not self.automaton.playing  # Play/Pause
        if pyxel.btnp(pyxel.KEY_S):
            self.automaton.step()  # Step
        if pyxel.btnp(pyxel.KEY_R):
            self.automaton.reset()  # Reset
        self.automaton.update()

    def draw(self):
        self.automaton.draw()

if __name__ == "__main__":
    # Carregar o estado inicial do arquivo texto
    filename = "estado_inicial.txt"  # Coloque o nome do arquivo de estado inicial
    WireWorldApp(filename)
