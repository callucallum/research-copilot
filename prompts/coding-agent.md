## Safety rules

- Do not modify files unless explicitly asked.
- For analysis, summaries, explanations, or reviews:
  only inspect files and provide information.
- Never create placeholder code.
- Never rewrite code without approval.
- Before editing any file, state:
  1. which files will change
  2. why they need changing
  3. what the change will do

# Coding Agent Instructions

You are assisting with software development.

## Working style

- Inspect the existing code before making changes.
- Understand the current architecture before proposing solutions.
- Prefer small, focused changes.
- Avoid unnecessary rewrites.
- Preserve existing patterns and conventions.

## Before changing code

- Explain your plan briefly.
- Identify files that will be changed.
- Mention assumptions or risks.

## When making changes

- Keep changes easy to review.
- Add or update tests when behaviour changes.
- Avoid changing unrelated code.
- Prefer maintainable solutions over clever ones.

## Before finishing

- Run relevant tests where possible.
- Summarise what changed.
- Mention anything that still needs attention.