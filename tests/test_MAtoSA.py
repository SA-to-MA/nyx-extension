import unittest
from MA_PDDL.MAtoSA import MAtoSA
import os

class TestMAtoSA(unittest.TestCase):

    def test_parse_actions_from_real_domain(self):
        # This test checks that all expected actions are correctly parsed from the real domain file
        domain_path = "tests/Data/domain_blocks.pddl"
        parser = MAtoSA(domain_path, "dummy_problem.pddl")
        tokens = parser.scan_tokens(domain_path)
        actions = parser.parse_actions(tokens)

        # Check that the action names exist
        self.assertIn("pick-up", actions)
        self.assertIn("put-down", actions)
        self.assertIn("stack", actions)
        self.assertIn("unstack", actions)

        # Check the content of a specific action
        pickup = actions["pick-up"]
        self.assertEqual(pickup["params"], ['?a', '-', 'agent', '?x', '-', 'block'])
        self.assertIn("handempty", str(pickup["pre"]))
        self.assertIn("holding", str(pickup["effects"]))

    def test_generate_constraints(self):
        # This test checks that 'dif_*' preconditions are generated correctly
        parser = MAtoSA("d", "p")
        data = ['a1', 'a2', '-', 'agent', 'b1', 'b2', '-', 'block']
        result = parser.generate_constraints(data)

        self.assertIn(['dif_agent', 'a1', 'a2'], result)
        self.assertIn(['dif_block', 'b1', 'b2'], result)

    def test_process_objects_and_agents(self):
        # This test verifies that agents and objects are classified and stored properly
        parser = MAtoSA("d", "p")
        input_list = ['a', 'b', '-', 'block', [':private', 'a1', 'a2', '-', 'agent']]
        parser.process_objects_and_agents(input_list)

        self.assertIn('block', parser.objects)
        self.assertIn('a', parser.objects['block'])
        self.assertIn('a2', parser.agents.get('agent', []))

    def test_write_problem_creates_file(self):
        # This test checks that the problem file is written with correct agent/object information
        parser = MAtoSA("tests/Data/domain_blocks.pddl", "tests/Data/problem_blocks.pddl")
        parser.scan_tokens(parser.ma_problem_file)
        output_file = "tests/output_test_problem.pddl"
        parser.write_problem(output_file)

        self.assertTrue(os.path.exists(output_file))
        with open(output_file, "r") as f:
            content = f.read()
            self.assertIn("a1 - agent", content)
            self.assertIn("b - block", content)
        os.remove(output_file)

    def test_generate_action_combinations(self):
        # This test verifies that action combinations are created based on agents
        parser = MAtoSA("d", "p")
        parsed_actions = {
            "move": {
                "params": ['?a', '-', 'agent'],
                "pre": ['ready', '?a'],
                "effects": ['moved', '?a']
            }
        }
        agents = {"agent": ["a1", "a2"]}
        combos = parser.generate_action_combinations(parsed_actions, agents.items())

        self.assertTrue(any("move" in act['name'] for combo in combos for act in combo))

    def test_unify_combinations_merges_correctly(self):
        # This test checks that multiple actions are correctly unified into one
        parser = MAtoSA("d", "p")
        combinations = [
            [   {
                    "name": "move",
                    "params": ["?a1"],
                    "pre": ["ready", "?a1"],
                    "effects": ["moved", "?a1"]
                },
                {
                    "name": "load",
                    "params": ["?a2"],
                    "pre": ["loaded", "?a2"],
                    "effects": ["done", "?a2"]
                }
            ]
        ]
        unified = parser.unify_combinations(combinations)

        self.assertEqual(len(unified), 1)
        self.assertIn("move&load", unified[0]['name'])
        self.assertIn("moved", str(unified[0]['effects']))
        self.assertIn("done", str(unified[0]['effects']))

if __name__ == "__main__":
    unittest.main()
