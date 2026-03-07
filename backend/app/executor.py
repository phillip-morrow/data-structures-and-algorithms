import io
import multiprocessing
import re
import traceback
from contextlib import redirect_stdout, redirect_stderr


TIMEOUT_SECONDS = 5
BANNED_IMPORTS = {"os", "sys", "subprocess", "shutil", "pathlib", "socket", "http", "urllib", "ctypes", "signal"}

ASSERT_EQ_PATTERN = re.compile(r"^assert\s+(.+?)\s*==\s*(.+)$")


def _format_assertion(test_line: str, namespace: dict) -> str:
    match = ASSERT_EQ_PATTERN.match(test_line)
    if not match:
        return "Assertion failed"
    expr, expected_expr = match.group(1).strip(), match.group(2).strip()
    try:
        actual = eval(compile(expr, "<eval>", "eval"), namespace)
        expected = eval(compile(expected_expr, "<eval>", "eval"), namespace)
        return f"Expected {expected!r}, got {actual!r}"
    except Exception:
        return "Assertion failed"


def _run_in_sandbox(user_code: str, test_code: str, result_queue: multiprocessing.Queue):
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()
    test_results = []

    for line in user_code.splitlines():
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            for banned in BANNED_IMPORTS:
                if banned in stripped:
                    result_queue.put({
                        "passed": False,
                        "output": f"Import not allowed: {banned}",
                        "test_results": [{"name": "security", "passed": False, "message": f"Blocked import: {banned}"}],
                    })
                    return

    namespace = {"__builtins__": __builtins__}

    try:
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            exec(compile(user_code, "<user_code>", "exec"), namespace)
    except Exception:
        error = traceback.format_exc()
        result_queue.put({
            "passed": False,
            "output": f"Error in your code:\n{error}",
            "test_results": [{"name": "compilation", "passed": False, "message": error}],
        })
        return

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
            msg = str(e) if str(e) else _format_assertion(test_line, namespace)
            test_results.append({"name": test_name, "passed": False, "message": msg})
        except Exception:
            all_passed = False
            error = traceback.format_exc()
            test_results.append({"name": test_name, "passed": False, "message": error})

    output = stdout_capture.getvalue()
    if stderr_capture.getvalue():
        output += "\n" + stderr_capture.getvalue()

    result_queue.put({
        "passed": all_passed,
        "output": output.strip(),
        "test_results": test_results,
    })


def execute_code(user_code: str, test_code: str) -> dict:
    result_queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=_run_in_sandbox, args=(user_code, test_code, result_queue))
    process.start()
    process.join(timeout=TIMEOUT_SECONDS)

    if process.is_alive():
        process.kill()
        process.join()
        return {
            "passed": False,
            "output": f"Time Limit Exceeded: your code took longer than {TIMEOUT_SECONDS} seconds. Check for infinite loops.",
            "test_results": [{"name": "timeout", "passed": False, "message": f"Execution exceeded {TIMEOUT_SECONDS}s"}],
        }

    if result_queue.empty():
        return {
            "passed": False,
            "output": "Code execution failed unexpectedly.",
            "test_results": [{"name": "runtime", "passed": False, "message": "Process exited without results"}],
        }

    return result_queue.get()
