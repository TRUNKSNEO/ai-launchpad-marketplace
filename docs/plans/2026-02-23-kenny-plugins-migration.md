# kenny-plugins Migration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a new personal plugin marketplace at `~/projects/kenny-plugins/` by migrating 10 plugins from `ai-launchpad-marketplace`, then cleaning up the public marketplace to keep only 2 plugins.

**Architecture:** Flat marketplace structure matching the existing `ai-launchpad-marketplace` convention — a `.claude-plugin/marketplace.json` registry pointing to plugin directories, each with their own `.claude-plugin/plugin.json`. No code changes needed inside plugins; this is a file-move operation with registry/README updates.

**Tech Stack:** Git, shell commands, JSON, Markdown

---

### Task 1: Initialize kenny-plugins Repository

**Files:**
- Create: `~/projects/kenny-plugins/.gitignore`

**Step 1: Create directory and init git**

Run:
```bash
mkdir -p ~/projects/kenny-plugins && cd ~/projects/kenny-plugins && git init
```
Expected: `Initialized empty Git repository in /Users/kennethliao/projects/kenny-plugins/.git/`

**Step 2: Create .gitignore**

Create `~/projects/kenny-plugins/.gitignore` with the same content as `~/projects/ai-launchpad-marketplace/.gitignore`:

```
# Python-generated files
__pycache__/
*.py[oc]
build/
dist/
wheels/
*.egg-info

# Virtual environments
.venv
venv/
env/

# Claude
.claude/

# MacOS
.DS_Store

# Uv
uv.lock

# Environment variables
.env

# Logs
*.log
logs/

# IDE
.vscode/
.idea/

# Temporary files
temp/
tmp/
*.tmp

# Worktrees
.worktrees/
```

**Step 3: Commit**

```bash
cd ~/projects/kenny-plugins && git add .gitignore && git commit -m "chore: init kenny-plugins repo with .gitignore"
```

---

### Task 2: Copy Plugin Directories

**Step 1: Copy all 10 plugin directories**

Run each copy from `~/projects/ai-launchpad-marketplace/` to `~/projects/kenny-plugins/`:

```bash
cp -R ~/projects/ai-launchpad-marketplace/writing ~/projects/kenny-plugins/
cp -R ~/projects/ai-launchpad-marketplace/content-strategy ~/projects/kenny-plugins/
cp -R ~/projects/ai-launchpad-marketplace/visual-design ~/projects/kenny-plugins/
cp -R ~/projects/ai-launchpad-marketplace/branding-kit ~/projects/kenny-plugins/
cp -R ~/projects/ai-launchpad-marketplace/art ~/projects/kenny-plugins/
cp -R ~/projects/ai-launchpad-marketplace/research ~/projects/kenny-plugins/
cp -R ~/projects/ai-launchpad-marketplace/youtube ~/projects/kenny-plugins/
cp -R ~/projects/ai-launchpad-marketplace/substack ~/projects/kenny-plugins/
cp -R ~/projects/ai-launchpad-marketplace/skill-factory ~/projects/kenny-plugins/
cp -R ~/projects/ai-launchpad-marketplace/skill-evolution ~/projects/kenny-plugins/
```

**Step 2: Verify all directories were copied**

Run:
```bash
ls ~/projects/kenny-plugins/
```
Expected: All 10 plugin directories present: art, branding-kit, content-strategy, research, skill-evolution, skill-factory, substack, visual-design, writing, youtube

**Step 3: Commit**

```bash
cd ~/projects/kenny-plugins && git add -A && git commit -m "feat: migrate 10 plugins from ai-launchpad-marketplace"
```

---

### Task 3: Create kenny-plugins marketplace.json

**Files:**
- Create: `~/projects/kenny-plugins/.claude-plugin/marketplace.json`

**Step 1: Create the .claude-plugin directory**

```bash
mkdir -p ~/projects/kenny-plugins/.claude-plugin
```

**Step 2: Create marketplace.json**

Create `~/projects/kenny-plugins/.claude-plugin/marketplace.json`:

```json
{
  "name": "kenny-plugins",
  "owner": {
    "name": "Kenny Liao"
  },
  "plugins": [
    {
      "name": "writing",
      "source": "./writing",
      "description": "A plugin for writing content in Kenny's authentic voice across all content types and platforms"
    },
    {
      "name": "content-strategy",
      "source": "./content-strategy",
      "description": "A plugin for content research, title generation, and hook creation across all platforms"
    },
    {
      "name": "visual-design",
      "source": "./visual-design",
      "description": "A plugin for creating visual assets including thumbnails and social media graphics"
    },
    {
      "name": "branding-kit",
      "source": "./branding-kit",
      "description": "A plugin to add branding capabilities to Claude Code"
    },
    {
      "name": "art",
      "source": "./art",
      "description": "A plugin to add art capabilities to Claude Code"
    },
    {
      "name": "research",
      "source": "./research",
      "description": "A plugin to add research capabilities to Claude Code"
    },
    {
      "name": "youtube",
      "source": "./youtube",
      "description": "A plugin for YouTube content workflows — orchestrates research, writing, and design skills for video production"
    },
    {
      "name": "substack",
      "source": "./substack",
      "description": "A plugin for Substack content workflows — orchestrates research, writing, and design skills for newsletter issues and Substack Notes"
    },
    {
      "name": "skill-factory",
      "source": "./skill-factory",
      "description": "A meta-plugin for creating new skills that conform to the composable skill architecture framework"
    },
    {
      "name": "skill-evolution",
      "source": "./skill-evolution",
      "description": "A meta-plugin for self-improving skills over time. Captures session friction and writes improvement notes to auto-memory."
    }
  ]
}
```

