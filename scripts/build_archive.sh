#!/bin/bash
# Extracts historical newspaper editions from git history into editions/<slug>/ directories.
# Run from the repo root (or any subdirectory — the script cds to root automatically).
set -e

cd "$(dirname "$0")/.."

python3 - <<'PYEOF'
import subprocess, os

EDITIONS = [
    ("fa84354", "spring-1907"),
    ("c76402d", "spring-1906"),
    ("091fc13", "fall-1905"),
    ("d281179", "spring-1905"),
    ("12fdb65", "fall-1904"),
    ("671ed49", "spring-1904"),
    ("bd12d8a", "fall-1903"),
]

ARCHIVE_LINK = (
    ' &nbsp;&mdash;&nbsp; '
    '<a href="../../archive.html" style="color:inherit;text-decoration:none;'
    "font-family:'Playfair Display',serif;font-size:12px;font-weight:700;"
    'text-transform:uppercase;letter-spacing:1px;border-bottom:1px solid #2f2f2f;">'
    'Archive</a>'
)

os.makedirs("editions", exist_ok=True)

for hash_, slug in EDITIONS:
    print(f"Extracting {slug} ({hash_})")
    os.makedirs(f"editions/{slug}/assets", exist_ok=True)

    # index.html: fix style path and inject archive nav
    html = subprocess.check_output(["git", "show", f"{hash_}:index.html"]).decode("utf-8", errors="replace")
    html = html.replace('href="style.css"', 'href="../../style.css"')
    html = html.replace("- Seven Pages</div>", f"- Seven Pages{ARCHIVE_LINK}</div>", 1)
    with open(f"editions/{slug}/index.html", "w") as f:
        f.write(html)

    # assets: copy each file as binary from that commit
    asset_paths = subprocess.check_output(
        ["git", "ls-tree", "--name-only", hash_, "assets/"]
    ).decode().splitlines()
    for asset_path in asset_paths:
        data = subprocess.check_output(["git", "show", f"{hash_}:{asset_path}"])
        dest = f"editions/{slug}/{asset_path}"
        with open(dest, "wb") as f:
            f.write(data)

print("Done.")
PYEOF
