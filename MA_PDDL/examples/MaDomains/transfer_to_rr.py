# This code is written by Yarin Benyamin.
# It is an work in progress of the code from the following link:
# https://github.com/SPL-BGU/ActionBasedNovelty/blob/main/heuristic_functions.py

import re
from pathlib import Path
from parse_pddl import preprocess_wbusy, postprocess
from functools import partial


def transform_action(match, agent_type):
    new_action, condition_lines, effect_lines = preprocess_wbusy(match)

    condition_lines += f"            (= (cur_turn) (turn ?{agent_type}))\n"
    effect_lines += f"            (increase (cur_turn) 1)\n"

    new_action = postprocess(match, new_action, condition_lines, effect_lines)

    return new_action


def transform_pddl(domain: str, problem: str, agent_types: list) -> str:
    """Transform a PDDL domain file to a roundrobin-action domain file.

    domain: str
        The path of the PDDL domain file.
    problem: str
        The path of the PDDL problem file.
    agent_types: list
        List of all the agents types
    """

    # Read the source domain file.
    with open(domain, "r") as f:
        source = f.read()

    # Ensure that the predicates block is present.
    if "(:predicates" not in source:
        source = re.sub(r"(\(:types[^\)]*\))", r"\1\n\n(:predicates)\n)", source)

    # Add lock machanism (busy) to types, predicates and functions
    busy_predicates = []
    # Search on predicates and functions
    pattern_section = r"\(:predicates([\s\S]+?)\)\s*\(:functions([\s\S]+?\))\s*\)"
    match = re.search(pattern_section, source)
    if match:
        relevant_text = match.group(1) + match.group(2)
        busy_predicates = re.findall(r"\((\w+)\)", relevant_text)
    # Combine objects
    source = re.sub(r"(\(:predicates)", rf"\1\n    (busy ?object)\n", source)
    for match in busy_predicates:
        source = re.sub(r"(\(:predicates)", rf"\1\n    (busy_{match})\n", source)

    # Add turn mechanism
    source = re.sub(
        r"(\(:functions)",
        rf"\1\n    (turn ?{agent_types[0][0]} - {agent_types[0]})\n (cur_turn)\n",
        source,
    )

    # Add plan cost mechanism
    source = re.sub(r"(\(:functions)", rf"\1\n    (plan_cost)\n", source)

    # Transform each action into durative-action
    # We use a regex to capture the parts of each action: name, parameters, precondition, effect.
    action_pattern = r"\(\:action\s+(\S+).*?:parameters\s*(\(.*?\)).*?:precondition\s+(\(and\s.*?\))\s+?:effect\s*(\(and\s.*?\)\s*\)\s*\))"

    output_domain = re.sub(
        action_pattern,
        partial(transform_action, agent_type=agent_types[0][0]),
        source,
        flags=re.DOTALL,
    )

    # Read the source problem file.
    with open(problem, "r") as f:
        problem = f.read()

    # Search for objects
    pattern_section = r"\(:objects([\s\S]+?)\)\s*"
    match = re.search(pattern_section, problem)
    if match:
        relevant_text = match.group(1)
        filtered = re.findall(r"([\w\s]+)-\s*[\w]+", relevant_text)
        objects_list = [word for m in filtered for word in m.strip().split()]
        agent_list = []
        for agent_type in agent_types:
            filtered = re.findall(rf"\n([\w\s]+)-\s*{agent_type}", relevant_text)
            agent_list += [word for m in filtered for word in m.strip().split()]
        agent_list.sort()

    pos_agents = "\n".join(["(busy {})".format(agent) for agent in agent_list])
    if len(objects_list) != 1:
        pos_agents = "(or " + pos_agents + ")"
    num_agents = len(agent_list)
    neg_objects = "\n".join(["(not (busy {}))".format(agent) for agent in objects_list])
    busy_predicates = "\n".join([f"(not (busy_{match}))" for match in busy_predicates])
    pass_time = f"""
    (:action NO_OP
        :parameters ()
        :precondition (and
            (< (cur_turn) {num_agents})
        )
        :effect (and
            (increase (cur_turn) 1)
        )
    )

    (:action PASS_TIME
        :parameters ()
        :precondition (and
            (>= (cur_turn) {num_agents})
            {pos_agents}
        )
        :effect (and
            {busy_predicates}
            {neg_objects}
            (assign (cur_turn) 1)
            (increase (plan_cost) 1)
        )
    )"""

    if output_domain.count("(") != output_domain.count(")"):
        output_domain = output_domain[:-2]

    output_domain = output_domain[:-2] + pass_time + "\n)"

    # Add turn mechanism to the problem file
    output_problem = re.sub(r"(\(:init)", rf"\1\n    (= (cur_turn) 1)", problem)
    for index, agent in enumerate(agent_list):
        output_problem = re.sub(
            r"(\(:init)", rf"\1\n    (= (turn {agent}) {index+1})", output_problem
        )

    # Add plan cost mechanism to the problem file
    output_problem = re.sub(r"(\(:init)", rf"\1\n    (= (plan_cost) 0)", output_problem)

    # Add metric to the problem file
    metric = "\n    (:metric minimize (plan_cost))"
    output_problem = output_problem[:-2] + metric + "\n)"

    return output_domain, output_problem


if __name__ == "__main__":

    domain_dir_list = ["minecraft", "sailing"]
    problem_id_list = list(range(1, 11))
    agent_types = ["agent", "boat"]

    for domain_dir in domain_dir_list:
        for problem_id in problem_id_list:
            domain = f"{domain_dir}/original_domain.pddl"
            problem = f"{domain_dir}/original_problem_{problem_id}.pddl"
            output_domain_filename = f"{domain_dir}/rr_domain_{problem_id}.pddl"
            output_problem_filename = f"{domain_dir}/rr_problem_{problem_id}.pddl"

            output_domain, output_problem = transform_pddl(
                domain, problem, agent_types=agent_types
            )

            with open(output_domain_filename, "w") as outfile:
                outfile.write(output_domain)
            with open(output_problem_filename, "w") as outfile:
                outfile.write(output_problem)

            print("Transformation complete.")
