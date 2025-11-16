# src/utils/router.py
import re
from typing import Optional, Tuple

# number pattern (integers and decimals, optional leading sign)
_NUM = r"-?\d+(?:\.\d+)?"

# operator words (order longer phrases first where relevant)
_OP_WORDS = [
    "divided by",
    "divided",
    "divide",
    "multiply",
    "times",
    "plus",
    "add",
    "minus",
    "subtract",
]

# map words/symbols to normalized operators
OPERATOR_MAP = {
    "+": "+",
    "plus": "+",
    "add": "+",

    "-": "-",
    "minus": "-",
    "subtract": "-",

    "*": "*",
    "x": "*",
    "times": "*",
    "multiply": "*",

    "/": "/",
    "÷": "/",
    "divide": "/",
    "divided": "/",
    "divided by": "/",
}

# Precompiled common regexes
# 1) symbol between numbers: e.g., "10-4", "10 - 4"
_SYMBOL_BETWEEN = re.compile(rf"^\s*({_NUM})\s*([+\-*/×÷])\s*({_NUM})\s*$", re.IGNORECASE)
# 2) number word number: "50 minus 25", "5 plus 3"
_WORD_BETWEEN = re.compile(
    rf"^\s*({_NUM})\s+({'|'.join(re.escape(w) for w in _OP_WORDS)})\s+({_NUM})\s*$",
    re.IGNORECASE,
)
# 3) verb-first: "multiply 4 and 6", "divide 8 by 2"
_VERB_FIRST = re.compile(
    rf"^\s*({'|'.join(re.escape(w) for w in _OP_WORDS)})\s+({_NUM})(?:\s*(?:and|by)\s*({_NUM}))\s*$",
    re.IGNORECASE,
)
# 4) subtract X from Y (reversed order): "subtract 5 from 10"
_SUBTRACT_FROM = re.compile(
    rf"^\s*(subtract|minus)\s+({_NUM})\s+from\s+({_NUM})\s*$", re.IGNORECASE
)

# 5) loose search variants for when user types longer sentences (not strict anchors)
_LOOSE_SYMBOL = re.compile(rf"({_NUM})\s*([+\-*/×÷])\s*({_NUM})", re.IGNORECASE)
_LOOSE_WORD = re.compile(
    rf"({_NUM}).*?({'|'.join(re.escape(w) for w in _OP_WORDS)}).*?({_NUM})", re.IGNORECASE
)


def is_math_query(text: str) -> bool:
    """Return True if the text looks like a simple binary math query."""
    if not text or not isinstance(text, str):
        return False
    t = text.strip().lower()

    # quick exact/anchored checks first
    if _SYMBOL_BETWEEN.match(t) or _WORD_BETWEEN.match(t) or _VERB_FIRST.match(t) or _SUBTRACT_FROM.match(t):
        return True

    # loose checks inside longer sentences
    if _LOOSE_SYMBOL.search(t) or _LOOSE_WORD.search(t):
        return True

    return False


def parse_math_expression(text: str) -> Optional[Tuple[float, str, float]]:
    """
    Parse a simple binary math expression and return (a, op, b)
    or None if no match.

    Covers patterns:
      - "10 - 4", "10-4", "10 -4"
      - "50 minus 25", "what is 5 plus 3"
      - "multiply 4 and 6", "divide 8 by 2"
      - "subtract 5 from 10" (note: result will be 10 - 5)
    """
    if not text or not isinstance(text, str):
        return None

    t = text.strip().lower()

    # 1) anchored symbol-based (best match)
    m = _SYMBOL_BETWEEN.match(t)
    if m:
        try:
            a = float(m.group(1))
            op_raw = m.group(2)
            b = float(m.group(3))
            op = {"+": "+", "-": "-", "*": "*", "/": "/", "×": "*", "÷": "/"}[op_raw]
            return (a, op, b)
        except Exception:
            return None

    # 2) anchored word-based: "5 plus 3"
    m = _WORD_BETWEEN.match(t)
    if m:
        try:
            a = float(m.group(1))
            op_word = m.group(2).strip()
            b = float(m.group(3))
            op = OPERATOR_MAP.get(op_word, None)
            if op:
                return (a, op, b)
        except Exception:
            return None

    # 3) verb-first: "multiply 4 and 6" or "multiply 4 by 6"
    m = _VERB_FIRST.match(t)
    if m:
        try:
            op_word = m.group(1).strip()
            a = float(m.group(2))
            b = float(m.group(3))
            op = OPERATOR_MAP.get(op_word, None)
            if op:
                return (a, op, b)
        except Exception:
            return None

    # 4) subtract X from Y -> "subtract 5 from 10" means 10 - 5
    m = _SUBTRACT_FROM.match(t)
    if m:
        try:
            # m.group(2) is X, m.group(3) is Y
            x = float(m.group(2))
            y = float(m.group(3))
            return (y, "-", x)
        except Exception:
            return None

    # 5) loose search in longer sentences (first occurrence)
    m = _LOOSE_SYMBOL.search(t)
    if m:
        try:
            a = float(m.group(1))
            op_raw = m.group(2)
            b = float(m.group(3))
            op = {"+": "+", "-": "-", "*": "*", "/": "/", "×": "*", "÷": "/"}[op_raw]
            return (a, op, b)
        except Exception:
            return None

    m = _LOOSE_WORD.search(t)
    if m:
        try:
            a = float(m.group(1))
            op_word = m.group(2).strip()
            b = float(m.group(3))
            op = OPERATOR_MAP.get(op_word, None)
            if op:
                return (a, op, b)
        except Exception:
            return None

    # nothing matched
    return None
