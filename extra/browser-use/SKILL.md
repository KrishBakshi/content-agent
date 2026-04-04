---
name: browser-use
description: 'Browser automation and live page inspection using Browser Use. Use for navigating web pages, capturing page state, extracting source-backed information, and handling interactive browsing flows.'
license: MIT
---

# Browser Use Agent

## Overview

A specialized skill for controlling and inspecting a live browser session. This skill uses `browser-use` as the default browser automation layer for research and interactive navigation tasks.

This repository is `uv`-managed. When using the local CLI from this project, prefer `uv run browser-use ...`.

## When to Use

Use this skill when:

- **Browser Automation**: Navigating pages, clicking elements, filling forms, and handling login or gated flows.
- **Live Research**: Reading current source pages when freshness matters.
- **Visual Inspection**: Capturing page state, screenshots, or visible content from dynamic sites.
- **Interactive Flows**: Working through multi-step browsing sequences such as X navigation.
- **Evidence Capture**: Extracting directly visible details from source pages before ranking or summarizing.

## Best Practices

- Open the target page first, then inspect the visible state before taking further actions.
- Refresh page state after any major navigation step.
- Prefer direct source-page inspection over secondary summaries when the task depends on recency.
- Mark evidence as weak when the page is partially gated or only partially visible.
- When a browsing task has an artifact contract, paste the exact JSON schema into the prompt and require machine-readable output only.
- In this repo, prefer `uv run browser-use ...` over bare `browser-use ...` in examples or operator instructions.