**Step 3: Commit**

```bash
cd ~/projects/kenny-plugins && git add .claude-plugin/marketplace.json && git commit -m "feat: add marketplace.json registry for kenny-plugins"
```

---

### Task 4: Create kenny-plugins README

**Files:**
- Create: `~/projects/kenny-plugins/README.md`

**Step 1: Create README.md**

Create `~/projects/kenny-plugins/README.md`:

```markdown
# Kenny Plugins

Personal Claude Code plugin marketplace for content creation, YouTube, newsletter, and skill development workflows.

## Installation

```bash
claude
/plugin marketplace add /path/to/kenny-plugins
```

## Plugins

### Foundation
- **writing** — Voice and copywriting across all platforms
- **content-strategy** — Research, titles, and hooks
- **visual-design** — Thumbnails, social graphics, newsletter visuals
- **branding-kit** — Brand guidelines and design system
- **art** — AI image generation via Gemini (nanobanana)
- **research** — Competitor analysis and web research

### Orchestrators
- **youtube** — End-to-end video planning workflows
- **substack** — Newsletter and Substack Notes workflows

### Meta
- **skill-factory** — Create and integrate new skills
- **skill-evolution** — Session retrospectives and skill improvement
```

**Step 2: Commit**

```bash
cd ~/projects/kenny-plugins && git add README.md && git commit -m "docs: add README for kenny-plugins"
```

---

### Task 5: Remove Migrated Plugins from ai-launchpad-marketplace

**Step 1: Delete the 10 plugin directories**

Run from `~/projects/ai-launchpad-marketplace/`:

```bash
rm -rf ~/projects/ai-launchpad-marketplace/writing
rm -rf ~/projects/ai-launchpad-marketplace/content-strategy
rm -rf ~/projects/ai-launchpad-marketplace/visual-design
rm -rf ~/projects/ai-launchpad-marketplace/branding-kit
rm -rf ~/projects/ai-launchpad-marketplace/art
rm -rf ~/projects/ai-launchpad-marketplace/research
rm -rf ~/projects/ai-launchpad-marketplace/youtube
rm -rf ~/projects/ai-launchpad-marketplace/substack
rm -rf ~/projects/ai-launchpad-marketplace/skill-factory
rm -rf ~/projects/ai-launchpad-marketplace/skill-evolution
```

**Step 2: Verify only personal-assistant, agent-teams, and support dirs remain**

Run:
```bash
ls ~/projects/ai-launchpad-marketplace/
```
Expected: agent-teams, archive, docs, personal-assistant, README.md, tests (and any other non-plugin directories)

**Step 3: Do NOT commit yet** — wait for Task 6 and 7 to update marketplace.json and README first.

---

### Task 6: Update ai-launchpad-marketplace marketplace.json

**Files:**
- Modify: `~/projects/ai-launchpad-marketplace/.claude-plugin/marketplace.json`

**Step 1: Replace marketplace.json content**

Replace the entire contents of `~/projects/ai-launchpad-marketplace/.claude-plugin/marketplace.json` with:

```json
{
  "name": "ai-launchpad",
  "owner": {
    "name": "Kenny Liao"
  },
  "plugins": [
    {
      "name": "personal-assistant",
      "source": "./personal-assistant",
      "description": "A plugin to turn Claude Code into your personal assistant"
    },
    {
      "name": "agent-teams",
      "source": "./agent-teams",
      "description": "A plugin for Claude Code agent team workflows — session viewing, analysis, and best practice evaluation"
    }
  ]
}
```

---

### Task 7: Update ai-launchpad-marketplace README

**Files:**
- Modify: `~/projects/ai-launchpad-marketplace/README.md`

**Step 1: Rewrite README to reflect only 2 remaining plugins**

Remove sections for YouTube, Skill Evolution, and any other migrated plugins. Keep the Personal Assistant section and add an Agent Teams section. Update the intro text and plugin count.

---

### Task 8: Commit ai-launchpad-marketplace Changes

**Step 1: Stage and commit all removals and updates**

```bash
cd ~/projects/ai-launchpad-marketplace && git add -A && git commit -m "refactor: migrate personal plugins to kenny-plugins

Moved 10 plugins (writing, content-strategy, visual-design, branding-kit,
art, research, youtube, substack, skill-factory, skill-evolution) to the
kenny-plugins personal marketplace. This public marketplace now contains
only personal-assistant and agent-teams."
```

---

### Task 9: Verify Both Marketplaces

**Step 1: Verify kenny-plugins structure**

Run:
```bash
ls ~/projects/kenny-plugins/
cat ~/projects/kenny-plugins/.claude-plugin/marketplace.json | python3 -m json.tool
```
Expected: 10 plugin directories, valid JSON with 10 plugin entries

**Step 2: Verify ai-launchpad-marketplace structure**

Run:
```bash
ls ~/projects/ai-launchpad-marketplace/
cat ~/projects/ai-launchpad-marketplace/.claude-plugin/marketplace.json | python3 -m json.tool
```
Expected: 2 plugin directories (personal-assistant, agent-teams), valid JSON with 2 plugin entries
