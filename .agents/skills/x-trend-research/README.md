# X Trend Research

Scrape visible X timeline posts within a requested time window with `browser-use` and save a strict JSON artifact.

## What It Does

1. Opens `https://x.com/home`
2. Uses the visible `Notifications` flow to find a notification item with a blue icon
3. Verifies that the resulting page is exactly `https://x.com/i/timeline`
4. Extracts only directly visible timeline posts
5. Scrolls downward and keeps collecting posts with visible timestamps inside the requested time window
6. Writes `./output/news-radar.json` by default

## Requirements

- An authenticated X session in Chrome
- A model credential
  - Preferred: `BROWSER_USE_API_KEY` for `ChatBrowserUse`
  - Supported fallback: `GOOGLE_API_KEY` for `ChatGoogle`
  - Fallback: `OPENAI_API_KEY`
- A Chrome profile path, either:
  - passed with `--user-data-dir`
  - or set in `.env` as `USER_DATA_DIR`
  - or set in `.env` as `BROWSER_USE_USER_DATA_DIR`

## Usage

Recommended monitored run:

```bash
uv run python .agents/skills/x-trend-research/x_trend_research.py \
  --profile-directory "Default" \
  --time-window-hours 1 \
  --headless \
  --model gemini-3.1-flash-lite-preview
```

Authenticated Chrome profile run:

```bash
uv run python .agents/skills/x-trend-research/x_trend_research.py \
  --user-data-dir "$HOME/Library/Application Support/Google/Chrome" \
  --profile-directory "Default" \
  --time-window-hours 1 \
  --headless \
  --model gemini-3.1-flash-lite-preview
```

If `USER_DATA_DIR` or `BROWSER_USE_USER_DATA_DIR` is already in `.env`, you can omit `--user-data-dir`:

```bash
uv run python .agents/skills/x-trend-research/x_trend_research.py \
  --profile-directory "Default" \
  --time-window-hours 1 \
  --headless \
  --model gemini-3.1-flash-lite-preview
```

Documented default mode:

```bash
uv run python .agents/skills/x-trend-research/x_trend_research.py \
  --user-data-dir "$HOME/Library/Application Support/Google/Chrome" \
  --profile-directory "Default" \
  --time-window-hours 1 \
  --headless \
  --model gemini-3.1-flash-lite-preview
```

Custom output path:

```bash
uv run python .agents/skills/x-trend-research/x_trend_research.py \
  --user-data-dir "$HOME/Library/Application Support/Google/Chrome" \
  --profile-directory "Default" \
  --time-window-hours 1 \
  --output ./output/news-radar.json \
  --headless \
  --model gemini-3.1-flash-lite-preview
```

## Notes

- The script fails explicitly if it cannot find a visible blue-icon notification item.
- The documented default CLI in this repo includes `--headless --model gemini-3.1-flash-lite-preview`.
- The script only includes posts whose visible relative timestamps are within `--time-window-hours`.
- The script scrolls downward until it stops finding in-window posts or reaches `--max-scrolls`.
- The browser-use logs may show several successful intermediate extraction results while the collector is still running. That is normal.
- Once started, let the script run uninterrupted and only observe its logs unless the user explicitly asks you to stop it.
- The final artifact is written when the Python process exits, so monitor the logs and wait for natural process completion before trusting `output/news-radar.json`.
- If X is partially gated, the script writes an error artifact instead of inventing data.
- The browser profile should not be in active use by another Chrome process while the script runs.
