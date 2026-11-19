"""Print the source strings and narration of gr4_triangles questions. Same arguments as gr4_angles_dump.py.

    python -X utf8 scripts/speech/g4/gr4_triangles_dump.py            # compact list
    python -X utf8 scripts/speech/g4/gr4_triangles_dump.py 0 40       # full source
    python -X utf8 scripts/speech/g4/gr4_triangles_dump.py nar 0 40   # narration only
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gr4_angles_dump as dump  # noqa: E402

dump.NODE = "gr4_triangles"
dump.OUT = os.path.join(dump.common.ROOT, "data", "question-speech", "parts-g4", dump.NODE + ".json")

if __name__ == "__main__":
    dump.main()
