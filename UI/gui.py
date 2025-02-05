import os
import tkinter as tk
from tkinter import ttk, filedialog
from MA_PDDL import MAtoSA
from MA_VIS import VisController
from PIL import Image, ImageTk


class ModernApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.configure(bg="#B3E5FC")  # Set light sky blue background
        # Load icons for buttons
        self.solve_icon = self.load_image("img/solve-icon.png", (30, 30))  # Size 30x30
        self.visualize_icon = self.load_image("img/visualize-icon.png", (30, 30))  # Size 30x30
        self.plan_icon = self.load_image("img/plan-icon.png", (30, 30))  # Size 30x30
        self.go_icon = self.load_image("img/go-icon.png", (30, 30))  # Size 30x30

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
            "PlanResults": self.create_plan_result_page,
            "VisResults": self.create_vis_results_page,
        }
        self.current_frame = None
        self.switch_page("Home")
        self.problem_file = ""
        self.domain_file = ""
        self.plan_file = ""
        self.plan_result = ""

    def load_image(self, path, size):
        """Loads an image and resizes it to the specified size."""
        image = Image.open(path)
        image = image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def switch_page(self, page_name):
        """Switch to a different page by destroying the current frame and creating a new one."""
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
        """Create the home page with navigation options."""
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
        # Icon for the Solve button
        solve_icon_label = tk.Label(
            self.current_frame,
            image=self.solve_icon,
            bg="#B3E5FC",
        )
        solve_icon_label.place(relx=0.35, rely=0.4, anchor="center")

        visualize_button = ttk.Button(
            self.current_frame, text="Visualize", style="Custom.TButton", command=lambda: self.switch_page("Visualize")
        )

        # Icon for the Visualize button
        visualize_icon_label = tk.Label(
            self.current_frame,
            image=self.visualize_icon,
            bg="#B3E5FC",
        )
        visualize_icon_label.place(relx=0.35, rely=0.5, anchor="center")

        solve_button.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.3)
        visualize_button.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.3)

    def select_domain_file(self):
        """Open a file dialog to select the domain file."""
        file_path = filedialog.askopenfilename(title="Select Domain File",
                                               filetypes=[("PDDL Files", "*.pddl"), ("All Files", "*.*")])
        if file_path:
            self.domain_file = file_path
            file_name = os.path.basename(file_path)  # Extract file name only
            self.domain_label_var.set(f"Selected: {file_name}")  # Update label

    def select_problem_file(self):
        """Open a file dialog to select the problem file."""
        file_path = filedialog.askopenfilename(title="Select Problem File",
                                               filetypes=[("PDDL Files", "*.pddl"), ("All Files", "*.*")])
        if file_path:
            self.problem_file = file_path
            file_name = os.path.basename(file_path)  # Extract file name only
            self.problem_label_var.set(f"Selected: {file_name}")  # Update label

    def select_plan_file(self):
        """Open a file dialog to select the plan file."""
        file_path = filedialog.askopenfilename(title="Select Plan File",
                                               filetypes=[("PDDL Files", "*.pddl"), ("All Files", "*.*")])
        if file_path:
            self.plan_file = file_path

    def handle_solve(self):
        # Check if both domain and problem files are selected
        if not self.domain_file or not self.problem_file:
            print("Error: Please select both domain and problem files before planning.")
            return

        # Call the solve function and save the result
        try:
            controller = MAtoSA.SolveController(self.domain_file, self.problem_file)
            self.plan_result = controller.solve()  # Save the plan result
            self.switch_page("PlanResults")  # Switch to the PlanResults page
        except Exception as e:
            print(f"An error occurred while planning: {e}")

    def show_solution(self):
        try:
            # Read the solution from the saved plan result
            with open(self.plan_result, "r") as file:
                solution = file.read()

            # Create a new page to display the solution
            self.current_frame.destroy()
            self.current_frame = tk.Frame(self, bg="#B3E5FC")
            self.current_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

            # Display the solution text
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

            # Add a back button to return to the Home page
            back_button = ttk.Button(
                self.current_frame,
                text="Back",
                style="Custom.TButton",
                command=lambda: self.switch_page("Home")
            )
            back_button.place(relx=0.5, rely=0.8, anchor="center", relwidth=0.3)

            # Add a button to switch to the visualization page
            vis_button = ttk.Button(
                self.current_frame,
                text="Visualize",
                style="Custom.TButton",
                command=lambda: self.switch_page("VisResults")
            )
            vis_button.place(relx=0.5, rely=0.7, anchor="center", relwidth=0.3)
        except Exception as e:
            print(f"An error occurred while reading the solution: {e}")

    def create_plan_result_page(self):
        # Create a label to display the path of the saved plan result
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

        # Add a button to show the solution
        show_button = ttk.Button(
            self.current_frame,
            text="Show Solution",
            style="Custom.TButton",
            command=lambda: self.show_solution()  # Display the solution
        )
        show_button.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.4)

        # Add a button to go back to the Home page
        back_button = ttk.Button(
            self.current_frame,
            text="Back to Home",
            style="Custom.TButton",
            command=lambda: self.switch_page("Home")
        )
        back_button.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.4)
##

    def create_solve_page(self):
        """Create the Solve page where the user can select input files and start the solving process."""
        # Title label for the Solve page
        label = tk.Label(
            self.current_frame,
            text="Solve problem",
            font=("Comic Sans MS", 24, "bold"),
            bg="#B3E5FC",
            fg="#0078D7",
        )
        label.place(relx=0.5, rely=0.1, anchor="center")

        # Variables to store the selected domain and problem file names
        self.domain_label_var = tk.StringVar(value="No file selected")
        self.problem_label_var = tk.StringVar(value="No file selected")
