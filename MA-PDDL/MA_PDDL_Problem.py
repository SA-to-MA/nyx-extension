import re
import sys
from pprint import pprint

class MultiAgentToSingleAgentConverter:
    def __init__(self, domain_file, problem_file):
        self.domain_file = domain_file
        self.problem_file = problem_file
        self.single_agent_domain = []
        self.single_agent_problem = []
        self.agent_types = set()

    def read_file(self, filename):
        """Reads and tokenizes the PDDL file."""
        with open(filename, 'r') as f:
            return re.sub(r';.*$', '', f.read(), flags=re.MULTILINE).splitlines()

    def parse_domain(self):
        """Parses the domain file and rewrites for single-agent."""
        domain_lines = self.read_file(self.domain_file)
        in_action = False
        current_action = []

        for line in domain_lines:
            stripped = line.strip()

            # Extract agent types from predicates or parameters
            if ':types' in stripped:
                agent_match = re.findall(r'\w+ - agent', stripped)
                self.agent_types.update([a.split()[0] for a in agent_match])

            # Detect and rewrite actions
            if stripped.startswith('(:action'):
                in_action = True
                current_action = [stripped]
                continue
            elif in_action:
                current_action.append(stripped)
                if stripped.endswith(')'):
                    in_action = False
                    # Rewrite actions for a single agent
                    self.rewrite_action(current_action)
                    current_action = []
                continue

            self.single_agent_domain.append(stripped)

    def rewrite_action(self, action_lines):
        """Rewrites multi-agent actions to single-agent compatible."""
        new_action = []
        for line in action_lines:
            if ':parameters' in line:
                # Remove agent parameters
                line = re.sub(r'\?\w+ - agent', '', line)
            new_action.append(line)
        self.single_agent_domain.extend(new_action)

    def parse_problem(self):
        """Parses the problem file and rewrites for single-agent."""
        problem_lines = self.read_file(self.problem_file)
        for line in problem_lines:
            stripped = line.strip()
            if ':objects' in stripped:
                # Remove agent objects
                line = re.sub(r'\w+ - agent', '', stripped)
            self.single_agent_problem.append(line)

    def write_to_file(self, output_domain, output_problem):
        """Writes the single-agent domain and problem to files."""
        with open(output_domain, 'w') as d:
            d.write('\n'.join(self.single_agent_domain))

        with open(output_problem, 'w') as p:
            p.write('\n'.join(self.single_agent_problem))

    def convert(self, output_domain='sa_domain.pddl', output_problem='sa_problem.pddl'):
        """Converts MA PDDL to SA PDDL and saves the results."""
        print("Parsing domain...")
        self.parse_domain()
        print("Parsing problem...")
        self.parse_problem()
        print("Writing output...")
        self.write_to_file(output_domain, output_problem)
        print("Conversion complete. Files saved:")
        print(f"  Domain: {output_domain}")
        print(f"  Problem: {output_problem}")


# Usage example
if __name__ == '__main__':
    domain_file = 'C:\\Users\\PC\\PycharmProjects\\nyx-extension\\MA-PDDL\\exMA\\car\\Car_MAPDDL_Domain'  # Replace with input domain file
    problem_file = 'C:\\Users\\PC\\PycharmProjects\\nyx-extension\\MA-PDDL\\exMA\\car\\problems\\problem_1.pddl'  # Replace with input problem file
    converter = MultiAgentToSingleAgentConverter(domain_file, problem_file)
    converter.convert()
