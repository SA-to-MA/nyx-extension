import os
import pandas as pd
import tkinter as tk
from tkinter import ttk

class StatsViewer:
    def __init__(self, log_dir="logs"):
        self.log_dir = os.path.abspath(log_dir)
        self.latest_log_path = self.get_latest_log_file()
        self.df = None
        self.tree = None

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

        self.df = pd.read_csv(self.latest_log_path, skiprows=data_start)
        return metadata, self.df

    def launch(self):
        metadata, df = self.read_log_data()

        root = tk.Tk()
        root.title("📊 Search Stats Viewer")
        screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
        window_width, window_height = int(screen_width * 0.75), int(screen_height * 0.75)
        x, y = (screen_width - window_width) // 2, (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 🖤 Use default theme (clam overrides foreground)
        style = ttk.Style(root)
        root.configure(bg="#1e1e1e")
        style.theme_use("default")  # <- default instead of clam

        style.configure("Treeview",
                        background="#2e2e2e",
                        foreground="#ffffff",  # <- white text
                        rowheight=25,
                        fieldbackground="#2e2e2e",
                        bordercolor="#444444")
        style.configure("Treeview.Heading",
                        background="#3e3e3e",
                        foreground="#ffffff",
                        font=("Segoe UI", 10, "bold"))
        style.configure("TLabel", background="#1e1e1e", foreground="#ffffff")
        style.configure("TButton", background="#333333", foreground="#ffffff")
        style.map("TButton", background=[("active", "#444444")])

        # 📋 Metadata
        metadata_text = tk.Text(root, height=6, bg="#2e2e2e", fg="#f0f0f0", font=("Segoe UI", 10), bd=0, padx=10, pady=10)
        metadata_text.insert("1.0", "\n".join(metadata))
        metadata_text.config(state="disabled")
        metadata_text.pack(fill="x", padx=10, pady=5)

        # 🔍 Search bar
        search_frame = ttk.Frame(root)
        search_frame.pack(fill="x", padx=10, pady=(5, 0))

        ttk.Label(search_frame, text="Search:").pack(side="left")

        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var)
        search_entry.pack(side="left", fill="x", expand=True, padx=5)

        ttk.Label(search_frame, text="in column:").pack(side="left", padx=(10, 2))

        column_var = tk.StringVar()
        column_var.set(df.columns[0])
        column_dropdown = ttk.Combobox(search_frame, textvariable=column_var, values=list(df.columns), state="readonly")
        column_dropdown.pack(side="left")

        # 📊 Table
        table_frame = ttk.Frame(root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(table_frame, columns=list(df.columns), show='headings')
        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=100)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)

        # ⛳ Tags for consistent text color
        self.tree.tag_configure("default", foreground="#ffffff")
        self.tree.tag_configure("max", background="#663399", foreground="#ffffff")

        max_queue = df["queue_size"].max() if "queue_size" in df.columns else None

        def insert_rows(filtered_df):
            self.tree.delete(*self.tree.get_children())
            for _, row in filtered_df.iterrows():
                tags = ("max",) if max_queue is not None and row.get("queue_size") == max_queue else ("default",)
                self.tree.insert("", "end", values=list(row), tags=tags)

        insert_rows(df)

        # 🔍 Search logic
        def perform_search(*_):
            query = search_var.get().lower()
            col = column_var.get()
            filtered = df[df[col].astype(str).str.lower().str.contains(query)]
            insert_rows(filtered)

        search_var.trace_add("write", perform_search)
        column_var.trace_add("write", perform_search)

        # ❌ Close Button
        button_frame = ttk.Frame(root)
        button_frame.pack(fill="x", pady=10)
        ttk.Button(button_frame, text="Close", command=root.destroy).pack(pady=5)

        root.mainloop()
        try:
            os.remove(self.latest_log_path)
            print(f"Deleted stats log: {self.latest_log_path}")
        except Exception as e:
            print(f"Failed to delete stats log: {e}")


def run_stats(log_dir="logs"):
    # Create a new StatsViewer instance pointing to the specified log directory
    viewer_ = StatsViewer(log_dir)
    # Launch the stats viewer GUI
    viewer_.launch()


if __name__ == "__main__":
    viewer = StatsViewer()
    viewer.launch()
