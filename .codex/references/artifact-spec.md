# Artifact Spec

This project works best when every step produces a predictable artifact that the next step can consume without reinterpretation.

Use the formats in this file as the canonical output contracts for skills and agent prompts.

## Shared Principles

- Keep outputs structured, compact, and reusable.
- Preserve timestamps, links, and uncertainty notes.
- Separate confirmed facts from rumor or weak evidence.
- Reuse topic IDs across research, writing, engagement, and Notion publishing.
- Prefer valid JSON for machine-readable artifacts and short Markdown sections for human-readable pages.
- When calling external tools, paste the exact JSON artifact shape into the prompt.
- For JSON artifacts, end the tool prompt with `Return valid JSON only. No prose.`
- Do not rely on downstream parsing to reconstruct a schema that was not enforced upstream.

## Research Artifact

Use this shape for `news-radar` outputs.

### Top-Level Fields

- `generated_at`
- `time_window_hours`
- `topic_count`
- `sources_checked`
- `notes`
- `topics`

### Topic Fields

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

### JSON Example

```json
{
  "generated_at": "2026-04-01T09:30:00Z",
  "time_window_hours": 6,
  "topic_count": 5,
  "sources_checked": [
    "https://x.com/i/timeline",
    "https://news.ycombinator.com/",
    "https://www.reddit.com/r/technews/hot/"
  ],
  "notes": "Ranks reflect recency, repetition across sources, and practical importance.",
  "topics": [
    {
      "topic_id": "T1",
      "rank": 1,
      "title": "Example model launch",
      "category": "model_release",
      "status": "confirmed",
      "summary": "A compact description of the development.",
      "why_it_matters": "The practical downstream implication.",
      "time_window_hours": 6,
      "timing_note": "Multiple public posts visible within the last 6 hours.",
      "signals": [
        "Repeated discussion from builders on X",
        "Official launch page published today"
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

## Microcontent Artifact

Use this shape for `viral-microcontent`.

### Fields

- `topic_id`
- `platform`
- `format`
- `max_chars`
- `variants`

### Variant Fields

- `variant_id`
- `hook`
- `body`
- `full_text`
- `angle`

### JSON Example

```json
{
  "topic_id": "T1",
  "platform": "x",
  "format": "short_post_variants",
  "max_chars": 200,
  "variants": [
    {
      "variant_id": "V1",
      "hook": "The real AI shift is not bigger models.",
      "body": "It is cheaper deployment to people who were priced out 6 months ago.",
      "full_text": "The real AI shift is not bigger models. It is cheaper deployment to people who were priced out 6 months ago.",
      "angle": "cost_and_access"
    }
  ]
}
```

## Engagement Artifact

Use this shape for `social-reply-guy`.

### Fields

- `generated_at`
- `platform`
- `selection_count`
- `targets`

### Target Fields

- `target_id`
- `post_author`
- `post_url`
- `post_summary`
- `why_this_post`
- `reply_angle`
- `reply_draft`
- `confidence`

### JSON Example

```json
{
  "generated_at": "2026-04-01T09:40:00Z",
  "platform": "x",
  "selection_count": 5,
  "targets": [
    {
      "target_id": "R1",
      "post_author": "Example Founder",
      "post_url": "https://x.com/example/status/2",
      "post_summary": "Founder argues that agent tooling is shifting from demos to operations.",
      "why_this_post": "Strong overlap with AI builders and enough room for a useful reply.",
      "reply_angle": "operational_tradeoff",
      "reply_draft": "The change that matters is not agent demos, it is who owns retries, evals, and failure routing in production.",
      "confidence": "medium"
    }
  ]
}
```

## Notion Page Structure

Use this section order unless the user asks for a different layout.

1. Title
2. Date
3. Scope
4. Ranked items
5. Links
6. Notes or uncertainty

### Markdown Example

```md
# AI / Tech Topics - Last 6 Hours

Date: 2026-04-01
Scope: X-first trend sweep with supporting links

## Topic T1 - Example model launch
Rank: 1
Status: Confirmed
Category: model_release
Summary: A compact description of the development.
Why it matters: The practical downstream implication.
Timing: Multiple public posts visible within the last 6 hours.
Signals:
- Repeated discussion from builders on X
- Official launch page published today
Links:
- https://x.com/example/status/1
- https://example.com/launch

## Notes
- Mark rumor clearly.
- Do not drop source links.
```
