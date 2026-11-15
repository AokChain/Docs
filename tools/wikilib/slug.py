"""Heading anchors the way GitHub makes them: lowercase, punctuation dropped,
each space turned into a hyphen. A repeated heading gets -1, -2 and so on,
so [[slug#anchor]] links match what GitHub shows for the same file."""
import re

_DROP = re.compile(r"[^\w\- ]")


def slugify(text):
    return _DROP.sub("", text.strip().lower()).replace(" ", "-")


class Slugger:
    """Unique anchors within one page (the github-slugger algorithm)."""

    def __init__(self, taken=()):
        self.occurrences = {name: 0 for name in taken}

    def slug(self, text):
        original = slugify(text) or "section"
        result = original
        while result in self.occurrences:
            self.occurrences[original] += 1
            result = f"{original}-{self.occurrences[original]}"
        self.occurrences[result] = 0
        return result
