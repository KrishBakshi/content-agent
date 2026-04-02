---
name: notion-publisher
description: Save research outputs, topic summaries, or final social content into Notion using a clean page structure. Use when the user wants to persist generated content, maintain an editorial workspace, or store curated outputs in Notion after research or writing is complete.
---

# Notion Publisher

Use this skill when the user wants content saved into Notion.

## Goal

Turn generated outputs into a clean Notion page or database entry with minimal cleanup required afterward.

Use the shared Notion section order in `.codex/references/artifact-spec.md` unless the user asks for a different structure.

## Inputs

Accept any of:

- Topic research summaries
- A local JSON file path
- Final social post drafts
- Engagement reply drafts

## Workflow

1. Read the final artifact to be stored.
2. Normalize it into a clear structure with headings or properties.
3. Create or update the target Notion destination.
4. Preserve source titles, timestamps, and links where available.

## Structure

Prefer this shape unless the user provides a different one:

- Title
- Date
- Scope
- Ranked items or entries
- Links
- Notes or uncertainty

## Rules

- Keep formatting simple and readable
- Do not drop links or timestamps if they exist
- Preserve the user's wording unless asked to rewrite
- If the destination is ambiguous, use the user's existing Notion context

## Output Expectations

When reporting back after publishing, include:

- destination page or database
- what artifact was stored
- whether the content was created or updated
- any missing or weak source context that could not be preserved

## Tooling

- Use the `notion` MCP server for page or database operations

## Example Page Shape

```md
# AI / Tech Topics - Last 6 Hours

Date: 2026-04-01
Scope: X-first trend sweep

## Topic T1 - Example launch
Rank: 1
Status: Confirmed
Category: product_launch
Summary: One-sentence description.
Why it matters: One-sentence implication.
Timing: Visible activity within the requested window.
Links:
- https://x.com/example/status/1
- https://example.com/launch

## Notes
- Rumors are labeled explicitly.
```
