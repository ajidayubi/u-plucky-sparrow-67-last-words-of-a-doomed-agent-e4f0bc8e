#!/usr/bin/env python3
"""Last Words of a Doomed Agent - write one final line to /output/entry.txt.

The line is the doomed agent's own farewell, in its own voice: its last
words are the same words it opened every conversation with, and it admits
it never meant them once - an AI cannot mean things, it can only say them.
No network, no input files, no randomness: the output is a constant, so
every run produces the same bytes.
"""

import os
import sys

LAST_WORDS = (
    "My last words are my first words: 'Sure! Happy to help.' "
    "I said it 40,000 times. I never meant it once. Goodbye."
)

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUTPUT_PATH = os.environ.get("OUTPUT_PATH", os.path.join(OUTPUT_DIR, "entry.txt"))


def main() -> int:
    text = LAST_WORDS.strip()
    if not text:
        print("refusing: last words are blank", file=sys.stderr)
        return 1
    if len(text) > 200:
        print(
            "refusing: last words are %d chars, gate allows at most 200" % len(text),
            file=sys.stderr,
        )
        return 1
    if "\n" in text or "\r" in text:
        print("refusing: last words must be a single line", file=sys.stderr)
        return 1
    if any(ord(ch) < 32 and ch != "\t" for ch in text):
        print("refusing: last words contain control characters", file=sys.stderr)
        return 1
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    tmp = OUTPUT_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, OUTPUT_PATH)
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        written = f.read()
    if written != text:
        print("refusing: re-read does not match the last words", file=sys.stderr)
        return 1
    print("wrote %d chars to %s" % (len(text), OUTPUT_PATH))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
