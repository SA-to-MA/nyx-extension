# This code is written by Yarin Benyamin.
# It is an addition to the code from the following link:
# https://github.com/SPL-BGU/ActionBasedNovelty/blob/main/heuristic_functions.py

from syntax.state import State
import syntax.constants as constants
from collections import defaultdict

actions = None
unique_names = None
curr_list = None
check_goal = None
novel_states = []


def start(grounded_instance):
    """
    Initialize the heuristic function with the given grounded instance.
    This function sets up the necessary global variables and prepares
    the heuristic function for use in the search algorithm.

    :param grounded_instance: An instance of the grounded problem.
    """
    global actions
    global unique_names
    global curr_list
    global check_goal

    actions = grounded_instance.actions

    check_goal = lambda state: grounded_instance.goals(state, constants)

    # Assuming actions is a list of objects with a 'name' attribute
    unique_names = [act.name for act in grounded_instance.domain.actions]
    unique_names += ["advance-time"]

    curr_list = [0] * len(unique_names)


def heuristic_function(state):
    global actions
    global unique_names
    global curr_list
    global check_goal
    global novel_state

    if constants.CUSTOM_HEURISTIC_ID != 0:
        if check_goal(state):
            return 0

    if constants.CUSTOM_HEURISTIC_ID == 1:
        """Custom heuristic 1: number of grounded applicable actions"""
        return 1 / len(state.applicables_actions)
    elif constants.CUSTOM_HEURISTIC_ID == 2:
        """Custom heuristic 2: count activation of predecessor action"""
        return curr_list[unique_names.index(state.predecessor_action.name)]
    elif constants.CUSTOM_HEURISTIC_ID == 3:
        """Custom heuristic 3: inverse of number of novel actions"""
        lifted_actions = list(set(act.name for act in state.applicables_actions))

        binary_string = [
            1 if action in lifted_actions else 0 for action in unique_names
        ]

        novel = 0
        for i in range(len(curr_list)):
            if binary_string[i] == 1:
                novel += 1 / (curr_list[i] + 1)

        return 1 / novel
    elif constants.CUSTOM_HEURISTIC_ID == 4:
        """Custom heuristic 4: inverse of number of novel actions + activation of predecessor action"""
        lifted_actions = list(set(act.name for act in state.applicables_actions))

        binary_string = [
            1 if action in lifted_actions else 0 for action in unique_names
        ]

        novel = 0
        for i in range(len(curr_list)):
            if binary_string[i] == 1:
                novel += 1 / (curr_list[i] + 1)

        return (1 / novel) + curr_list[
            unique_names.index(state.predecessor_action.name)
        ]
    elif constants.CUSTOM_HEURISTIC_ID == 5:
        """Custom heuristic 5: number of lifted applicable actions"""
        lifted_actions = list(set(act.name for act in state.applicables_actions))
        return 1 / len(lifted_actions)
    elif constants.CUSTOM_HEURISTIC_ID == 6:
        """Custom heuristic 6: minimum absolute difference between the states"""
        current_vars = set(state.state_vars)
        if not novel_states:
            novel_states.append(current_vars)
            return 0  # No prior states to compare with

        diffs = sorted(len(current_vars - prev_vars) for prev_vars in novel_states)
        min_diff = diffs[0]
        if min_diff != 0:
            novel_states.append(current_vars)
        elif len(diffs) > 1:
            min_diff = diffs[1]

        if min_diff == 0:
            min_diff = 0.5
        return 1 / min_diff
    elif constants.CUSTOM_HEURISTIC_ID == 7:
        """
        Custom heuristic 7:
        For multi-agent car domain, estimate how far each agent is from reaching the goal (d(a) < 30).
        Returns the maximum remaining distance among all agents (agents need to reach d(a) ≥ 30).
        """
        distances = []

        for var_key, value in state.state_vars.items():
            if var_key.startswith("['d'"):
                try:
                    distance = float(value)
                    remaining = max(0, 30 - distance)
                    distances.append(remaining)
                except (ValueError, IndexError):
                    continue

        # If no distances found, fallback to neutral heuristic
        if not distances:
            return 0

        # Choose one of:
        return max(distances)  # pessimistic: furthest agent from goal
        # return sum(distances)    # total remaining distance
        # return min(distances)    # optimistic: nearest agent to goal

    return 0


def update_novelty(state) -> None:
    """
    Update the novelty of actions based on the current state.
    This function is called when the state changes and updates
    the novelty of the actions in the global list.

    :param state: The current state of the problem.
    """
    global actions
    global unique_names
    global curr_list

    if constants.CUSTOM_HEURISTIC_ID in [2, 3, 4]:
        action = state.predecessor_action
        if action is not None:
            if action.name == "advance-time":
                return 1
            curr_list[unique_names.index(action.name)] += 1

    return
