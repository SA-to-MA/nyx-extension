import subprocess

from MA_PDDL.MAtoSA import MAtoSA


def solve(domain_file, problem_file):
    satoma = MAtoSA(domain_file, problem_file)
    new_domain = "../MA_PDDL/outputs/domain.pddl"
    new_problem = "../MA_PDDL/outputs/problem.pddl"
    satoma.generate(new_domain, new_problem)
    command = [
        'python',
        '../nyx.py',
        new_domain,
        new_problem,
        '-t:1 -pt'
    ]
    command = " ".join(command)
    subprocess.run(command, text=True, capture_output=True)
    return r'../MA_PDDL/outputs/plans/plan1_problem.pddl'