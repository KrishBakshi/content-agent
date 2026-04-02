---
name: news-radar
description: Research the last X hours of an AI-focused social timeline and breaking AI news, rank the top 5 most important or trending topics, include the latest startup, product, and feature updates, and save the result as a structured local JSON file. Use when the user wants a fast research sweep, trend summary, or topic shortlist grounded in current chatter and news.
---

# News Radar

Use this skill when the user wants high-signal trend discovery from recent social and news activity.

## Goal

Produce a ranked list of exactly 5 high-signal AI or tech topics from the requested time window, usually `3`, `6`, `12`, or `24` hours.

The output must be valid JSON and should follow the canonical structure in `.codex/references/artifact-spec.md`.

## Required Inputs

- Time window in hours
- Feed or timeline source if the user provides one
- Output path if the user specifies one

If the user does not give an output path, default to `./output/news-radar.json`.

## Required Context To Preserve

- `topic_id` values such as `T1`, `T2`, `T3`
- exact time window
- source URLs
- confidence and uncertainty notes
- whether an item is confirmed, disputed, or rumor

## Data Sources

- Use `comet-mcp` for research and discovery
- Default source set:
  - X timeline: use `x-research-naviagation` and confirm the final destination is `https://x.com/i/timeline`
  - Hacker News: `https://news.ycombinator.com/`
  - Reddit Tech News hot: `https://www.reddit.com/r/technews/hot/`
- When the user provides a URL, explicitly instruct Comet to navigate to that URL first.
- Prioritize AI startup launches, model releases, tooling updates, funding, product announcements, and major breaking news
- Prefer recency and cross-source repetition over vanity metrics alone

## Comet Usage

- Connect to Comet browser first
- If the user provides a URL, open that exact URL first
- Navigate the default source pages directly inside the browser
- Scrape the visible page content in Comet after opening the page
- Use `comet_ask` or Comet search only to support discovery or fill gaps
- Do not rely on generic research summaries alone when the user wants a fresh trend read from the source pages
- If a source is dynamic or partially gated, capture what is directly visible and mark weak evidence clearly

## Workflow

1. Open the requested URL first if the user provides one, otherwise open the default source pages in Comet browser.
2. Scrape the relevant visible page content in Comet.
3. Gather candidate items from the requested time window.
4. Deduplicate stories that describe the same event.
5. Rank by a mix of recency, breadth of discussion, practical importance, and likely downstream attention.
6. Return exactly 5 topics unless the user explicitly asks for a different count.
7. Save the result to a local JSON file.

## Output Contract

Return JSON with this shape:

- `generated_at`
- `time_window_hours`
- `topic_count`
- `sources_checked`
- `notes`
- `topics`

Each entry in `topics` must include:

- `topic_id`
- `rank`
- `title`
- `category`
- `status`
- `summary`
- `why_it_matters`
- `time_window_hours`
- `timing_note`
- `signals`
- `source_links`
- `confidence`

## Ranking Heuristics

Use this order of importance:

1. Confirmed and recent
2. Repeated across multiple visible sources
3. Likely to matter to AI builders, operators, founders, or product teams
4. Specific enough to summarize in one paragraph
5. Not redundant with another selected topic

## Evidence Rules

- Mark `status` as `confirmed`, `rumor`, or `mixed`.
- Do not imply precise timing if the visible source does not support it.
- If the evidence is thin, keep the item but explain the weakness in `timing_note` or `notes`.
- Do not promote pure engagement bait or opinion discourse unless it maps to a concrete development.

## Quality Bar

- Avoid repeating near-identical stories
- Distinguish rumor from confirmed updates
- Keep summaries compact and concrete
- If evidence is thin, say so directly in the JSON

## Local Storage

Write valid JSON only. Create the parent directory if needed.

## Example

```json
{
  "generated_at": "2026-04-01T09:30:00Z",
  "time_window_hours": 6,
  "topic_count": 5,
  "sources_checked": [
    "https://x.com/i/timeline",
    "https://news.ycombinator.com/"
  ],
  "notes": "Ranking favors recent, repeated, and practically important stories.",
  "topics": [
    {
      "topic_id": "T1",
      "rank": 1,
      "title": "Example launch",
      "category": "product_launch",
      "status": "confirmed",
      "summary": "One-sentence description of the development.",
      "why_it_matters": "One-sentence practical implication.",
      "time_window_hours": 6,
      "timing_note": "Visible posts and source pages indicate activity within the requested window.",
      "signals": [
        "Repeated mentions from builders on X",
        "Official launch page linked in public posts"
      ],
      "source_links": [
        "https://x.com/example/status/1",
        "https://example.com/launch"
      ],
      "confidence": "high"
    }
  ]
}
```
