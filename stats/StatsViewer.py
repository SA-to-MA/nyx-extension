import os
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class StatsViewer:
    def __init__(self, log_dir="logs"):
        self.log_dir = os.path.abspath(log_dir)
        self.latest_log_path = self.get_latest_log_file()

    def get_latest_log_file(self):
        files = [f for f in os.listdir(self.log_dir) if f.endswith(".csv")]
        if not files:
            raise FileNotFoundError("No CSV log files found in logs directory.")
        latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(self.log_dir, f)))
        return os.path.join(self.log_dir, latest_file)

    def read_log_data(self):
        metadata = []
        data_start = 0

        with open(self.latest_log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line.startswith("timestamp"):
                    data_start = i
                    break
                metadata.append(line.strip())

        df = pd.read_csv(self.latest_log_path, skiprows=data_start)
        return metadata, df

    def launch(self):
        metadata, df = self.read_log_data()

        root = tk.Tk()
        root.title("Search Stats Viewer")

        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate 3/4 size
        window_width = int(screen_width * 0.75)
        window_height = int(screen_height * 0.75)

        # Center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Metadata panel
        metadata_text = tk.Text(root, height=6)
        metadata_text.insert("1.0", "\n".join(metadata))
        metadata_text.config(state="disabled")
        metadata_text.pack(fill="x", padx=10, pady=5)

        # Table Frame
        table_frame = ttk.Frame(root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Treeview (table)
        columns = list(df.columns)
        tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", stretch=True, width=100)

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        tree.pack(side="left", fill="both", expand=True)

        # Insert rows
        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        # Close Button
        button_frame = ttk.Frame(root)
        button_frame.pack(fill="x", pady=10)

        close_btn = ttk.Button(button_frame, text="Close", command=root.destroy)
        close_btn.pack(pady=5)

        root.mainloop()

# if __name__ == "__main__":
#     viewer = StatsViewer()
#     viewer.launch()

