# YouTube

End-to-end YouTube video planning — orchestrates research, writing, and design skills into YouTube-specific production workflows.

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) (required for the YouTube Data API script)
- AI Launchpad marketplace added — see [main README](../README.md)
- `YOUTUBE_API_KEY` environment variable set with a [YouTube Data API](https://developers.google.com/youtube/v3/getting-started) key

## Installation

```
/plugin install youtube@ai-launchpad-marketplace
```

Restart Claude Code for the changes to take effect.

## Skills

| Skill | Description |
|-------|-------------|
| `youtube-data` | Retrieve YouTube data: search videos, get details, fetch transcripts, read comments, discover trending/related content |
| `plan-video` | Complete video planning: research, titles, thumbnails, hooks, content outline |
| `repurpose-video` | Repurpose a completed video into newsletter issues, social posts, and more |
| `newsletter-to-video` | Convert a newsletter issue into a YouTube video outline |
| `create-post` | Create YouTube community posts for engagement |

## Agents

| Agent | Description |
|-------|-------------|
| YouTube Researcher | Expert researcher using the YouTube Data API script via Bash |
| Thumbnail Reviewer | Evaluates thumbnail concepts against proven design patterns |
