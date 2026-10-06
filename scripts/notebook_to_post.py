#!/usr/bin/env python3
"""Convert Jupyter notebooks in notebooks/ to blog posts in src/pages/posts/.

Usage:
    python scripts/notebook_to_post.py            # convert all notebooks
    python scripts/notebook_to_post.py my-nb.ipynb

Notebook front matter: put a raw cell at the very top of the notebook with
JSON metadata (title, description, date, tags). If absent, defaults are used.

The notebook is executed (so plots/outputs are fresh) and converted to
Markdown with outputs embedded, saved as a .md post with front matter.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NB_DIR = ROOT / "notebooks"
POSTS_DIR = ROOT / "src" / "pages" / "posts"

# Metadata in raw cell: title, description, date, tags.
DEFAULT_META = {
    "title": "Untitled Notebook",
    "description": "A notebook post.",
    "date": "2025-01-01",
    "tags": ["notebook"],
}


def extract_meta(nb):
    meta = dict(DEFAULT_META)
    cell = nb.get("cells", [])
    if cell and cell[0].get("cell_type") == "raw":
        try:
            parsed = json.loads(cell[0].get("source", ""))
            meta.update(parsed)
        except json.JSONDecodeError:
            pass
    return meta


def main():
    if not NB_DIR.exists():
        sys.exit(f"Notebook directory not found: {NB_DIR}")

    targets = [NB_DIR / name for name in sys.argv[1:]] or sorted(NB_DIR.glob("*.ipynb"))
    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    for nb_path in targets:
        nb = json.loads(nb_path.read_text(encoding="utf-8"))
        meta = extract_meta(nb)
        md_path = POSTS_DIR / (nb_path.stem + ".md")

        # Execute notebook and convert to Markdown with embedded outputs.
        subprocess.run(
            [
                "jupyter",
                "nbconvert",
                "--to",
                "notebook",
                "--execute",
                "--inplace",
                str(nb_path),
            ],
            check=True,
            cwd=ROOT,
        )

        # First execute in-place to refresh outputs, then export to Markdown.
        subprocess.run(
            [
                "jupyter",
                "nbconvert",
                "--to",
                "markdown",
                str(nb_path),
            ],
            check=True,
            cwd=NB_DIR,
        )

        # nbconvert writes <stem>.md and <stem>_files/ next to the notebook.
        converted = nb_path.with_suffix(".md")
        if not converted.exists():
            sys.exit(f"nbconvert did not produce {converted}")

        # Move generated image files into public/notebook-assets/<stem>/.
        assets_src = nb_path.with_name(nb_path.stem + "_files")
        assets_dir = ROOT / "public" / "notebook-assets" / nb_path.stem
        if assets_src.exists():
            assets_dir.mkdir(parents=True, exist_ok=True)
            for img in assets_src.iterdir():
                (assets_dir / img.name).write_bytes(img.read_bytes())
            # Rewrite image links in the Markdown to the public path.
            body = converted.read_text(encoding="utf-8")
            body = body.replace(f"{nb_path.stem}_files/", f"/notebook-assets/{nb_path.stem}/")
            converted.write_text(body, encoding="utf-8")
            for img in assets_src.iterdir():
                img.unlink()
            assets_src.rmdir()

        tags = meta.get("tags", [])
        if isinstance(tags, list):
            tags = [str(t) for t in tags]
        else:
            tags = [str(tags)]

        front = [
            "---",
            f"title: {json.dumps(meta['title'])}",
            f"description: {json.dumps(meta['description'])}",
            f"date: {json.dumps(str(meta['date']))}",
            f"tags: {json.dumps(tags)}",
            "---",
            "",
        ]
        md_path.write_text(
            "\n".join(front) + converted.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        converted.unlink()
        print(f"Converted {nb_path.name} -> {md_path}")


if __name__ == "__main__":
    main()
