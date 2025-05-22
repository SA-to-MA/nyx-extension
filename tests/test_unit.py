import pytest
import os
import sys
from pathlib import Path

# Set paths relative to this test file
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Data"

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from MA_PDDL.MAtoSA import MAtoSA, SolveController
from UI.gui import is_valid_pddl_file
from VIS.Search_VIS.BlocksTree import random_color, parse_state

# ------------------------------
# Tests for VIS/Search_VIS/BlocksTree
# ------------------------------

def test_random_color_range():
    """Test that the function returns a valid RGB color tuple between 0 and 255."""
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

# ------------------------------
# Tests for SolveController - plan parsing
# ------------------------------

def test_get_parsed_plan_solution_not_found():
    """Test that SolveController returns 'Solution not found' for missing plan file."""
    controller = SolveController(
        str(DATA_DIR / "domain_blocks.pddl"),
        str(DATA_DIR / "problem_blocks.pddl"),
        "Blocks",
        "-t:1 -pt"
    )
    controller.plan = str(DATA_DIR / "non_existent_plan.pddl")
    parsed = controller.getParsedPlan()
    assert "Solution not found" in parsed

# ------------------------------
# Tests for MAtoSA core methods
# ------------------------------

def test_parse_actions_from_real_domain():
    """Test parsing of all expected actions from a real domain file. """
    domain_path = str(DATA_DIR / "domain_blocks.pddl")
    problem_path = str(DATA_DIR / "problem_blocks.pddl")
    parser = MAtoSA(domain_path, problem_path)
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
    """ Test generating unique constraints (dif_*) between different objects."""
    parser = MAtoSA(str(DATA_DIR / "domain_blocks.pddl"), str(DATA_DIR / "problem_blocks.pddl"))
    data = ['a1', 'a2', '-', 'agent', 'b1', 'b2', '-', 'block']
    constraints = parser.generate_constraints(data)

    assert ['dif_agent', 'a1', 'a2'] in constraints
    assert ['dif_block', 'b1', 'b2'] in constraints


def test_process_objects_and_agents():
    """Test correct categorization of agents and objects from input list."""
    parser = MAtoSA(str(DATA_DIR / "domain_blocks.pddl"), str(DATA_DIR / "problem_blocks.pddl"))
    input_list = ['a', 'b', '-', 'block', [':private', 'a1', 'a2', '-', 'agent']]
    parser.process_objects_and_agents(input_list)

    assert "block" in parser.objects
    assert 'a' in parser.objects["block"]
    assert 'a2' in parser.agents.get("agent", [])


def test_write_problem_creates_file(tmp_path):
    """Test that a problem file is correctly generated and saved."""
    parser = MAtoSA(str(DATA_DIR / "domain_blocks.pddl"), str(DATA_DIR / "problem_blocks.pddl"))
    parser.scan_tokens(parser.ma_problem_file)

    output_file = tmp_path / "output_test_problem.pddl"
    parser.write_problem(str(output_file))

    assert output_file.exists()
    content = output_file.read_text()
    assert "a1 - agent" in content
    assert "b - block" in content


def test_generate_action_combinations():
    """Test generation of all possible combinations of actions across agents."""
    parser = MAtoSA(str(DATA_DIR / "domain_blocks.pddl"), str(DATA_DIR / "problem_blocks.pddl"))
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
    """Test merging multiple single-agent actions into one joint action."""
    parser = MAtoSA(str(DATA_DIR / "domain_blocks.pddl"), str(DATA_DIR / "problem_blocks.pddl"))
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
