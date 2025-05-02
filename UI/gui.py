import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from MA_PDDL import MAtoSA
from VIS.VisController import main, run
from VIS.Search_VIS import ChunkedTreeViewer
from stats.StatsViewer import run_stats

SUPPORTED_DOMAINS = ["Blocks", "Car", "Sleeping Beauty", "PolyCraft", "Other"]


def is_valid_pddl_file(filepath, file_type):
    """
    file_type: either 'domain' or 'problem'
    """
    try:
        with open(filepath, 'r') as f:
            content = f.read().lower()
            return f"(define ({file_type}" in content
    except Exception as e:
        print(f"Failed to read file: {filepath}. Error: {e}")
        return False


class ModernApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg="#1E1E1E")  # Set background color
        self.protocol("WM_DELETE_WINDOW", self.on_closing) # Handle window close event
        # Store the base directory of images once
        self.image_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
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
            font=("Roboto", 17, "bold"),
            padding=(35, 18),
            background="#444444",
            foreground="white",
            relief="flat",
        )
        self.style.map(
            "Custom.TButton",
            background=[("active", "#666666"), ("pressed", "#777777")],
            relief=[("pressed", "sunken"), ("!pressed", "flat")]
        )

        # Customize label style (for standard text labels)
        self.style.configure(
            "Custom.TLabel",
            font=("Roboto", 14),
            background="#1E1E1E",  # Dark background
            foreground="#E0E0E0",  # Light text color
            wraplength=800,  # Ensures text remains readable
            justify="center"
        )

        # Initial Page
        self.pages = {
            "Home": self.create_home_page,
            "Solve": self.create_solve_page,
            "Visualize": self.create_vis_page,
            "PlanResults": self.create_plan_result_page,
            "VisResults": self.create_vis_results_page,
            "show_solution": self.show_solution,
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

    def on_closing(self):
        """Handle the window close event."""
        try:
            ChunkedTreeViewer.delete_all_chunks()
        except Exception as e:
            print("Failed to delete chunks:", e)

        self.destroy()

    def create_file_input(self, label_text, y_position, button_command, variable):
        """Create a labeled file input field with a selection button and a file name preview."""

        # Label for the input type (e.g. "Domain Input")
        label = ttk.Label(self.current_frame, text=label_text, style="Custom.TLabel")
        label.place(relx=0.15, rely=y_position, anchor="center")

        # Button to open file dialog
        button = ttk.Button(self.current_frame, text=f"Choose {label_text.split()[0]} File", command=button_command)
        button.place(relx=0.5, rely=y_position, anchor="center", relwidth=0.4)

        # Label to display the selected file name
        file_label = ttk.Label(self.current_frame, textvariable=variable, style="TLabel")
        file_label.place(relx=0.5, rely=y_position + 0.05, anchor="center")

    def create_dropdown_input(self, label_text, y_position, options, variable):
        """Create a dropdown input field that matches the file input fields in position and width."""

        # Label for the dropdown (same position as file input labels)
        label = ttk.Label(self.current_frame, text=label_text, style="Custom.TLabel")
        label.place(relx=0.15, rely=y_position, anchor="center")

        # Dropdown (Combobox) - matches the width and positioning of file input button
        dropdown = ttk.Combobox(self.current_frame, textvariable=variable, values=options, state="readonly", width=25)
        dropdown.place(relx=0.5, rely=y_position, anchor="center", relwidth=0.4)

        # Set default value if options exist
        if options:
            variable.set(options[0])  # Default selection

    def create_button_with_icon(self, text, y_position, command, icon=None, width=0.5, relx=0.5):
        """Create a stylish button with an icon and hover effects."""

        # Create the button with a new, modern style
        button = ttk.Button(self.current_frame, text=text, style="Custom.TButton", command=command)

        button.place(relx=relx, rely=y_position, anchor="center", relwidth=width, height=60)
        if icon:
            icon_label = tk.Label(self.current_frame, image=icon, bg="#1E1E1E")
            icon_label.place(relx=relx - 0.18, rely=y_position, anchor="center")

    def load_image(self, filename, size):
        """Load and resize an image from the app's image directory."""
        image_path = os.path.join(self.image_dir, filename)

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        image = Image.open(image_path)
        image = image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def add_back_button(self, target_page):
        """Add a back button in the top-left corner."""
        back_label = tk.Label(
            self.current_frame, text="\u2190", bg="#444444", fg="white", font=("Arial", 20, "bold"), cursor="hand2"
        )
        back_label.place(relx=0.02, rely=0.02, anchor="nw")  # Position in the top-left corner
        back_label.bind("<Button-1>", lambda e: self.switch_page(target_page))  # Bind left-click to switch page

    def switch_page(self, page_name):
        """Switch to a different page by destroying the current frame and creating a new one."""
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self, bg="#1E1E1E")  # Create a new frame
        self.current_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Call the page creation function
        self.pages[page_name]()

    def create_page_title_and_background(self, title_text, y_position=0.10):
        """Create a standardized background,  and title for all pages."""
        bg_image = tk.PhotoImage(file="img/background.png")  # Load the background image
        bg_label = tk.Label(self.current_frame, image=bg_image)
        bg_label.image = bg_image  # Keep a reference to prevent garbage collection
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fill the entire window

        glow_label = tk.Label(self.current_frame, text=title_text,
                              font=("Roboto", 26, "bold"), bg="#1E1E1E", fg="#808080")
        glow_label.place(relx=0.5, rely=y_position+0.05, anchor="center")
        label = tk.Label(self.current_frame, text=title_text,
                         font=("Roboto", 26, "bold"), bg="#1E1E1E", fg="#808080", padx=10, pady=10)  # Title label
        label.place(relx=0.5, rely=y_position+0.05, anchor="center")  # Position in the center
        # Adding a hover effect
        label.bind("<Enter>", lambda e: label.config(fg="#FFFFFF"))
        label.bind("<Leave>", lambda e: label.config(fg="#E0E0E0"))

        underline = tk.Frame(self.current_frame, bg="#A8A8A8", height=3, width=350)
        underline.place(relx=0.5, rely=0.20, anchor="center")

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

    def validate_input_files(self, next_page):
        """Validate input files"""
        if not self.domain_file or not self.problem_file:
            messagebox.showerror("Missing Input", "Please select both domain and problem files before continuing.")
            return

        # Validate domain file content
        if not is_valid_pddl_file(self.domain_file, "domain"):
            messagebox.showerror("Invalid Domain File",
                                 "The selected domain file is not valid or missing (define (domain ...) definition.")
            return

        if not is_valid_pddl_file(self.problem_file, "problem"):
            messagebox.showerror("Invalid Problem File",
                                 "The selected problem file is not valid or missing (define (problem ...) definition.")
            return

        if self.plan_file:  # If a plan file is already selected, skip planning
            print("Using existing plan file:", self.plan_file)
            self.switch_page(next_page)
            return

        print("DOMAIN FILE:", self.domain_file)
        print("PROBLEM FILE:", self.problem_file)
        print("CONFIG FILE:", self.config_file)
        print("SELECTED DOMAIN:", self.selected_domain.get())

        try:
            self.controller = MAtoSA.SolveController(self.domain_file, self.problem_file, self.selected_domain.get(),
                                                     self.config_file)
            self.plan_file = self.controller.getPlanFile()
            self.switch_page(next_page)
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Invalid Input", f"Error:\n{e}")

    def create_frame(self, y_position, height=40, width=0.97, bg="#1E1E1E"):
        """Create a reusable frame at a specific vertical position for layout alignment."""
        frame = tk.Frame(self.current_frame, bg=bg)
        frame.place(relx=0.5, rely=y_position, anchor="center", relwidth=width, height=height)
        return frame

    def create_home_page(self):
        """Create the Home page with project introduction and main navigation buttons."""
        self.create_page_title_and_background("MA-PlanX")  # Set page title and background

        subtitle = ttk.Label(
            self.current_frame,
            text="A Multi-Agent Planning and Visualization framework based on NYX,\n"
                 "designed for solving PDDL+ domains with numeric and durative actions",
            style="Custom.TLabel"
        )
        subtitle.place(relx=0.5, rely=0.25, anchor="center")

        self.create_button_with_icon(text="Solve", y_position=0.45, command=lambda: self.switch_page("Solve"), relx=0.5,
                                     icon=self.solve_icon)
        self.create_button_with_icon(text="Visualize", y_position=0.58, command=lambda: self.switch_page("Visualize"),
                                     relx=0.5, icon=self.visualize_icon)

    def create_solve_page(self):
        """Create the Solve page where the user can select input files and start the solving process."""
        self.create_page_title_and_background("Solve Problem")  # Create the title and background

        self.create_frame(0.25)
        self.create_frame(0.37)
        self.create_frame(0.49)
        self.create_frame(0.61)

        # Create domain selection dropdown
        self.create_dropdown_input("Select Domain:", 0.25, SUPPORTED_DOMAINS, self.selected_domain)

        # Create input fields
        self.create_file_input("Domain Input:", 0.37, self.select_domain_file, self.domain_label_var)
        self.create_file_input("Problem Input:", 0.49, self.select_problem_file, self.problem_label_var)
        self.create_file_input("Configuration (optional):", 0.61, self.select_config_file, self.config_label_var)

        self.create_button_with_icon(text="Plan", y_position=0.85, command=lambda: self.validate_input_files("PlanResults"),
                                     icon=self.plan_icon, relx=0.50)

        # Add a back button to return to the Home page
        self.add_back_button("Home")

    def create_plan_result_page(self):
        """Display the result after successful planning."""
        self.create_page_title_and_background("Plan saved to:")

        path_label = ttk.Label(
                self.current_frame, text=self.plan_file, style="Custom.TLabel", wraplength=300, justify="center")
        path_label.place(relx=0.5, rely=0.36, anchor="center")

        # Add a button to show the solution
        self.create_button_with_icon(text="Show Solution", y_position=0.61, command=lambda: self.show_solution(),
                                     icon=self.solve_icon)
        self.create_button_with_icon(text="Show Statistics", y_position=0.73,
                                    command=lambda: run_stats(os.path.abspath("../stats/logs")),  icon=self.go_icon)
        self.add_back_button("Solve")
        self.create_button_with_icon(text="Home", y_position=0.85, command=lambda: self.switch_page("Home"),
                                     icon=self.home_icon)

    def show_solution(self):
        """Display the parsed plan solution after successful solving."""
        # Determine if we should parse or use an existing plan file
        plan_file = self.plan_file if self.plan_file else ""
        parse = not bool(self.plan_file)
        try:
            solution = self.controller.getParsedPlan()  # Retrieve the parsed plan from the controller
            self.create_page_title_and_background("The solution:")
            # Scrollable text area for long solution output
            text_frame = tk.Frame(self.current_frame, bg="#1E1E1E")
            text_frame.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.85, relheight=0.30)

            scrollbar = tk.Scrollbar(text_frame)
            scrollbar.pack(side="right", fill="y")

            solution_text = tk.Text(text_frame, yscrollcommand=scrollbar.set, font=("Roboto", 14),
                                    bg="#1E1E1E", fg="#E0E0E0", wrap="word", relief="flat")
            solution_text.insert("1.0", solution)
            solution_text.config(state="disabled")  # Make read-only
            solution_text.pack(fill="both", expand=True)

            scrollbar.config(command=solution_text.yview)

            # Navigation buttons
            self.add_back_button("PlanResults")
            self.create_button_with_icon(text="Visualize", y_position=0.61,
                                         command=lambda: run(self.selected_domain.get(), self.domain_file, self.problem_file, parse, plan_file,
                              self.config_file), icon=self.visualize_icon)
            self.create_button_with_icon(text="Show search tree", y_position=0.73,
                                         command=lambda: ChunkedTreeViewer.main(self.selected_domain.get().lower())
                                            , icon=self.solve_icon)
            self.create_button_with_icon(text="Home", y_position=0.85, command=lambda: self.switch_page("Home"),
                                         icon=self.home_icon)

        except Exception as e:
            messagebox.showerror("Solution Error", f"An error occurred while reading the solution:\n{e}")

    def create_vis_page(self):
        """Create the 'Visualize' page where the user selects input files and initiates the visualization process."""
        self.create_page_title_and_background("Visualize")  # Set title and background

        # Layout placeholders for input sections
        self.create_frame(0.25)  # Dropdown
        self.create_frame(0.35)  # Domain file
        self.create_frame(0.45)  # Problem file
        self.create_frame(0.55)  # Plan file (optional)
        self.create_frame(0.65)  # Config file (optional)

        # Input fields
        self.create_dropdown_input("Select Domain:", 0.25, SUPPORTED_DOMAINS, self.selected_domain)
        self.create_file_input("Domain Input:", 0.35, self.select_domain_file, self.domain_label_var)
        self.create_file_input("Problem Input:", 0.45, self.select_problem_file, self.problem_label_var)
        self.create_file_input("Plan Input (optional):", 0.55, self.select_plan_file, self.plan_label_var)
        self.create_file_input("Configuration (optional):", 0.65, self.select_config_file, self.config_label_var)

        # Action button
        self.create_button_with_icon(text="Visualize solution", y_position=0.85,
                                     command=lambda: self.validate_input_files("VisResults"), icon=self.go_icon, relx=0.50)
        # Navigation
        self.add_back_button("Home")

    def create_vis_results_page(self):
        """Run the visualization and display a result message or error."""
        # Determine if we should parse or use an existing plan file
        plan_file = self.plan_file if self.plan_file else ""
        parse = not bool(self.plan_file)

        try:
            run(self.selected_domain.get(), self.domain_file, self.problem_file, parse, plan_file,
                              self.config_file)  # Run the visualization with the selected inputs
            self.create_page_title_and_background("Visualization completed successfully!")
            #self.create_button_with_icon(text="Visualize search tree", y_position=0.68,
            #                             command=lambda: self.switch_page("STVisualize"), icon=self.go_icon, relx=0.50)
        except Exception as e:
            messagebox.showerror("Visualization Error", f"An error occurred while visualizing:\n{e}")

        self.add_back_button("Visualize")
        self.create_button_with_icon(text="Home", y_position=0.85, command=lambda: self.switch_page("Home"),
                                     icon=self.home_icon)


if __name__ == "__main__":
    app = ModernApp()
    app.mainloop()


