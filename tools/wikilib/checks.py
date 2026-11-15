"""Text rules for every page: English only, and nothing private.

Each rule looks at the raw file, line by line, so a message can point at the
line to fix. The same rules run over commit subjects shown on Recent changes.
"""
import codecs
import re

# Hangul Jamo, Compatibility Jamo, Jamo Extended-A, Syllables, Jamo Extended-B
HANGUL_RANGES = ((0x1100, 0x11FF), (0x3130, 0x318F), (0xA960, 0xA97F), (0xAC00, 0xD7A3), (0xD7B0, 0xD7FF))
HANGUL = re.compile("[" + "".join(f"{chr(a)}-{chr(b)}" for a, b in HANGUL_RANGES) + "]")

# user@host.tld. "git@github.com:org/repo" (an SSH remote) is not an address.
EMAIL = re.compile(r"(?<![\w.%+-])([A-Za-z0-9._%+-]+)@([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,})(?![\w-])")

# 10.0.0.0/8, 172.16.0.0/12 and 192.168.0.0/16. Examples belong in the
# documentation ranges (192.0.2.x, 198.51.100.x, 203.0.113.x) or 127.0.0.1.
PRIVATE_IP = re.compile(
    r"(?<![\d.])(?:10\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])|192\.168)\.\d{1,3}\.\d{1,3}(?!\.?\d)"
)

# Names that must not appear in the wiki, kept in ROT13 so that this file
# does not spell them out.
_BLOCKED = tuple(codecs.decode(w, "rot13") for w in ("pynhqr", "naguebcvp"))
_BLOCKED_RE = re.compile("|".join(_BLOCKED), re.IGNORECASE)


def text_problems(line):
    """Problems in one line of text, as short messages."""
    found = []
    if HANGUL.search(line):
        found.append("Hangul text: the wiki is English only")
    for m in EMAIL.finditer(line):
        if m.group(1) == "git" and line[m.end():m.end() + 1] == ":":
            continue
        found.append(f"email address {m.group(0)!r}: no email addresses in the wiki")
    for m in PRIVATE_IP.finditer(line):
        found.append(f"private IP address {m.group(0)!r}: use 127.0.0.1 or 192.0.2.x in examples")
    for m in _BLOCKED_RE.finditer(line):
        found.append(f"blocked word {m.group(0)!r}")
    return found


def file_problems(text, label, first_line=1):
    """All text problems in a file, as 'label:line: message'."""
    out = []
    for n, line in enumerate(text.splitlines(), first_line):
        for problem in text_problems(line):
            out.append(f"{label}:{n}: {problem}")
    return out
