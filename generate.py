"""Generate terminal theme files from palette.json."""

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PALETTE = ROOT / "palette.json"
THEMES = ROOT / "themes"


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def hex_to_float(h: str) -> tuple[float, float, float]:
    r, g, b = hex_to_rgb(h)
    return r / 255.0, g / 255.0, b / 255.0


def load_palette() -> dict:
    with open(PALETTE) as f:
        return json.load(f)


# ── Ghostty ──────────────────────────────────────────────────────────────────


def write_ghostty(palette: dict) -> None:
    c = palette["colors"]
    ansi = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
    lines = [
        f"background = {c['background']}",
        f"foreground = {c['foreground']}",
        f"cursor-color = {c['cursor']}",
        f"cursor-text = {c['cursor_text']}",
        f"selection-background = {c['selection']}",
        f"selection-foreground = {c['selection_text']}",
    ]
    for i, name in enumerate(ansi):
        lines.append(f"palette = {i}={c[name]}")
    for i, name in enumerate(ansi):
        lines.append(f"palette = {i + 8}={c[f'bright_{name}']}")
    (THEMES / "ghostty").write_text("\n".join(lines) + "\n")


# ── iTerm2 ───────────────────────────────────────────────────────────────────


def iterm_color(h: str, alpha: float = 1.0) -> dict:
    r, g, b = hex_to_float(h)
    return {
        "Red Component": r,
        "Green Component": g,
        "Blue Component": b,
        "Alpha Component": alpha,
        "Color Space": "sRGB",
    }


def write_iterm2(palette: dict) -> None:
    c = palette["colors"]
    ansi = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
    profile: dict = {
        "Name": "Default",
        "Guid": "A1B2C3D4-5678-9012-ABCD-DOTFILES0001",
        "Dynamic Profile Parent Name": "Default",
    }
    for i, name in enumerate(ansi):
        profile[f"Ansi {i} Color"] = iterm_color(c[name])
    for i, name in enumerate(ansi):
        profile[f"Ansi {i + 8} Color"] = iterm_color(c[f"bright_{name}"])
    profile["Background Color"] = iterm_color(c["background"])
    profile["Foreground Color"] = iterm_color(c["foreground"])
    profile["Bold Color"] = iterm_color(c["bold"])
    profile["Cursor Color"] = iterm_color(c["cursor"])
    profile["Cursor Text Color"] = iterm_color(c["cursor_text"])
    profile["Cursor Guide Color"] = iterm_color(c["cursor_guide"])
    profile["Selection Color"] = iterm_color(c["selection"], alpha=0.14509804546833038)
    profile["Selected Text Color"] = iterm_color(c["selection_text"])
    profile["Badge Color"] = iterm_color(c["badge"], alpha=0.5)
    profile["Link Color"] = iterm_color(c["link"])
    profile["Match Background Color"] = iterm_color(c["match"])
    doc = {"Profiles": [profile]}
    with open(THEMES / "iterm2.json", "w") as f:
        json.dump(doc, f, indent=2)
        f.write("\n")


# ── Neovim ───────────────────────────────────────────────────────────────────


def write_neovim(palette: dict) -> None:
    c = palette["colors"]
    ansi_order = [
        "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
        "bright_black", "bright_red", "bright_green", "bright_yellow",
        "bright_blue", "bright_magenta", "bright_cyan", "bright_white",
    ]
    lines = [
        '-- Auto-generated from palette.json — do not edit manually',
        "local M = {}",
        "",
        "function M.setup()",
        '  vim.o.termguicolors = true',
    ]
    for i, name in enumerate(ansi_order):
        lines.append(f'  vim.g.terminal_color_{i} = "{c[name]}"')
    lines += [
        "",
        f'  vim.api.nvim_set_hl(0, "Normal", {{ fg = "{c["foreground"]}", bg = "{c["background"]}" }})',
        f'  vim.api.nvim_set_hl(0, "Cursor", {{ fg = "{c["cursor_text"]}", bg = "{c["cursor"]}" }})',
        f'  vim.api.nvim_set_hl(0, "Visual", {{ bg = "{c["selection"]}" }})',
        f'  vim.api.nvim_set_hl(0, "CursorLine", {{ bg = "{c["cursor_guide"]}" }})',
        f'  vim.api.nvim_set_hl(0, "Search", {{ fg = "{c["background"]}", bg = "{c["match"]}" }})',
        "end",
        "",
        "return M",
    ]
    (THEMES / "neovim.lua").write_text("\n".join(lines) + "\n")


# ── Main ─────────────────────────────────────────────────────────────────────


def main() -> None:
    os.makedirs(THEMES, exist_ok=True)
    palette = load_palette()
    write_ghostty(palette)
    write_iterm2(palette)
    write_neovim(palette)
    print(f"Generated themes in {THEMES}/")


if __name__ == "__main__":
    main()
