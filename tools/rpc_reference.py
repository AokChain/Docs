#!/usr/bin/env python3
"""Generate the RPC reference pages of the wiki from a running AokChain node.

The script starts aokchaind on regtest with a new, temporary data directory,
asks it for `help` and for `help <command>` of every command, writes

    pages/reference/rpc.md               index of all commands by category
    pages/reference/rpc-<category>.md    one page per category, one ### per command

and stops the node again with `aokchain-cli stop`. The text of every command is
the node's own help text; nothing is added to it.

    tools/rpc_reference.py --aokchaind /path/to/aokchaind --aokchain-cli /path/to/aokchain-cli

The programs can also be given as the environment variables AOKCHAIND and
AOKCHAIN_CLI. The node listens on no P2P port (-listen=0), makes no outgoing
connections (-connect=0) and uses its own RPC port (the first free one from
19200 to 19299 unless --rpcport is given), so it does not disturb a node that
already runs on the same computer.

Some help texts depend on the state of the node, so the script reads them in
the state a real node is in: the chain is past the token activation height
(10 blocks are made on regtest), and the wallet is encrypted. The commands
whose help only an unencrypted wallet shows (encryptwallet) are read before
the wallet is encrypted. The commands of the "hidden" category, which `help`
does not list, are read by name.

--save-json FILE keeps the help texts; --from-json FILE writes the pages from
such a file without starting a node.
"""

import argparse
import json
import os
import re
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import time

GENERATED_BY = "tools/rpc_reference.py"

# Display names and one-line summaries of the categories that `help` prints.
# A category that is not listed here still gets a page, titled after its name.
CATEGORIES = {
    "addressindex": ("Address index", "Balances, transactions and unspent outputs of addresses, read from the address index."),
    "blockchain": ("Blockchain", "Blocks, the chain state, the mempool, governance, the snapshot and the block archives."),
    "control": ("Control", "Memory, running commands, uptime, help and stopping the node."),
    "generating": ("Generating", "Making proof-of-work blocks on regtest, and the generate setting."),
    "mining": ("Mining", "Block templates, mining and staking information, and block submission."),
    "network": ("Network", "Peers, connections, bans and network traffic."),
    "rawtransactions": ("Raw transactions", "Creating, signing, checking and sending transactions by hand."),
    "tokens": ("Tokens", "Issuing, reissuing, transferring and looking up tokens and user names."),
    "util": ("Utilities", "Multisig addresses, fee estimates, message signatures, address checks and recovery words."),
    "wallet": ("Wallet", "Keys, addresses, balances, payments, backups, encryption and the wallet files."),
    "hidden": ("Not listed by help", "Commands for testing and debugging that `help` does not list."),
}

# The commands of the "hidden" category of AokChain Core 4.0 (the source tables
# of src/rpc/*.cpp and src/wallet/rpcwallet.cpp). `help` does not list them;
# `help <command>` answers for each. A name the node does not know is skipped.
HIDDEN_COMMANDS = [
    "echo", "echojson", "estimaterawfee", "invalidateblock", "logging", "reconsiderblock",
    "resendwallettransactions", "setmocktime", "waitforblock", "waitforblockheight", "waitfornewblock",
]

# Commands whose help text begins with the usage line of another command, so that `help`
# lists them under that name (src/wallet/rpcdump.cpp: removeaddress prints the usage of
# importaddress). They are found by name when the listing shows the same line twice.
EXTRA_CANDIDATES = ["removeaddress"]

FIRST_PORT, LAST_PORT = 19200, 19299
TOKEN_HEIGHT = 10  # regtest: tokens are active from this height
LABEL = None       # --label


class NodeError(Exception):
    pass


def free_port(first, last):
    for port in range(first, last + 1):
        for family, host in ((socket.AF_INET, "127.0.0.1"), (socket.AF_INET6, "::1")):
            try:
                with socket.socket(family, socket.SOCK_STREAM) as s:
                    s.bind((host, port))
            except OSError:
                if family == socket.AF_INET:
                    break
        else:
            return port
    raise NodeError("no free port from %d to %d" % (first, last))


