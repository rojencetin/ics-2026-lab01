"""Tests for Lab 1. Run them with:  python3 check.py   (or: python3 -m pytest)"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRATCH = r"https://scratch\.mit\.edu/projects/\d+/?"


def readme():
    return (ROOT / "README.md").read_text(encoding="utf-8")


def answers():
    out = {}
    for line in (ROOT / "answers.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip().lower()] = v.strip()
    return out


# Part A ---------------------------------------------------------------------

def test_meow_link():
    """Part A: README links your meow project"""
    m = re.search(r"Meow:\s*(" + SCRATCH + ")", readme())
    assert m, "no scratch.mit.edu/projects/ link after 'Meow:' in README.md (Share → Copy Link in Scratch)"


# Part B ---------------------------------------------------------------------

def test_project_link():
    """Part B: README links your own project"""
    m = re.search(r"Project:\s*(" + SCRATCH + ")", readme())
    assert m, "no scratch.mit.edu/projects/ link after 'Project:' in README.md"


def test_project_description():
    """Part B: README describes your project (at least 20 words after the link)"""
    text = readme().split("Project:", 1)[-1]
    text = re.sub(SCRATCH, "", text).replace("(write here)", "")
    words = re.findall(r"[A-Za-zÇĞİÖŞÜçğıöşü]{2,}", text.split("One or two sentences")[-1])
    assert len(words) >= 20, f"write one or two sentences about your project under Part B ({len(words)} words so far)"


# Part C ---------------------------------------------------------------------

def test_binary_answers():
    """Part C: 13, 42 and 100 in binary (q1–q3)"""
    a = answers()
    expected = {"q1": "00001101", "q2": "00101010", "q3": "01100100"}
    for k, v in expected.items():
        assert a.get(k) == v, f"{k} should be the 8-bit binary of {int(v, 2)}, got {a.get(k)!r}"


def test_decimal_and_ascii():
    """Part C: 10101010 in decimal (q4) and the ASCII text 01001000 01101001 (q5)"""
    a = answers()
    assert a.get("q4") == "170", f"q4: 10101010 in decimal, got {a.get('q4')!r}"
    assert a.get("q5") == "Hi", f"q5: decode the two bytes with the ASCII table (case matters), got {a.get('q5')!r}"


def test_byte_and_search():
    """Part C: values in a byte (q6) and binary-search steps for a billion (q7)"""
    a = answers()
    assert a.get("q6") == "256", f"q6: how many values fit in 8 bits? got {a.get('q6')!r}"
    assert a.get("q7") in {"30", "31"}, f"q7: look at the lecture's search table, got {a.get('q7')!r}"


# Part D ---------------------------------------------------------------------

def test_pseudocode():
    """Part D: pseudocode has 6+ numbered steps, an 'if' and a loop, and is not the example"""
    text = (ROOT / "pseudocode.txt").read_text(encoding="utf-8")
    assert "Pick up the first paper" not in text, "replace the example algorithm with your own"
    steps = re.findall(r"^\s*\d+[.)]?\s+\S", text, re.M)
    assert len(steps) >= 6, f"need at least 6 numbered lines, found {len(steps)}"
    low = text.lower()
    assert " if " in low or low.strip().startswith("if"), "use at least one 'if' step"
    assert any(w in low for w in ["go back to line", "repeat", "while", "until"]), "use a loop: 'go back to line N', 'repeat', 'while' or 'until'"
