#!/usr/bin/env python3
"""Rewrites the README's method tables (between the GENERATED markers) from the spec."""

from __future__ import annotations

from pathlib import Path

from spec import attribute, endpoints, load, tags_in_order

README = Path(__file__).resolve().parent.parent / "README.md"
BEGIN = "<!-- BEGIN GENERATED API REFERENCE -->"
END = "<!-- END GENERATED API REFERENCE -->"


def main() -> None:
    items = endpoints(load())
    sections = []
    for tag in tags_in_order(items):
        rows = [
            f"| `client.{attribute(tag)}.{e.method}()` | `GET {e.path}` | {e.summary.replace('|', chr(92) + '|')} |"
            for e in items
            if e.tag == tag
        ]
        sections.append("\n".join([f"### {tag}", "", "| Method | Endpoint | What it returns |", "| --- | --- | --- |", *rows]))
    text = README.read_text(encoding="utf-8")
    begin, end = text.find(BEGIN), text.find(END)
    if begin == -1 or end < begin:
        raise SystemExit(f"README.md is missing the {BEGIN} / {END} markers.")
    README.write_text(text[: begin + len(BEGIN)] + "\n\n" + "\n\n".join(sections) + "\n\n" + text[end:], encoding="utf-8")
    print("README method tables regenerated.")


if __name__ == "__main__":
    main()
