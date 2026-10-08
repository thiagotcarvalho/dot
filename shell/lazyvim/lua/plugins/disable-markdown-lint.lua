-- Disable the markdown linter (markdownlint-cli2) while keeping the rest of the
-- LazyVim markdown extra (marksman LSP, rendering, conform formatting).
-- Function form is required: LazyVim concatenates list-valued opts, so a plain
-- `linters_by_ft = { markdown = {} }` would merge into the existing entry
-- instead of clearing it.
return {
  "mfussenegger/nvim-lint",
  optional = true,
  opts = function(_, opts)
    if opts.linters_by_ft then
      opts.linters_by_ft.markdown = {}
    end
    return opts
  end,
}
