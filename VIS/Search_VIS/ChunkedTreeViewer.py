import pickle
import os
import pygame
from VIS.Search_VIS import BlocksTree, CarTree, MinecraftTree

# TODO: leave empty
DOMAIN = ""

# Constants
pygame.init()
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
WIDTH, HEIGHT = int(SCREEN_WIDTH * 0.9), int(SCREEN_HEIGHT * 0.9)
NODE_RADIUS = 20
BACKGROUND_COLOR = (255, 255, 255)
NODE_COLOR = (173, 216, 230)
EDGE_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)
SELECTED_COLOR = (255, 165, 0)
FONT_SIZE = 16
CHUNK_SIZE = 200  # Increase chunk size to 100 nodes
EXPANDABLE_COLOR = (100, 200, 255)  # Light blue

parent_references = {}  # Stores references for all parent-child relationships across chunks

from pathlib import Path
import subprocess

# Get the Git repo root directory
def get_repo_root() -> Path:
    return Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode().strip())

def get_chunk_files():
    """Retrieve and sort the chunk files."""
    repo_root = get_repo_root()
    directory = repo_root / "VIS/Search_VIS/search_tree"  # Always under root/logs
    files = [f for f in os.listdir(directory) if f.startswith("tree_chunk_") and f.endswith(".pkl")]
    return sorted(files, key=lambda x: int(x.split("_")[-1].split(".")[0]))

def delete_all_chunks():
    """
    Deletes all chunk files from the search_tree directory.
    Intended to be called from the GUI when the user exits the program.
    """
    try:
        repo_root = get_repo_root()
        directory = repo_root / "VIS/Search_VIS/search_tree"
        deleted_any = False # Track if any files were deleted
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if (
                    filename.startswith("tree_chunk_")
                    and filename.endswith(".pkl")
                    and os.path.isfile(file_path)  # ensures no folders touched
            ):
                os.remove(file_path)
                deleted_any = True
                print(f"Deleted: {filename}")  # Log the deleted files

        if not deleted_any:
            print("...No chunks found to delete.")
        else:
            print("All chunk files deleted.")
    except Exception as e:
        print(f"Failed to delete chunk files: {e}")

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
    repo_root = get_repo_root()
    directory = repo_root / "VIS/Search_VIS/search_tree"  # Always under root/logs
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
            node_positions[node] = (x, y, node.original_idx)  # Use permanent index

    for node in nodes:
        if node.parent and node.parent not in node_positions:
            missing_parents[node] = parent_references.get(node, None)

    return node_positions, missing_parents


def show_node_info(node):
    """Generate an overlay with structured state information, keeping the table as the background."""

    info_width, info_height = WIDTH + 25, HEIGHT * 0.3
    info_surface = pygame.Surface((info_width, info_height))
    info_surface.fill((200, 200, 200))  # Default background in case image fails
    font = pygame.font.Font(None, 24)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RESOURCES_DIR = os.path.join(BASE_DIR, "resources")

    if DOMAIN == "blocks":
        BlocksTree.render_domain(node, info_surface, font, RESOURCES_DIR, info_width, info_height)
    elif DOMAIN == "car":
        CarTree.render_domain(node, info_surface, font, RESOURCES_DIR, info_width, info_height)
    elif DOMAIN == "polycraft":
        MinecraftTree.render_domain(node, info_surface, font, RESOURCES_DIR, info_width, info_height)

    return info_surface  # Return the surface to be drawn


def draw_buttons(screen):
    font = pygame.font.Font(None, 24)
    next_button = pygame.Rect(WIDTH - 120, HEIGHT - 50, 100, 40)
    back_button = pygame.Rect(WIDTH - 240, HEIGHT - 50, 100, 40)
    pygame.draw.rect(screen, (200, 200, 200), next_button)
    pygame.draw.rect(screen, (200, 200, 200), back_button)
    screen.blit(font.render("Next", True, (0, 0, 0)), (WIDTH - 95, HEIGHT - 40))
    screen.blit(font.render("Back", True, (0, 0, 0)), (WIDTH - 215, HEIGHT - 40))
    return next_button, back_button

