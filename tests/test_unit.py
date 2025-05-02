import pytest
import os
import sys

# Make sure we can import properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from MA_PDDL.MAtoSA import MAtoSA, SolveController
from UI.gui import is_valid_pddl_file
from VIS.Search_VIS.BlocksTree import random_color, parse_state

# ------------------------------
# Tests for VIS/Search_VIS/BlocksTree
# ------------------------------

def test_random_color_range():
    """Test that random_color() returns a tuple of three integers between 0 and 255."""
    color = random_color()
    assert isinstance(color, tuple)
    assert len(color) == 3
    assert all(0 <= c <= 255 for c in color)


def test_parse_state_basic():
    """Test parsing of a simple block-world state."""
    state_vars = {
        "['on', 'a', 'b']": True,
        "['ontable', 'b']": True,
        "['holding', 'agent1', 'c']": True,
        "['handempty', 'agent2']": True,
        "['on', 'c', 'a']": False  # Should be ignored
    }
    parsed = parse_state(state_vars)

    assert parsed["on"]["a"] == "b"
    assert "b" in parsed["ontable"]
    assert parsed["holding"]["agent1"] == "c"
    assert "agent2" in parsed["handempty"]
    assert "c" not in parsed["on"]


def test_parse_state_empty():
    """Test parsing an empty state dictionary."""
    parsed = parse_state({})
    assert parsed["on"] == {}
    assert parsed["ontable"] == []
    assert parsed["holding"] == {}
    assert parsed["handempty"] == []


# ------------------------------
# Tests for file validation
# ------------------------------

def test_is_valid_pddl_file_domain(tmp_path):
    """Test detection of a valid domain PDDL file."""
    domain_file = tmp_path / "domain.pddl"
    domain_file.write_text("(define (domain blocks))")
    assert is_valid_pddl_file(str(domain_file), "domain")


def test_is_valid_pddl_file_problem(tmp_path):
    """Test detection of a valid problem PDDL file."""
    problem_file = tmp_path / "problem.pddl"
    problem_file.write_text("(define (problem blocks-problem))")
    assert is_valid_pddl_file(str(problem_file), "problem")


def test_is_valid_pddl_file_invalid(tmp_path):
    """Test that a non-PDDL file is rejected."""
    invalid_file = tmp_path / "invalid.txt"
    invalid_file.write_text("This is not a valid PDDL content.")
    assert not is_valid_pddl_file(str(invalid_file), "domain")


# ------------------------------
# Tests for SolveController - plan parsing
# ------------------------------

def test_get_parsed_plan_solution_not_found():
    """Test that SolveController returns 'Solution not found' for missing plan file."""
    controller = SolveController(
        "tests/Data/domain_blocks.pddl",
        "tests/Data/problem_blocks.pddl",
        "Blocks",
        "-t:1 -pt"
    )
    controller.plan = "tests/Data/non_existent_plan.pddl"  # Force a non-existing plan
    parsed = controller.getParsedPlan()
    assert parsed == "Solution not found"


# ------------------------------
# Tests for MAtoSA core methods
# ------------------------------

def test_parse_actions_from_real_domain():
    """Test that expected actions are parsed correctly from domain."""
    domain_path = "tests/Data/domain_blocks.pddl"
    parser = MAtoSA(domain_path, "tests/Data/problem_blocks.pddl")
    tokens = parser.scan_tokens(domain_path)
    actions = parser.parse_actions(tokens)

    assert "pick-up" in actions
    assert "put-down" in actions
    assert "stack" in actions
    assert "unstack" in actions

    pickup = actions["pick-up"]
    assert pickup["params"] == ['?a', '-', 'agent', '?x', '-', 'block']
    assert any("handempty" in str(cond) for cond in pickup["pre"])
    assert any("holding" in str(cond) for cond in pickup["effects"])


def test_generate_constraints():
    """Test generating 'dif_*' constraints between different types."""
    parser = MAtoSA("tests/Data/domain_blocks.pddl", "tests/Data/problem_blocks.pddl")
    data = ['a1', 'a2', '-', 'agent', 'b1', 'b2', '-', 'block']
    constraints = parser.generate_constraints(data)

    assert ['dif_agent', 'a1', 'a2'] in constraints
    assert ['dif_block', 'b1', 'b2'] in constraints


def test_process_objects_and_agents():
    """Test proper separation of objects and agents."""
    parser = MAtoSA("tests/Data/domain_blocks.pddl", "tests/Data/problem_blocks.pddl")
    input_list = ['a', 'b', '-', 'block', [':private', 'a1', 'a2', '-', 'agent']]
    parser.process_objects_and_agents(input_list)

    assert "block" in parser.objects
    assert 'a' in parser.objects["block"]
    assert 'a2' in parser.agents.get("agent", [])


def test_write_problem_creates_file(tmp_path):
    """Test that a problem file is correctly generated and saved."""
    parser = MAtoSA("tests/Data/domain_blocks.pddl", "tests/Data/problem_blocks.pddl")
    parser.scan_tokens(parser.ma_problem_file)

    output_file = tmp_path / "output_test_problem.pddl"
    parser.write_problem(str(output_file))

    assert output_file.exists()
    content = output_file.read_text()
    assert "a1 - agent" in content
    assert "b - block" in content


def test_generate_action_combinations():
    """Test that action combinations are generated for agents."""
    parser = MAtoSA("tests/Data/domain_blocks.pddl", "tests/Data/problem_blocks.pddl")
    parsed_actions = {
        "move": {
            "params": ['?a', '-', 'agent'],
            "pre": ['ready', '?a'],
            "effects": ['moved', '?a']
        }
    }
    agents = {"agent": ["a1", "a2"]}
    combos = parser.generate_action_combinations(parsed_actions, agents.items())

    assert any("move" in act["name"] for combo in combos for act in combo)


def test_unify_combinations_merges_correctly():
    """Test that multiple actions are unified correctly."""
    parser = MAtoSA("tests/Data/domain_blocks.pddl", "tests/Data/problem_blocks.pddl")
    combinations = [
        [
            {"name": "move", "params": ["?a1"], "pre": ["ready", "?a1"], "effects": ["moved", "?a1"]},
            {"name": "load", "params": ["?a2"], "pre": ["loaded", "?a2"], "effects": ["done", "?a2"]}
        ]
    ]
    unified = parser.unify_combinations(combinations)

    assert len(unified) == 1
    assert "move&load" in unified[0]["name"]
    assert any("moved" in str(effect) for effect in unified[0]["effects"])
    assert any("done" in str(effect) for effect in unified[0]["effects"])

