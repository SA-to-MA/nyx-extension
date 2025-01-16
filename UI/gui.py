import tkinter as tk
from tkinter import ttk

class ModernApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Modern Minimal GUI")
        self.geometry("400x300")
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
        self.current_frame.pack(fill="both", expand=True)

        # Call the page creation function
        self.pages[page_name]()

    def create_home_page(self):
        label = ttk.Label(self.current_frame, text="Welcome to MA Nyx and Visualization", style="TLabel")
        label.pack(pady=20)

        button1 = ttk.Button(self.current_frame, text="Solve", command=lambda: self.switch_page("Solve"))
        button2 = ttk.Button(self.current_frame, text="Visualize", command=lambda: self.switch_page("Visualize"))

        button1.pack(pady=10)
        button2.pack(pady=10)

    def create_solve_page(self):
        label = ttk.Label(self.current_frame, text="Solve", style="TLabel")
        label.pack(pady=20)
        back_button = ttk.Button(self.current_frame, text="Back to Home", command=lambda: self.switch_page("Home"))
        back_button.pack(pady=10)

    def create_vis_page(self):
        label = ttk.Label(self.current_frame, text="Visualize", style="TLabel")
        label.pack(pady=20)
        back_button = ttk.Button(self.current_frame, text="Back to Home", command=lambda: self.switch_page("Home"))
        back_button.pack(pady=10)

if __name__ == "__main__":
    app = ModernApp()
    app.mainloop()
