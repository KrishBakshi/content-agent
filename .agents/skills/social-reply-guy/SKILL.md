---
name: social-reply-guy
description: Review an AI-focused feed, pick the 5 most relevant posts to engage with, and draft useful replies designed to attract like-minded people interested in AI, tools, and individual skill leverage. Use when the user wants reply strategy, comment drafts, or high-signal engagement opportunities on X or LinkedIn.
---

# Social Reply Guy

Use this skill when the user wants to engage on social platforms in a targeted way.

## Goal

Find the best posts to reply to and draft replies that feel informed, relevant, and likely to attract the right audience.

The output should follow the engagement artifact contract in `.codex/references/artifact-spec.md`.

## Platforms

- X
- LinkedIn

## Workflow

1. Review the available feed or post set.
2. Score posts for relevance, audience overlap, and conversation quality.
3. Select the top 5 engagement targets.
4. Draft one reply per target.
5. Keep replies additive, not repetitive or clout-chasing.

## Output Contract

Return:

- `generated_at`
- `platform`
- `selection_count`
- `targets`

Each target must include:

- `target_id`
- `post_author`
- `post_url`
- `post_summary`
- `why_this_post`
- `reply_angle`
- `reply_draft`
- `confidence`

## Selection Criteria

- Strong overlap with AI builders, operators, founders, or tool users
- Enough momentum to matter but not so saturated that a reply is invisible
- A reply can add a real perspective, example, or clarification

## Reply Rules

- Sound like a smart peer, not a fan account
- Add one concrete idea, example, or point of tension
- Avoid empty praise
- Avoid long threads unless asked
- Match the platform's tone

If the user wants it, also include a suggested posting order.

## Example

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
      "post_summary": "Founder argues that agent tooling is moving from demos to operations.",
      "why_this_post": "The audience overlap is strong and there is room for a concrete operational reply.",
      "reply_angle": "operational_tradeoff",
      "reply_draft": "The hard part now is not getting agents to work once. It is owning retries, evals, and failure routing after launch.",
      "confidence": "medium"
    }
  ]
}
```
