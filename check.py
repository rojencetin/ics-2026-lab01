"""
check.py · friendly test runner, in the spirit of CS50's check50.

    python3 check.py

:) means a check passed, :( means it failed (with a hint).
The autograder on GitHub runs exactly the same tests.
"""
import sys

try:
    import pytest
except ImportError:
    sys.exit("pytest is not installed. Run:  pip install -r requirements.txt")

GREEN, RED, DIM, END = "\033[32m", "\033[31m", "\033[2m", "\033[0m"
if not sys.stdout.isatty():
    GREEN = RED = DIM = END = ""


class Reporter:
    def __init__(self):
        self.passed = self.failed = 0
        self.items = {}

    @staticmethod
    def describe(item):
        return (getattr(item, "function", None).__doc__ or item.name).strip().splitlines()[0]

    def pytest_collection_modifyitems(self, items):
        self.items = {i.nodeid: i for i in items}

    def pytest_runtest_logreport(self, report):
        item = self.items.get(report.nodeid)
        if report.when == "call" or (report.when == "setup" and report.outcome != "passed"):
            desc = self.describe(item) if item else report.nodeid
            if report.passed:
                self.passed += 1
                print(f"{GREEN}:) {desc}{END}")
            else:
                self.failed += 1
                msg = str(report.longrepr.reprcrash.message) if hasattr(report.longrepr, "reprcrash") else str(report.longrepr)
                hint = msg.split("\n")[0].replace("AssertionError: ", "")
                print(f"{RED}:( {desc}{END}\n    {DIM}{hint[:300]}{END}")

    def pytest_collectreport(self, report):
        if report.failed:
            print(f"{RED}:( could not load the tests{END}\n    {report.longreprtext.strip().splitlines()[-1]}")


if __name__ == "__main__":
    r = Reporter()
    code = pytest.main(["-p", "no:terminal", "-p", "no:cacheprovider", "tests"], plugins=[r])
    total = r.passed + r.failed
    print(f"\n{r.passed}/{total} checks passed" if total else "\nno checks ran")
    if total and r.passed == total:
        print(f"{GREEN}All green. Submit with:  git add -A && git commit -m \"Lab 1\" && git push{END}")
    sys.exit(0 if code == 0 else 1)
