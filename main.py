"""One Line, No Deadline Met — make.fun program/v1 entry.

The program writes a single-line joke excusing a missed deadline to
``<output>/entry.txt``. It is fully deterministic: the same line is written
on every run, with no randomness, no clock reads and no network access,
so two runs of the entry always produce byte-identical output.

The joke is a breakup joke: the deadline wanted commitment, the speaker
wanted to see other projects. One sentence, punch at the end, an angle
you do not hear a hundred times.
"""

import os
import sys

# The entry: one sentence, one line, under the 200-character cap.
ENTRY = (
    "I didn't miss the deadline, we broke up \u2014 "
    "it wanted commitment, and I wanted to see other projects."
)

MAX_CHARS = 200


def validate(text):
    """Check the entry against the sealed gate's rules.

    The gate requires UTF-8 text of 1 to 200 characters, not only
    whitespace, and the brief requires a single line.
    """
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d cap" % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")  # must be valid UTF-8
    return text


def read_back(path, expected):
    """Read the file back and confirm it holds exactly what we wrote.

    A trailing newline or a partial write would change the bytes the
    judge sees, so the read-back must match the entry character for
    character before the run can report success.
    """
    with open(path, "r", encoding="utf-8", newline="") as handle:
        actual = handle.read()
    if actual != expected:
        raise ValueError(
            "read-back mismatch: wrote %d characters, read %d"
            % (len(expected), len(actual))
        )
    return actual


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    entry = validate(ENTRY)
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(entry)
    read_back(path, entry)
    print("wrote %s (%d characters)" % (path, len(entry)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
