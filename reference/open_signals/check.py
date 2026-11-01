"""Check every synthetic vector against the reference implementation.

Usage, from the repository root:

    PYTHONPATH=reference python3 -m open_signals.check spec/vectors

Exit status 0 when every vector passes, 1 otherwise.
"""

import json
import math
import pathlib
import sys

from .rules import RULES

REL_TOL = 1e-9
ABS_TOL = 1e-9


def matches(expected, actual):
    """Expected is a subset of actual; numbers compare with a small tolerance."""
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(
            k in actual and matches(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        return (isinstance(actual, list) and len(expected) == len(actual)
                and all(matches(e, a) for e, a in zip(expected, actual)))
    if isinstance(expected, bool) or isinstance(actual, bool):
        return expected is actual
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        return math.isclose(expected, actual, rel_tol=REL_TOL, abs_tol=ABS_TOL)
    return expected == actual


def run_vector(vector):
    """Return None when the vector passes, else a message."""
    func = RULES.get(vector["rule"])
    if func is None:
        return "no implementation for rule %s" % vector["rule"]
    want_error = vector.get("expect_error")
    try:
        actual = func(vector["inputs"])
    except ValueError as exc:
        if want_error and want_error in str(exc):
            return None
        return "raised %r" % str(exc)
    except Exception as exc:  # a crash is a failed vector, not a crashed run
        return "crashed: %s: %s" % (type(exc).__name__, exc)
    if want_error:
        return "expected an error containing %r, got %r" % (want_error, actual)
    if not matches(vector["expected"], actual):
        return "expected %r, got %r" % (vector["expected"], actual)
    return None


def load_vectors(directory):
    vectors = []
    for path in sorted(pathlib.Path(directory).glob("*.json")):
        with open(path, encoding="utf-8") as handle:
            for vector in json.load(handle)["vectors"]:
                vectors.append((path.name, vector))
    return vectors


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    directory = argv[0] if argv else "spec/vectors"
    vectors = load_vectors(directory)
    if not vectors:
        print("no vectors found in %s" % directory)
        return 1
    failures = 0
    for name, vector in vectors:
        problem = run_vector(vector)
        if problem:
            failures += 1
            print("FAIL %s %s [%s]: %s" % (name, vector["id"], vector["rule"], problem))
    print("%d vectors, %d passed, %d failed" % (len(vectors), len(vectors) - failures, failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
