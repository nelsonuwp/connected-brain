#!/usr/bin/env python3
"""
_bridge.py — Sync between connected-brain vault/53-products and product-strategy-gfl

Usage:
  python3 _bridge.py push ["commit message"]   # vault/53-products → git → Confluence
  python3 _bridge.py pull                      # Confluence → git → vault/53-products

Exclusion rules (nothing matching these ever touches gfl):
  - Any file or folder whose name starts with _ (e.g. _supplemental-data/, _notes.md)
  - Any file in EXCLUDE_FILES below
"""

import sys
import re
import subprocess
from pathlib import Path

VAULT_DIR = Path.home() / "connected-brain/vault/53-products"
GFL_DOCS  = Path.home() / "code/product-strategy-gfl/docs"
GFL_REPO  = Path.home() / "code/product-strategy-gfl"

# Specific filenames to always exclude
EXCLUDE_FILES = {'sync.py', '.DS_Store'}


def is_excluded(path: Path) -> bool:
    """Return True if any part of this path starts with _ or is in EXCLUDE_FILES."""
    for part in path.parts:
        if part.startswith('_') or part in EXCLUDE_FILES:
            return True
    return False


def slugify(s):
    s = s.lower()
    s = re.sub(r'[_\s]+', '-', s)
    s = re.sub(r'[^a-z0-9\-.]', '', s)
    return s


def split_frontmatter(text):
    """Return (frontmatter_block, body). frontmatter_block includes the --- delimiters."""
    if not text.startswith('---'):
        return '', text
    end = text.find('---', 3)
    if end == -1:
        return '', text
    return text[:end + 3], text[end + 3:].lstrip('\n')


def vault_to_gfl_path(vault_file):
    """
    Find the corresponding gfl docs path for a vault file.
    Handles slugified filenames (AptCloud_Aptum_IaaS_PRD.md → aptcloud-aptum-iaas-prd.md).
    Returns the gfl path regardless of whether it exists yet (for new files).
    """
    rel = vault_file.relative_to(VAULT_DIR)

    # Try direct match first
    direct = GFL_DOCS / rel
    if direct.exists():
        return direct

    # Try slugified match
    parts = rel.parts
    slug_parts = []
    for p in parts:
        if p.endswith('.md'):
            slug_parts.append(slugify(p[:-3]) + '.md')
        else:
            slug_parts.append(slugify(p))
    return GFL_DOCS / Path(*slug_parts)


def push(message='sync: from connected-brain vault'):
    """Push vault/53-products → product-strategy-gfl/docs → git → Confluence."""
    changed = False

    for vault_file in sorted(VAULT_DIR.rglob("*.md")):
        rel = vault_file.relative_to(VAULT_DIR)
        if is_excluded(rel):
            continue

        gfl_file = vault_to_gfl_path(vault_file)
        vault_content = vault_file.read_text(encoding='utf-8')
        _, vault_body = split_frontmatter(vault_content)

        if gfl_file.exists():
            gfl_content = gfl_file.read_text(encoding='utf-8')
            frontmatter, _ = split_frontmatter(gfl_content)
            # Keep gfl's front-matter, replace body with vault content
            new_content = (frontmatter + '\n\n' + vault_body) if frontmatter else vault_body
            if new_content != gfl_content:
                gfl_file.write_text(new_content, encoding='utf-8')
                print(f"  updated: {gfl_file.relative_to(GFL_REPO)}")
                changed = True
        else:
            # New file — gfl will create the Confluence page on next push
            gfl_file.parent.mkdir(parents=True, exist_ok=True)
            gfl_file.write_text(vault_body, encoding='utf-8')
            print(f"  created: {gfl_file.relative_to(GFL_REPO)}")
            changed = True

    if changed:
        subprocess.run(['git', 'add', '-A'], cwd=GFL_REPO, check=True)
        has_staged = subprocess.run(
            ['git', 'diff', '--cached', '--quiet'], cwd=GFL_REPO
        ).returncode != 0
        if has_staged:
            subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=GFL_REPO, check=True
            )
            subprocess.run(['git', 'push'], cwd=GFL_REPO, check=True)
            print("  → pushed to product-strategy-gfl (gfl will update Confluence)")
    else:
        print("  no changes")


def pull():
    """Pull Confluence → git → vault/53-products, stripping gfl front-matter."""
    # Step 1: pull from git remote (other contributors' pushes)
    print("  git pull...")
    subprocess.run(['git', 'pull'], cwd=GFL_REPO, check=True)

    # Step 2: pull from Confluence explicitly (gfl fetches page tree and merges)
    print("  gfl pull...")
    subprocess.run(['gfl', 'pull'], cwd=GFL_REPO, check=True)

    # Step 2: copy gfl docs → vault, stripping front-matter
    for gfl_file in sorted(GFL_DOCS.rglob("*.md")):
        content = gfl_file.read_text(encoding='utf-8')
        _, body = split_frontmatter(content)
        vault_file = VAULT_DIR / gfl_file.relative_to(GFL_DOCS)
        vault_file.parent.mkdir(parents=True, exist_ok=True)
        existing = vault_file.read_text(encoding='utf-8') if vault_file.exists() else None
        if existing != body:
            vault_file.write_text(body, encoding='utf-8')
            print(f"  updated: {vault_file.relative_to(VAULT_DIR)}")


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in ('push', 'pull'):
        print('Usage: _bridge.py push ["commit message"] | pull')
        sys.exit(1)
    if sys.argv[1] == 'push':
        msg = sys.argv[2] if len(sys.argv) > 2 else 'sync: from connected-brain vault'
        print("Pushing vault → product-strategy-gfl → Confluence...")
        push(msg)
    else:
        print("Pulling Confluence → product-strategy-gfl → vault...")
        pull()