####################
        # Domain input label and button
        domain_label = ttk.Label(self.current_frame, text="Domain Input:", style="TLabel")
        domain_label.place(relx=0.2, rely=0.25, anchor="center")

        domain_button = ttk.Button(
            self.current_frame,
            text="Choose Domain File",
            style="File.TButton",
            command=self.select_domain_file
        )
        domain_button.place(relx=0.5, rely=0.25, anchor="center", relwidth=0.4)

        # Label to display the selected domain file name
        domain_file_label = ttk.Label(self.current_frame, textvariable=self.domain_label_var, style="TLabel")
        domain_file_label.place(relx=0.5, rely=0.3, anchor="center")

        # Problem input label and button
        problem_label = ttk.Label(self.current_frame, text="Problem Input:", style="TLabel")
        problem_label.place(relx=0.2, rely=0.4, anchor="center")

        problem_button = ttk.Button(
            self.current_frame,
            text="Choose Problem File",
            style="File.TButton",
            command=self.select_problem_file
        )
        problem_button.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.4)

        # Label to display the selected problem file name
        problem_file_label = ttk.Label(self.current_frame, textvariable=self.problem_label_var, style="TLabel")
        problem_file_label.place(relx=0.5, rely=0.45, anchor="center")

        # Button to start the solving process
        plan_button = ttk.Button(
            self.current_frame,
            text="Plan",
            style="Custom.TButton",
            command=self.handle_solve
        )
        plan_button.place(relx=0.5, rely=0.55, anchor="center", relwidth=0.3)

        # Add a back button to return to the Home page
        self.add_back_button("Home")

    def create_vis_page(self):
        """Create the Visualize page where the user can select input files for visualization."""
        # Title label for the Visualize page
        label = tk.Label(
            self.current_frame,
            text="Visualize",
            font=("Comic Sans MS", 24, "bold"),
            bg="#B3E5FC",
            fg="#0078D7",
        )
        label.place(relx=0.5, rely=0.1, anchor="center")
        self.add_back_button("Home")

        # Domain input label and button
        domain_label = ttk.Label(self.current_frame, text="Domain Input:", style="TLabel")
        domain_label.place(relx=0.2, rely=0.25, anchor="center")

        domain_button = ttk.Button(
            self.current_frame,
            text="Choose Domain File",
            command=self.select_domain_file
        )
        domain_button.place(relx=0.55, rely=0.25, anchor="center", relwidth=0.4)

        # Problem input label and button
        problem_label = ttk.Label(self.current_frame, text="Problem Input:", style="TLabel")
        problem_label.place(relx=0.2, rely=0.35, anchor="center")

        problem_button = ttk.Button(
            self.current_frame,
            text="Choose Problem File",
            command=self.select_problem_file
        )
        problem_button.place(relx=0.55, rely=0.35, anchor="center", relwidth=0.4)

        # Plan input label and button (optional)
        plan_label = ttk.Label(self.current_frame, text="Plan Input (optional):", style="TLabel")
        plan_label.place(relx=0.2, rely=0.45, anchor="center")

        plan_button = ttk.Button(
            self.current_frame,
            text="Choose Plan File",
            command=self.select_plan_file
        )
        plan_button.place(relx=0.55, rely=0.45, anchor="center", relwidth=0.4)

        # Go button to start visualization
        go_button = ttk.Button(
            self.current_frame,
            text="Go!",
            style="Custom.TButton",
            command=lambda: self.switch_page("VisResults")
        )
        go_button.place(relx=0.55, rely=0.55, anchor="center", relwidth=0.2)

        # Add a back button to return to the Home page
        self.add_back_button("Home")

    def create_vis_results_page(self):
        """Create the Visualization Results page to display the outcome of the visualization."""
        # Destroy the current frame if it exists
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self, bg="#B3E5FC")
        self.current_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Check if a plan file exists
        if hasattr(self, 'plan_file'):
            plan_file = self.plan_file
            parse = False  # No parsing needed because a plan file exists
        else:
            plan_file = ""
            parse = True  # Parsing is needed because no plan file exists

        # Call the visualization function and handle results or errors
        try:
            VisController.run(self.domain_file, self.problem_file, parse, plan_file)

            # Display a success message
            result_label = tk.Label(
                self.current_frame,
                text="Visualization completed successfully!",
                font=("Comic Sans MS", 16),
                bg="#B3E5FC",
                fg="#0078D7",
            )
            result_label.place(relx=0.5, rely=0.3, anchor="center")
        except Exception as e:
            # Display an error message if visualization fails
            error_label = tk.Label(
                self.current_frame,
                text=f"An error occurred:\n{e}",
                font=("Comic Sans MS", 14),
                bg="#B3E5FC",
                fg="#FF0000",
                wraplength=400,
            )
            error_label.place(relx=0.5, rely=0.3, anchor="center")

        # Add a button to return to the Home page
        back_button = ttk.Button(
            self.current_frame,
            text="Back to Home",
            style="Custom.TButton",
            command=lambda: self.switch_page("Home"),
        )
        back_button.place(relx=0.5, rely=0.8, anchor="center", relwidth=0.3)


if __name__ == "__main__":
    app = ModernApp()
    app.mainloop()