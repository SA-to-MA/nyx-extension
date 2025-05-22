# This code is written by Yarin Benyamin.
# It is an work in progress of the code from the following link:
# https://github.com/SPL-BGU/ActionBasedNovelty/blob/main/heuristic_functions.py

import re


def process_block(block: list) -> tuple:
    """
    Process the preconditions or effects block.
    block: list
        The lines of the main block.
    """

    condition = block
    condition = re.sub(r"^\(and", "", condition).strip()
    if condition.endswith(")"):
        condition = condition[:-1].strip()
    condition = [line.strip() for line in condition.splitlines() if line.strip()]

    funcs = set()
    condition_lines = ""
    for cond in condition:
        if cond == ")":
            continue
        if cond.count("(") != cond.count(")"):
            cond = cond[:-1]

        con = cond[1:-1]
        if "(" in con:
            match = re.search(r"\((.*?)\)", con)
            if match:
                var = match.group(1)
            else:
                continue
        else:
            var = cond[1:-1]
        if len(var.split(" ")) == 1:
            funcs.add(var)

        condition_lines += f"            {cond}\n"

    return condition_lines, funcs


def preprocess(match) -> tuple:
    """ "
    Preprocess the action block."
    match: re.Match
        The match object.
    return: tuple
        The new action, parameters block, condition lines, precond funcs, effect lines, effect funcs.
    """

    action_name = match.group(1).strip()
    new_action = f"    (:action {action_name}\n"

    parameters_block = match.group(2).strip()
    new_action += f"        :parameters {parameters_block}\n"

    precond_block = match.group(3).strip()
    effect_block = match.group(4).strip()

    # Transform the preconditions
    condition_lines, precond_funcs = process_block(precond_block)

    # Transform the effects
    effect_lines, effect_funcs = process_block(effect_block)

    return (
        new_action,
        parameters_block,
        condition_lines,
        precond_funcs,
        effect_lines,
        effect_funcs,
    )


def preprocess_wbusy(match) -> tuple:
    """
    Preprocess the action block with busy mechanism.
    match: re.Match
        The match object.
    return: tuple
        The new action, condition lines, effect lines.
    """

    (
        new_action,
        parameters_block,
        condition_lines,
        precond_funcs,
        effect_lines,
        effect_funcs,
    ) = preprocess(match)

    parameters = parameters_block[1:-1].split(" ")
    parameters = [token for token in parameters if token.startswith("?")]
    for parameter in parameters:
        condition_lines += f"            (not (busy {parameter}))\n"
        effect_lines += f"            (busy {parameter})\n"
    for func in precond_funcs.union(effect_funcs):
        condition_lines += f"            (not (busy_{func}))\n"
        effect_lines += f"            (busy_{func})\n"

    return new_action, condition_lines, effect_lines


def postprocess(match, new_action, condition_lines, effect_lines) -> str:
    """
    Postprocess the action block.
    match: re.Match
        The match object.
    new_action: str
        The new action block.
    condition_lines: str
        The condition lines.
    effect_lines: str
        The effect lines.
    return: str
        The new action block.
    """

    new_action += "        :precondition (and\n" + condition_lines + "        )\n"
    new_action += "        :effect (and\n" + effect_lines + "        )"

    match = match.group().strip()
    if match.count("(") > match.count(")"):
        new_action += "\n"
    else:
        new_action += ")\n"

    return new_action
