import tkinter as tk
import solve

'''
    Tkinter is ideal here because it’s built into Python, simple to use, 
    supports structured layouts, and provides professional-looking widgets like dropdowns and buttons. 
    It’s cross-platform and allows for faster, cleaner GUI development compared to Pygame.
'''

def solve_problem():
    solve.solve_problem_page(root)


def visualize_search():
    print("Visualize Search selected!")


def visualize_plan():
    print("Visualize Plan selected!")


# Main window setup
root = tk.Tk()
root.title("MA-PDDL+ Solver")
root.geometry("800x600")
root.configure(bg="#f2e5bf")  # Soft cream background

# Title
title = tk.Label(root, text="Welcome to the MA-PDDL+ Solver", bg="#f2e5bf", fg="#257180", font=("Montserrat", 24, "bold"))
title.pack(pady=20)

# Buttons
button_frame = tk.Frame(root, bg="#f2e5bf")
button_frame.pack(pady=50)

solve_button = tk.Button(
    button_frame, text="Solve Problem", bg="#fd8b51", fg="white",
    font=("Roboto", 16), command=solve_problem  # Navigate to solve page
)
solve_button.pack(fill="x", pady=10)

visualize_search_button = tk.Button(
    button_frame, text="Visualize Search", bg="#fd8b51", fg="white",
    font=("Roboto", 16), command=visualize_search  # Placeholder for search
)
visualize_search_button.pack(fill="x", pady=10)

visualize_plan_button = tk.Button(
    button_frame, text="Visualize Plan", bg="#fd8b51", fg="white",
    font=("Roboto", 16), command=visualize_plan  # Placeholder for plan
)
visualize_plan_button.pack(fill="x", pady=10)

root.mainloop()
