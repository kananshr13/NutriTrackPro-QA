import json
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone


PROJECT_ROOT = Path(__file__).resolve().parent.parent

XML_FILE = PROJECT_ROOT / "reports" / "test-results.xml"
OUTPUT_FILE = PROJECT_ROOT / "dashboard" / "data" / "test-results.json"


def get_status(testcase):
    """
    Determine the final status of a pytest test case.
    """

    if testcase.find("failure") is not None:
        return "failed"

    if testcase.find("error") is not None:
        return "error"

    if testcase.find("skipped") is not None:
        return "skipped"

    return "passed"


def get_failure_message(testcase):
    """
    Extract useful failure information when a test fails.
    """

    failure = testcase.find("failure")

    if failure is not None:
        return failure.get("message") or failure.text or ""

    error = testcase.find("error")

    if error is not None:
        return error.get("message") or error.text or ""

    return ""


def get_test_cases(root):
    """
    Extract individual test cases from the JUnit XML file.
    """

    tests = []

    for testcase in root.iter("testcase"):

        name = testcase.get("name", "Unknown test")
        classname = testcase.get("classname", "")
        duration = float(testcase.get("time", 0))

        # Example classname:
        #
        # automation.api.test_auth
        #
        # We use the final meaningful module name as the suite.
        suite = classname.split(".")[-1]

        if suite.startswith("test_"):
            suite = suite[5:]

        suite = suite.replace("_", " ").title()

        status = get_status(testcase)

        tests.append(
            {
                "name": name,
                "suite": suite,
                "status": status,
                "duration": round(duration, 3),
                "details": get_failure_message(testcase),
            }
        )

    return tests


def generate_report():
    if not XML_FILE.exists():
        raise FileNotFoundError(
            f"Pytest XML report not found: {XML_FILE}\n"
            "Run pytest with --junitxml=reports/test-results.xml first."
        )

    tree = ET.parse(XML_FILE)
    root = tree.getroot()

    test_cases = get_test_cases(root)

    total = len(test_cases)

    passed = sum(
        1 for test in test_cases
        if test["status"] == "passed"
    )

    failed = sum(
        1 for test in test_cases
        if test["status"] == "failed"
    )

    errors = sum(
        1 for test in test_cases
        if test["status"] == "error"
    )

    skipped = sum(
        1 for test in test_cases
        if test["status"] == "skipped"
    )

    duration = sum(
        test["duration"]
        for test in test_cases
    )

    pass_rate = (
        round((passed / total) * 100, 2)
        if total
        else 0
    )

    suites = {}

    for test in test_cases:

        suite_name = test["suite"]

        if suite_name not in suites:
            suites[suite_name] = {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "errors": 0,
            }

        suites[suite_name]["total"] += 1

        if test["status"] == "passed":
            suites[suite_name]["passed"] += 1

        elif test["status"] == "failed":
            suites[suite_name]["failed"] += 1

        elif test["status"] == "skipped":
            suites[suite_name]["skipped"] += 1

        elif test["status"] == "error":
            suites[suite_name]["errors"] += 1

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),

        "summary": {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "errors": errors,
            "pass_rate": pass_rate,
            "duration": round(duration, 3),
        },

        "suites": suites,

        "tests": test_cases,
    }

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=2
        )

    print("QA report generated successfully.")
    print(f"Input:  {XML_FILE}")
    print(f"Output: {OUTPUT_FILE}")
    print()
    print(f"Total:    {total}")
    print(f"Passed:   {passed}")
    print(f"Failed:   {failed}")
    print(f"Skipped:  {skipped}")
    print(f"Errors:   {errors}")
    print(f"Pass rate: {pass_rate}%")
    print(f"Duration: {round(duration, 3)}s")


if __name__ == "__main__":
    generate_report()