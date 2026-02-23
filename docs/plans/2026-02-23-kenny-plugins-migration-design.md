# Design: kenny-plugins Personal Marketplace

**Date:** 2026-02-23
**Status:** Approved

## Context

The AI Launchpad Marketplace contains 12 plugins — most are personal-use content creation and workflow tools. The public GitHub repo is shared with YouTube viewers, but only 2 plugins (personal-assistant, agent-teams) are intended for public distribution. The remaining 10 plugins need a separate private repo.

## Decision

Create `~/projects/kenny-plugins/` as a self-contained personal plugin marketplace. Migrate 10 plugins via copy. Remove them from the public marketplace.

## Plugins to Migrate (10)

**Foundation:** writing, content-strategy, visual-design, branding-kit, art, research
**Orchestrators:** youtube, substack
**Meta:** skill-factory, skill-evolution

## Plugins Staying in Public Marketplace (2)

personal-assistant (Elle), agent-teams

## Target Structure

```
kenny-plugins/
├── .claude-plugin/marketplace.json
├── README.md
├── writing/
├── content-strategy/
├── visual-design/
├── branding-kit/
├── art/
├── research/
├── youtube/
├── substack/
├── skill-factory/
└── skill-evolution/
```

## Migration Steps

1. Create ~/projects/kenny-plugins/ with git init
2. Copy all 10 plugin directories as-is (preserving internal structure)
3. Create marketplace.json with all 10 plugins
4. Create minimal README.md
5. Remove 10 plugins from ai-launchpad-marketplace
6. Update ai-launchpad-marketplace marketplace.json (keep personal-assistant + agent-teams)
7. Update ai-launchpad-marketplace README.md
8. Commit both repos
