import io
import sys
import traceback
from contextlib import redirect_stdout, redirect_stderr


TIMEOUT_SECONDS = 5
BANNED_IMPORTS = {"os", "sys", "subprocess", "shutil", "pathlib", "socket", "http", "urllib", "ctypes", "signal"}


def execute_code(user_code: str, test_code: str) -> dict:
    """
    Execute user code then run test assertions against it.

    Returns dict with:
      - passed: bool
      - output: str (combined stdout + errors)
      - test_results: list of {name, passed, message}
    """
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()
    test_results = []

    for line in user_code.splitlines():
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            for banned in BANNED_IMPORTS:
                if banned in stripped:
                    return {
                        "passed": False,
                        "output": f"Import not allowed: {banned}",
                        "test_results": [{"name": "security", "passed": False, "message": f"Blocked import: {banned}"}],
                    }

    namespace = {"__builtins__": __builtins__}

    try:
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            exec(compile(user_code, "<user_code>", "exec"), namespace)
    except Exception:
        error = traceback.format_exc()
        return {
            "passed": False,
            "output": f"Error in your code:\n{error}",
            "test_results": [{"name": "compilation", "passed": False, "message": error}],
        }

    test_lines = [t.strip() for t in test_code.strip().splitlines() if t.strip() and not t.strip().startswith("#")]
    all_passed = True

    for i, test_line in enumerate(test_lines):
        test_name = f"Test {i + 1}: {test_line[:60]}"
        try:
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(compile(test_line, "<test>", "exec"), namespace)
            test_results.append({"name": test_name, "passed": True, "message": "Passed"})
        except AssertionError as e:
            all_passed = False
            test_results.append({"name": test_name, "passed": False, "message": str(e) or "Assertion failed"})
        except Exception:
            all_passed = False
            error = traceback.format_exc()
            test_results.append({"name": test_name, "passed": False, "message": error})

    output = stdout_capture.getvalue()
    if stderr_capture.getvalue():
        output += "\n" + stderr_capture.getvalue()

    return {
        "passed": all_passed,
        "output": output.strip(),
        "test_results": test_results,
    }
