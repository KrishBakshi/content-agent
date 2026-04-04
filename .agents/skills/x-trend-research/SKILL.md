---
name: x-trend-research
description: >
  Work with the X timeline scraper in
  .agents/skills/x-trend-research/x_trend_research.py. Use this skill when the
  user wants to run, debug, modify, or inspect the X scraper, change the time
  window, adjust scrolling behavior, update navigation to the X timeline,
  monitor live collection logs, or validate the generated JSON artifact in
  output/news-radar.json.
allowed-tools: Read, Bash(uv run python .agents/skills/x-trend-research/x_trend_research.py:*), Bash(uv run pyright:*), Bash(uv run ruff check:*), Bash(uv run python -m py_compile:*)
---

# X Trend Research Scraper

Use this skill for the local X scraper at:

- `.agents/skills/x-trend-research/x_trend_research.py`

Default artifact path:

- `output/news-radar.json`

## Workflow

1. Read the scraper file first.
2. If the user wants a run, use `uv run python .agents/skills/x-trend-research/x_trend_research.py --headless --model gemini-3.1-flash-lite-preview`.
3. Prefer passing `--headless --model gemini-3.1-flash-lite-preview` on the CLI as the documented default unless the user asks for a different model.
4. If the user wants a narrower scrape, pass `--time-window-hours N`.
5. Once the script starts, do not interrupt, redirect, or second-guess it unless the user explicitly asks. Observe the live logs and let the process stop on its own.
6. The browser-use agent may emit multiple successful intermediate extraction blocks before the script exits. Treat those as progress only, not completion.
7. Treat the saved artifact as final only after the Python process exits naturally. The file is written in `async_main()`, not during intermediate extraction passes.
8. If the user wants a fast stable run, use `--headless --model gemini-3.1-flash-lite-preview` unless they ask for a different model.
9. After changes, validate with:
   - `uv run python .agents/skills/x-trend-research/x_trend_research.py --headless --model gemini-3.1-flash-lite-preview`
   - `uv run pyright .agents/skills/x-trend-research/x_trend_research.py`
   - `uv run ruff check .agents/skills/x-trend-research/x_trend_research.py`
   - `uv run python -m py_compile .agents/skills/x-trend-research/x_trend_research.py`

## Runtime Notes

- The script expects an authenticated X browser profile.
- It can read user data dir from:
  - `--user-data-dir`
  - `USER_DATA_DIR`
  - `BROWSER_USE_USER_DATA_DIR`
  - `CHROME_USER_DATA_DIR`
- Supported model envs in the script:
  - `BROWSER_USE_API_KEY`
  - `GOOGLE_API_KEY`
  - `OPENAI_API_KEY`

## Current Behavior

- Navigation to `https://x.com/i/timeline` is deterministic and browser-driven.
- The script scrolls downward and collects only posts with parseable visible relative timestamps inside `--time-window-hours`.
- The collector runs repeated extraction passes while scrolling, so repeated `Final Result` log blocks during the run are expected.
- While a run is active, the correct operator behavior is hands-off observation. Do not stop the run just because intermediate output looks complete.
- `output/news-radar.json` is written once the run exits, either with a success artifact or a structured error artifact.
- It writes JSON with:
  - `generated_at`
  - `time_window_hours`
  - `post_count`
  - `sources_checked`
  - `notes`
  - `posts`

## Debug Priorities

- If navigation fails, inspect the notification selection flow first.
- If scraping is slow, check repeated extraction passes and screenshot-related waits.
- If logs look successful but the artifact file is stale, confirm whether the process has actually exited yet.
- If output looks noisy, inspect timestamp parsing and post dedupe behavior.
- If the user asks for a specific model, run with `--model` rather than editing the script unless they explicitly want a code change.
- Treat `--headless --model gemini-3.1-flash-lite-preview` as the default documented invocation in this repo.
