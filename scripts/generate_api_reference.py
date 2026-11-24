#!/usr/bin/env python3
"""Rewrites the README's method tables (between the GENERATED markers) from the spec."""

from __future__ import annotations

import re
from pathlib import Path

from spec import attribute, endpoints, load, tags_in_order

README = Path(__file__).resolve().parent.parent / "README.md"
BEGIN = "<!-- BEGIN GENERATED API REFERENCE -->"
END = "<!-- END GENERATED API REFERENCE -->"


def short(summary: str) -> str:
    """What an endpoint returns, in a few words: its summary's first sentence, up to its
    first colon or comma ("A profile: name, bio…" is "A profile")."""
    sentence = re.split(r"\.(?:\s|$)", summary.strip())[0]
    head = re.split(r": |, | \(", sentence)[0]
    return (head[:1].upper() + head[1:]).replace("|", "\\|")


def main() -> None:
    items = endpoints(load())
    sections = []
    for tag in tags_in_order(items):
        rows = [f"| `{attribute(tag)}.{e.method}()` | {short(e.summary)} |" for e in items if e.tag == tag]
        sections.append("\n".join([f"### {tag}", "", "| Method | Description |", "| --- | --- |", *rows]))
    text = README.read_text(encoding="utf-8")
    begin, end = text.find(BEGIN), text.find(END)
    if begin == -1 or end < begin:
        raise SystemExit(f"README.md is missing the {BEGIN} / {END} markers.")
    README.write_text(
        text[: begin + len(BEGIN)] + "\n\n" + "\n\n".join(sections) + "\n\n" + text[end:], encoding="utf-8", newline="\n"
    )
    print("README method tables regenerated.")


if __name__ == "__main__":
    main()
