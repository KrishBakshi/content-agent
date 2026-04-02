---
name: viral-microcontent
description: Turn a selected trend, news item, or source note into short-form viral social content with a strong hook and concise body under 200 characters. Use when the user wants punchy posts, multiple variants, or a short elaboration pattern such as why the topic matters.
---

# Viral Microcontent

Use this skill when the user wants concise distribution copy for social platforms.

## Goal

Generate compact, high-retention social copy from a single topic while preserving the topic's actual claim and context.

The output should follow the canonical variant structure in `.codex/references/artifact-spec.md`.

## Default Constraints

- Stay under `200` characters unless the user overrides it
- Lead with a hook
- Follow with a tight payoff
- Avoid filler, hashtags, and generic hype unless requested

## Inputs

Accept any of:

- A topic title
- A research summary
- A JSON topic object from `news-radar`
- A direct user brief

Prefer structured input with:

- `topic_id`
- `title`
- `summary`
- `why_it_matters`
- `confidence`

## Workflow

1. Identify the core claim, surprise, or tension in the topic.
2. Write a hook that earns attention quickly.
3. Finish with a compact body that explains the point or implication.
4. If the user asks to elaborate, append a short second line in a pattern like `Here's why this matters: ...`

## Output Contract

Return either a compact JSON object or an equivalent plainly labeled structure with:

- `topic_id`
- `platform`
- `format`
- `max_chars`
- `variants`

Each entry in `variants` must include:

- `variant_id`
- `hook`
- `body`
- `full_text`
- `angle`

## Output Modes

- Single post
- Multiple variants
- Hook-only options
- Hook plus explanation

## Writing Rules

- Prefer specificity over adjectives
- Avoid corporate tone
- Make the implication legible in one read
- Use plain ASCII unless the user asks for something else
- If facts are uncertain, do not manufacture certainty

## Quality Bar

- The post should feel publishable without cleanup.
- The hook should introduce tension, surprise, or consequence.
- The body should clarify the point instead of repeating the hook.
- Avoid sounding like a summary bot.

## Example

```json
{
  "topic_id": "T1",
  "platform": "x",
  "format": "short_post_variants",
  "max_chars": 200,
  "variants": [
    {
      "variant_id": "V1",
      "hook": "The biggest AI shift is not smarter models.",
      "body": "It is who can finally afford to ship them.",
      "full_text": "The biggest AI shift is not smarter models. It is who can finally afford to ship them.",
      "angle": "cost_and_access"
    }
  ]
}
```
