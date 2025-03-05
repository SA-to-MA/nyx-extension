import os
import tkinter as tk
from tkinter import ttk, filedialog
from MA_PDDL import MAtoSA
from VIS import VisController
from PIL import Image, ImageTk
from pathlib import Path

SUPPORTED_DOMAINS = ["Blocks", "Car", "Sleeping Beauty", "Other"]


class ModernApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.configure(bg="#B3E5FC")  # Set light sky blue background
        # Load icons for buttons
        self.solve_icon = self.load_image("solve-icon.png", (30, 30))  # Size 30x30
        self.visualize_icon = self.load_image("visualize-icon.png", (30, 30))  # Size 30x30
        self.plan_icon = self.load_image("plan-icon.png", (30, 30))  # Size 30x30
        self.go_icon = self.load_image("go-icon.png", (30, 30))  # Size 30x30
        self.home_icon = self.load_image("home-icon.png", (30, 30))  # Size 30x30

        self.title("SAtoMA Nyx and Visualization")  # Set window title
        self.geometry("800x600")  # Set window size

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
        self.config_file = ""
        self.controller = None
        self.selected_domain = tk.StringVar()

        self.domain_label_var = tk.StringVar(value="No file selected")  # Initialize with default text
        self.problem_label_var = tk.StringVar(value="No file selected")
        self.plan_label_var = tk.StringVar(value="No file selected")
        self.config_label_var = tk.StringVar(value="No file selected")

    def create_dropdown_input(self, label_text, y_position, options, variable):
        """Create a dropdown input field that matches the file input fields in position and width."""

        # Label for the dropdown (same position as file input labels)
        label = ttk.Label(self.current_frame, text=label_text, style="TLabel")
        label.place(relx=0.2, rely=y_position, anchor="center")

        # Dropdown (Combobox) - matches the width and positioning of file input button
        dropdown = ttk.Combobox(self.current_frame, textvariable=variable, values=options, state="readonly", width=25)
        dropdown.place(relx=0.55, rely=y_position, anchor="center", relwidth=0.4)

        # Set default value if options exist
        if options:
            variable.set(options[0])  # Default selection

    def create_button_with_icon(self, text, y_position, command, icon=None, width=0.3, relx=0.5):
        """Create a button with an icon positioned to the left of the button."""
        # Create the button
        button = ttk.Button(self.current_frame, text=text, style="Custom.TButton", command=command)
        button.place(relx=relx, rely=y_position, anchor="center", relwidth=width)

        # Position the icon just left to the button
        if icon:
            icon_label = tk.Label(self.current_frame, image=icon, bg="#B3E5FC",)
            # Adjust relx to position it closer to the left edge of the button
            icon_label.place(relx=relx+0.05 - (width / 2) - 0.05, rely=y_position, anchor="center")

    def load_image(self, filename, size):
        """Loads an image and resizes it to the specified size."""
        # Get the directory where gui.py is located
        base_path = os.path.dirname(os.path.abspath(__file__))

        # Construct the absolute path to the image inside UI/img/
        image_path = os.path.join(base_path, "img", filename)  # Use filename directly

        # Ensure the file exists before opening
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        # Open, resize, and convert to Tkinter PhotoImage
        image = Image.open(image_path)
        image = image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def add_back_button(self, target_page):
        """Add a back button in the top-left corner."""
        back_label = tk.Label(
            self.current_frame, text="\u2190", bg="#B3E5FC", fg="#0078D7", font=("Arial", 20, "bold"), cursor="hand2"
        )
        back_label.place(relx=0.02, rely=0.02, anchor="nw")  # Position in the top-left corner
        back_label.bind("<Button-1>", lambda e: self.switch_page(target_page))  # Bind left-click to switch page

    def create_file_input(self, label_text, y_position, button_command, variable):  # Create a file input field

        # Label for input
        label = ttk.Label(self.current_frame, text=label_text, style="TLabel")
        label.place(relx=0.2, rely=y_position, anchor="center")

        # Button for file selection
        button = ttk.Button(
            self.current_frame,
            text=f"Choose {label_text.split()[0]} File",
            command=button_command
        )
        button.place(relx=0.55, rely=y_position, anchor="center", relwidth=0.4)

        # Display selected file name
        file_label = ttk.Label(self.current_frame, textvariable=variable, style="TLabel")
        file_label.place(relx=0.55, rely=y_position + 0.05, anchor="center")

    def switch_page(self, page_name):
        """Switch to a different page by destroying the current frame and creating a new one."""
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self, bg="#B3E5FC")  # Create a new frame
        self.current_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Call the page creation function
        self.pages[page_name]()

    def create_home_page(self):
        """Create the home page with navigation options."""
        label = tk.Label(self.current_frame, text="Welcome to SAtoMA Nyx and Visualization",
                         font=("Comic Sans MS", 24, "bold"), bg="#B3E5FC", fg="#0078D7", padx=10, pady=10)
        label.place(relx=0.5, rely=0.2, anchor="center")

        # Solve button with icon
        self.create_button_with_icon(text="Solve", y_position=0.4, command=lambda: self.switch_page("Solve"),
                                     icon=self.solve_icon)

        # Visualize button with icon
        self.create_button_with_icon(text="Visualize", y_position=0.5, command=lambda: self.switch_page("Visualize"),
                                     icon=self.visualize_icon)

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
            file_name = os.path.basename(file_path)  # Extract file name only
            self.plan_label_var.set(f"Selected: {file_name}")  # Update label

    def select_config_file(self):
        """Open a file dialog to select the config file."""
        file_path = filedialog.askopenfilename(title="Select Config File",
                                               filetypes=[("TXT Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.config_file = file_path
            file_name = os.path.basename(file_path)  # Extract file name only
            self.config_label_var.set(f"Selected: {file_name}")  # Update label

    def handle_solve(self):
        # Check if both domain and problem files are selected
        if not self.domain_file or not self.problem_file:
            print("Error: Please select both domain and problem files before planning.")
            return

        # Call the solve function and save the result
        try:
            self.controller = MAtoSA.SolveController(self.domain_file, self.problem_file, self.selected_domain.get(), self.config_file)
            self.plan_file = self.controller.getPlanFile()  # Save the plan result
            self.switch_page("PlanResults")  # Switch to the PlanResults page
        except Exception as e:
            print(f"An error occurred while planning: {e}")

    def show_solution(self):
        try:
            solution = self.controller.getParsedPlan()

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

            # Add a back button to return to the previous page using "add_back_button" method
            self.add_back_button("PlanResults")
            # add a button to switch to the previous page using "create_button_with_icon" method
            self.create_button_with_icon(text="Visualize", y_position=0.7, command=lambda: self.switch_page("VisResults"), icon=self.visualize_icon)
            self.create_button_with_icon(text="Home", y_position=0.8, command=lambda: self.switch_page("Home"), icon=self.home_icon)

        except Exception as e:
            print(f"An error occurred while reading the solution: {e}")

    def create_plan_result_page(self):
        # Create a label to display the path of the saved plan result
        result_label = tk.Label(
            self.current_frame,
            text=f"Plan saved to:\n{self.plan_file}",
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

        # Add a back button to return to the previous page using "add_back_button" method
        self.add_back_button("Solve")
        self.create_button_with_icon(text="home", y_position=0.7, command=lambda: self.switch_page("home"), icon=self.home_icon)

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

        # Create domain selection dropdown
        self.create_dropdown_input("Select Domain:", 0.25, SUPPORTED_DOMAINS, self.selected_domain)

        # Create input fields
        self.create_file_input("Domain Input:", 0.35, self.select_domain_file, self.domain_label_var)
        self.create_file_input("Problem Input:", 0.5, self.select_problem_file, self.problem_label_var)
        self.create_file_input("Configuration (optional):", 0.65, self.select_config_file, self.config_label_var)

        self.create_button_with_icon(text="Plan", y_position=0.8,  command=self.handle_solve, icon=self.plan_icon, relx=0.54) # Plan button

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

        # Create domain selection dropdown
        self.create_dropdown_input("Select Domain:", 0.25, SUPPORTED_DOMAINS, self.selected_domain)

        # Create input fields
        self.create_file_input("Domain Input:", 0.35, self.select_domain_file, self.domain_label_var)
        self.create_file_input("Problem Input:", 0.45, self.select_problem_file, self.problem_label_var)
        self.create_file_input("Plan Input (optional):", 0.55, self.select_plan_file, self.plan_label_var)
        self.create_file_input("Configuration (optional):", 0.65, self.select_config_file, self.config_label_var)

        self.create_button_with_icon(text="Go!", y_position=0.8,  command=lambda: self.switch_page("VisResults"), icon=self.go_icon, relx=0.54)  # Plan button

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
        if len(self.plan_file) != 0:
            plan_file = self.plan_file
            parse = False  # No parsing needed because a plan file exists
        else:
            plan_file = ""
            parse = True  # Parsing is needed because no plan file exists

        # Call the visualization function and handle results or errors
        try:
            VisController.run(self.selected_domain.get(), self.domain_file, self.problem_file, parse, plan_file, self.config_file)

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

        # Add a button to return to the last page using "add_back_button" method
        self.add_back_button("Visualize")
        self.create_button_with_icon(text="Home", y_position=0.8, command=lambda: self.switch_page("Home"), icon=self.home_icon)


if __name__ == "__main__":
    app = ModernApp()
    app.mainloop()