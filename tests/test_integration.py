import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import glob
import pytest
from MA_PDDL.MAtoSA import SolveController


@pytest.fixture(scope="session")
def solve_controller():
    """
    Fixture to run SolveController once for all tests in the session.
    This prepares a plan file and search tree in advance.
    """
    print("[Setup] Running SolveController once for all tests...")
    controller = SolveController(
        "tests/Data/domain_blocks.pddl",
        "tests/Data/problem_blocks.pddl",
        "Blocks",
        "-t:1 -pt"
    )
    return controller

# --- Tests for successful and valid behavior ---


def test_generate_and_solve_blocks(solve_controller):
    """
    Verify that solving creates a valid plan file and a search statistics file.
    """
    plan_path = solve_controller.getPlanFile()
    assert plan_path and os.path.exists(plan_path), "Plan file was not created."

    with open(plan_path, "r") as f:
        content = f.read()
    assert any(action in content for action in ["pick-up", "stack", "unstack", "put-down"]), "Expected actions not found in the plan."

    log_files = glob.glob("stats/logs/search_stats_*.csv")
    print(f"[Test] Found {len(log_files)} search stats file(s).")
    assert len(log_files) > 0, "Search stats file was not created."


def test_get_parsed_plan_blocks(solve_controller):
    """
    Verify that the parsed plan output contains key terms like 'agent' and 'block'.
    """
    parsed = solve_controller.getParsedPlan()
    assert "pick-up" in parsed
    assert "agent" in parsed
    assert "block" in parsed


def test_search_tree_file_created():
    """
    Check that search tree chunk files (.pkl) were created after solving.
    """
    tree_files = glob.glob("VIS/Search_VIS/search_tree/tree_chunk_*.pkl")
    print(f"[Test] Found {len(tree_files)} search tree chunk(s).")
    assert len(tree_files) > 0, "Search tree chunk files were not created."


def test_search_tree_structure():
    """
    Verify that each search tree chunk file is non-empty and valid.
    """
    tree_files = glob.glob("VIS/Search_VIS/search_tree/tree_chunk_*.pkl")
    assert len(tree_files) > 0, "No search tree chunk files found."
    for tree_file in tree_files:
        assert os.path.getsize(tree_file) > 0, f"Tree chunk file {tree_file} is empty."

# --- Tests for invalid and error scenarios ---


def test_fail_on_missing_domain_file():
    """
    Expect FileNotFoundError if the domain file is missing.
    """
    with pytest.raises(FileNotFoundError):
        SolveController(
            "tests/Data/does_not_exist.pddl",
            "tests/Data/problem_blocks.pddl",
            "Blocks",
            "-t:1 -pt"
        )


def test_fail_on_missing_problem_file():
    """
    Expect FileNotFoundError if the problem file is missing.
    """
    with pytest.raises(FileNotFoundError):
        SolveController(
            "tests/Data/domain_blocks.pddl",
            "tests/Data/does_not_exist.pddl",
            "Blocks",
            "-t:1 -pt"
        )


def test_fail_on_empty_files():
    """
    Expect a specific parsing exception when domain and problem files are empty.
    """
    with pytest.raises(Exception, match="Malformed expression"):
        SolveController(
            "tests/Data/empty_domain.pddl",
            "tests/Data/empty_problem.pddl",
            "Blocks",
            "-t:1 -pt"
        )


def test_fail_on_invalid_domain_syntax():
    """
    Expect a parsing exception if the domain file has syntax errors (missing parentheses).
    """
    with pytest.raises(Exception, match="Missing close parentheses"):
        SolveController(
            "tests/Data/bad_domain.pddl",
            "tests/Data/problem_blocks.pddl",
            "Blocks",
            "-t:1 -pt"
        )


def test_fail_on_invalid_problem_file():
    """
    Expect a general exception if the problem file is structurally invalid.
    """
    with pytest.raises(Exception):
        SolveController(
            "tests/Data/domain_blocks.pddl",
            "tests/Data/bad_problem.pddl",
            "Blocks",
            "-t:1 -pt"
        )


def test_fail_on_invalid_plan_file():
    """Force the controller to parse a bad plan file and expect a fallback message."""
    solve_controller = SolveController(
        "tests/Data/domain_blocks.pddl",
        "tests/Data/problem_blocks.pddl",
        "Blocks",
        "-t:1 -pt"
    )
    solve_controller.plan = "tests/Data/bad_plan.pddl"  # Override to bad plan
    parsed = solve_controller.getParsedPlan()
    assert parsed == "Solution not found", f"Expected 'Solution not found', but got: {parsed}"


def test_invalid_config_file_format():
    """
    Pass an invalid config string and expect SolveController to still generate a plan.
    (NYX should internally handle the bad config string.)
    """
    controller = SolveController(
        "tests/Data/domain_blocks.pddl",
        "tests/Data/problem_blocks.pddl",
        "Blocks",
        "bad_flag_syntax"
    )
    plan_file = controller.getPlanFile()
    assert plan_file is not None
