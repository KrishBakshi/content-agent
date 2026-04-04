# Project Agents

This repository is a small Codex-native content system. It is organized around reusable skills and lightweight agent prompts for AI trend research, content drafting, social engagement, and Notion publishing.

## Purpose

The project is intended to support this workflow:

1. Research the last `X` hours of AI news and social chatter
2. Rank the top 5 topics worth covering
3. Turn one topic into short-form content
4. Find relevant posts to engage with
5. Save research or final drafts into Notion

## Repo Structure

- `.agents/skills/` contains Codex skills that should be invoked by name
- `.codex/agents/` contains reusable agent prompt files
- `.codex/config.toml` defines MCP servers used by the workflow
- `README.md` gives the high-level overview

## Runtime

This project is `uv`-managed.

- Prefer `uv run` for local commands in this repo
- If `browser-use` is invoked locally, run it as `uv run browser-use ...`
- Do not document or suggest bare `python`, `pip`, or `browser-use` commands when the `uv run` form is available

## Available Skills

### `$news-radar`

Use for recent trend discovery. This skill should:

- gather recent AI news and social signals
- check the default source set:
  - X timeline via `$x-trend-research`
  - Hacker News: `https://news.ycombinator.com/`
  - Reddit Tech News hot: `https://www.reddit.com/r/technews/hot/`
- cluster duplicate stories
- rank the top 5 topics
- save output to a local JSON file

### `$x-trend-research`

Use for X or Twitter source collection. This skill should:

- collect visible X timeline posts inside the requested time window
- serve as the X source collector before downstream ranking
- land on `https://x.com/i/timeline`, extract visible posts, and save a reusable JSON artifact

### `$viral-microcontent`

Use for short-form social writing. This skill should:

- convert a topic into under-200-character posts
- lead with a strong hook
- optionally add a short explanation of why the topic matters

### `$social-reply-guy`

Use for engagement selection and reply drafting. This skill should:

- scan a feed or post set
- choose 5 posts worth engaging with
- draft concise replies that add value

### `$notion-publisher`

Use for persistence into Notion. This skill should:

- store research summaries or content drafts
- preserve timestamps, titles, and links
- keep formatting simple and readable

## Available Agent Prompts

### `trend-researcher`

Responsible for recent-topic discovery and ranked research output.

File: [.codex/agents/trend-researcher.md](/Users/nasiwakmac/wrk/content-agent/.codex/agents/trend-researcher.md)

### `content-writer`

Responsible for turning selected topics into concise publishable content.

File: [.codex/agents/content-writer.md](/Users/nasiwakmac/wrk/content-agent/.codex/agents/content-writer.md)

### `engagement-operator`

Responsible for selecting posts to engage with and drafting replies.

File: [.codex/agents/engagement-operator.md](/Users/nasiwakmac/wrk/content-agent/.codex/agents/engagement-operator.md)

### `notion-publisher`

Responsible for writing finalized artifacts into Notion.

File: [.codex/agents/notion-publisher.md](/Users/nasiwakmac/wrk/content-agent/.codex/agents/notion-publisher.md)

### `content-orchestrator`

Responsible for coordinating the full workflow end to end.

File: [.codex/agents/content-orchestrator.md](/Users/nasiwakmac/wrk/content-agent/.codex/agents/content-orchestrator.md)

## MCP Dependencies

Referenced in [.codex/config.toml](/Users/nasiwakmac/wrk/content-agent/.codex/config.toml):

- `browser-use` for browser-driven research and live page inspection
- `notion` for publishing

## Working Rules

- Keep outputs structured and reusable across steps
- Prefer concise, high-signal writing over filler
- Preserve source links and timing context where available
- Default research output path is `./output/news-radar.json`
- Treat rumor and confirmed updates differently
- When a skill or agent has a JSON artifact contract, include the exact JSON schema in the live tool prompt
- For browser-driven research calls, explicitly say `Return valid JSON only. No prose.`
- Keep the workflow integral: `x-trend-research` collects X posts first, `news-radar` ranks the combined source set, downstream steps consume the structured artifact rather than re-inventing it
- When documenting repo commands, prefer `uv run ...` examples
- Do not rely on post-processing to recover structure that should have been enforced in the prompt

## Recommended Flow

1. Use `$x-trend-research` to collect X posts and produce the X source artifact
2. Use `$news-radar` to combine sources and rank the topic shortlist
3. Use `$viral-microcontent` on the selected topic
4. Use `$social-reply-guy` for outbound engagement opportunities
5. Use `$notion-publisher` to store the result

## Example Invocations

- `Use $x-trend-research to collect visible X posts from the last 6 hours and save them locally.`
- `Use $news-radar to scan the last 6 hours of AI news and save the result locally.`
- `Use $viral-microcontent to turn topic 3 into five sharper post variants.`
- `Use $social-reply-guy to pick the best 5 posts to reply to today.`
- `Use $notion-publisher to save this research and final draft into Notion.`
- `Use $browser-use for live source inspection, or run local browser automation with uv run browser-use ...`

## Prompting Guardrail

Before sending any live research prompt to `browser-use` or another browsing tool:

1. Identify the artifact contract for that step.
2. Paste the exact expected JSON shape into the prompt.
3. Instruct the tool to return valid JSON only and no surrounding prose.
4. Reject prompts that describe fields in prose without embedding the schema.
