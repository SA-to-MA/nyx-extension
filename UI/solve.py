import tkinter as tk
from tkinter import ttk


def solve_problem_page(parent):
    # New window for the "Solve Problem" page
    solve_window = tk.Toplevel(parent)
    solve_window.title("Solve Problem")
    solve_window.geometry("600x400")
    solve_window.configure(bg="#f2e5bf")

    # Dropdown menu
    dropdown_label = tk.Label(solve_window, text="Choose Domain", bg="#f2e5bf", fg="#257180", font=("Roboto", 14, "bold"))
    dropdown_label.pack(pady=10)

    selected_domain = tk.StringVar(value="Car")
    dropdown = ttk.Combobox(solve_window, textvariable=selected_domain, values=["Car", "Sleeping Beauty", "Special"], state="readonly")
    dropdown.pack(pady=10)

    # Radio buttons
    radio_frame = tk.Frame(solve_window, bg="#f2e5bf")
    radio_frame.pack(pady=20)

    radio_choice = tk.StringVar(value="Generate Manually")

    generate_radio = tk.Radiobutton(
        radio_frame, text="Generate Manually", variable=radio_choice, value="Generate Manually", bg="#f2e5bf"
    )
    generate_radio.pack(anchor="w")

    generate_subtext = tk.Label(radio_frame, text="Generate MA-PDDL+ File", bg="#f2e5bf", fg="gray")
    generate_subtext.pack(anchor="w", padx=20)

    upload_radio = tk.Radiobutton(
        radio_frame, text="Upload MA-PDDL+ File", variable=radio_choice, value="Upload MA-PDDL+ File", bg="#f2e5bf"
    )
    upload_radio.pack(anchor="w")

    upload_subtext = tk.Label(radio_frame, text="Insert your own problem file", bg="#f2e5bf", fg="gray")
    upload_subtext.pack(anchor="w", padx=20)

    # Next button
    def next_button_action():
        print(f"Selected Domain: {selected_domain.get()}")
        print(f"Selected Option: {radio_choice.get()}")
        solve_window.destroy()

    next_button = tk.Button(solve_window, text="Next →", bg="#fd8b51", fg="white", command=next_button_action)
    next_button.pack(pady=20)
