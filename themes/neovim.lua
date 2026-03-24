-- Auto-generated from palette.json — do not edit manually
local M = {}

function M.setup()
  vim.o.termguicolors = true
  vim.g.terminal_color_0 = "#1b1e28"
  vim.g.terminal_color_1 = "#d0679d"
  vim.g.terminal_color_2 = "#5de4c7"
  vim.g.terminal_color_3 = "#fffac2"
  vim.g.terminal_color_4 = "#89ddff"
  vim.g.terminal_color_5 = "#f087bd"
  vim.g.terminal_color_6 = "#89ddff"
  vim.g.terminal_color_7 = "#ffffff"
  vim.g.terminal_color_8 = "#a6accd"
  vim.g.terminal_color_9 = "#d0679d"
  vim.g.terminal_color_10 = "#5de4c7"
  vim.g.terminal_color_11 = "#fffac2"
  vim.g.terminal_color_12 = "#add7ff"
  vim.g.terminal_color_13 = "#f087bd"
  vim.g.terminal_color_14 = "#add7ff"
  vim.g.terminal_color_15 = "#ffffff"

  vim.api.nvim_set_hl(0, "Normal", { fg = "#e4f0fb", bg = "#1b1e28" })
  vim.api.nvim_set_hl(0, "Cursor", { fg = "#1b1e28", bg = "#5de4c7" })
  vim.api.nvim_set_hl(0, "Visual", { bg = "#717cb4" })
  vim.api.nvim_set_hl(0, "CursorLine", { bg = "#303340" })
  vim.api.nvim_set_hl(0, "Search", { fg = "#1b1e28", bg = "#fffac2" })
end

return M
