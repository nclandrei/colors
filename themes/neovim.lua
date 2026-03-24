-- Auto-generated from palette.json — do not edit manually
local M = {}

function M.setup()
  vim.o.termguicolors = true
  vim.g.terminal_color_0 = "#24292e"
  vim.g.terminal_color_1 = "#f97583"
  vim.g.terminal_color_2 = "#85e89d"
  vim.g.terminal_color_3 = "#ffea7f"
  vim.g.terminal_color_4 = "#79b8ff"
  vim.g.terminal_color_5 = "#b392f0"
  vim.g.terminal_color_6 = "#73e3ff"
  vim.g.terminal_color_7 = "#f6f8fa"
  vim.g.terminal_color_8 = "#959da5"
  vim.g.terminal_color_9 = "#f97583"
  vim.g.terminal_color_10 = "#85e89d"
  vim.g.terminal_color_11 = "#ffea7f"
  vim.g.terminal_color_12 = "#79b8ff"
  vim.g.terminal_color_13 = "#b392f0"
  vim.g.terminal_color_14 = "#73e3ff"
  vim.g.terminal_color_15 = "#f6f8fa"

  vim.api.nvim_set_hl(0, "Normal", { fg = "#f6f8fa", bg = "#24292e" })
  vim.api.nvim_set_hl(0, "Cursor", { fg = "#24292e", bg = "#85e89d" })
  vim.api.nvim_set_hl(0, "Visual", { bg = "#c8c8fa" })
  vim.api.nvim_set_hl(0, "CursorLine", { bg = "#2f363d" })
  vim.api.nvim_set_hl(0, "Search", { fg = "#24292e", bg = "#fefb52" })
end

return M
