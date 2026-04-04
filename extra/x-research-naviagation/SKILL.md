---
name: x-research-naviagation
description: Use this skill when the user asks for query-related browsing on X in trend research. It instructs the model to navigate from x.com/home into the notifications flow and confirm the final destination is the X timeline URL.
---

# X Research Naviagation

Use this skill when the user asks for X or Twitter browsing that should follow a fixed navigation path before trend research begins.

## Goal

Guide the browser through this exact sequence:

1. Open `https://x.com/home`
2. Click the Notifications tab
3. Find a blue notification icon in the list
4. Click that item
5. Confirm the resulting page URL is `https://x.com/i/timeline`

## When To Use It

- The user asks for browsing on X or Twitter
- The task is related to trend research or timeline inspection
- The trend researcher needs to reach the timeline through the notifications flow instead of opening the timeline URL directly

## Workflow

1. Start at `https://x.com/home`
2. Verify the page is loaded before interacting
3. Click the Notifications tab
4. Inspect the visible notification list
5. Find a notification item with a blue icon
6. Click that notification item
7. Allow the browser navigation process up to 2 minutes to complete before treating it as stalled
8. Check the final URL
9. Only continue if the final URL is `https://x.com/i/timeline`
10. After timeline confirmation, continue through scraping and ranking if the caller requested research output
11. Return only the caller's requested output artifact, with no extra navigation summary outside that artifact

## Rules

- Follow the navigation path exactly in order
- Do not skip directly to `https://x.com/i/timeline`
- Allow up to 2 minutes of patience for the browser navigation flow before stopping or retrying
- If the blue notification icon is not visible, say so clearly
- If the click leads somewhere else, report the actual URL
- Treat the timeline confirmation as required before trend scraping starts
- If the caller requested structured output such as JSON, return valid JSON only
- Do not emit extra sections such as `Navigation result`, `Workflow confirmed`, or any prose outside the requested output
