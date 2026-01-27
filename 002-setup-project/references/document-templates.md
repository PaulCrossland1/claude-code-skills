# Document Templates

## Directory Structure

**All project documentation lives under `.claude/`** — single source of truth:

```
project-name/
├── .claude/                    # All project metadata & documentation
│   ├── PRD.md                  # Requirements (from 001, if saved)
│   ├── ARCHITECTURE.md         # Technical blueprint
│   ├── DECISIONS.md            # Architecture decisions
│   ├── ENV-SETUP.md            # Environment requirements
│   ├── tasks.json              # Task breakdown
│   ├── CONTEXT.md              # Current state (updated each task)
│   ├── PROGRESS-NOTES.md       # Append-only work log
│   ├── BLOCKERS.md             # Issues needing human
│   └── prompts/                # Subagent prompt history (from 003)
│       ├── T001.md
│       ├── T002.md
│       └── ...
└── [project source files...]
```

---

## CONTEXT.md Template

**Purpose**: The first file any agent reads. Rolling summary of project state.

**⚠️ IMPORTANT**: The section headings in this template are used by `/003-execute-tasks` via regex patterns. If you modify the heading names (e.g., `## What's Been Built`, `## Next Steps`), you must also update the `update_context()` function in 003-execute-tasks/SKILL.md to match.

```markdown
# [Project Name] — Current Context

**Last Updated**: [timestamp]
**Current Task**: [T00X] [Task Name]
**Progress**: [X]/[Y] tasks completed

## Project Summary

[1-2 sentence description of what we're building]

## What's Been Built

### Completed Components
- [x] [Component 1] — [brief description]
- [x] [Component 2] — [brief description]

### In Progress
- [ ] [Current work] — [what's happening]

### Not Started
- [ ] [Future component] — [T00X]

## Key Files

| File | Purpose | Status |
|------|---------|--------|
| `src/components/X.tsx` | [purpose] | Complete |
| `src/api/routes.ts` | [purpose] | In Progress |

## Active Decisions

- **[Decision Area]**: [What was decided and why]
- **[Decision Area]**: [What was decided and why]

## Known Issues

- [Issue 1] — [status/workaround]
- [Issue 2] — [status/workaround]

## Next Steps

1. Complete [current task]
2. Then [next task]
3. Blocked on: [if any]

---

*This file is auto-updated after each task completion.*
```

---

## ARCHITECTURE.md Template

**Purpose**: Technical blueprint. Rarely changes after initial creation.

```markdown
# [Project Name] — Architecture

## System Overview

```
[High-level ASCII diagram showing major components]

┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────→│   Server    │────→│  Database   │
│  (React)    │←────│  (Node.js)  │←────│ (PostgreSQL)│
└─────────────┘     └─────────────┘     └─────────────┘
```

## Technology Stack

| Layer | Technology | Version | Rationale |
|-------|------------|---------|-----------|
| Frontend | [React/Next.js] | [18.x] | [Why chosen] |
| Backend | [Node.js/Express] | [20.x] | [Why chosen] |
| Database | [PostgreSQL] | [15.x] | [Why chosen] |
| ORM | [Prisma] | [5.x] | [Why chosen] |
| Auth | [Clerk/Supabase] | [latest] | [Why chosen] |
| Hosting | [Vercel/Railway] | — | [Why chosen] |

## Component Architecture

### [Component 1 Name]

**Purpose**: [What it does]

**Key Files**:
- `path/to/file.ts` — [purpose]
- `path/to/file.ts` — [purpose]

**Dependencies**:
- [Internal]: [component]
- [External]: [package]

**Data Flow**:
```
[Input] → [Processing] → [Output]
```

### [Component 2 Name]
[Repeat structure]

## Data Models

### [Entity Name]
```typescript
interface EntityName {
  id: string;
  field: type;
  // ...
}
```

**Relationships**:
- Has many: [Entity]
- Belongs to: [Entity]

## API Design

### Endpoints Overview
| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| GET | /api/resource | List resources | Required |
| POST | /api/resource | Create resource | Required |

### [Endpoint Group] Details
[Detailed API contracts from PRD]

## File Structure

```
project-name/
├── src/
│   ├── app/                    # Next.js app router
│   │   ├── api/                # API routes
│   │   └── (pages)/            # Page routes
│   ├── components/             # React components
│   │   ├── ui/                 # Base UI components
│   │   └── features/           # Feature-specific
│   ├── lib/                    # Utilities
│   │   ├── api/                # API client
│   │   ├── db/                 # Database client
│   │   └── utils/              # Helpers
│   ├── hooks/                  # React hooks
│   └── types/                  # TypeScript types
├── prisma/                     # Database schema
├── public/                     # Static assets
└── tests/                      # Test files
```

## Integration Points

| System | Protocol | Purpose |
|--------|----------|---------|
| [External API] | REST | [What it does] |
| [Service] | WebSocket | [What it does] |

## Security Considerations

- [ ] Authentication: [approach]
- [ ] Authorization: [approach]
- [ ] Data validation: [approach]
- [ ] Rate limiting: [approach]

## Performance Targets

| Metric | Target |
|--------|--------|
| Page Load | < [X]s |
| API Response (p95) | < [X]ms |
| Build Time | < [X]s |

---

*Generated from PRD v[X]. Update if architecture changes significantly.*
```

