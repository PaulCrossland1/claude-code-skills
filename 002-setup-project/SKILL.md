---
name: 002-setup-project
description: Transform requirements into an executable project scaffold with sequential tasks. Generates tasks.json (task breakdown), ARCHITECTURE.md (technical blueprint), CONTEXT.md (agent briefing), and supporting docs. Use after /001-scope-project for medium+ scope projects that need structured execution. Invoke with /project-setup.
---

# Project Setup — Requirements to Executable Tasks

Transform project requirements into an executable structure with sequential tasks.

**When to use:** Medium to large scope projects that benefit from structured task breakdown. Skip this for scripts, quick fixes, or simple features — just build those directly.

---

## Step 1: Find or Gather Requirements

Requirements can come from multiple sources:

### Option A: Existing Document
If there's a PRD or requirements doc from 001-scope-project:

```json
{
  "questions": [{
    "question": "Where are the requirements?",
    "header": "Source",
    "options": [
      {"label": ".claude/PRD.md", "description": "Standard location"},
      {"label": "Other file", "description": "I'll specify the path"},
      {"label": "Earlier in chat", "description": "We discussed requirements already"}
    ],
    "multiSelect": false
  }]
}
```

### Option B: From Chat Context
If requirements were discussed but not saved to a file, work from that context. Summarize what you understand:

> "Based on our discussion, here's what I understand:
> - [Core functionality]
> - [Tech stack]
> - [Key requirements]
>
> I'll generate the project structure from this. Correct?"

**Important:** When working from chat context:
1. Set `requirements_source: "chat"` in tasks.json (not `"file"`)
2. Include a detailed requirements summary in `.claude/CONTEXT.md` under "Project Summary"
3. Task descriptions should reference "See CONTEXT.md" rather than "See PRD.md"

### Option C: No Requirements Yet
If invoked without prior requirements work:

> "I don't see a requirements doc. Should we:
> 1. Run /001-scope-project first to gather requirements?
> 2. You describe the project now and I'll work from that?"

---

## Step 2: Assess Scope

Before generating 20-40 tasks, confirm this warrants structured execution:

```json
{
  "questions": [{
    "question": "How substantial is this project?",
    "header": "Scope Check",
    "options": [
      {"label": "Multi-day project", "description": "Needs structured task breakdown"},
      {"label": "Day or two", "description": "Maybe 5-10 tasks"},
      {"label": "Few hours", "description": "Might be overkill to formalize"}
    ],
    "multiSelect": false
  }]
}
```

For small scope, suggest:
> "For a few hours of work, you might not need full project scaffolding. Want to just start building, or proceed with formal setup anyway?"

---

## Step 3: Confirm Project Directory

```json
{
  "questions": [{
    "question": "Where should the project be created?",
    "header": "Project Path",
    "options": [
      {"label": "Current directory", "description": "Create .claude/ here"},
      {"label": "New subdirectory", "description": "Create project-name/ folder"},
      {"label": "Specify path", "description": "I'll provide the path"}
    ],
    "multiSelect": false
  }]
}
```

---

## Step 4: Generate Project Structure

### 4a. Create Architecture Document

Read requirements and generate `.claude/ARCHITECTURE.md`:
- Tech stack decisions
- Data models
- API design
- File structure plan

Use template from [document-templates.md](references/document-templates.md).

### 4b. Generate Task Breakdown

Create `.claude/tasks.json` following [task-generation.md](references/task-generation.md):

1. **Identify phases** from requirements
2. **Extract components** per phase
3. **Order by dependency** (foundation → data → core → api → ui → test)
4. **Write success criteria** (every task must be verifiable)

**Scale to scope:**
| Project Size | Typical Tasks |
|--------------|---------------|
| Small (few hours) | 3-8 tasks |
| Medium (days) | 10-20 tasks |
| Large (weeks) | 20-40 tasks |

Use schema from [task-schema.md](references/task-schema.md).

### 4c. Generate Supporting Documents

Create remaining docs using templates:

- `.claude/CONTEXT.md` — Initial state summary
- `.claude/PROGRESS-NOTES.md` — Empty log
- `.claude/BLOCKERS.md` — Empty blockers file
- `.claude/ENV-SETUP.md` — Environment requirements
- `.claude/DECISIONS.md` — Initial architecture decisions

### 4d. Create Directory Structure

Create empty directories matching ARCHITECTURE.md file structure.

---

## Step 5: Output Summary

Present what was created:

```
✓ Created project structure at /path/to/project

Generated:
- tasks.json: [X] tasks across [Y] phases
- ARCHITECTURE.md: Technical blueprint
- CONTEXT.md: Initial agent briefing
- ENV-SETUP.md: Environment requirements

First task: [T001 description]

Ready to start? Run /003-execute-tasks
```

---

## Output Structure

**All project documentation lives under `.claude/`:**

```
project-name/
├── .claude/
│   ├── PRD.md              # Requirements (if saved)
│   ├── ARCHITECTURE.md     # Technical blueprint
│   ├── DECISIONS.md        # Architecture decisions
│   ├── ENV-SETUP.md        # Environment requirements
│   ├── tasks.json          # Task breakdown
│   ├── CONTEXT.md          # Current state
│   ├── PROGRESS-NOTES.md   # Work log
│   └── BLOCKERS.md         # Issues needing human
└── [project source files]
```

---

## Task Generation Rules

### Atomicity
Each task completable in single agent session (~15-30 min).

**Too big**: "Build authentication system"
**Right size**: "Create User model and Prisma schema"

### Verifiability
Every task has automated success criteria:
- `file_exists` — Check file/directory
- `command_succeeds` — Run command, check exit 0
- `type_checks` — TypeScript compiles
- `test_passes` — Specific tests pass

### Sequential Ordering
Tasks execute in order. Each task's `depends_on` references prior tasks.

### Complexity Estimation
| Complexity | Duration | Example |
|------------|----------|---------|
| trivial | <5 min | Config file change |
| simple | 5-15 min | Single model/component |
| moderate | 15-30 min | Feature with multiple files |
| complex | 30-60 min | Integration, significant logic |

---

## CONTEXT.md Purpose

**Most important file for agent continuity.**

Each subagent starts fresh. CONTEXT.md tells it:
- What the project is
- What's been built
- What files exist
- Current task
- Key decisions made

Updated after each task completion.

---

## References

- **[task-schema.md](references/task-schema.md)** — JSON schema, success criteria types
- **[document-templates.md](references/document-templates.md)** — Templates for all generated docs
- **[task-generation.md](references/task-generation.md)** — Requirements-to-tasks methodology
