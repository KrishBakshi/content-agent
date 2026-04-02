---
name: comet-browser
description: Use comet-mcp for browser navigation, live web browsing, search, and page inspection when the user needs current information from the web, source-backed research, or interaction with dynamic pages. Use when the task depends on recent online information, direct page reads, or browser-based discovery.
---

# Comet Browser

Use this skill when the user needs current information from the web and the task benefits from navigating pages directly in Comet browser.

## Goal

Use `comet-mcp` as the default web tool for:

- browser navigation
- URL-first page scraping
- web search
- browsing live pages
- checking dynamic or JavaScript-heavy sites
- gathering source-backed findings

This skill is for live context gathering, not loose summarization. The result should preserve source URLs, time context, and uncertainty.

## When To Use It

- The user asks to browse, search, look something up, or verify current information
- The answer depends on recent developments, live pages, or source links
- A page likely needs browser rendering instead of static fetching
- The task involves moving through a site or feed rather than answering from a single search result
- The user gives a specific URL and wants that page scraped

## Workflow

1. Connect to Comet browser first.
2. If the user provides a URL, open that exact URL before doing anything else.
3. Scrape the visible content from the target page in Comet.
4. Use `comet_ask` to support discovery, summarize what is on the page, or widen the search when navigation alone is not enough.
5. If the task needs deeper synthesis across multiple sources, use search or research mode after browsing the core pages.
6. Keep or return source links, dates, and confidence where possible.

## Output Contract

Return concise findings with:

- `title`
- `summary`
- `source_links`
- `date_context`
- `confidence`
- `notes`

When the user specifies an exact output schema, return that schema only.
Do not prepend or append navigation summaries, status updates, headings, or explanatory prose outside the requested payload.
If the task asks for JSON, return valid JSON only.
If the task asks for a fixed number of items, return exactly that count unless the visible evidence does not support it, and then explain the shortfall inside the requested output fields rather than outside the payload.

## Tool Guidance

- Use `comet_connect` at the start of browser-based tasks
- Use the user-provided URL as the first navigation target when one exists
- Use browser navigation and scraping as the primary workflow
- Use `comet_mode` with `search` for normal web search
- Use `comet_mode` with `research` for deeper multi-source research
- Use `comet_ask` to support the navigation workflow, not replace it by default
- Use `comet_poll` for long-running research tasks
- Use `comet_screenshot` if visual confirmation from a page is useful
- Use `comet_stop` if the active task goes off track

## Prompting Rules

- Be explicit about what to find
- Include recency constraints when they matter
- Ask for source URLs in the result
- Separate confirmed facts from inference
- Prefer primary sources when available
- When the caller provides a target output format, tell Comet to return only that format and nothing else

## Example

```json
{
  "title": "Example launch page",
  "summary": "A direct summary of what is visible on the live page.",
  "source_links": [
    "https://example.com/launch"
  ],
  "date_context": "Page published today; exact timestamp not visible on page.",
  "confidence": "medium",
  "notes": "Source is live but the timing detail is partial."
}
```

## Quality Bar

- Do not answer from memory when live verification is needed
- Prefer direct sources over reposts or summaries
- Call out stale, conflicting, or weak evidence
- Keep browser navigation focused on the user’s question
