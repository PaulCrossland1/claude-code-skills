# Claude Project Automation Suite

A human-directed skill ecosystem for structured software project execution using Claude Code.

## Philosophy: Human-in-the-Loop

This suite is built on a core principle: **humans should remain in control of AI-assisted development**.

Full automation sounds appealing, but it creates problems:
- Runaway failures that compound before you notice
- Decisions made without your input
- Costs spiraling out of control
- Black-box execution you can't debug
- No opportunity for course correction

**This suite keeps you in the driver's seat.** You guide discovery, review plans, and approve each task execution. The AI does the heavy lifting; you make the decisions.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    HUMAN-DIRECTED PIPELINE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│   │     001      │    │     002      │    │     003      │      │
│   │    SCOPE     │───▶│    SETUP     │───▶│   EXECUTE    │◀─┐   │
│   │   PROJECT    │    │   PROJECT    │    │    TASKS     │  │   │
│   └──────────────┘    └──────────────┘    └──────┬───────┘  │   │
│         │                    │                   │          │   │
│         ▼                    ▼                   ▼          │   │
│     Human guides        Human reviews       Human chooses   │   │
│     discovery           task breakdown      provider/model──┘   │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  SUBAGENT (your choice)                                 │   │
│   │  ┌─────────┐  ┌─────────┐                               │   │
│   │  │ Claude  │  │  Codex  │                               │   │
│   │  │ haiku   │  │  mini   │                               │   │
│   │  │ sonnet  │  │  medium │                               │   │
│   │  │ opus    │  │  max    │                               │   │
│   │  └─────────┘  └─────────┘                               │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   YOU are the orchestrator — not a nested agent                 │
└─────────────────────────────────────────────────────────────────┘
```

**Key insight:** You choose the right model for each task. Simple tasks? Use haiku (fast, cheap). Complex architecture? Use opus (most capable). Different providers excel at different things.

---

## The Skills

### 000-install — Environment Setup

**Purpose:** Bootstrap and validate the development environment.

**What it does:**
- Checks for required CLI tools (claude, node, git, etc.)
- Verifies skills are installed correctly
- Creates missing project directories
- Tests subagent execution
- Diagnoses configuration issues

**When to use:**
- First time setup on a new machine
- After updating skills
- When troubleshooting issues

```bash
/000-install          # Full environment check
/000-install --fix    # Auto-fix missing components
```

---

### 001-scope-project — Requirements Discovery

**Purpose:** Natural conversation to understand what you're building, then targeted questions to nail down details.

**How it works:**
1. **Open prompt** — "What are we working on today?" (you describe freely)
2. **Targeted questions** — Model asks follow-ups based on what you said
3. **Adapt to scope** — Small script? 2-3 questions. Full product? Deep discovery.
4. **Generate doc** — Match output to scope (or skip doc for tiny things)

**Key principle:** Start open, let you describe intent naturally, then use AskUserQuestion to drill down on specifics. Don't over-engineer small requests.

**Works for:** Anything from a 10-line script to a full product. The depth of questioning matches the scope.

**Output:**
```
.claude/
└── [requirements].md   # Only for medium+ scope
```

```bash
/001-scope-project    # Start discovery conversation
```

---

### 002-setup-project — Project Scaffolding

**Purpose:** Transform requirements into executable task breakdown. For medium+ scope projects.

**When to use:** Projects that benefit from structured execution (multi-day efforts). Skip for scripts, quick fixes, or simple features.

**Input flexibility:**
- PRD.md from 001-scope-project
- Any requirements doc
- Requirements discussed in chat (no file needed)

**What it does:**
- Finds/gathers requirements from available sources
- Confirms scope warrants structured approach
- Generates task breakdown scaled to project size
- Creates architecture and context docs

**Output:**
```
.claude/
├── ARCHITECTURE.md     # Technical blueprint
├── tasks.json          # Task breakdown (3-40 tasks based on scope)
├── CONTEXT.md          # Agent briefing
├── ENV-SETUP.md        # Environment setup
└── [other docs]
```

```bash
/002-setup-project    # Generate project structure
```

---

### 003-execute-tasks — Task Execution

**Purpose:** Execute a single task by spawning a **subagent of your choice** (Claude or Codex CLI).

**What it does:**
- Reads task details from tasks.json
- Generates a detailed prompt with full project context
- **Asks YOU to choose: Provider → Model → Permissions**
- Spawns the appropriate CLI tool
- Parses completion signals
- Sweeps documentation updates
- **Simplifies/polishes code** the subagent wrote
- Reports results for your review

**Human involvement:** You choose provider, model, and permissions for each task. You decide when to run the next task.

**Provider & Model Selection:**

| Provider | Models | Best For |
|----------|--------|----------|
| **Claude** | haiku, sonnet, opus | General coding, most tasks |
| **Codex** | mini, medium, max | Bug fixes, performance reviews |

Task complexity guides model selection:
- `simple` → haiku / mini (fast, cheap)
- `moderate` → sonnet / medium (balanced)
- `complex` → opus / max (most capable)

**Execution Flow:**
```
┌─────────────────────────────────────────────────────────────┐
│ 003-execute-tasks                                           │
├─────────────────────────────────────────────────────────────┤
│ 1. Loads context modules                                    │
│ 2. Read task from tasks.json                                │
│ 3. Generate prompt with full project context                │
│ 4. Ask YOU: Provider? Model? Permissions?                   │
│ 5. Spawn subagent CLI with your choices                     │
│ 6. Subagent completes task + emits completion signal        │
│ 7. Parse completion signal                                  │
│ 8. Sweep & enhance documentation                            │
│ 9. Simplify & polish code (conditional — see below)         │
│ 10. Report results — YOU decide to continue or stop         │
└─────────────────────────────────────────────────────────────┘
```

**Step 9 (Code Simplification):** This step applies project code standards from ARCHITECTURE.md to new/modified code. It's conditional:
- **Applied for:** Feature code, business logic, complex components
- **Skipped for:** Config files, trivial changes, setup tasks

```bash
/003-execute-tasks              # Run next pending task
/003-execute-tasks run T015     # Run specific task
```

---

## Project File Structure

After running through the pipeline, your project will have:

**All project documentation lives under `.claude/`** — single source of truth:

```
my-project/
├── .claude/                        # All project metadata & documentation
│   ├── PRD.md                      # Requirements (from 001, if saved)
│   ├── ARCHITECTURE.md             # Technical blueprint
│   ├── DECISIONS.md                # Architectural decisions
│   ├── ENV-SETUP.md                # Environment requirements
│   ├── tasks.json                  # Task breakdown with dependencies
│   ├── CONTEXT.md                  # Current state for AI agents
│   ├── PROGRESS-NOTES.md           # Log of completed work
│   ├── BLOCKERS.md                 # Blocked task tracking
│   └── prompts/                    # Subagent prompt history (from 003)
│       └── T001.md, T002.md, ...
│
├── src/                            # Source code (structure varies)
│   └── ...
│
└── package.json / pyproject.toml   # Project config
```

---

## The tasks.json Format

The heart of the system is the task breakdown:

```json
{
  "project": "my-app",
  "version": "1.0.0",
  "generated": "2026-01-14T10:00:00Z",
  "tasks": [
    {
      "id": "T001",
      "name": "Initialize monorepo structure",
      "description": "Set up Turborepo with npm workspaces...",
      "phase": "foundation",
      "complexity": "simple",
      "depends_on": [],
      "status": "completed",
      "outputs": ["package.json", "turbo.json"],
      "success_criteria": [
        {"type": "file_exists", "path": "package.json"},
        {"type": "command_succeeds", "command": "npm install"}
      ]
    },
    {
      "id": "T002",
      "name": "Configure TypeScript",
      "depends_on": ["T001"],
      "status": "pending",
      ...
    }
  ]
}
```

**Key Fields:**
- `depends_on`: Task IDs that must complete first
- `complexity`: simple | moderate | complex (affects model selection)
- `phase`: Groups related tasks (foundation, data-layer, api, ui, testing)
- `success_criteria`: Automated verification after task completion

---

## Workflow Example

### Starting a New Project

```bash
# 1. Set up environment (first time only)
/000-install