---

## PROGRESS-NOTES.md Template

**Purpose**: Append-only log of all work done. Never delete entries.

```markdown
# [Project Name] — Progress Notes

## Task Log

---

### [T001] [Task Name]

**Status**: Completed ✓
**Started**: [timestamp]
**Completed**: [timestamp]

**Actions Taken**:
- [What was done]
- [What was done]

**Files Created/Modified**:
- `path/to/file.ts` — [what changed]

**Decisions Made**:
- [Decision]: [rationale]

**Issues Encountered**:
- [Issue]: [resolution]

**Notes**:
[Any additional context]

---

### [T002] [Task Name]
[Repeat structure]

---

## Blockers History

| Date | Blocker | Resolution | Resolved |
|------|---------|------------|----------|
| [date] | [description] | [how resolved] | ✓/✗ |

---

*Append new entries at the bottom. Never delete or modify existing entries.*
```

---

## BLOCKERS.md Template

**Purpose**: Track issues requiring human intervention.

```markdown
# [Project Name] — Blockers

## Active Blockers

### [B001] [Blocker Title]

**Severity**: Critical | High | Medium | Low
**Blocking Tasks**: T00X, T00Y
**Discovered**: [timestamp]

**Description**:
[What the blocker is]

**Required Action**:
- [ ] [What human needs to do]

**Workaround** (if any):
[Temporary solution]

---

## Resolved Blockers

### [B000] [Blocker Title]
**Resolved**: [timestamp]
**Resolution**: [How it was fixed]

---

*Update this file when blockers are discovered or resolved.*
```

---

## ENV-SETUP.md Template

**Purpose**: Document all environment requirements.

```markdown
# [Project Name] — Environment Setup

## Prerequisites

- Node.js [version]
- [Other tools]

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://...` |
| `AUTH_SECRET` | Session encryption key | 32+ char string |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | 3000 |

## External Services Setup

### [Service Name]
1. Go to [URL]
2. Create account/project
3. Copy API key to `[ENV_VAR]`

## Local Development

```bash
# Install dependencies
npm install

# Set up environment
cp .env.example .env.local
# Edit .env.local with your values

# Run database migrations
npx prisma migrate dev

# Start development server
npm run dev
```

## Verification

Run these commands to verify setup:
```bash
npm run typecheck    # Should pass
npm run lint         # Should pass
npm run test         # Should pass
npm run dev          # Should start on :3000
```

---

*Keep this file updated as new services are added.*
```

---

## DECISIONS.md Template

**Purpose**: Architecture Decision Records.

```markdown
# [Project Name] — Architecture Decisions

## ADR-001: [Decision Title]

**Date**: [timestamp]
**Status**: Accepted | Superseded | Deprecated
**Context Task**: T00X

### Context
[What situation led to this decision]

### Decision
[What was decided]

### Rationale
[Why this option was chosen]

### Alternatives Considered
1. [Alternative 1] — [Why rejected]
2. [Alternative 2] — [Why rejected]

### Consequences
- **Positive**: [benefits]
- **Negative**: [trade-offs]
- **Risks**: [potential issues]

---

## ADR-002: [Next Decision]
[Repeat structure]

---

*Add new decisions at the bottom. Never delete existing entries.*
```
