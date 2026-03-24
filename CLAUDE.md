# Colors

Single-source terminal color palette repo.

## Structure

- `palette.json` — canonical color definitions (single source of truth)
- `generate.py` — reads palette.json, writes all target theme files (stdlib only, no deps)
- `themes/` — generated output, committed to repo

## Workflow

1. Edit `palette.json`
2. Run `uv run generate.py`
3. Commit both palette.json and themes/

## Conventions

- All colors are hex strings in palette.json
- generate.py uses stdlib only (json, os, pathlib) — no external deps
- iTerm2 profile uses GUID `A1B2C3D4-5678-9012-ABCD-DOTFILES0001` and inherits from Default
- iTerm2 selection has custom alpha (0.145), badge has alpha 0.5
- Ghostty theme is symlinked from `~/.config/ghostty/themes/colors`
- iTerm2 JSON is symlinked from `~/Library/Application Support/iTerm2/DynamicProfiles/colors.json`
- Both symlinks are managed by `~/code/dotfiles/Makefile`
