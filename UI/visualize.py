import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


# Visualization for Search
def visualize_search_page(parent):
    # New window for the "Visualize Search" page
    visualize_window = tk.Toplevel(parent)
    visualize_window.title("Visualize Search")
    visualize_window.geometry("600x400")
    visualize_window.configure(bg="#f2e5bf")

    # Dropdown for domain selection
    domain_label = tk.Label(
        visualize_window,
        text="Select a Domain:",
        bg="#f2e5bf",
        fg="#257180",
        font=("Roboto", 14, "bold")
    )
    domain_label.pack(pady=10)

    selected_domain = tk.StringVar(value="Car")
    domain_dropdown = ttk.Combobox(
        visualize_window,
        textvariable=selected_domain,
        values=["Car", "Sleeping Beauty", "Special"],
        state="readonly"
    )
    domain_dropdown.pack(pady=10)

    # Dropdown for problem selection
    problem_label = tk.Label(
        visualize_window,
        text="Select a Problem:",
        bg="#f2e5bf",
        fg="#257180",
        font=("Roboto", 14, "bold")
    )
    problem_label.pack(pady=10)

    selected_problem = tk.StringVar(value="1")
    problem_dropdown = ttk.Combobox(
        visualize_window,
        textvariable=selected_problem,
        values=["1", "2", "3"],
        state="readonly"
    )
    problem_dropdown.pack(pady=10)

    # Dropdown for algorithm selection
    algorithm_label = tk.Label(
        visualize_window,
        text="Select an Algorithm:",
        bg="#f2e5bf",
        fg="#257180",
        font=("Roboto", 14, "bold")
    )
    algorithm_label.pack(pady=10)

    selected_algorithm = tk.StringVar(value="BFS")
    algorithm_dropdown = ttk.Combobox(
        visualize_window,
        textvariable=selected_algorithm,
        values=["BFS"],
        state="readonly"
    )
    algorithm_dropdown.pack(pady=10)

    # Button to start visualization
    def start_visualization():
        print(f"Domain: {selected_domain.get()}")
        print(f"Problem: {selected_problem.get()}")
        print(f"Algorithm: {selected_algorithm.get()}")
        visualize_window.destroy()

    start_button = tk.Button(
        visualize_window,
        text="Visualize",
        bg="#fd8b51",
        fg="white",
        command=start_visualization
    )
    start_button.pack(pady=20)


def visualize_plan_page(parent):
    # New window for the "Visualize Plan" page
    visualize_window = tk.Toplevel(parent)
    visualize_window.title("Visualize Plan")
    visualize_window.geometry("600x400")
    visualize_window.configure(bg="#f2e5bf")

    # Title
    title_label = tk.Label(
        visualize_window,
        text="Visualize Plan",
        bg="#f2e5bf",
        fg="#257180",
        font=("Montserrat", 18, "bold")
    )
    title_label.pack(pady=20)

    # Dropdown for domain selection
    domain_label = tk.Label(
        visualize_window,
        text="Select a Domain:",
        bg="#f2e5bf",
        fg="#257180",
        font=("Roboto", 14, "bold")
    )
    domain_label.pack(pady=10)

    selected_domain = tk.StringVar(value="Car")
    domain_dropdown = ttk.Combobox(
        visualize_window,
        textvariable=selected_domain,
        values=["Car", "Sleeping Beauty", "Special"],
        state="readonly",
        font=("Roboto", 12)
    )
    domain_dropdown.pack(pady=5, ipadx=5)

    # Line for "Choose/Upload a Plan"
    plan_label = tk.Label(
        visualize_window,
        text="Select a Plan or Upload:",
        bg="#f2e5bf",
        fg="#257180",
        font=("Roboto", 14, "bold")
    )
    plan_label.pack(pady=15)

    # Frame for plan selection and upload button
    plan_frame = tk.Frame(visualize_window, bg="#f2e5bf")
    plan_frame.pack(pady=10)

    # Dropdown for plan selection
    selected_plan = tk.StringVar(value="None")
    plan_dropdown = ttk.Combobox(
        plan_frame,
        textvariable=selected_plan,
        values=["Plan 1", "Plan 2", "Plan 3", "None"],
        state="readonly",
        font=("Roboto", 12),
        width=20
    )
    plan_dropdown.grid(row=0, column=0, padx=5, pady=10, ipadx=5)

    # Upload Plan button
    def upload_plan():
        file_path = filedialog.askopenfilename(
            title="Select Plan File",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )
        if file_path:
            print(f"Uploaded Plan: {file_path}")
            selected_plan.set("Custom Plan Uploaded")
            # Keep the window open

    upload_button = tk.Button(
        plan_frame,
        text="Upload Plan",
        bg="#fd8b51",
        fg="white",
        font=("Roboto", 12, "bold"),
        command=upload_plan,
        padx=10
    )
    upload_button.grid(row=0, column=1, padx=10)

    # Visualize button
    def start_visualization():
        domain = selected_domain.get()
        plan = selected_plan.get()
        print(f"Domain: {domain}")
        print(f"Plan: {plan if plan != 'None' else 'Custom Plan Uploaded'}")
        visualize_window.destroy()

    start_button = tk.Button(
        visualize_window,
        text="Visualize",
        bg="#fd8b51",
        fg="white",
        font=("Roboto", 14, "bold"),
        command=start_visualization,
        padx=15
    )
    start_button.pack(pady=30)