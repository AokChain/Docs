#!/usr/bin/env python3
"""Generate the configuration options page of the wiki from the programs' own help.

    tools/options_reference.py --aokchaind /path/to/aokchaind \
        [--aokchain-qt /path/to/aokchain-qt] [--aokchain-cli /path/to/aokchain-cli] \
        [--aokchain-tx /path/to/aokchain-tx] [--aokchain-wallet /path/to/aokchain-wallet]

reads `aokchaind -help` and `aokchaind -help -help-debug` (and the same of
aokchain-qt for the options of the GUI wallet, and the help of aokchain-cli,
aokchain-tx and aokchain-wallet) and writes pages/reference/configuration-options.md,
grouped by the sections of the help. The text of every option is the program's
own; nothing is added to it. The programs can also be given as AOKCHAIND,
AOKCHAIN_QT, AOKCHAIN_CLI, AOKCHAIN_TX and AOKCHAIN_WALLET.

`-help` starts no node and reads no data directory. aokchain-qt runs with
QT_QPA_PLATFORM=offscreen and a temporary HOME, so it needs no display and
leaves no settings behind.

A few defaults depend on the computer that prints the help (-dbcache follows
the memory of the computer); the page names them.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

GENERATED_BY = "tools/options_reference.py"
SLUG = "configuration-options"

# Options that the programs read but that -help does not list, with what the
# source does with them (AokChain Core 4.0: src/wallet/init.cpp, src/miner.h,
# src/validation.h, src/init.cpp, src/rpc/tokens.cpp). They are written by hand.
NOT_IN_HELP = [
    ("-staking", "Search for stakes with the wallets that are loaded, from the start (default: 0). "
                 "The GUI wallet starts with the staking switch in this position. `getstakinginfo` reports it as `enabled`."),
    ("-tokenindex", "Maintain the token address index, used by listaddressesbytoken, listtokenbalancesbyaddress "
                    "and listuniquetokenholders (default: 1). Changing it needs a rebuild with -reindex."),
]

# Help texts whose default depends on the computer that prints them.
MACHINE_DEFAULTS = {
    "-dbcache": "The default is 1024 MiB on a computer with at least 4 GiB of memory and 450 MiB otherwise; the help prints the value for the computer it runs on.",
}

GROUP_TITLES = {"Options": "General options", "UI Options": "GUI options"}


def run_help(program, *args, env=None):
    result = subprocess.run([program] + list(args), stdin=subprocess.DEVNULL, capture_output=True,
                            text=True, timeout=120, env=env)
    if result.returncode != 0 or not result.stdout.strip():
        raise RuntimeError("%s %s failed: %s" % (program, " ".join(args), result.stderr.strip()))
    return result.stdout


def parse(text):
    """[(group, [(option, description), ...]), ...] in the order of the help."""
    groups, option, lines = [], None, []

    def flush():
        nonlocal option, lines
        if option is not None:
            groups[-1][1].append((option, " ".join(l.strip() for l in lines).strip()))
        option, lines = None, []

    for line in text.split("\n"):
        if re.match(r"^\S.*:\s*$", line):
            flush()
            groups.append([line.strip().rstrip(":"), []])
        elif re.match(r"^  -\S", line) and groups:
            flush()
            option = line.strip()
        elif line.startswith("   ") and option is not None:
            lines.append(line)
        elif not line.strip():
            continue
        elif option is not None:
            lines.append(line)
    flush()
    return [(g, opts) for g, opts in groups if opts]


def option_name(option):
    return re.split(r"[=<\[ ]", option, 1)[0]


def md_text(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"([\\`*_\[\]|])", r"\\\1", text)
    return text


def code(text):
    ticks = "``" if "`" in text else "`"
    pad = " " if text.startswith("`") or text.endswith("`") else ""
    return "%s%s%s%s%s" % (ticks, pad, text, pad, ticks)


def version_of(program):
    first = run_help(program, "-version").split("\n")[0]
    m = re.search(r"v(\d+\.\d+\.\d+)", first)
    return m.group(1) if m else first


def table(options, notes):
    out = ["| Option | Description |", "|---|---|"]
    for option, description in options:
        out.append("| %s | %s |" % (code(option), md_text(description)))
    out.append("")
    for option, _ in options:
        if option_name(option) in notes:
            out.append("> [!NOTE]\n> %s: %s\n" % (code(option_name(option)), md_text(notes[option_name(option)])))
    return "\n".join(out) + "\n"


def anchor_title(group):
    return GROUP_TITLES.get(group, group[:1].upper() + group[1:])


def verbatim_help(program):
    """The help of a tool as it prints it, without the version line."""
    lines = run_help(program, "-help").rstrip().split("\n")
    if lines and "version" in lines[0]:
        lines = lines[1:]
    while lines and not lines[0].strip():
        lines = lines[1:]
    return "\n".join(l.rstrip() for l in lines)


def build(daemon, qt, cli, label, tx=None, wallet_tool=None):
    regular = parse(run_help(daemon, "-help"))
    full = parse(run_help(daemon, "-help", "-help-debug"))
    shown = {o for _, opts in regular for o, _ in opts}

    gui_regular, gui_debug = [], []
    if qt:
        home = tempfile.mkdtemp(prefix="optref-")
        env = dict(os.environ, QT_QPA_PLATFORM="offscreen", HOME=home, XDG_CONFIG_HOME=os.path.join(home, ".config"))
        try:
            qt_regular = parse(run_help(qt, "-help", env=env))
            qt_full = parse(run_help(qt, "-help", "-help-debug", env=env))
        finally:
            shutil.rmtree(home, ignore_errors=True)
        daemon_names = {option_name(o) for _, opts in full for o, _ in opts}
        gui_shown = {o for _, opts in qt_regular for o, _ in opts}
        for group, opts in qt_full:
            mine = [(o, d) for o, d in opts if option_name(o) not in daemon_names]
            gui_regular += [(o, d) for o, d in mine if o in gui_shown]
            gui_debug += [(o, d) for o, d in mine if o not in gui_shown]

    cli_groups = parse(run_help(cli, "-help")) if cli else []

    out = ["---", "title: Configuration options",
           "description: Every option of aokchaind, the GUI wallet and the command-line tools, from the programs' own help, grouped as -help prints them.",
           "order: 11", "generated_by: " + GENERATED_BY, "---", ""]
    out.append("The options of %s, as `aokchaind -help` prints them. Give an option on the command line as "
               "`-name=value`, or write it as a line `name=value` in `aokchain.conf` (where the file lives is on "
               "[[configure-a-node]]). A setting on the command line wins over the same setting in the file. "
               "A switch such as `-txindex` is turned on with `1` and off with `0`, and `-nofoo` is the same as `-foo=0`.\n"
               % md_text(label))
    out.append("The GUI wallet, `aokchain-qt`, takes the same options except `-daemon` and `-daemonwait`, "
               "and the few of its own listed under [GUI options](#gui-options).\n")
    out.append("## Contents\n")
    sections = [anchor_title(g) for g, _ in regular]
    if gui_regular:
        sections.append("GUI options")
    sections += ["Options not listed by -help", "Debugging options"]
    if cli_groups:
        sections.append("aokchain-cli options")
    if tx:
        sections.append("aokchain-tx")
    if wallet_tool:
        sections.append("aokchain-wallet")
    for title in sections:
        out.append("- [%s](#%s)" % (title, re.sub(r"[^a-z0-9 -]", "", title.lower()).replace(" ", "-")))
    out.append("")

    for group, opts in regular:
        out.append("## %s\n" % anchor_title(group))
        out.append(table(opts, MACHINE_DEFAULTS))
    if gui_regular:
        out.append("## GUI options\n")
        out.append("Only `aokchain-qt` reads these.\n")
        out.append(table(gui_regular, {}))

    out.append("## Options not listed by -help\n")
    out.append("The programs read these options although `-help` does not show them.\n")
    out.append("| Option | Description |\n|---|---|")
    for option, description in NOT_IN_HELP:
        out.append("| %s | %s |" % (code(option), md_text(description).replace("\\`", "`")))
    out.append("")

    out.append("## Debugging options\n")
    out.append("`aokchaind -help -help-debug` adds these options for testing and debugging. Several of them "
               "only work on regtest. They are grouped as the help groups them.\n")
    regular_groups = {g for g, _ in regular}
    for group, opts in full:
        extra = [(o, d) for o, d in opts if o not in shown]
        if extra:
            title = anchor_title(group) if group not in regular_groups else "%s (debugging)" % anchor_title(group)
            out.append("### %s\n" % title)
            out.append(table(extra, MACHINE_DEFAULTS))
    if gui_debug:
        out.append("### GUI options (debugging)\n")
        out.append(table(gui_debug, {}))

    if cli_groups:
        out.append("## aokchain-cli options\n")
        out.append("`aokchain-cli` sends one command to a running node (see [[json-rpc]]). It reads the RPC settings "
                   "(`rpcuser`, `rpcpassword`, `rpcport`, `rpcconnect`) from the same `aokchain.conf`, or uses the "
                   "cookie file of the data directory. These are its options, as `aokchain-cli -help` prints them.\n")
        merged = [(o, d) for _, opts in cli_groups for o, d in opts]
        out.append(table(merged, {}))
    if tx:
        out.append("## aokchain-tx\n")
        out.append("`aokchain-tx` creates and changes raw transactions without a node (see [[raw-transactions]]). "
                   "This is its help. It also takes `time=<unix time>`, which sets the time of the transaction "
                   "and is not listed.\n")
        out.append("```text\n%s\n```\n" % verbatim_help(tx))
    if wallet_tool:
        out.append("## aokchain-wallet\n")
        out.append("`aokchain-wallet` works on a wallet file while no node uses it. This is its help.\n")
        out.append("```text\n%s\n```\n" % verbatim_help(wallet_tool))
    return "\n".join(out).rstrip("\n") + "\n"


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--aokchaind", default=os.environ.get("AOKCHAIND"), help="path to aokchaind (or $AOKCHAIND)")
    parser.add_argument("--aokchain-qt", dest="qt", default=os.environ.get("AOKCHAIN_QT"), help="path to aokchain-qt (or $AOKCHAIN_QT); optional")
    parser.add_argument("--aokchain-cli", dest="cli", default=os.environ.get("AOKCHAIN_CLI"), help="path to aokchain-cli (or $AOKCHAIN_CLI); optional")
    parser.add_argument("--aokchain-tx", dest="tx", default=os.environ.get("AOKCHAIN_TX"), help="path to aokchain-tx (or $AOKCHAIN_TX); optional")
    parser.add_argument("--aokchain-wallet", dest="wallet", default=os.environ.get("AOKCHAIN_WALLET"), help="path to aokchain-wallet (or $AOKCHAIN_WALLET); optional")
    parser.add_argument("--out", default=os.path.join(root, "pages", "reference", SLUG + ".md"), help="the page to write")
    parser.add_argument("--label", help='the version the page names, e.g. "AokChain Core 4.0.5" (default: from aokchaind -version)')
    args = parser.parse_args()
    if not args.aokchaind:
        parser.error("give --aokchaind or set AOKCHAIND")
    for path in (args.aokchaind, args.qt, args.cli, args.tx, args.wallet):
        if path and not os.access(path, os.X_OK):
            parser.error("not an executable program: " + path)
    label = args.label or "AokChain Core " + version_of(args.aokchaind)
    page = build(args.aokchaind, args.qt, args.cli, label, args.tx, args.wallet)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(page)
    print(os.path.relpath(args.out, root))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, subprocess.TimeoutExpired) as e:
        sys.exit("options_reference.py: %s" % e)
