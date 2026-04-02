# Content Agent

This repo defines reusable Codex skills and agent prompts for a repeatable AI-content workflow.

The main improvement target in this project is consistency: every research, writing, engagement, and publishing step should produce a predictable artifact with enough context for the next step to consume directly.

## Workflow

1. Research the last `X` hours of AI and tech activity.
2. Rank the top 5 topics.
3. Turn one topic into short-form content.
4. Pick posts worth replying to.
5. Save outputs into Notion.

## Canonical Artifact Contract

Use the shared reference at [.codex/references/artifact-spec.md](/Users/nasiwakmac/wrk/content-agent/.codex/references/artifact-spec.md) as the source of truth for:

- `news-radar` JSON structure
- `viral-microcontent` output shape
- `social-reply-guy` reply selection structure
- Notion page section order

Every prompt and skill should preserve:

- stable topic IDs
- timestamps and time-window context
- source links
- explicit confidence or uncertainty notes

## Skills

This repo includes the following reusable skills:

1. `news-radar`
2. `viral-microcontent`
3. `social-reply-guy`
4. `notion-publisher`
5. `comet-browser`
6. `x-research-naviagation`

The MCP servers already configured in [.codex/config.toml](/Users/nasiwakmac/wrk/content-agent/.codex/config.toml) are:

- `comet-mcp` for research
- `notion` for publishing and storage

## Layout

- `.agents/skills/` contains Codex-discoverable skills
- `.codex/agents/` contains reusable agent prompt files
- `.codex/references/` contains shared artifact and prompt reference material

## Skill Summary

### `news-radar`

Research the last `X` hours of AI and tech activity, deduplicate overlapping items, rank exactly 5 topics, and save valid JSON that matches the shared artifact spec.

### `viral-microcontent`

Turn one topic into concise social copy with a fixed variant structure and a clear hook-plus-payoff pattern.

### `social-reply-guy`

Select the 5 best posts to engage with and return replies in a stable, reusable target list.

### `notion-publisher`

Convert a final artifact into a clean Notion page or database entry while preserving links, timestamps, topic IDs, and section order.

### `comet-browser`

Use `comet-mcp` for current, source-backed research when the task depends on live web information.

### `x-research-naviagation`

Use this whenever X or Twitter research is part of the workflow. It is the canonical navigation reference for reaching the X timeline before continuing trend research.

## Agents

- `trend-researcher.md`
- `content-writer.md`
- `engagement-operator.md`
- `notion-publisher.md`
- `content-orchestrator.md`

## Prompting Standard

Prompts in this repo should be:

- explicit about inputs
- explicit about output format
- strict about uncertainty handling
- concise enough to execute reliably
- strong enough to preserve context across handoffs

Each skill or agent prompt should ideally answer:

1. What is the mission?
2. What inputs are required?
3. What exact output shape is expected?
4. What quality bar must be met?
5. What example should the model imitate?

## Example Invocations

To use these in Codex, invoke the skills by name, for example:

- `Use $news-radar to gather the top AI topics from the last 6 hours.`
- `Use $viral-microcontent to draft three hooks for topic 2.`
- `Use $social-reply-guy to find five posts worth engaging with today.`
- `Use $notion-publisher to save these final drafts to Notion.`
- `Use $comet-browser to search the web for the latest information on this topic and cite the sources.`
