import tkinter as tk
from tkinter import ttk, filedialog
from MA_PDDL import SolveController

class ModernApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.configure(bg="#B3E5FC")  # Light sky blue background

        self.title("SAtoMA Nyx and Visualization")
        self.geometry("800x600")

        # Create a ttk Style
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        # Customize button style
        self.style.configure(
            "Custom.TButton",
            font=("Segoe UI", 14, "bold"),
            padding=10,
            background="#0078D7",
            foreground="white",
            borderwidth=0,
            relief="flat",
        )
        self.style.map(
            "Custom.TButton",
            background=[("active", "#005A9E")],
            foreground=[("active", "white")],
        )

        # Customize label style
        self.style.configure(
            "TLabel", font=("Arial", 14), background="#B3E5FC", foreground="#2d3436"
        )

        # Initial Page
        self.pages = {
            "Home": self.create_home_page,
            "Solve": self.create_solve_page,
            "Visualize": self.create_vis_page,
            "PlanResults": self.create_result_page,
        }
        self.current_frame = None
        self.switch_page("Home")
        self.problem_file = ""
        self.domain_file = ""
        self.plan_file = ""
        self.plan_result = ""

    def switch_page(self, page_name):
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self, bg="#B3E5FC")
        self.current_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Call the page creation function
        self.pages[page_name]()

    def add_back_button(self, target_page):
        """Add a back button in the top-left corner."""
        back_label = tk.Label(
            self.current_frame, text="\u2190", bg="#B3E5FC", fg="#0078D7", font=("Arial", 20, "bold"), cursor="hand2"
        )
        back_label.place(relx=0.02, rely=0.02, anchor="nw")  # Position in the top-left corner
        back_label.bind("<Button-1>", lambda e: self.switch_page(target_page))  # Bind left-click to switch page

    def create_home_page(self):
        label = tk.Label(
            self.current_frame,
            text="Welcome to SAtoMA Nyx and Visualization",
            font=("Comic Sans MS", 24, "bold"),
            bg="#B3E5FC",
            fg="#0078D7",
            padx=10,
            pady=10,
        )
        label.place(relx=0.5, rely=0.2, anchor="center")

        solve_button = ttk.Button(
            self.current_frame, text="Solve", style="Custom.TButton", command=lambda: self.switch_page("Solve")
        )
        visualize_button = ttk.Button(
            self.current_frame, text="Visualize", style="Custom.TButton", command=lambda: self.switch_page("Visualize")
        )

        solve_button.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.3)
        visualize_button.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.3)


    def select_domain_file(self):
        file_path = filedialog.askopenfilename(title="Select Domain File",
                                               filetypes=[("PDDL Files", "*.pddl"), ("All Files", "*.*")])
        if file_path:
            self.domain_file = file_path

    def select_problem_file(self):
        file_path = filedialog.askopenfilename(title="Select Problem File",
                                               filetypes=[("PDDL Files", "*.pddl"), ("All Files", "*.*")])
        if file_path:
            self.problem_file = file_path

    def select_plan_file(self):
        file_path = filedialog.askopenfilename(title="Select Plan File",
                                               filetypes=[("PDDL Files", "*.pddl"), ("All Files", "*.*")])
        if file_path:
            self.plan_file = file_path

    def handle_solve(self):
        if not self.domain_file or not self.problem_file:
            print("Error: Please select both domain and problem files before planning.")
            return

        # Call the solve function and save the result
        try:
            self.plan_result = SolveController.solve(self.domain_file, self.problem_file)
            self.switch_page("PlanResults")
        except Exception as e:
            print(f"An error occurred while planning: {e}")

    def show_solution(self):
        try:
            with open(self.plan_result, "r") as file:
                solution = file.read()

            # Create a new page to show the solution
            self.current_frame.destroy()
            self.current_frame = tk.Frame(self, bg="#B3E5FC")
            self.current_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

            solution_label = tk.Label(
                self.current_frame,
                text=solution,
                font=("Comic Sans MS", 12),
                bg="#B3E5FC",
                fg="#333333",
                wraplength=600,
                justify="left",
            )
            solution_label.place(relx=0.5, rely=0.3, anchor="center")

            # Add a back button
            back_button = ttk.Button(
                self.current_frame,
                text="Back",
                style="Custom.TButton",
                command=lambda: self.switch_page("Home")
            )
            back_button.place(relx=0.5, rely=0.8, anchor="center", relwidth=0.3)
        except Exception as e:
            print(f"An error occurred while reading the solution: {e}")

    def create_result_page(self):
        # Create a label to display the result path
        result_label = tk.Label(
            self.current_frame,
            text=f"Plan saved to:\n{self.plan_result}",
            font=("Comic Sans MS", 16),
            bg="#B3E5FC",
            fg="#0078D7",
            wraplength=400,
            justify="center",
        )
        result_label.place(relx=0.5, rely=0.3, anchor="center")

        # Add "Show Solution" button
        show_button = ttk.Button(
            self.current_frame,
            text="Show Solution",
            style="Custom.TButton",
            command=lambda: self.show_solution()
        )
        show_button.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.4)

        # Add "Back to Home" button
        back_button = ttk.Button(
            self.current_frame,
            text="Back to Home",
            style="Custom.TButton",
            command=lambda: self.switch_page("Home")
        )
        back_button.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.4)

    def create_solve_page(self):
        label = tk.Label(
            self.current_frame,
            text="Solve problem",
            font=("Comic Sans MS", 24, "bold"),
            bg="#B3E5FC",
            fg="#0078D7",
        )
        label.place(relx=0.5, rely=0.1, anchor="center")

        domain_label = ttk.Label(self.current_frame, text="Domain Input:", style="TLabel")
        domain_label.place(relx=0.2, rely=0.25, anchor="center")

        domain_button = ttk.Button(self.current_frame, text="Choose Domain File", style="Custom.TButton",
                                   command=self.select_domain_file)
        domain_button.place(relx=0.5, rely=0.25, anchor="center", relwidth=0.4)

        problem_label = ttk.Label(self.current_frame, text="Problem Input:", style="TLabel")
        problem_label.place(relx=0.2, rely=0.35, anchor="center")

        problem_button = ttk.Button(self.current_frame, text="Choose Problem File", style="Custom.TButton",
                                    command=self.select_problem_file)
        problem_button.place(relx=0.5, rely=0.35, anchor="center", relwidth=0.4)

        plan_button = ttk.Button(self.current_frame, text="Plan", style="Custom.TButton", command=self.handle_solve)
        plan_button.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.3)

        self.add_back_button("Home")

    def create_vis_page(self):
        label = tk.Label(
            self.current_frame,
            text="Visualize",
            font=("Comic Sans MS", 24, "bold"),
            bg="#B3E5FC",
            fg="#0078D7",
        )
        label.place(relx=0.5, rely=0.1, anchor="center")
        self.add_back_button("Home")

        # תווית קלט של תחום
        domain_label = ttk.Label(self.current_frame, text="Domain Input:", style="TLabel")
        domain_label.place(relx=0.2, rely=0.25, anchor="center")

        # כפתור בחירת תחום
        domain_button = ttk.Button(self.current_frame, text="Choose Domain File", command=self.select_domain_file)
        domain_button.place(relx=0.55, rely=0.25, anchor="center", relwidth=0.4)

        # תווית קלט של בעיה
        problem_label = ttk.Label(self.current_frame, text="Problem Input:", style="TLabel")
        problem_label.place(relx=0.2, rely=0.35, anchor="center")

        # כפתור בחירת בעיה
        problem_button = ttk.Button(self.current_frame, text="Choose Problem File", command=self.select_problem_file)
        problem_button.place(relx=0.55, rely=0.35, anchor="center", relwidth=0.4)

        # תווית קלט של תכנית (אופציונלי)
        plan_label = ttk.Label(self.current_frame, text="Plan Input (optional):", style="TLabel")
        plan_label.place(relx=0.2, rely=0.45, anchor="center")

        # כפתור בחירת תכנית
        plan_button = ttk.Button(self.current_frame, text="Choose Plan File", command=self.select_plan_file)
        plan_button.place(relx=0.55, rely=0.45, anchor="center", relwidth=0.4)

        # כפתור Go
        go_button = ttk.Button(self.current_frame, text="Go!", command=self.select_plan_file)
        go_button.place(relx=0.55, rely=0.55, anchor="center", relwidth=0.2)

        self.add_back_button("Home")

if __name__ == "__main__":
    app = ModernApp()
    app.mainloop()
