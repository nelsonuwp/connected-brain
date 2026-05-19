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

    Special case: if the vault file is folder/index.md and gfl has a post-pull
    folder.md alongside folder/, prefer folder/index.md (reconcile_structure()
    should have already restored this, but guard here too).
    """
    rel = vault_file.relative_to(VAULT_DIR)

    # Try direct match first
    direct = GFL_DOCS / rel
    if direct.exists():
        return direct

    # If this is an index.md, check for the pull-renamed folder.md form and
    # prefer the index.md path so reconcile stays in effect.
    if rel.name == 'index.md' and len(rel.parts) > 1:
        folder_md = GFL_DOCS / rel.parent.with_suffix('.md')
        if folder_md.exists() and (GFL_DOCS / rel.parent).is_dir():
            # reconcile_structure() should have moved this already; return the
            # canonical index.md path so the content lands in the right place.
            return direct  # direct doesn't exist yet → bridge will create it

    # Try slugified match
    parts = rel.parts
    slug_parts = []
    for p in parts:
        if p.endswith('.md'):
            slug_parts.append(slugify(p[:-3]) + '.md')
        else:
            slug_parts.append(slugify(p))
    return GFL_DOCS / Path(*slug_parts)


def reconcile_structure():
    """
    gfl pull renames folder/index.md → folder.md (inconsistent with gfl push's
    ensurePushParents() which only looks for folder/index.md). Restore the correct
    naming on both the working tree and the confluence tracking branch so that
    parent page IDs are found correctly on the next push.
    """
    # Find folder.md + sibling folder/ pairs in working tree
    pairs = []
    for gfl_file in sorted(GFL_DOCS.rglob("*.md")):
        if gfl_file.name == 'index.md':
            continue
        dir_path = gfl_file.with_suffix('')
        if dir_path.is_dir():
            pairs.append((gfl_file, dir_path / 'index.md'))

    if not pairs:
        return

    # Step 1: Fix working tree — move folder.md → folder/index.md
    for folder_md, index_md in pairs:
        folder_content = folder_md.read_text(encoding='utf-8')
        folder_fm, _ = split_frontmatter(folder_content)
        if index_md.exists():
            # Merge page ID from folder.md into existing index.md's frontmatter
            _, existing_body = split_frontmatter(index_md.read_text(encoding='utf-8'))
            new_content = (folder_fm + '\n\n' + existing_body) if folder_fm else existing_body
            index_md.write_text(new_content, encoding='utf-8')
        else:
            index_md.write_text(folder_content, encoding='utf-8')
        folder_md.unlink()

    # Step 2: Fix confluence branch using git plumbing (no checkout required)
    import os, tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix='.gfl-idx') as tmp:
        tmp_index = tmp.name
    try:
        env = os.environ.copy()
        env['GIT_INDEX_FILE'] = tmp_index

        tree_hash = subprocess.run(
            ['git', 'rev-parse', 'confluence^{tree}'],
            cwd=GFL_REPO, capture_output=True, text=True, check=True
        ).stdout.strip()

        subprocess.run(['git', 'read-tree', tree_hash],
                       cwd=GFL_REPO, env=env, check=True)

        any_changed = False
        for folder_md, index_md in pairs:
            rel_old = str(folder_md.relative_to(GFL_REPO))
            rel_new = str(index_md.relative_to(GFL_REPO))

            lt = subprocess.run(
                ['git', 'ls-tree', 'confluence', rel_old],
                cwd=GFL_REPO, capture_output=True, text=True
            )
            if lt.returncode != 0 or not lt.stdout.strip():
                continue
            blob_hash = lt.stdout.strip().split()[2]

            subprocess.run(['git', 'update-index', '--remove', rel_old],
                           cwd=GFL_REPO, env=env, check=True)
            subprocess.run(
                ['git', 'update-index', '--add', '--cacheinfo',
                 f'100644,{blob_hash},{rel_new}'],
                cwd=GFL_REPO, env=env, check=True
            )
            any_changed = True

        if any_changed:
            new_tree = subprocess.run(
                ['git', 'write-tree'], cwd=GFL_REPO, env=env,
                capture_output=True, text=True, check=True
            ).stdout.strip()

            cur_commit = subprocess.run(
                ['git', 'rev-parse', 'confluence'],
                cwd=GFL_REPO, capture_output=True, text=True, check=True
            ).stdout.strip()

            new_commit = subprocess.run(
                ['git', 'commit-tree', new_tree, '-p', cur_commit,
                 '-m', 'chore: restore index.md structure for parent lookup'],
                cwd=GFL_REPO, capture_output=True, text=True, check=True
            ).stdout.strip()

            subprocess.run(
                ['git', 'update-ref', 'refs/heads/confluence', new_commit],
                cwd=GFL_REPO, check=True
            )
            print(f"  reconciled: {len([p for p in pairs])} index file(s) restored on confluence branch")
    finally:
        os.unlink(tmp_index)


def push(message='sync: from connected-brain vault'):
    """Push vault/53-products → product-strategy-gfl/docs → git → Confluence."""
    reconcile_structure()
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

    # Step 2: pull from Confluence explicitly (gfl fetches page tree, merges, updates local docs)
    print("  gfl pull...")
    subprocess.run(['gfl', 'pull'], cwd=GFL_REPO, check=True)

    # Step 3: copy gfl docs → vault, stripping front-matter
    expected_vault_files = set()
    for gfl_file in sorted(GFL_DOCS.rglob("*.md")):
        content = gfl_file.read_text(encoding='utf-8')
        _, body = split_frontmatter(content)
        vault_file = VAULT_DIR / gfl_file.relative_to(GFL_DOCS)
        vault_file.parent.mkdir(parents=True, exist_ok=True)
        expected_vault_files.add(vault_file)
        existing = vault_file.read_text(encoding='utf-8') if vault_file.exists() else None
        if existing != body:
            vault_file.write_text(body, encoding='utf-8')
            print(f"  updated: {vault_file.relative_to(VAULT_DIR)}")

    # Step 4: delete vault files that no longer exist in gfl (deleted from Confluence)
    for vault_file in sorted(VAULT_DIR.rglob("*.md")):
        rel = vault_file.relative_to(VAULT_DIR)
        if is_excluded(rel):
            continue
        if vault_file not in expected_vault_files:
            vault_file.unlink()
            print(f"  deleted: {rel} (removed from Confluence)")


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
