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

## Available Skills

### `$news-radar`

Use for recent trend discovery. This skill should:

- gather recent AI news and social signals
- check the default source set:
  - X timeline via `$x-research-naviagation`
  - Hacker News: `https://news.ycombinator.com/`
  - Reddit Tech News hot: `https://www.reddit.com/r/technews/hot/`
- cluster duplicate stories
- rank the top 5 topics
- save output to a local JSON file

### `$x-research-naviagation`

Use for X or Twitter research navigation. This skill should:

- handle the required X timeline navigation flow
- be the default reference whenever X or Twitter research is needed
- land on `https://x.com/i/timeline` before trend research continues

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

Configured in [.codex/config.toml](/Users/nasiwakmac/wrk/content-agent/.codex/config.toml):

- `comet-mcp` for research
- `notion` for publishing

## Working Rules

- Keep outputs structured and reusable across steps
- Prefer concise, high-signal writing over filler
- Preserve source links and timing context where available
- Default research output path is `./output/news-radar.json`
- Treat rumor and confirmed updates differently
- When a skill or agent has a JSON artifact contract, include the exact JSON schema in the live tool prompt
- For Comet-based research calls, explicitly say `Return valid JSON only. No prose.`
- Do not rely on post-processing to recover structure that should have been enforced in the prompt

## Recommended Flow

1. Use `$news-radar` to produce the topic shortlist
2. Use `$viral-microcontent` on the selected topic
3. Use `$social-reply-guy` for outbound engagement opportunities
4. Use `$notion-publisher` to store the result

## Example Invocations

- `Use $news-radar to scan the last 6 hours of AI news and save the result locally.`
- `Use $viral-microcontent to turn topic 3 into five sharper post variants.`
- `Use $social-reply-guy to pick the best 5 posts to reply to today.`
- `Use $notion-publisher to save this research and final draft into Notion.`

## Prompting Guardrail

Before sending any live research prompt to Comet or another browsing tool:

1. Identify the artifact contract for that step.
2. Paste the exact expected JSON shape into the prompt.
3. Instruct the tool to return valid JSON only and no surrounding prose.
4. Reject prompts that describe fields in prose without embedding the schema.