# 2. Create PRD through guided discovery
/001-scope-project
# Answer questions about your app idea...
# Review and refine the PRD
# Output: .claude/PRD.md

# 3. Generate project scaffold and task breakdown
/002-setup-project
# Review the task breakdown
# Output: .claude/tasks.json, ARCHITECTURE.md, etc.

# 4. Execute tasks one at a time (YOU are the orchestrator)
/003-execute-tasks    # Review result, then...
/003-execute-tasks    # Review result, then...
/003-execute-tasks    # Continue until done
```

### Resuming an Interrupted Project

```bash
# Check current state
cat .claude/CONTEXT.md

# Run next task
/003-execute-tasks
```

---

## Why Human-in-the-Loop?

| Aspect | Full Automation | Human-Directed |
|--------|-----------------|----------------|
| **Oversight** | None until failure | Every task |
| **Course correction** | After damage done | Before each task |
| **Cost control** | Runaway possible | You approve each |
| **Learning** | Black box | You see each step |
| **Debugging** | Hard to trace | Clear task boundaries |
| **Complexity** | Nested agents | Simple, flat |

### Why NOT Full Automation?

We tried it. Here's what happens:
1. **Nested agents can't answer questions** — AskUserQuestion is user-facing; agents can't respond to each other's questions
2. **Errors compound** — One bad decision cascades through subsequent tasks
3. **No visibility** — You only find out something went wrong after it's done
4. **Expensive mistakes** — Runaway execution burns through API credits

### Benefits of This Approach

1. **Context Preservation** — `CONTEXT.md` gives any agent full project awareness
2. **Resumability** — Pick up exactly where you left off
3. **Scalability** — Dependency management and phased execution for large projects
4. **Provider Flexibility** — Choose Claude or Codex and the specific model for each task
5. **Cost Efficiency** — Use haiku for simple tasks ($), opus for complex ($$$)
6. **Quality Control** — Code simplification pass after each task ensures consistency
7. **Debugging** — When something fails, you know exactly which task and why

---

## Installation

### Quick Install

```bash
# Clone or download the skills
git clone <repo> ~/claude-skills

