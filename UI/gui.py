import tkinter as tk
from tkinter import ttk, filedialog


class ModernApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Modern Minimal GUI")
        self.geometry("800x600")  # גודל ברירת מחדל
        self.configure(bg="#f5f5f5")

        # Create a ttk Style
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        # Customize button style
        self.style.configure("TButton", font=("Arial", 12), padding=10, background="#0984e3", foreground="white")
        self.style.map("TButton",
                       background=[("active", "#74b9ff")],
                       foreground=[("active", "white")])

        # Customize label style
        self.style.configure("TLabel", font=("Arial", 14), background="#f5f5f5", foreground="#2d3436")

        # Initial Page
        self.pages = {
            "Home": self.create_home_page,
            "Solve": self.create_solve_page,
            "Visualize": self.create_vis_page,
        }
        self.current_frame = None
        self.switch_page("Home")

    def switch_page(self, page_name):
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self, bg="#f5f5f5")
        self.current_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Call the page creation function
        self.pages[page_name]()

    def add_back_button(self, target_page):
        """Add a back button in the top-left corner."""
        back_label = tk.Label(
            self.current_frame, text="←", bg="#f5f5f5", fg="black", font=("Arial", 24, "bold"), cursor="hand2"
        )
        back_label.place(relx=0.02, rely=0.02, anchor="nw")  # Position in the top-left corner
        back_label.bind("<Button-1>", lambda e: self.switch_page(target_page))  # Bind left-click to switch page

    def create_home_page(self):
        label = ttk.Label(self.current_frame, text="Welcome to SAtoMA Nyx and Visualization", style="TLabel")
        label.place(relx=0.5, rely=0.2, anchor="center")

        button1 = ttk.Button(self.current_frame, text="Solve", command=lambda: self.switch_page("Solve"))
        button2 = ttk.Button(self.current_frame, text="Visualize", command=lambda: self.switch_page("Visualize"))

        button1.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.3)
        button2.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.3)

    def select_domain_file(self):
        file_path = filedialog.askopenfilename(title="Select Domain File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            print(f"Selected Domain File: {file_path}")

    def select_problem_file(self):
        file_path = filedialog.askopenfilename(title="Select Problem File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            print(f"Selected Problem File: {file_path}")

    def create_solve_page(self):
        label = ttk.Label(self.current_frame, text="Solve", style="TLabel")
        label.place(relx=0.5, rely=0.1, anchor="center")

        domain_label = ttk.Label(self.current_frame, text="Domain Input:", style="TLabel")
        domain_label.place(relx=0.2, rely=0.25, anchor="center")

        domain_button = ttk.Button(self.current_frame, text="Choose Domain File", command=self.select_domain_file)
        domain_button.place(relx=0.5, rely=0.25, anchor="center", relwidth=0.4)

        problem_label = ttk.Label(self.current_frame, text="Problem Input:", style="TLabel")
        problem_label.place(relx=0.2, rely=0.35, anchor="center")

        problem_button = ttk.Button(self.current_frame, text="Choose Problem File", command=self.select_problem_file)
        problem_button.place(relx=0.5, rely=0.35, anchor="center", relwidth=0.4)

        plan_button = ttk.Button(self.current_frame, text="Plan", command=lambda: print("Plan button clicked"))
        plan_button.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.3)

        self.add_back_button("Home")

    def create_vis_page(self):
        label = ttk.Label(self.current_frame, text="Visualize", style="TLabel")
        label.place(relx=0.5, rely=0.1, anchor="center")
        self.add_back_button("Home")


if __name__ == "__main__":
    app = ModernApp()
    app.mainloop()
