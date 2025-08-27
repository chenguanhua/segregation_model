import streamlit as st
import streamlit.components.v1 as components
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors

# Define the colors and their positions
colors = ['white', 'blue', 'red'] # (value, color) pairs

# Create the colormap
custom_cmap = mcolors.LinearSegmentedColormap.from_list("BlueBlackRed", colors)

st.title("Schelling's Segregation Model")

# components.iframe("http://nifty.stanford.edu/2014/mccown-schelling-model-segregation/", width=800, height=600, scrolling=True)
import streamlit as st

st.markdown("""
### Schelling's Segregation Model

Schelling's Segregation Model is a simple agent-based model demonstrating how small individual preferences can lead to large-scale segregation patterns.  
In the model:
- A grid represents a neighborhood.
- Agents belong to two groups (e.g., red and blue).
- Each agent prefers that a certain percentage of its neighbors are of the same group (the **tolerance level**).
- If the tolerance is not met, the agent moves to an empty location.

Over time, even with mild preferences, the system often evolves into highly segregated neighborhoods — illustrating how local behaviors can lead to unintended global patterns.
""")

st.markdown("Below are the specific steps that lead to a working simulation, please complete each piece of code in an orderly manner.")

if 'init_state' not in st.session_state:
    st.session_state.init_state = True

if 'move_state' not in st.session_state:
    st.session_state.move_state = True

if 'anim_state' not in st.session_state:
    st.session_state.anim_state = True

initialization_code = st.checkbox("Step 1: Initialize the world", key='init_state')

if initialization_code:
    st.code('''def create_grid(size, empty_ratio, group_ratio):
    """Create the initial grid with two groups and empty spaces."""
    grid = []
    total_cells = size * size
    group1_count = int(total_cells * group_ratio / 2)
    group2_count = int(total_cells * group_ratio / 2)
    empty_count = total_cells - group1_count - group2_count

    cells = ['A'] * group1_count + ['B'] * group2_count + [''] * empty_count
    random.shuffle(cells)

    for i in range(size):
        grid.append(cells[i * size:(i + 1) * size])
    return grid''')

movement_code = st.checkbox("Step 2: Move unsatisfied resident to a random empty room", key='move_state')

if movement_code:
    st.code('''def move_unsatisfied(grid, threshold):
    """Move unsatisfied residents to empty cells."""
    size = len(grid)
    unsatisfied = []
    for x in range(size):
        for y in range(size):
            if grid[x][y] and is_unsatisfied(x, y, grid, threshold):
                unsatisfied.append((x, y))

    empty_cells = find_empty_cell(grid)
    for x, y in unsatisfied:
        ex, ey = random.choice(empty_cells)
        empty_cells.remove((ex, ey))
        empty_cells.append((x, y))
        grid[ex][ey], grid[x][y] = grid[x][y], ''')

animation_code = st.checkbox("Step 3: Run the simulation", key='anim_state')

if animation_code:
    st.code('''def schelling_simulation(size, empty_ratio, group_ratio, threshold, iterations):
    """Run Schelling's segregation simulation."""
    grid = create_grid(size, empty_ratio, group_ratio)
    print("Initial Grid:")
    history = [display_grid(grid)]

    for i in range(iterations):
        info.markdown(f"Creating Simulation: {(i+1)/iterations*100:.2f}%.")
        move_unsatisfied(grid, threshold)

        history.append(display_grid(grid))
        plt.pause(0.1)

    return history''')


def create_grid(size, empty_ratio, group_ratio):
    """Create the initial grid with two groups and empty spaces."""
    grid = []
    total_cells = size * size
    group1_count = int(total_cells * group_ratio / 2)
    group2_count = int(total_cells * group_ratio / 2)
    empty_count = total_cells - group1_count - group2_count

    cells = ['A'] * group1_count + ['B'] * group2_count + [''] * empty_count
    random.shuffle(cells)

    for i in range(size):
        grid.append(cells[i * size:(i + 1) * size])
    return grid

def display_grid(grid):
    """Display the grid."""

    vis = []
    for row in grid:
        vis.append([['', 'A', 'B'].index(cell) for cell in row])
    return vis



def is_unsatisfied(x, y, grid, threshold):
    """Check if a resident at (x, y) is unsatisfied."""
    size = len(grid)
    current = grid[x][y]
    if current == '':
        return False

    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size:
                neighbors.append(grid[nx][ny])

    same_group_count = neighbors.count(current)
    total_neighbors = len([n for n in neighbors if n])
    return total_neighbors > 0 and (same_group_count / total_neighbors) < threshold

def find_empty_cell(grid):
    """Find a random empty cell."""
    empty_cells = [(x, y) for x in range(len(grid)) for y in range(len(grid[x])) if grid[x][y] == '']
    return empty_cells

def move_unsatisfied(grid, threshold):
    """Move unsatisfied residents to empty cells."""
    size = len(grid)
    unsatisfied = []
    for x in range(size):
        for y in range(size):
            if grid[x][y] and is_unsatisfied(x, y, grid, threshold):
                unsatisfied.append((x, y))

    empty_cells = find_empty_cell(grid)
    for x, y in unsatisfied:
        ex, ey = random.choice(empty_cells)
        empty_cells.remove((ex, ey))
        empty_cells.append((x, y))
        grid[ex][ey], grid[x][y] = grid[x][y], ''

def schelling_simulation(size, empty_ratio, group_ratio, threshold, iterations):
    """Run Schelling's segregation simulation."""
    grid = create_grid(size, empty_ratio, group_ratio)
    history = [display_grid(grid)]

    for i in range(iterations):
        info.markdown(f"Creating Simulation: {(i+1)/iterations*100:.2f}%.")
        move_unsatisfied(grid, threshold)
        history.append(display_grid(grid))
        plt.pause(0.02)

    return history

if 'show_run_simulation' not in st.session_state:
    st.session_state.show_run_simulation = False

def update():
    st.session_state.init_state = not st.session_state.init_state
    st.session_state.move_state = not st.session_state.move_state
    st.session_state.anim_state = not st.session_state.anim_state

if st.button("Simulation", on_click=update):
    st.session_state.show_run_simulation = True

if st.button("Tutorial", on_click=update):
    st.session_state.show_run_simulation = False
    st.rerun()

if st.session_state.show_run_simulation:
    info = st.empty()
    st.sidebar.title("Parameters")

    # Parameters
    size = int(st.sidebar.text_input("Input the grid size:", 100))  # Grid size
    threshold = float(
        st.sidebar.slider("Select the similarity threshold:", 0.0, 1.0, 0.5))  # Similarity threshold for satisfaction

    empty_ratio = 0.2  # Percentage of empty spaces
    group_ratio = 0.8  # Percentage of cells occupied by residents
    iterations = 30  # Number of iterations

    if st.sidebar.button("Run"):
        history = schelling_simulation(size, empty_ratio, group_ratio, threshold, iterations)

        def frame(i):
            ax.clear()
            ax.set_title(f"Iteration {i}")
            ax.imshow(history[i], cmap=custom_cmap)


        fig, ax = plt.subplots(figsize=(8, 6))

        anim = FuncAnimation(fig, frame, interval=50, frames=len(history), repeat=False)
        components.html(anim.to_jshtml(), height=1000)

