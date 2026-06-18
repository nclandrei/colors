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

    bg        = c["background"]
    fg        = c["foreground"]
    cursor    = c["cursor"]
    cursor_tx = c["cursor_text"]
    sel       = c["selection"]
    sel_tx    = c["selection_text"]
    guide     = c["cursor_guide"]
    match     = c["match"]
    link      = c["link"]
    badge     = c["badge"]
    red       = c["red"]
    green     = c["green"]
    yellow    = c["yellow"]
    blue      = c["blue"]
    magenta   = c["magenta"]
    cyan      = c["cyan"]
    gray      = c["bright_black"]

    out: list[str] = []
    a = out.append

    a('-- Auto-generated from palette.json — do not edit manually')
    a('vim.cmd("highlight clear")')
    a('if vim.fn.exists("syntax_on") == 1 then vim.cmd("syntax reset") end')
    a('vim.o.termguicolors = true')
    a('vim.g.colors_name = "colors"')
    a('')
    a('local hl = vim.api.nvim_set_hl')
    a('local function link(from, to) hl(0, from, { link = to }) end')
    a('')
    a('-- Terminal palette')
    for i, name in enumerate(ansi_order):
        a(f'vim.g.terminal_color_{i} = "{c[name]}"')
    a('')
    a('-- Editor UI')
    a(f'hl(0, "Normal",       {{ fg = "{fg}", bg = "{bg}" }})')
    a(f'hl(0, "NormalFloat",  {{ fg = "{fg}", bg = "{guide}" }})')
    a(f'hl(0, "FloatBorder",  {{ fg = "{gray}", bg = "{guide}" }})')
    a(f'hl(0, "FloatTitle",   {{ fg = "{blue}", bg = "{guide}", bold = true }})')
    a(f'hl(0, "Cursor",       {{ fg = "{cursor_tx}", bg = "{cursor}" }})')
    a(f'hl(0, "CursorLine",   {{ bg = "{guide}" }})')
    a(f'hl(0, "CursorColumn", {{ bg = "{guide}" }})')
    a(f'hl(0, "ColorColumn",  {{ bg = "{guide}" }})')
    a(f'hl(0, "LineNr",       {{ fg = "{gray}" }})')
    a(f'hl(0, "CursorLineNr", {{ fg = "{fg}", bold = true }})')
    a(f'hl(0, "SignColumn",   {{ bg = "NONE" }})')
    a(f'hl(0, "Visual",       {{ fg = "{sel_tx}", bg = "{sel}" }})')
    a(f'hl(0, "VisualNOS",    {{ bg = "{sel}" }})')
    a(f'hl(0, "Search",       {{ fg = "{bg}", bg = "{match}" }})')
    a(f'hl(0, "IncSearch",    {{ fg = "{bg}", bg = "{match}" }})')
    a(f'hl(0, "CurSearch",    {{ fg = "{bg}", bg = "{match}" }})')
    a(f'hl(0, "MatchParen",   {{ fg = "{yellow}", bold = true, underline = true }})')
    a(f'hl(0, "NonText",      {{ fg = "{gray}" }})')
    a(f'hl(0, "Whitespace",   {{ fg = "{guide}" }})')
    a(f'hl(0, "EndOfBuffer",  {{ fg = "{bg}" }})')
    a(f'hl(0, "Directory",    {{ fg = "{blue}" }})')
    a(f'hl(0, "Title",        {{ fg = "{blue}", bold = true }})')
    a(f'hl(0, "WinSeparator", {{ fg = "{guide}" }})')
    a(f'hl(0, "VertSplit",    {{ fg = "{guide}" }})')
    a(f'hl(0, "StatusLine",   {{ fg = "{fg}", bg = "{guide}" }})')
    a(f'hl(0, "StatusLineNC", {{ fg = "{gray}", bg = "{guide}" }})')
    a(f'hl(0, "TabLine",      {{ fg = "{gray}", bg = "{guide}" }})')
    a(f'hl(0, "TabLineSel",   {{ fg = "{fg}", bg = "{bg}", bold = true }})')
    a(f'hl(0, "TabLineFill",  {{ bg = "{guide}" }})')
    a(f'hl(0, "WinBar",       {{ fg = "{fg}", bg = "{bg}" }})')
    a(f'hl(0, "WinBarNC",     {{ fg = "{gray}", bg = "{bg}" }})')
    a(f'hl(0, "Folded",       {{ fg = "{gray}", bg = "{guide}" }})')
    a(f'hl(0, "FoldColumn",   {{ fg = "{gray}" }})')
    a(f'hl(0, "Pmenu",        {{ fg = "{fg}", bg = "{guide}" }})')
    a(f'hl(0, "PmenuSel",     {{ fg = "{bg}", bg = "{blue}", bold = true }})')
    a(f'hl(0, "PmenuSbar",    {{ bg = "{guide}" }})')
    a(f'hl(0, "PmenuThumb",   {{ bg = "{gray}" }})')
    a(f'hl(0, "WildMenu",     {{ fg = "{bg}", bg = "{blue}" }})')
    a(f'hl(0, "ModeMsg",      {{ fg = "{fg}", bold = true }})')
    a(f'hl(0, "MoreMsg",      {{ fg = "{blue}" }})')
    a(f'hl(0, "Question",     {{ fg = "{blue}" }})')
    a(f'hl(0, "ErrorMsg",     {{ fg = "{red}", bold = true }})')
    a(f'hl(0, "WarningMsg",   {{ fg = "{yellow}" }})')
    a(f'hl(0, "SpecialKey",   {{ fg = "{gray}" }})')
    a(f'hl(0, "Conceal",      {{ fg = "{gray}" }})')
    a('')
    a('-- Classic syntax')
    a(f'hl(0, "Comment",         {{ fg = "{gray}", italic = true }})')
    a(f'hl(0, "Constant",        {{ fg = "{cyan}" }})')
    a(f'hl(0, "String",          {{ fg = "{green}" }})')
    a(f'hl(0, "Character",       {{ fg = "{green}" }})')
    a(f'hl(0, "Number",          {{ fg = "{magenta}" }})')
    a(f'hl(0, "Boolean",         {{ fg = "{magenta}" }})')
    a(f'hl(0, "Float",           {{ fg = "{magenta}" }})')
    a(f'hl(0, "Identifier",      {{ fg = "{fg}" }})')
    a(f'hl(0, "Function",        {{ fg = "{blue}" }})')
    a(f'hl(0, "Statement",       {{ fg = "{red}" }})')
    a(f'hl(0, "Conditional",     {{ fg = "{red}" }})')
    a(f'hl(0, "Repeat",          {{ fg = "{red}" }})')
    a(f'hl(0, "Label",           {{ fg = "{red}" }})')
    a(f'hl(0, "Operator",        {{ fg = "{fg}" }})')
    a(f'hl(0, "Keyword",         {{ fg = "{red}" }})')
    a(f'hl(0, "Exception",       {{ fg = "{red}" }})')
    a(f'hl(0, "PreProc",         {{ fg = "{magenta}" }})')
    a(f'hl(0, "Include",         {{ fg = "{magenta}" }})')
    a(f'hl(0, "Define",          {{ fg = "{magenta}" }})')
    a(f'hl(0, "Macro",           {{ fg = "{magenta}" }})')
    a(f'hl(0, "PreCondit",       {{ fg = "{magenta}" }})')
    a(f'hl(0, "Type",            {{ fg = "{yellow}" }})')
    a(f'hl(0, "StorageClass",    {{ fg = "{yellow}" }})')
    a(f'hl(0, "Structure",       {{ fg = "{yellow}" }})')
    a(f'hl(0, "Typedef",         {{ fg = "{yellow}" }})')
    a(f'hl(0, "Special",         {{ fg = "{cyan}" }})')
    a(f'hl(0, "SpecialChar",     {{ fg = "{cyan}" }})')
    a(f'hl(0, "Tag",             {{ fg = "{red}" }})')
    a(f'hl(0, "Delimiter",       {{ fg = "{fg}" }})')
    a(f'hl(0, "SpecialComment",  {{ fg = "{cyan}", italic = true }})')
    a(f'hl(0, "Debug",           {{ fg = "{red}" }})')
    a(f'hl(0, "Underlined",      {{ fg = "{blue}", underline = true }})')
    a(f'hl(0, "Todo",            {{ fg = "{yellow}", bold = true }})')
    a(f'hl(0, "Error",           {{ fg = "{red}", bold = true }})')
    a('')
    a('-- Treesitter (@-captures)')
    a('link("@comment",              "Comment")')
    a('link("@string",               "String")')
    a('link("@string.escape",        "Special")')
    a('link("@character",            "Character")')
    a('link("@number",               "Number")')
    a('link("@boolean",              "Boolean")')
    a('link("@float",                "Float")')
    a('link("@function",             "Function")')
    a('link("@function.call",        "Function")')
    a(f'hl(0, "@function.builtin",   {{ fg = "{cyan}" }})')
    a('link("@function.macro",       "Macro")')
    a('link("@method",               "Function")')
    a('link("@method.call",          "Function")')
    a('link("@constructor",          "Type")')
    a(f'hl(0, "@parameter",          {{ fg = "{fg}" }})')
    a('link("@keyword",              "Keyword")')
    a('link("@keyword.function",     "Keyword")')
    a('link("@keyword.operator",     "Keyword")')
    a('link("@keyword.return",       "Keyword")')
    a('link("@conditional",          "Conditional")')
    a('link("@repeat",               "Repeat")')
    a('link("@label",                "Label")')
    a('link("@operator",             "Operator")')
    a('link("@exception",            "Exception")')
    a('link("@variable",             "Identifier")')
    a(f'hl(0, "@variable.builtin",   {{ fg = "{cyan}" }})')
    a(f'hl(0, "@variable.member",    {{ fg = "{cyan}" }})')
    a(f'hl(0, "@field",              {{ fg = "{cyan}" }})')
    a(f'hl(0, "@property",           {{ fg = "{cyan}" }})')
    a('link("@constant",             "Constant")')
    a(f'hl(0, "@constant.builtin",   {{ fg = "{cyan}" }})')
    a('link("@constant.macro",       "Macro")')
    a('link("@type",                 "Type")')
    a(f'hl(0, "@type.builtin",       {{ fg = "{yellow}" }})')
    a('link("@type.definition",      "Typedef")')
    a(f'hl(0, "@namespace",          {{ fg = "{yellow}" }})')
    a(f'hl(0, "@module",             {{ fg = "{yellow}" }})')
    a('link("@include",              "Include")')
    a('link("@punctuation",          "Delimiter")')
    a('link("@punctuation.bracket",  "Delimiter")')
    a('link("@punctuation.delimiter","Delimiter")')
    a('link("@punctuation.special",  "Special")')
    a(f'hl(0, "@tag",                {{ fg = "{red}" }})')
    a(f'hl(0, "@tag.attribute",      {{ fg = "{yellow}" }})')
    a(f'hl(0, "@tag.delimiter",      {{ fg = "{fg}" }})')
    a(f'hl(0, "@text",               {{ fg = "{fg}" }})')
    a('hl(0, "@text.strong",         { bold = true })')
    a('hl(0, "@text.emphasis",       { italic = true })')
    a('hl(0, "@text.underline",      { underline = true })')
    a(f'hl(0, "@text.title",         {{ fg = "{blue}", bold = true }})')
    a(f'hl(0, "@text.literal",       {{ fg = "{green}" }})')
    a(f'hl(0, "@text.uri",           {{ fg = "{blue}", underline = true }})')
    a(f'hl(0, "@text.todo",          {{ fg = "{yellow}", bold = true }})')
    a(f'hl(0, "@text.note",          {{ fg = "{blue}", bold = true }})')
    a(f'hl(0, "@text.warning",       {{ fg = "{yellow}", bold = true }})')
    a(f'hl(0, "@text.danger",        {{ fg = "{red}", bold = true }})')
    a(f'hl(0, "@text.diff.add",      {{ fg = "{green}" }})')
    a(f'hl(0, "@text.diff.delete",   {{ fg = "{red}" }})')
    a('')
    a('-- LSP semantic tokens')
    a('link("@lsp.type.function",   "Function")')
    a('link("@lsp.type.method",     "Function")')
    a('link("@lsp.type.variable",   "Identifier")')
    a('link("@lsp.type.parameter",  "@parameter")')
    a('link("@lsp.type.property",   "@property")')
    a('link("@lsp.type.type",       "Type")')
    a('link("@lsp.type.struct",     "Structure")')
    a('link("@lsp.type.enum",       "Type")')
    a('link("@lsp.type.enumMember", "Constant")')
    a('link("@lsp.type.interface",  "Type")')
    a('link("@lsp.type.class",      "Type")')
    a('link("@lsp.type.namespace",  "@namespace")')
    a('link("@lsp.type.macro",      "Macro")')
    a('link("@lsp.type.keyword",    "Keyword")')
    a('link("@lsp.type.string",     "String")')
    a('link("@lsp.type.comment",    "Comment")')
    a('')
    a('-- Diagnostics')
    a(f'hl(0, "DiagnosticError", {{ fg = "{red}" }})')
    a(f'hl(0, "DiagnosticWarn",  {{ fg = "{yellow}" }})')
    a(f'hl(0, "DiagnosticInfo",  {{ fg = "{blue}" }})')
    a(f'hl(0, "DiagnosticHint",  {{ fg = "{cyan}" }})')
    a(f'hl(0, "DiagnosticOk",    {{ fg = "{green}" }})')
    a(f'hl(0, "DiagnosticUnderlineError", {{ undercurl = true, sp = "{red}" }})')
    a(f'hl(0, "DiagnosticUnderlineWarn",  {{ undercurl = true, sp = "{yellow}" }})')
    a(f'hl(0, "DiagnosticUnderlineInfo",  {{ undercurl = true, sp = "{blue}" }})')
    a(f'hl(0, "DiagnosticUnderlineHint",  {{ undercurl = true, sp = "{cyan}" }})')
    a('link("DiagnosticVirtualTextError", "DiagnosticError")')
    a('link("DiagnosticVirtualTextWarn",  "DiagnosticWarn")')
    a('link("DiagnosticVirtualTextInfo",  "DiagnosticInfo")')
    a('link("DiagnosticVirtualTextHint",  "DiagnosticHint")')
    a('')
    a('-- Diff')
    a(f'hl(0, "DiffAdd",    {{ fg = "{green}",  bg = "{guide}" }})')
    a(f'hl(0, "DiffChange", {{ fg = "{blue}",   bg = "{guide}" }})')
    a(f'hl(0, "DiffDelete", {{ fg = "{red}",    bg = "{guide}" }})')
    a(f'hl(0, "DiffText",   {{ fg = "{yellow}", bg = "{guide}", bold = true }})')
    a('')
    a('-- Gitsigns')
    a(f'hl(0, "GitSignsAdd",    {{ fg = "{green}" }})')
    a(f'hl(0, "GitSignsChange", {{ fg = "{blue}" }})')
    a(f'hl(0, "GitSignsDelete", {{ fg = "{red}" }})')
    a('')
    a('-- Telescope')
    a('link("TelescopeBorder",        "FloatBorder")')
    a('link("TelescopePromptBorder",  "FloatBorder")')
    a('link("TelescopeResultsBorder", "FloatBorder")')
    a('link("TelescopePreviewBorder", "FloatBorder")')
    a(f'hl(0, "TelescopeSelection",   {{ bg = "{guide}", bold = true }})')
    a(f'hl(0, "TelescopeMatching",    {{ fg = "{match}", bold = true }})')
    a(f'hl(0, "TelescopePromptPrefix",{{ fg = "{blue}" }})')
    a('')
    a('-- nvim-cmp')
    a('link("CmpItemAbbr",            "Pmenu")')
    a(f'hl(0, "CmpItemAbbrMatch",     {{ fg = "{match}", bold = true }})')
    a(f'hl(0, "CmpItemAbbrMatchFuzzy",{{ fg = "{match}", bold = true }})')
    a(f'hl(0, "CmpItemAbbrDeprecated",{{ fg = "{gray}", strikethrough = true }})')
    a(f'hl(0, "CmpItemKindFunction",  {{ fg = "{blue}" }})')
    a(f'hl(0, "CmpItemKindMethod",    {{ fg = "{blue}" }})')
    a(f'hl(0, "CmpItemKindVariable",  {{ fg = "{fg}" }})')
    a(f'hl(0, "CmpItemKindKeyword",   {{ fg = "{red}" }})')
    a(f'hl(0, "CmpItemKindClass",     {{ fg = "{yellow}" }})')
    a(f'hl(0, "CmpItemKindInterface", {{ fg = "{yellow}" }})')
    a(f'hl(0, "CmpItemKindModule",    {{ fg = "{yellow}" }})')
    a(f'hl(0, "CmpItemKindSnippet",   {{ fg = "{magenta}" }})')
    a(f'hl(0, "CmpItemKindText",      {{ fg = "{fg}" }})')
    a(f'hl(0, "CmpItemMenu",          {{ fg = "{gray}" }})')
    a('')
    a('-- Trouble')
    a('link("TroubleNormal",       "NormalFloat")')
    a(f'hl(0, "TroubleText",       {{ fg = "{fg}" }})')
    a(f'hl(0, "TroubleCount",      {{ fg = "{magenta}" }})')
    a('link("TroubleFile",         "Directory")')
    a('link("TroubleSource",       "Comment")')
    a('')
    a('-- Indent-blankline (v3)')
    a(f'hl(0, "IblIndent",         {{ fg = "{guide}" }})')
    a(f'hl(0, "IblScope",          {{ fg = "{gray}" }})')
    a('')
    a('-- Misc references kept for downstream use')
    a(f'-- link={link} badge={badge}')

    (THEMES / "colors.lua").write_text("\n".join(out) + "\n")
    legacy = THEMES / "neovim.lua"
    if legacy.exists():
        legacy.unlink()


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
