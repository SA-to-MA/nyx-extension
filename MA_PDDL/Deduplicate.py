# Yarin added
import re

def transform_pddl(
    domain: str,
    output_domain_filename: str,
):
    """Transform a PDDL domain file to a joint-action domain file.

    domain: str
        The path of the PDDL domain file.
    output_domain_filename: str
        The path of the output domain file.
    """

    # Read the source domain file.
    with open(domain, "r") as f:
        source = f.read()

    # Check each action if have duplicate variables
    # We use a regex to capture the parts of each action: name, parameters, precondition, effect.
    action_pattern = r"\(\:action\s+(\S+).*?:parameters\s*(\(.*?\)).*?:precondition\s+(\(and\s.*?\))\s+?:effect\s*(\(and\s.*?\)\s*\)\s*\))"

    def transform_action(match):
        def duplicate_detection(block: list) -> tuple:
            """
            Process the preconditions or effects block.
            lines: list
                The lines of the block
            return: bool
                True if duplicate variable detected, False otherwise
            """
            condition = block
            condition = re.sub(r"^\(and", "", condition).strip()
            if condition.endswith(")"):
                condition = condition[:-1].strip()
            condition = [
                line.strip() for line in condition.splitlines() if line.strip()
            ]

            dup_detection = []
            for cond in condition:
                if cond == ")":
                    continue
                if cond.count("(") != cond.count(")"):
                    cond = cond[:-1]
                con = cond[1:-1]
                if "(" in con:
                    match = re.search(r"\((.*?)\)", con)
                    var = match.group(1)
                else:
                    var = cond[1:-1]
                lst = var.split(" ")
                if lst[-1] == "":
                    lst = lst[:-1]
                if len(lst) == 1:
                    if var in dup_detection:
                        return True
                    else:
                        dup_detection.append(var)

            return False

        # Check the preconditions
        precond_block = match.group(3).strip()
        precond_detected = duplicate_detection(precond_block)

        # Check the effects
        effect_block = match.group(4).strip()
        effect_detected = duplicate_detection(effect_block)

        if effect_detected or precond_detected:
            return ""
        return match.group().strip()

    new_str = re.sub(action_pattern, transform_action, source, flags=re.DOTALL)

    with open(output_domain_filename, "w") as outfile:
        outfile.write(new_str)