"""Generate src/app/tokens.css from design/tokens.json.

design/tokens.json is the single source of truth for the Socratic design
system. Tailwind reads it directly (tailwind.config.ts); this script emits the
same values as CSS custom properties for the hand-written classes in
src/app/globals.css.

Run from the repo root after editing tokens.json:

    python scripts/build_tokens.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "design" / "tokens.json"
OUT = ROOT / "src" / "app" / "tokens.css"


def main() -> None:
    tokens = json.loads(SRC.read_text(encoding="utf-8"))
    lines = [
        "/* GENERATED from design/tokens.json by scripts/build_tokens.py — do not edit by hand. */",
        ":root {",
        "  /* Colors */",
    ]
    for name, tok in tokens["color"].items():
        lines.append(f"  --color-{name}: {tok['$value']};")

    lines += ["", "  /* Typography — Scale */"]
    for name, tok in tokens["typography"].items():
        v = tok["$value"]
        lines.append(f"  --text-{name}: {v['fontSize']};")
        lines.append(f"  --leading-{name}: {v['lineHeight']};")
        lines.append(f"  --weight-{name}: {v['fontWeight']};")

    lines += ["", "  /* Spacing */"]
    for name, tok in tokens["spacing"].items():
        lines.append(f"  --spacing-{name}: {tok['$value']};")

    lines += ["", "  /* Border Radius */"]
    for name, tok in tokens["radius"].items():
        lines.append(f"  --radius-{name}: {tok['$value']};")

    lines += ["", "  /* Borders */"]
    for name, tok in tokens["border"].items():
        lines.append(f"  --border-{name}: {tok['$value']};")

    lines += ["", "  /* Shadows */"]
    for name, tok in tokens["shadow"].items():
        lines.append(f"  --shadow-{name}: {tok['$value']};")

    lines += ["", "  /* Surfaces */"]
    for name, tok in tokens["surface"].items():
        lines.append(f"  --surface-{name}: {tok['$value']};")

    lines += ["}", ""]
    OUT.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(lines)} lines)")


if __name__ == "__main__":
    main()