class Node:
    """aokchaind on regtest in a data directory of its own."""

    def __init__(self, daemon, cli, workdir, rpcport):
        self.daemon = daemon
        self.cli_path = cli
        self.datadir = tempfile.mkdtemp(prefix="rpcref-", dir=workdir)
        self.rpcport = rpcport
        self.proc = None

    def start(self):
        args = [
            self.daemon, "-regtest", "-datadir=" + self.datadir,
            "-listen=0", "-connect=0", "-dnsseed=0", "-upnp=0", "-discover=0", "-listenonion=0",
            "-bootstrap=0", "-snapshot=0", "-staking=0", "-server=1", "-keypool=1",
            "-rpcport=%d" % self.rpcport, "-printtoconsole=0",
        ]
        self.proc = subprocess.Popen(args, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                     stderr=subprocess.PIPE)
        deadline = time.time() + 180
        while True:
            if self.proc.poll() is not None:
                err = self.proc.stderr.read().decode("utf-8", "replace")
                raise NodeError("aokchaind ended at start (exit %s): %s" % (self.proc.returncode, err.strip()))
            result = self.run("getblockcount", check=False)
            if result.returncode == 0:
                return
            if time.time() > deadline:
                raise NodeError("aokchaind does not answer: " + result.stderr.strip())
            time.sleep(0.5)

    def run(self, *params, check=True):
        args = [self.cli_path, "-regtest", "-datadir=" + self.datadir, "-rpcport=%d" % self.rpcport]
        result = subprocess.run(args + list(params), stdin=subprocess.DEVNULL, capture_output=True,
                                text=True, timeout=120)
        if check and result.returncode != 0:
            raise NodeError("aokchain-cli %s: %s" % (" ".join(params), result.stderr.strip()))
        return result

    def wait_exit(self, timeout):
        """Wait until the process has ended by itself (after stop or encryptwallet)."""
        try:
            self.proc.wait(timeout=timeout)
            return True
        except subprocess.TimeoutExpired:
            return False

    def stop(self, remove=True):
        try:
            if self.proc is not None and self.proc.poll() is None:
                self.run("stop", check=False)
                if not self.wait_exit(120):
                    # it did not stop on the RPC: end the process this script started, by its PID
                    self.proc.terminate()
                    if not self.wait_exit(60):
                        self.proc.kill()
                        self.proc.wait()
        finally:
            self.proc = None
            if remove:
                shutil.rmtree(self.datadir, ignore_errors=True)


def listing(node):
    """[[category, [first line of each help, ...]], ...] as `help` prints them."""
    categories = []
    for line in node.run("help").stdout.splitlines():
        line = line.rstrip()
        m = re.match(r"^== (.+) ==$", line)
        if m:
            categories.append([m.group(1), []])
        elif line and categories:
            categories[-1][1].append(line)
    if not categories:
        raise NodeError("`help` listed no commands")
    return categories


def help_text(node, name):
    text = node.run("help", name).stdout.rstrip("\n")
    if text.startswith("help: unknown command"):
        return None
    return text


def resolve(node, categories):
    """{category: {name: text}}. `help` prints the first line of each help text, which is
    normally the command and its arguments; when that line names another command, the
    command is found among the names that the examples of all help texts call."""
    found, unresolved = {}, []
    for category, lines in categories:
        found.setdefault(category, {})
        for line in lines:
            name = line.split()[0]
            text = help_text(node, name)
            already = any(name in c for c in found.values())
            if text is not None and text.split("\n")[0].rstrip() == line and not already:
                found[category][name] = text
            else:
                unresolved.append((category, line))
    if unresolved:
        known = {n for c in found.values() for n in c}
        texts = [t for c in found.values() for t in c.values()]
        candidates = set()
        for t in texts:
            candidates.update(re.findall(r"aokchain-cli\s+(?:-\S+\s+)*([a-z][a-z0-9]+)", t))
            candidates.update(re.findall(r'"method":\s*"([a-z][a-z0-9]+)"', t))
        candidates.update(EXTRA_CANDIDATES)
        candidates -= known
        by_first_line = {}
        for name in sorted(candidates):
            text = help_text(node, name)
            if text is not None:
                by_first_line.setdefault(text.split("\n")[0].rstrip(), []).append((name, text))
        for category, line in unresolved:
            matches = by_first_line.get(line, [])
            matches = [m for m in matches if m[0] not in known]
            if not matches:
                raise NodeError("cannot tell which command `help` lists as: " + line)
            name, text = matches[0]
            found[category][name] = text
            known.add(name)
    return found