# Install all skills
cd ~/claude-skills
for skill in 000-install 001-scope-project 002-setup-project 003-execute-tasks; do
  if [ -d "$skill" ]; then
    cp -r "$skill" ~/.claude/skills/
  elif [ -f "$skill.skill" ]; then
    unzip -o "$skill.skill" -d ~/.claude/skills/
  fi
done

# Verify installation
/000-install
```

### Requirements

| Component | Required | Notes |
|-----------|----------|-------|
| Claude Code CLI | Yes | `npm install -g @anthropic-ai/claude-code` |
| Node.js 18+ | Yes | For most project types |
| Git | Yes | Version control |
| Codex CLI | Optional | Alternative provider |

---

## Troubleshooting

### Skills not appearing

```bash
# Verify installation location
ls ~/.claude/skills/

# Each skill needs SKILL.md
cat ~/.claude/skills/003-execute-tasks/SKILL.md | head -5
```

### Subagent hangs on execution

Complex prompts with special characters cause shell parsing issues. The skills use temp files:

```bash
# Correct approach (used by skills)
cat > /tmp/prompt.txt << 'EOF'
Complex prompt with `backticks` and "quotes"
EOF
claude --model sonnet -p "$(cat /tmp/prompt.txt)"
```

### Task stuck in "pending" with completed dependencies

```bash
# Check tasks.json for the task status
cat .claude/tasks.json | jq '.tasks[] | select(.id == "T015")'

# Manually run the task
/003-execute-tasks run T015
```

---

## Contributing

### Adding New Skills

1. Create directory: `~/claude-skills/XXX-skill-name/`
2. Add `SKILL.md` with frontmatter
3. Add references/scripts/assets as needed
4. Package: `zip -r XXX-skill-name.skill XXX-skill-name/`
5. Install: `unzip -o XXX-skill-name.skill -d ~/.claude/skills/`

### Skill Frontmatter Format

```yaml
---
name: skill-name
description: When to use this skill and what it does.
---

# Skill Title

Content here...
```

---

## License

MIT License - Use freely, attribution appreciated.