def draw_button(screen, rect, label, disabled=False):
    font = pygame.font.Font(None, 24)
    color = (200, 200, 200) if disabled else (150, 150, 150)
    text_color = (180, 180, 180) if disabled else (0, 0, 0)

    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (100, 100, 100), rect, 2)

    text_surface = font.render(label, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def draw_tree(screen, nodes, selected_node, node_positions, missing_parents, solution_node=None):
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.Font(None, FONT_SIZE)

    for node, (x, y, idx) in node_positions.items():
        if node.parent and node.parent in node_positions:
            parent_x, parent_y, _ = node_positions[node.parent]
            pygame.draw.line(screen, EDGE_COLOR, (x, y - NODE_RADIUS), (parent_x, parent_y + NODE_RADIUS), 2)
        elif node in missing_parents and missing_parents[node] is not None:
            pygame.draw.line(screen, EDGE_COLOR, (x, y - NODE_RADIUS), (x, 50), 2)  # Placeholder for external parent

    for node, (x, y, idx) in node_positions.items():
        if node == solution_node:
            color = (0, 200, 0)  # Green for solution
        elif node == selected_node:
            color = SELECTED_COLOR
        elif node.children and any(child not in node_positions for child in node.children):
            color = EXPANDABLE_COLOR  # Node has hidden children → can be expanded
        else:
            color = NODE_COLOR  # Leaf or fully expanded

        pygame.draw.circle(screen, color, (x, y), NODE_RADIUS)
        pygame.draw.circle(screen, EDGE_COLOR, (x, y), NODE_RADIUS, 2)

        text = font.render(str(idx), True, TEXT_COLOR)
        screen.blit(text, (x - NODE_RADIUS // 2, y - NODE_RADIUS // 2))


def show_loading_screen(screen, message="Loading..."):
    """
    Displays a loading screen with a background image and animated text.

    Args:
       screen (pygame.Surface): The surface to draw on.
       message (str): The message to show (default is "Loading...").
    """
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))  # Path to current file
        resources_dir = os.path.join(base_path, "resources")
        background_path = os.path.join(resources_dir, "loading_bg.jpg")

        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        screen.blit(background, (0, 0))
    except Exception:
        screen.fill((230, 230, 230))  # Fallback light neutral background

    font = pygame.font.SysFont("Segue UI", 48)

    text_surface = font.render(message, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    screen.blit(text_surface, text_rect)

    pygame.display.flip()


def get_visible_nodes(root_nodes, expanded_nodes):
    """
    Returns a list of nodes that are currently visible in the tree.

    A node is visible if it's a root or reachable by expanding its parent.

    Args:
        root_nodes (list): List of root nodes (nodes with no parent).
        expanded_nodes (set): Set of nodes that have been expanded.

    Returns:
        list: All currently visible nodes in the tree.
    """
    visible = set()

    def dfs(node):
        if node in visible:
            return
        visible.add(node)
        if node in expanded_nodes:
            for child in node.children:
                dfs(child)

    for root in root_nodes:
        dfs(root)

    return list(visible)

def setup_new_nodes(new_nodes, loaded_nodes, seen_indices):
    """
    Prepares newly loaded nodes by assigning them unique indices and ensuring no duplicates.

    Args:
        new_nodes (list): List of newly loaded nodes from a chunk.
        loaded_nodes (list): The master list of all currently loaded nodes.
        seen_indices (set): A set of indices already used (for avoiding duplication).
    """
    for node in new_nodes:
        if not hasattr(node, "index"):
            node.index = len(seen_indices)

        if node.index not in seen_indices:
            node.original_idx = node.index
            node.children = []
            loaded_nodes.append(node)
            seen_indices.add(node.index)

def link_parents(loaded_nodes, index_to_node):
    """
    Reconstructs parent-child relationships between nodes after loading.

    Each node’s parent is looked up via its index, and the node is added to that parent’s children list.

    Args:
        loaded_nodes (list): All currently loaded nodes.
        index_to_node (dict): Mapping of index -> node object.
    """
    for node in loaded_nodes:
        if node.parent and hasattr(node.parent, "index"):
            parent_index = node.parent.index
            if parent_index in index_to_node:
                parent_node = index_to_node[parent_index]
                if node not in parent_node.children:
                    parent_node.children.append(node)


def main(domain_name):
    global DOMAIN
    DOMAIN = domain_name
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame Search Tree Viewer")
    clock = pygame.time.Clock()

    show_loading_screen(screen, "Loading search tree...")

    preload_parent_references()
    chunks = get_chunk_files()
    current_chunk_index = 0

    loaded_nodes = []
    seen_indices = set()
    index_to_node = {}
    visible_chunks = set()

    # Load only the first chunk initially
    new_nodes = load_chunk(chunks[0])
    setup_new_nodes(new_nodes, loaded_nodes, seen_indices)
    index_to_node.update({node.index: node for node in new_nodes})
    link_parents(loaded_nodes, index_to_node)
    visible_chunks.add(0)

    root_nodes = [node for node in loaded_nodes if node.parent is None]
    expanded_nodes = set()
    visible_nodes = get_visible_nodes(root_nodes, expanded_nodes)
    node_positions, missing_parents = compute_node_positions(visible_nodes)

    selected_node = root_nodes[0] if root_nodes else None
    if selected_node:
        expanded_nodes.add(selected_node)
        visible_nodes = get_visible_nodes(root_nodes, expanded_nodes)
        node_positions, missing_parents = compute_node_positions(visible_nodes)

    node_info_surface = None
    state_window_position = (WIDTH - 520, 50)

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        draw_tree(screen, visible_nodes, selected_node, node_positions, missing_parents)

        next_button, back_button = draw_buttons(screen)
        draw_button(screen, next_button, "Next", disabled=current_chunk_index >= len(chunks) - 1)
        draw_button(screen, back_button, "Back", disabled=current_chunk_index == 0)

        if selected_node:
            if node_info_surface is None:
                node_info_surface = show_node_info(selected_node)
            screen.blit(node_info_surface, state_window_position)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if next_button.collidepoint(mx, my) and current_chunk_index < len(chunks) - 1:
                    current_chunk_index += 1
                    visible_chunks.add(current_chunk_index)
                    new_nodes = load_chunk(chunks[current_chunk_index])
                    setup_new_nodes(new_nodes, loaded_nodes, seen_indices)
                    index_to_node.update({node.index: node for node in new_nodes})
                    link_parents(loaded_nodes, index_to_node)

                    root_nodes = [node for node in loaded_nodes if node.parent is None]

                    visible_nodes = get_visible_nodes(root_nodes, expanded_nodes)
                    node_positions, missing_parents = compute_node_positions(visible_nodes)
                    node_info_surface = None

                elif back_button.collidepoint(mx, my) and current_chunk_index > 0:
                    visible_chunks.remove(current_chunk_index)
                    current_chunk_index -= 1

                    loaded_nodes = []
                    seen_indices = set()
                    index_to_node = {}
                    for i in sorted(visible_chunks):
                        chunk_nodes = load_chunk(chunks[i])
                        setup_new_nodes(chunk_nodes, loaded_nodes, seen_indices)
                        index_to_node.update({node.index: node for node in chunk_nodes})
                    link_parents(loaded_nodes, index_to_node)

                    root_nodes = [node for node in loaded_nodes if node.parent is None]
                    visible_nodes = get_visible_nodes(root_nodes, expanded_nodes)
                    node_positions, missing_parents = compute_node_positions(visible_nodes)
                    selected_node = None
                    node_info_surface = None

                else:
                    for node, (x, y, idx) in node_positions.items():
                        if (x - mx) ** 2 + (y - my) ** 2 <= NODE_RADIUS ** 2:
                            if node in expanded_nodes:
                                expanded_nodes.remove(node)
                            else:
                                expanded_nodes.add(node)

                            selected_node = node
                            visible_nodes = get_visible_nodes(root_nodes, expanded_nodes)
                            node_positions, missing_parents = compute_node_positions(visible_nodes)
                            node_info_surface = show_node_info(selected_node)
                            break

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main("polycraft")