def collect(node):
    """{"version", "categories": [[category, [names]]], "help": {name: text}, "note": {name: text}}"""
    # tokens are active from height 10 on regtest; below it every token help says so
    address = node.run("getnewaddress").stdout.strip()
    node.run("generatetoaddress", str(TOKEN_HEIGHT), address)
    info = json.loads(node.run("getnetworkinfo").stdout)
    plain = resolve(node, listing(node))

    # the wallet commands that only an encrypted wallet explains
    node.run("encryptwallet", secrets.token_hex(16), check=False)  # the node stops after it
    if not node.wait_exit(120):
        raise NodeError("the node did not stop after encryptwallet")
    node.start()
    crypted = resolve(node, listing(node))

    merged = {}
    for source in (plain, crypted):  # the texts of the encrypted wallet win
        for category, commands in source.items():
            merged.setdefault(category, {}).update(commands)
    hidden = {}
    for name in HIDDEN_COMMANDS:
        text = help_text(node, name)
        if text is not None and not any(name in c for c in merged.values()):
            hidden[name] = text
    if hidden:
        merged["Hidden"] = hidden

    order = [c for c, _ in listing(node)]
    order += [c for c in merged if c not in order]
    return {
        "version": info["subversion"],
        "categories": [[c, sorted(merged[c])] for c in order if c in merged],
        "help": {n: t for c in merged.values() for n, t in c.items()},
    }


# ---------------------------------------------------------------- rendering

HEADING = re.compile(r"^(Arguments|Result|Results|Examples?|Named arguments)(\s*\(.*\))?\s*:?\s*$")


