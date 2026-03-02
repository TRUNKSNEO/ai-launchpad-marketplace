# AI Launchpad Marketplace

A curated collection of Claude Code plugins to unlock your personal workflows.

## Quick Start

### Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (for MCP servers and CLI tools)

Individual plugins may have additional requirements — refer to each plugin's README.

### Installation

1. Start Claude Code anywhere.
2. Add the marketplace:

```
/plugin marketplace add https://github.com/kenneth-liao/ai-launchpad-marketplace.git
```

3. Browse and install plugins interactively with `/plugin`.

## Available Plugins

| Plugin | Description |
|--------|-------------|
| [Personal Assistant (Elle)](./personal-assistant) | Persistent-memory personal assistant that learns your preferences and context |
| [YouTube](./youtube) | End-to-end YouTube video planning — research, titles, thumbnails, hooks, scripts |
| [Substack](./substack) | Newsletter and Substack Notes content workflows |
| [Writing](./writing) | Authentic voice writing across all content types and platforms |
| [Content Strategy](./content-strategy) | Topic research, title generation, and hook creation |
| [Visual Design](./visual-design) | Thumbnails, social media graphics, and visual assets |
| [Art](./art) | AI image generation and editing via Gemini |
| [Branding Kit](./branding-kit) | Design systems and brand guidelines |
| [Research](./research) | Web research and competitor analysis |
| [Agent Teams](./agent-teams) | Agent team session viewing and analysis |
| [Scheduler](./scheduler) | Cross-platform scheduled automation — recurring skills, prompts, and scripts |
| [Skill Forge](./skill-forge) | Full skill lifecycle — create, integrate, and improve skills |

## Keeping Plugins Updated

By default, third-party marketplaces do **not** auto-update. Enable it so new plugins and updates arrive automatically:

1. Run `/plugin` to open the plugin manager.
2. Navigate to **Marketplaces**, select this marketplace.
3. Choose **Enable auto-update**.

Once enabled, Claude Code refreshes the marketplace and updates installed plugins at startup.

**Manual updates:**

```
/plugin marketplace update ai-launchpad-marketplace   # update all plugins
/plugin update plugin-name                             # update a single plugin
```

## Author

**Kenny Liao (The AI Launchpad)**
[YouTube](https://www.youtube.com/@KennethLiao) · [GitHub](https://github.com/kenneth-liao)
