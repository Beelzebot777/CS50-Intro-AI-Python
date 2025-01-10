import sys
from tabulate import tabulate
from PIL import Image, ImageDraw

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Maze():
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def solve(self):
        """Finds a solution to maze, if one exists."""
        self.num_explored = 0
        start = Node(state=self.start, parent=None, action=None)
        #frontier = StackFrontier()
        frontier = QueueFrontier()
        frontier.add(start)
        self.explored = set()

        # Preparar tabla de datos para exportar
        table_data = []
        headers = ["Interation", "Current Node(Y,X)", "Parent", "Action", "Frontier", "Explored"]
        iteration = 0

        while True:
            if frontier.empty():
                raise Exception("no solution")

            node = frontier.remove()
            self.num_explored += 1
            iteration += 1

            # Registrar información de la iteración
            current_state = node.state
            parent_state = node.parent.state if node.parent else None
            action = node.action
            frontier_states = [n.state for n in frontier.frontier]
            explored_states = list(self.explored)

            table_data.append([
                iteration,
                current_state,
                parent_state,
                action,
                frontier_states,
                explored_states
            ])

            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)

                # Exportar tabla a archivo
                with open("tabla.txt", "w") as file:
                    file.write(tabulate(table_data, headers=headers, tablefmt="grid"))
                return

            self.explored.add(node.state)

            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    def output_image(self, filename, show_solution=True, show_explored=False):
        cell_size = 50
        cell_border = 2
        label_size = 20

        img_width = self.width * cell_size + label_size
        img_height = self.height * cell_size + label_size

        img = Image.new("RGBA", (img_width, img_height), "black")
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        
        # Draw grid with walls, start, goal, solution, and explored states
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                x_start = j * cell_size + label_size
                y_start = i * cell_size + label_size
                x_end = x_start + cell_size - cell_border
                y_end = y_start + cell_size - cell_border

                if col:
                    fill = (40, 40, 40)  # Dark Gray
                elif (i, j) == self.start:
                    fill = (255, 0, 0)  # Red
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)  # Green
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)  # Yellow
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)  # Red
                else:
                    fill = (237, 240, 252)  # White

                draw.rectangle([(x_start, y_start), (x_end, y_end)], fill=fill)

        # Add labels for X and Y axes
        for i in range(self.height):
            y_label = i * cell_size + label_size + cell_size // 2
            draw.text((5, y_label - 10), str(i), fill="white")

        for j in range(self.width):
            x_label = j * cell_size + label_size + cell_size // 2
            draw.text((x_label - 10, 5), str(j), fill="white")

        img.save(filename)

if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1])
print("Maze:")
m.print()

print("Solving...")
m.solve()

print("States Explored:", m.num_explored)

print("Solution:")
m.print()
m.output_image("maze_ini.png", show_explored=False, show_solution=False)
m.output_image("maze_end.png", show_explored=True)
