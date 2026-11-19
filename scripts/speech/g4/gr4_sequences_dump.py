"""Print the source of the gr4_sequences questions (and, with --spoken, the narration beside it).

    python -X utf8 scripts/speech/g4/gr4_sequences_dump.py [start] [count] [--spoken] [--only] [--ids] [--grep=<regex>]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gr4_algebra_dump  # noqa: E402  (the same printer, pointed at this topic)

if __name__ == "__main__":
    gr4_algebra_dump.main("gr4_sequences")
