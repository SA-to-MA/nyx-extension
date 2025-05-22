import sys
import os
import glob
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


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

    log_files = glob.glob(os.path.join("stats", "logs", "search_stats_*.csv"))
    assert len(log_files) > 0, "Search stats file was not created."


def test_get_parsed_plan_blocks(solve_controller):
    """
    Check that parsed plan contains meaningful structured output.
    """
    parsed = solve_controller.getParsedPlan()
    assert "pick-up" in parsed
    assert "agent" in parsed
    assert "block" in parsed

# --- Tests for invalid and error scenarios ---


def test_fail_on_missing_domain_file():
    """
    Raise FileNotFoundError if domain file is missing.
    """
    with pytest.raises(FileNotFoundError):
        SolveController(
            os.path.join("tests", "Data", "missing_domain.pddl"),
            os.path.join("tests", "Data", "problem_blocks.pddl"),
            "Blocks",
            "-t:1 -pt"
        )


def test_fail_on_missing_problem_file():
    """
    Raise FileNotFoundError if problem file is missing.
    """
    with pytest.raises(FileNotFoundError):
        SolveController(
            os.path.join("tests", "Data", "domain_blocks.pddl"),
            os.path.join("tests", "Data", "missing_problem.pddl"),
            "Blocks",
            "-t:1 -pt"
        )


def test_fail_on_empty_files():
    """
    Expect parsing error if domain and problem files are empty.    """
    with pytest.raises(Exception, match="Malformed expression"):
        SolveController(
            os.path.join("tests", "Data", "empty_domain.pddl"),
            os.path.join("tests", "Data", "empty_problem.pddl"),
            "Blocks",
            "-t:1 -pt"
        )


def test_fail_on_invalid_domain_syntax():
    """
    Raise error when domain file has invalid PDDL syntax.
    """
    with pytest.raises(Exception, match="Missing close parentheses"):
        SolveController(
            os.path.join("tests", "Data", "bad_domain.pddl"),
            os.path.join("tests", "Data", "problem_blocks.pddl"),
            "Blocks",
            "-t:1 -pt"
        )


def test_fail_on_invalid_problem_file():
    """
   Raise error if if the problem file is structurally invalid.
    """
    with pytest.raises(Exception):
        SolveController(
            os.path.join("tests", "Data", "domain_blocks.pddl"),
            os.path.join("tests", "Data", "bad_problem.pddl"),
            "Blocks",
            "-t:1 -pt"
        )


def test_fail_on_invalid_plan_file():
    """Force the controller to parse a bad plan file and expect a fallback message."""
    controller = SolveController(
        os.path.join("tests", "Data", "domain_blocks.pddl"),
        os.path.join("tests", "Data", "problem_blocks.pddl"),
        "Blocks",
        "-t:1 -pt"
    )
    controller.plan = os.path.join("tests", "Data", "bad_plan.pddl")
    parsed = controller.getParsedPlan()
    assert "MALFORMED" in parsed


def test_invalid_config_file_format():
    """
    Pass an invalid config string and expect SolveController to still generate a plan.
    (NYX should internally handle the bad config string.)
    """
    controller = SolveController(
        os.path.join("tests", "Data", "domain_blocks.pddl"),
        os.path.join("tests", "Data", "problem_blocks.pddl"),
        "Blocks",
        "bad_flag_syntax"
    )
    plan_file = controller.getPlanFile()
    assert plan_file is not None

