#!/bin/bash
# setup.sh — Run from inside projects/daily-digest/
#
# Copies connectors from email-agent, installs deps, validates structure.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
EMAIL_AGENT="$REPO_ROOT/projects/email-agent"

echo "=== Daily Digest Setup ==="
echo "  Project:    $SCRIPT_DIR"
echo "  Repo root:  $REPO_ROOT"
echo ""

# ── Step 1: Copy connectors from email-agent ────────────────────────────────
echo "Step 1: Copying connectors from email-agent..."
for file in openrouter.py source_artifact.py llm_io.py; do
    src="$EMAIL_AGENT/connectors/$file"
    dst="$SCRIPT_DIR/connectors/$file"
    if [ -f "$src" ]; then
        cp "$src" "$dst"
        echo "  ✓ $file"
    else
        echo "  ✗ $src not found — copy manually"
    fi
done
echo ""

# ── Step 2: Create outputs directory ─────────────────────────────────────────
echo "Step 2: Creating outputs directory..."
mkdir -p "$SCRIPT_DIR/outputs"
echo "  ✓ outputs/"
echo ""

# ── Step 3: Check .env vars ──────────────────────────────────────────────────
echo "Step 3: Checking .env for required vars..."
ENV_FILE="$REPO_ROOT/.env"
MISSING=0
for var in MS_CLIENT_ID MS_TENANT_ID OPENROUTER_API_KEY; do
    if grep -q "^${var}=" "$ENV_FILE" 2>/dev/null; then
        echo "  ✓ $var"
    else
        echo "  ✗ $var — not found in .env"
        MISSING=1
    fi
done

# Check for new vars
for var in DIGEST_USER_EMAIL DIGEST_USER_DISPLAY_NAMES; do
    if grep -q "^${var}=" "$ENV_FILE" 2>/dev/null; then
        echo "  ✓ $var"
    else
        echo "  ⚠ $var — not found (add from env_additions.txt)"
        MISSING=1
    fi
done
echo ""

# ── Step 4: Install dependencies ─────────────────────────────────────────────
echo "Step 4: Installing Python dependencies..."
pip install -r "$SCRIPT_DIR/requirements.txt" --quiet 2>/dev/null || {
    echo "  ⚠ pip install failed — try: pip install -r requirements.txt"
}
echo ""

# ── Step 5: Validate imports ─────────────────────────────────────────────────
echo "Step 5: Validating imports..."
cd "$SCRIPT_DIR"
python3 -c "
import sys
ok = True

# Check connectors exist
for f in ['connectors/openrouter.py', 'connectors/source_artifact.py', 'connectors/llm_io.py']:
    from pathlib import Path
    if Path(f).exists():
        print(f'  ✓ {f}')
    else:
        print(f'  ✗ {f} — missing')
        ok = False

# Check core imports
try:
    from schemas.inbound_item import InboundItem, make_item_id
    print('  ✓ schemas.inbound_item')
except Exception as e:
    print(f'  ✗ schemas.inbound_item: {e}')
    ok = False

try:
    import numpy as np
    print('  ✓ numpy')
except ImportError:
    print('  ✗ numpy — pip install numpy')
    ok = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    print('  ✓ scikit-learn')
except ImportError:
    print('  ✗ scikit-learn — pip install scikit-learn')
    ok = False

try:
    from sentence_transformers import SentenceTransformer
    print('  ✓ sentence-transformers')
except ImportError:
    print('  ⚠ sentence-transformers — will use TF-IDF fallback')

try:
    import yaml
    print('  ✓ pyyaml')
except ImportError:
    print('  ✗ pyyaml — pip install pyyaml')
    ok = False

if ok:
    print('\n  All checks passed.')
else:
    print('\n  Some checks failed — see above.')
    sys.exit(1)
" || true
echo ""

# ── Done ──────────────────────────────────────────────────────────────────────
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "  1. Add env vars from env_additions.txt to $ENV_FILE"
echo "  2. Update Azure App Registration: add Chat.Read + Chat.ReadBasic permissions"
echo "  3. Test email-only:  python run_pipeline.py --sources email"
echo "  4. Test with Teams:  python run_pipeline.py --sources email,teams"
echo ""
