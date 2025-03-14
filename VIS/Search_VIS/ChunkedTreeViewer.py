import pickle
import os
import tkinter as tk
from tkinter import Label, Button


class ChunkedTreeViewerInteractive:
    def __init__(self, root, folder="search_tree"):
        """Initialize the GUI for an interactive search tree visualization."""
        self.root = root
        self.folder = folder
        self.chunks = self._get_chunk_files()
        self.current_chunk_index = 0
        self.total_chunks = len(self.chunks)
        self.node_positions = {}  # Store node positions

        if not self.chunks:
            print("[ERROR] No tree chunks found!")
            return

        # UI Elements
        self.label = Label(root, text=f"Chunk {self.current_chunk_index + 1} / {self.total_chunks}", font=("Arial", 14))
        self.label.pack()

        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")  # White background
        self.canvas.pack()

        self.prev_button = Button(root, text="Previous", command=self.prev_chunk, state=tk.DISABLED)
        self.prev_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.next_button = Button(root, text="Next", command=self.next_chunk)
        self.next_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.display_chunk(self.current_chunk_index)

    def _get_chunk_files(self):
        """Retrieve and sort the chunk files."""
        files = [f for f in os.listdir(self.folder) if f.startswith("tree_chunk_") and f.endswith(".pkl")]
        return sorted(files, key=lambda x: int(x.split("_")[-1].split(".")[0]))

    def load_chunk(self, chunk_index):
        """Load a specific chunk."""
        filename = os.path.join(self.folder, self.chunks[chunk_index])
        if not os.path.exists(filename):
            print(f"[ERROR] Chunk {chunk_index} not found.")
            return []
        with open(filename, "rb") as file:
            return pickle.load(file)

    def display_chunk(self, chunk_index):
        """Load and visualize the current chunk interactively in Tkinter."""
        nodes = self.load_chunk(chunk_index)
        if not nodes:
            print("[ERROR] No nodes in this chunk!")
            return

        self.label.config(text=f"Chunk {chunk_index + 1} / {self.total_chunks}")

        self.canvas.delete("all")  # Clear previous nodes

        self.node_positions.clear()

        # Organize nodes into levels based on their depth
        levels = {}
        for node in nodes:
            depth = node.state.depth if hasattr(node.state, "depth") else 0
            if depth not in levels:
                levels[depth] = []
            levels[depth].append(node)

        # Layout configuration for better spacing
        width, height = 800, 600
        max_depth = max(levels.keys()) if levels else 1
        y_spacing = height // (max_depth + 2)  # More spacing per level

        for depth, level_nodes in levels.items():
            x_spacing = width // (len(level_nodes) + 2)  # Avoid edge crowding
            for i, node in enumerate(level_nodes):
                x = (i + 1) * x_spacing
                y = (depth + 1) * y_spacing
                self.node_positions[node] = (x, y)

                # Draw smaller node circles
                self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="lightblue", outline="black", width=2)
                self.canvas.create_text(x, y, text=f"Node {i + 1}", font=("Arial", 10))

                # Make node clickable
                self.canvas.tag_bind(
                    self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill=""),
                    "<Button-1>", lambda event, n=node: self.on_node_click(n))

                # Draw edges to parent
                if node.parent and node.parent in self.node_positions:
                    parent_x, parent_y = self.node_positions[node.parent]
                    self.canvas.create_line(x, y - 15, parent_x, parent_y + 15, fill="black", width=2)

        # Enable/Disable buttons based on index
        self.prev_button.config(state=tk.NORMAL if chunk_index > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if chunk_index < self.total_chunks - 1 else tk.DISABLED)

    def on_node_click(self, node):
        """Handle node click event."""
        print(f"[INFO] Clicked on Node: {hash(node.state)}")
        self.label.config(text=f"Selected Node: {hash(node.state)}")

    def next_chunk(self):
        """Move to the next chunk."""
        if self.current_chunk_index < self.total_chunks - 1:
            self.current_chunk_index += 1
            self.display_chunk(self.current_chunk_index)

    def prev_chunk(self):
        """Move to the previous chunk."""
        if self.current_chunk_index > 0:
            self.current_chunk_index -= 1
            self.display_chunk(self.current_chunk_index)


# Tkinter Main Loop
root = tk.Tk()
root.title("Interactive Search Tree Viewer")
viewer = ChunkedTreeViewerInteractive(root)
root.mainloop()
