"""Dates and changes from git: "Last updated" on each page and the Recent
changes page. A page that was never committed has no date."""
import subprocess
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Commit:
    hash: str
    date: str          # YYYY-MM-DD, committer date
    time: str          # ISO 8601, committer date
    subject: str
    files: list = field(default_factory=list)   # (status, path, old path or "")


def _git(cwd, *args):
    try:
        out = subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True, text=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    return out.stdout


def toplevel(path):
    out = _git(path, "rev-parse", "--show-toplevel")
    return Path(out.strip()) if out else None


def log(repo, subdir, limit=None):
    """Commits that touched subdir (a path inside repo), newest first."""
    args = ["log", "--no-merges", "-M", "--format=%x1e%H%x1f%cs%x1f%cI%x1f%s", "--name-status"]
    if limit:
        args.append(f"-n{limit}")
    rel = Path(subdir).resolve().relative_to(Path(repo).resolve())
    out = _git(repo, *args, "--", str(rel) or ".")
    if not out:
        return []
    commits = []
    for record in out.split("\x1e")[1:]:
        head, _, rest = record.partition("\n")
        parts = head.split("\x1f")
        if len(parts) != 4:
            continue
        commit = Commit(*parts)
        for line in rest.splitlines():
            if not line.strip():
                continue
            cols = line.split("\t")
            status = cols[0][:1]
            if status in ("R", "C") and len(cols) >= 3:
                commit.files.append((status, cols[2], cols[1]))
            elif len(cols) >= 2:
                commit.files.append((status, cols[1], ""))
        commits.append(commit)
    return commits


def last_changed(commits):
    """Path -> date of the newest commit that touched it."""
    dates = {}
    for c in commits:
        for _status, path, _old in c.files:
            dates.setdefault(path, c.date)
    return dates
