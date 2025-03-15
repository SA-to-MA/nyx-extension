import pickle
import os
import pygame
import tkinter as tk
from tkinter import messagebox

# Constants
pygame.init()
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
WIDTH, HEIGHT = int(SCREEN_WIDTH * 1.2), int(SCREEN_HEIGHT * 1.2)
NODE_RADIUS = 25
BACKGROUND_COLOR = (255, 255, 255)
NODE_COLOR = (173, 216, 230)
EDGE_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)
SELECTED_COLOR = (255, 165, 0)
FONT_SIZE = 16
CHUNK_SIZE = 100  # Increase chunk size to 100 nodes

directory = "search_tree"
parent_references = {}  # Stores references for all parent-child relationships across chunks


def get_chunk_files():
    """Retrieve and sort the chunk files."""
    files = [f for f in os.listdir(directory) if f.startswith("tree_chunk_") and f.endswith(".pkl")]
    return sorted(files, key=lambda x: int(x.split("_")[-1].split(".")[0]))


def preload_parent_references():
    """Load all parent-child relationships across chunks to track missing parents."""
    global parent_references
    chunks = get_chunk_files()
    for chunk_file in chunks:
        nodes = load_chunk(chunk_file)
        for node in nodes:
            if node.parent:
                parent_references[node] = node.parent


def load_chunk(filename):
    """Load a specific chunk."""
    with open(os.path.join(directory, filename), "rb") as file:
        return pickle.load(file)


def compute_node_positions(nodes):
    """Compute positions for nodes and track missing parents."""
    levels = {}
    node_positions = {}
    missing_parents = {}  # Store missing parent references

    if not nodes:
        return node_positions, missing_parents

    for idx, node in enumerate(nodes):
        depth = node.state.depth if hasattr(node.state, "depth") else 0
        if depth not in levels:
            levels[depth] = []
        levels[depth].append((idx, node))

    max_depth = max(levels.keys()) if levels else 1
    y_spacing = HEIGHT // (max_depth + 2)

    for depth, level_nodes in levels.items():
        x_spacing = WIDTH // (len(level_nodes) + 2)
        for i, (idx, node) in enumerate(level_nodes):
            x = (i + 1) * x_spacing
            y = (depth + 1) * y_spacing
            node_positions[node] = (x, y, idx)

    for node in nodes:
        if node.parent and node.parent not in node_positions:
            missing_parents[node] = parent_references.get(node, None)

    return node_positions, missing_parents


def show_node_info(node):
    """Display node state information in a popup."""
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Node Info", f"Node State: {node.state}")


def draw_buttons(screen):
    font = pygame.font.Font(None, 24)
    next_button = pygame.Rect(WIDTH - 120, HEIGHT - 50, 100, 40)
    back_button = pygame.Rect(WIDTH - 240, HEIGHT - 50, 100, 40)
    pygame.draw.rect(screen, (200, 200, 200), next_button)
    pygame.draw.rect(screen, (200, 200, 200), back_button)
    screen.blit(font.render("Next", True, (0, 0, 0)), (WIDTH - 95, HEIGHT - 40))
    screen.blit(font.render("Back", True, (0, 0, 0)), (WIDTH - 215, HEIGHT - 40))
    return next_button, back_button


def draw_tree(screen, nodes, selected_node, node_positions, missing_parents):
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.Font(None, FONT_SIZE)

    for node, (x, y, idx) in node_positions.items():
        if node.parent and node.parent in node_positions:
            parent_x, parent_y, _ = node_positions[node.parent]
            pygame.draw.line(screen, EDGE_COLOR, (x, y - NODE_RADIUS), (parent_x, parent_y + NODE_RADIUS), 2)
        elif node in missing_parents and missing_parents[node] is not None:
            pygame.draw.line(screen, EDGE_COLOR, (x, y - NODE_RADIUS), (x, 50), 2)  # Placeholder for external parent

    for node, (x, y, idx) in node_positions.items():
        color = SELECTED_COLOR if node == selected_node else NODE_COLOR
        pygame.draw.circle(screen, color, (x, y), NODE_RADIUS)
        pygame.draw.circle(screen, EDGE_COLOR, (x, y), NODE_RADIUS, 2)
        text = font.render(str(idx), True, TEXT_COLOR)
        screen.blit(text, (x - NODE_RADIUS // 2, y - NODE_RADIUS // 2))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame Search Tree Viewer")
    clock = pygame.time.Clock()

    preload_parent_references()  # Load all parent relationships
    chunks = get_chunk_files()
    if not chunks:
        print("No chunks found.")
        return

    current_chunk_index = 0
    nodes = load_chunk(chunks[current_chunk_index])[:CHUNK_SIZE]  # Load up to CHUNK_SIZE nodes
    node_positions, missing_parents = compute_node_positions(nodes)
    selected_node = None

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        draw_tree(screen, nodes, selected_node, node_positions, missing_parents)
        next_button, back_button = draw_buttons(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if next_button.collidepoint(mx, my) and current_chunk_index < len(chunks) - 1:
                    current_chunk_index += 1
                    nodes = load_chunk(chunks[current_chunk_index])[:CHUNK_SIZE]
                    node_positions, missing_parents = compute_node_positions(nodes)
                    selected_node = None
                elif back_button.collidepoint(mx, my) and current_chunk_index > 0:
                    current_chunk_index -= 1
                    nodes = load_chunk(chunks[current_chunk_index])[:CHUNK_SIZE]
                    node_positions, missing_parents = compute_node_positions(nodes)
                    selected_node = None
                else:
                    for node, (x, y, idx) in node_positions.items():
                        if (x - mx) ** 2 + (y - my) ** 2 <= NODE_RADIUS ** 2:
                            selected_node = node
                            show_node_info(node)
                            break

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()