import pickle
import os
import pygame
from VIS.Search_VIS import BlocksTree, CarTree, MinecraftTree, SailingTree
from pathlib import Path
import subprocess

# --- Constants and Setup ---
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
EXPANDABLE_COLOR = (100, 200, 255)
DOMAIN = ""
index_counter = [1]

# --- Utility Functions ---
def get_repo_root() -> Path:
    return Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode().strip())

def get_latest_tree_file():
    repo_root = get_repo_root()
    directory = repo_root / "VIS/Search_VIS/search_tree"
    files = [f for f in os.listdir(directory) if f.startswith("search_tree_") and f.endswith(".pkl")]
    if not files:
        raise FileNotFoundError("No search tree files found.")
    return str(directory / sorted(files, key=lambda f: float(f.split("_")[-1][:-4]))[-1])

def load_full_tree():
    file_path = get_latest_tree_file()
    with open(file_path, "rb") as file:
        root = pickle.load(file)
    return root

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
                    filename.startswith("search_tree_")
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

# --- Node Handling ---
def compute_node_positions(nodes):
    levels = {}
    node_positions = {}

    # Sort potential root nodes by current index (if any) to pick the lowest
    root_nodes = sorted(
        [node for node in nodes if getattr(node.state, "depth", 0) == 0],
        key=lambda n: getattr(n, "index", float("inf"))
    )

    # Assign index 1 to the root node if it doesn't have one
    if root_nodes:
        root = root_nodes[0]
        if not hasattr(root, "index"):
            root.index = index_counter[0]
            index_counter[0] += 1

    # Assign levels and missing indices
    for node in nodes:
        if not hasattr(node, "index"):
            node.index = index_counter[0]
            index_counter[0] += 1
        depth = getattr(node.state, "depth", 0)
        levels.setdefault(depth, []).append(node)

    # Calculate spacing
    max_depth = max(levels.keys(), default=1)
    y_spacing = HEIGHT // (max_depth + 2)

    for depth, level_nodes in levels.items():
        x_spacing = WIDTH // (len(level_nodes) + 2)
        for i, node in enumerate(level_nodes):
            x = (i + 1) * x_spacing
            y = (depth + 1) * y_spacing
            node_positions[node] = (x, y, node.index)

    return node_positions

def draw_tree(screen, nodes, selected_node, node_positions):
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.Font(None, FONT_SIZE)

    for node, (x, y, idx) in node_positions.items():
        if node.parent in node_positions:
            parent_x, parent_y, _ = node_positions[node.parent]
            pygame.draw.line(screen, EDGE_COLOR, (x, y - NODE_RADIUS), (parent_x, parent_y + NODE_RADIUS), 2)

    for node, (x, y, idx) in node_positions.items():
        color = SELECTED_COLOR if node == selected_node else (EXPANDABLE_COLOR if node.children else NODE_COLOR)
        pygame.draw.circle(screen, color, (x, y), NODE_RADIUS)
        pygame.draw.circle(screen, EDGE_COLOR, (x, y), NODE_RADIUS, 2)
        text = font.render(str(idx), True, TEXT_COLOR)
        screen.blit(text, (x - NODE_RADIUS // 2, y - NODE_RADIUS // 2))

def show_node_info(node):
    info_width, info_height = WIDTH + 25, HEIGHT * 0.3
    info_surface = pygame.Surface((info_width, info_height))
    info_surface.fill((200, 200, 200))
    font = pygame.font.Font(None, 24)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RESOURCES_DIR = os.path.join(BASE_DIR, "resources")
    if DOMAIN == "blocks":
        BlocksTree.render_domain(node, info_surface, font, RESOURCES_DIR, info_width, info_height)
    elif DOMAIN == "car":
        CarTree.render_domain(node, info_surface, font, RESOURCES_DIR, info_width, info_height)
    elif DOMAIN == "polycraft":
        MinecraftTree.render_domain(node, info_surface, font, RESOURCES_DIR, info_width, info_height)
    elif DOMAIN == "sailing":
        SailingTree.render_domain(node, info_surface, font, RESOURCES_DIR, info_width, info_height)
    return info_surface

def get_visible_nodes(root_node, expanded_nodes):
    visible = set()
    def dfs(node):
        if node in visible:
            return
        visible.add(node)
        if node in expanded_nodes:
            for child in node.children:
                dfs(child)
    dfs(root_node)
    return list(visible)

# --- Loading ---
def show_loading_screen(screen, message="Loading tree..."):
    repo_root = get_repo_root()
    bg_path = repo_root / "VIS" / "Search_VIS" / "resources" / "loading_bg.jpg"

    background_image = pygame.image.load(bg_path).convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    screen.blit(background_image, (0, 0))  # Draw background image
    font = pygame.font.SysFont(None, 48)
    text_surface = font.render(message, True, (255, 255, 255))  # Black text
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

# --- Main Function ---
def main(domain_name):
    global DOMAIN
    DOMAIN = domain_name
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    show_loading_screen(screen)
    pygame.display.set_caption("Pygame Search Tree Viewer")
    clock = pygame.time.Clock()

    root_node = load_full_tree()
    expanded_nodes = set()
    selected_node = root_node
    expanded_nodes.add(root_node)

    visible_nodes = get_visible_nodes(root_node, expanded_nodes)
    node_positions = compute_node_positions(visible_nodes)
    node_info_surface = show_node_info(selected_node)

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        draw_tree(screen, visible_nodes, selected_node, node_positions)
        if node_info_surface:
            screen.blit(node_info_surface, (WIDTH - 520, 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for node, (x, y, _) in node_positions.items():
                    if (x - mx) ** 2 + (y - my) ** 2 <= NODE_RADIUS ** 2:
                        if node in expanded_nodes:
                            expanded_nodes.remove(node)
                        else:
                            expanded_nodes.add(node)
                        selected_node = node
                        visible_nodes = get_visible_nodes(root_node, expanded_nodes)
                        node_positions = compute_node_positions(visible_nodes)
                        node_info_surface = show_node_info(selected_node)
                        break

        clock.tick(30)
    pygame.quit()

if __name__ == "__main__":
    main("polycraft")