def md_text(text, table=False):
    """Escape help text so that Markdown shows it as it is (CommonMark and other dialects)."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"([\\`*_\[\]])", r"\\\1", text)
    text = text.replace("~~", "\\~\\~")
    if table:
        text = text.replace("|", "\\|")
    # what would start a heading or a list at the beginning of a paragraph
    text = re.sub(r"^(\s*)([#+-])", r"\1\\\2", text)
    text = re.sub(r"^(\s*\d+)([.)])", r"\1\\\2", text)
    return text


def trim_blank(lines):
    while lines and not lines[0].strip():
        lines = lines[1:]
    while lines and not lines[-1].strip():
        lines = lines[:-1]
    return lines


def split_help(name, text):
    """(usage lines, description lines, [[heading, lines], ...])"""
    lines = text.split("\n")
    usage, i = [], 0
    # the first lines that start with the command (or with the name it prints) are the usage;
    # a lone line that ends like a sentence is a description
    first = lines[0].split()[0] if lines and lines[0].split() else name
    while i < len(lines) and lines[i].strip():
        words = lines[i].split()
        sentence = re.search(r"[a-z]\.$", lines[i].rstrip()) is not None
        if words[0] in (name, first) and not sentence:
            usage.append(lines[i].rstrip())
            i += 1
        else:
            break
    description, sections = [], []
    for line in lines[i:]:
        if HEADING.match(line):
            sections.append([line.strip(), []])
        elif sections:
            sections[-1][1].append(line.rstrip())
        else:
            description.append(line.rstrip())
    return usage, description, sections


def paragraphs(lines):
    out, current = [], []
    for line in lines + [""]:
        if line.strip():
            current.append(line)
        elif current:
            out.append(current)
            current = []
    return out


def preformatted_line(line, k):
    """A line that the help text lays out by hand: JSON, an example, a list, an indented line."""
    stripped = line.strip()
    if k > 0 and line.startswith("  "):
        return True
    if stripped[:1] in ("{", "}", "[", "]") or stripped.startswith(("> ", "- ")):
        return True
    if re.match(r'^"[^"]*"\s*:', stripped) or re.match(r"^\d+[.)]\s", stripped):
        return True
    return False


def split_paragraph(paragraph):
    """(the leading prose lines, the lines laid out by hand that follow them)"""
    for k, line in enumerate(paragraph):
        if preformatted_line(line, k):
            return paragraph[:k], paragraph[k:]
    return paragraph, []


def fence(lines):
    body = "\n".join(trim_blank(lines))
    ticks = "```"
    while ticks in body:
        ticks += "`"
    return "%stext\n%s\n%s\n" % (ticks, body, ticks)


def command_markdown(name, text):
    usage, description, sections = split_help(name, text)
    out = ["### %s\n" % name]
    if usage:
        out.append(fence(usage))
        printed = usage[0].split()[0]
        if name not in printed.split("|"):
            out.append("> [!NOTE]\n> The usage line of this help text names `%s`; the command is `%s`.\n"
                       % (printed, name))
    for paragraph in paragraphs(trim_blank(description)):
        prose, laid_out = split_paragraph(paragraph)
        if prose:
            out.append(md_text(" ".join(l.strip() for l in prose)) + "\n")
        if laid_out:
            out.append(fence(laid_out))
    for heading, lines in sections:
        lines = trim_blank(lines)
        out.append("**%s**\n" % md_text(heading.rstrip(":").strip()))
        if lines:
            out.append(fence(lines))
    return "\n".join(out)


def category_slug(name):
    return "rpc-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def category_title(name):
    return CATEGORIES.get(name.lower(), (name, None))[0]


def category_blurb(name):
    return CATEGORIES.get(name.lower(), (name, ""))[1] or ""


def front_matter(title, description, order, aliases=None):
    if len(description) > 160:
        raise ValueError("description too long: " + description)
    lines = ["---", "title: " + title, "description: " + description, "order: %d" % order]
    if aliases:
        lines.append("aliases: [%s]" % ", ".join(aliases))
    lines += ["generated_by: " + GENERATED_BY, "---", ""]
    return "\n".join(lines)


ABBREVIATIONS = ("e.g.", "i.e.", "eg.", "etc.", "vs.")


def summary_line(name, text, table=False):
    """The first sentence of the description, for the lists of commands."""
    _, description, _ = split_help(name, text)
    found = paragraphs(trim_blank(description))
    lines = split_paragraph(found[0])[0] if found else []
    if not lines:
        return ""
    # the help texts put a sentence on a line of its own, often without a full stop
    words = []
    for k, line in enumerate(lines):
        words.append(line.strip())
        ends = re.search(r"[.!?]$", line.strip()) and not line.strip().endswith(ABBREVIATIONS)
        starts_new = k + 1 < len(lines) and lines[k + 1].strip()[:1].isupper()
        if (ends or starts_new) and len(" ".join(words)) >= 15:
            break
    summary = " ".join(words)
    # cut after the first full stop that ends a sentence
    for m in re.finditer(r"[.!?](?=\s)", summary):
        head = summary[:m.end()]
        if len(head) >= 15 and not head.endswith(ABBREVIATIONS):
            summary = head
            break
    if len(summary) > 150:
        summary = summary[:147].rsplit(" ", 1)[0] + " ..."
    return md_text(summary, table=table)


def version_label(version):
    """ "/AokChain:4.0.5/" -> "AokChain Core 4.0.5"; --label overrides it."""
    if LABEL:
        return LABEL
    m = re.search(r"(\d+\.\d+\.\d+)", version)
    return "AokChain Core %s" % m.group(1) if m else version


EXAMPLES_NOTE = (
    "> [!NOTE]\n"
    "> Many examples in these help texts come from the upstream code: their addresses are often\n"
    "> Bitcoin addresses, and their `curl` lines use port 8766. An AokChain node answers JSON-RPC on\n"
    "> port 33440 (mainnet) or 44550 (testnet and regtest) unless `rpcport` says otherwise; see [[json-rpc]].\n"
)


def index_page(data):
    listed = [(c, cmds) for c, cmds in data["categories"] if c.lower() != "hidden"]
    total = sum(len(cmds) for _, cmds in listed)
    out = [front_matter("RPC commands", "Every JSON-RPC command of AokChain Core 4.0, by category, with a link to the help text of each.", 10, ["rpc"])]
    out.append("Every command that %s answers over JSON-RPC and `aokchain-cli`, by category. "
               "Each name links to the command's help text, the same text that "
               "`aokchain-cli help <command>` prints. How to send a call is on [[json-rpc]].\n"
               % md_text(version_label(data["version"])))
    out.append("## Categories\n")
    for name, commands in data["categories"]:
        out.append("- [[%s|%s]] (%d): %s" % (category_slug(name), category_title(name), len(commands),
                                            md_text(category_blurb(name).replace("`", ""))))
    out.append("")
    out.append("`aokchain-cli help` lists %d commands. The commands under [[rpc-hidden|Not listed by help]] are "
               "for testing and debugging; `aokchain-cli help <command>` still explains each.\n" % total)
    out.append("> [!NOTE]\n> Wallet commands act on the wallet that the node has loaded. With several wallets "
               "loaded, name one with `aokchain-cli -rpcwallet=<name>`, or send the call to the path "
               "`/wallet/<name>` of the JSON-RPC address.\n")
    for name, commands in data["categories"]:
        slug = category_slug(name)
        out.append("## %s\n" % category_title(name))
        for command in commands:
            summary = summary_line(command, data["help"][command])
            out.append("- [[%s#%s|%s]]%s" % (slug, command, command, (": " + summary) if summary else ""))
        out.append("")
    return "\n".join(out)


def category_page(data, name, commands, order):
    title = category_title(name)
    blurb = category_blurb(name).replace("`", "")
    description = "RPC reference: %s" % (blurb[0].lower() + blurb[1:]) if blurb else "RPC reference: the %s commands." % title.lower()
    if len(description) > 160:
        description = "RPC reference: the %s commands of AokChain Core." % title.lower()
    out = [front_matter("RPC: %s" % title, description, order)]
    if name.lower() == "hidden":
        out.append("`aokchain-cli help` does not list these commands. They are meant for testing and "
                   "debugging; some of them change what the node considers valid until they are undone. "
                   "This is the help text that %s prints for each with `aokchain-cli help <command>`. "
                   "All categories are on [[rpc]].\n" % md_text(version_label(data["version"])))
    else:
        out.append("The help text of every command in the %s category, as %s prints it with "
                   "`aokchain-cli help <command>`. All categories are on [[rpc]].\n"
                   % (title.lower(), md_text(version_label(data["version"]))))
    out.append(EXAMPLES_NOTE)
    out.append("| Command | Summary |\n|---|---|")
    for command in commands:
        out.append("| [%s](#%s) | %s |" % (command, command, summary_line(command, data["help"][command], table=True)))
    out.append("")
    for command in commands:
        out.append(command_markdown(command, data["help"][command]))
    return "\n".join(out)


def write_pages(data, outdir):
    os.makedirs(outdir, exist_ok=True)
    written = []
    path = os.path.join(outdir, "rpc.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(index_page(data).rstrip("\n") + "\n")
    written.append(path)
    for i, (name, commands) in enumerate(data["categories"]):
        path = os.path.join(outdir, category_slug(name) + ".md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(category_page(data, name, commands, 20 + i).rstrip("\n") + "\n")
        written.append(path)
    # remove pages of categories that are gone from the help
    keep = {os.path.basename(p) for p in written}
    for old in os.listdir(outdir):
        if old.startswith("rpc-") and old.endswith(".md") and old not in keep:
            with open(os.path.join(outdir, old), encoding="utf-8") as f:
                if ("generated_by: " + GENERATED_BY) in f.read(2000):
                    os.remove(os.path.join(outdir, old))
    return written


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--aokchaind", default=os.environ.get("AOKCHAIND"), help="path to aokchaind (or $AOKCHAIND)")
    parser.add_argument("--aokchain-cli", dest="cli", default=os.environ.get("AOKCHAIN_CLI"), help="path to aokchain-cli (or $AOKCHAIN_CLI)")
    parser.add_argument("--out", default=os.path.join(root, "pages", "reference"), help="folder of the pages (default: pages/reference)")
    parser.add_argument("--workdir", default=os.environ.get("AOK_DOCS_WORKDIR"), help="folder for the temporary data directory (default: the system's temporary folder)")
    parser.add_argument("--rpcport", type=int, help="RPC port of the temporary node (default: the first free one from %d to %d)" % (FIRST_PORT, LAST_PORT))
    parser.add_argument("--label", help='the version the pages name, e.g. "AokChain Core 4.0.5" (default: the version of the node)')
    parser.add_argument("--save-json", help="also write the help texts to this file")
    parser.add_argument("--from-json", help="write the pages from a file of --save-json, without starting a node")
    args = parser.parse_args()
    global LABEL
    LABEL = args.label

    if args.from_json:
        with open(args.from_json, encoding="utf-8") as f:
            data = json.load(f)
    else:
        if not args.aokchaind or not args.cli:
            parser.error("give --aokchaind and --aokchain-cli, or set AOKCHAIND and AOKCHAIN_CLI")
        for path in (args.aokchaind, args.cli):
            if not os.access(path, os.X_OK):
                parser.error("not an executable program: " + path)
        if args.workdir:
            os.makedirs(args.workdir, exist_ok=True)
        node = Node(os.path.abspath(args.aokchaind), os.path.abspath(args.cli), args.workdir,
                    args.rpcport or free_port(FIRST_PORT, LAST_PORT))
        try:
            node.start()
            data = collect(node)
        finally:
            node.stop()
    if args.save_json:
        with open(args.save_json, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=1, ensure_ascii=False)
    for path in write_pages(data, args.out):
        print(os.path.relpath(path, root))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except NodeError as e:
        sys.exit("rpc_reference.py: %s" % e)
