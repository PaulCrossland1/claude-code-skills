# Task Schema Reference

## tasks.json Structure

```json
{
  "project": {
    "name": "project-name",
    "requirements_source": "file" | "chat",
    "requirements_path": "./.claude/PRD.md",  // optional, if source is "file"
    "created_at": "2024-01-15T10:00:00Z",
    "total_tasks": 25,
    "completed_tasks": 0
  },
  "tasks": [Task]
}
```

**Note**: `requirements_source` indicates where requirements came from:
- `"file"` — A saved PRD.md or requirements doc (path in `requirements_path`)
- `"chat"` — Requirements gathered from conversation (summarized in CONTEXT.md)

**When to use each:**
- Use `"file"` when `/001-scope-project` saved a PRD.md or user provides a requirements doc
- Use `"chat"` when requirements were discussed but user chose not to save a file
- When `"chat"` is used, ensure CONTEXT.md contains a detailed "Project Summary" section

## Task Object

```json
{
  "id": "T001",
  "name": "Short task name",
  "description": "Detailed description of what this task accomplishes",
  "category": "setup|data|feature|integration|api|ui|testing|documentation",
  "phase": "foundation|data-layer|core|integration|ui|testing|polish",
  "depends_on": null | ["T000"],
  "estimated_complexity": "trivial|simple|moderate|complex",
  "context_files": ["paths agent should READ"],
  "output_files": ["paths agent will CREATE/MODIFY"],
  "success_criteria": [SuccessCriterion],
  "subagent_prompt": "Rich, detailed prompt for the executing agent (see Subagent Prompt section below)",
  "status": "pending|in_progress|completed|blocked|skipped",
  "started_at": null,
  "completed_at": null,
  "blocked_reason": null,
  "notes": null
}
```

## Success Criterion Types

### file_exists
Check if file or directory exists.
```json
{
  "type": "file_exists",
  "target": "src/components/Button.tsx",
  "description": "Button component created"
}
```

### file_contains
Check if file contains a pattern (regex supported).
```json
{
  "type": "file_contains",
  "target": "package.json",
  "pattern": "\"react\":\\s*\"\\^18",
  "description": "React 18 installed"
}
```

### command_succeeds
Run command, verify exit code 0.
```json
{
  "type": "command_succeeds",
  "command": "npm run build",
  "timeout_seconds": 120,
  "description": "Project builds without errors"
}
```

### test_passes
Run specific test file or pattern.
```json
{
  "type": "test_passes",
  "command": "npm test -- --testPathPattern=genome",
  "description": "Genome tests pass"
}
```

### type_checks
TypeScript compiles without errors.
```json
{
  "type": "type_checks",
  "command": "npx tsc --noEmit",
  "description": "No TypeScript errors"
}
```

### lint_passes
Linter runs without errors.
```json
{
  "type": "lint_passes",
  "command": "npm run lint",
  "description": "No linting errors"
}
```

### server_responds
HTTP endpoint returns expected status.
```json
{
  "type": "server_responds",
  "method": "GET",
  "url": "http://localhost:3000/api/health",
  "expected_status": 200,
  "description": "Health endpoint responds"
}
```

### env_var_set
Environment variable is defined.
```json
{
  "type": "env_var_set",
  "variable": "DATABASE_URL",
  "description": "Database connection configured"
}
```

### manual_verify
Requires human confirmation (use sparingly).
```json
{
  "type": "manual_verify",
  "instruction": "Open browser to localhost:3000 and verify login flow works",
  "description": "Login flow verified manually"
}
```

---

## Task Categories

| Category | Description | Examples |
|----------|-------------|----------|
| `setup` | Project initialization | Init repo, install deps, configure tools |
| `data` | Data layer | Database schema, models, migrations |
| `feature` | Core functionality | Business logic, algorithms |
| `integration` | Connect systems | Auth integration, API connections |
| `api` | API endpoints | Routes, controllers, validation |
| `ui` | User interface | Components, pages, styles |
| `testing` | Test coverage | Unit tests, integration tests, E2E |
| `documentation` | Docs and comments | README, API docs, inline comments |

---

## Task Phases (Execution Order)

1. **foundation** - Project setup, tooling, config
2. **data-layer** - Database, schemas, models
3. **core** - Core business logic, algorithms
4. **integration** - Connecting internal systems
5. **api** - API endpoints
6. **ui** - User interface
7. **testing** - Test coverage
8. **polish** - Edge cases, error handling, optimization

---

## Example: Complete Task

```json
{
  "id": "T005",
  "name": "Implement Genome data model",
  "description": "Create the Genome TypeScript interface and Prisma schema matching the PRD specification. Include all 11 parameters (steering, throttle, brake).",
  "category": "data",
  "phase": "data-layer",
  "depends_on": ["T004"],
  "estimated_complexity": "simple",
  "context_files": [
    ".claude/CONTEXT.md",
    ".claude/ARCHITECTURE.md#data-models",
    "shared/types/index.ts"
  ],
  "output_files": [
    "shared/types/Genome.ts",
    "prisma/schema.prisma"
  ],
  "success_criteria": [
    {
      "type": "file_exists",
      "target": "shared/types/Genome.ts",
      "description": "Genome type file created"
    },
    {
      "type": "file_contains",
      "target": "shared/types/Genome.ts",
      "pattern": "steerFromCenter|steerToCheckpoint|throttleBase",
      "description": "Contains genome parameters"
    },
    {
      "type": "type_checks",
      "command": "npx tsc --noEmit",
      "description": "TypeScript compiles"
    }
  ],
  "subagent_prompt": "Create the Genome data model representing a kart's AI brain parameters.\n\n## Background\nIn Genetic Kart, each kart is driven by a 'genome' — a set of 11 numerical parameters that control steering, throttle, and braking. The User model (T004) is already complete in shared/types/User.ts — follow the same named export pattern.\n\n## Requirements\nCreate shared/types/Genome.ts with a TypeScript interface containing: id (UUID string), userId (references User.id), name (string, max 50 chars), generation (number, starts at 1), parameters object with 11 fields (steerFromCenter, steerToCheckpoint, throttleBase, throttleStraight, brakeAngle, brakePower, lookahead, driftTendency, recoveryAggression, riskTolerance, topSpeedBias — all numbers with defined ranges), fitness (number, nullable), createdAt, updatedAt.\n\nAdd a Prisma model in prisma/schema.prisma. Store parameters as Json field. Add @relation to User (one-to-many).\n\n## Patterns\n- Read shared/types/User.ts for export pattern\n- Add Genome to shared/types/index.ts barrel export\n- Use @id, @default(uuid()), @relation decorators matching existing models\n\n## Constraints\n- Do NOT add API routes or service logic (separate tasks)\n- Do NOT create migration files (T010 handles that)\n- Parameter ranges are documentation only at type level; validation is in the API layer (T017)",
  "status": "pending",
  "started_at": null,
  "completed_at": null,
  "blocked_reason": null,
  "notes": null
}
```

---

## Subagent Prompt — Rich Task Prompts

The `subagent_prompt` field is the most important field for task execution quality. It is the primary instruction the executing agent receives. **Do not leave it null.** Generate it at project setup time (002) so every task is immediately executable with full context.

### What a subagent_prompt must contain

Every `subagent_prompt` should be a multi-paragraph, self-contained brief covering **all** of the following:

1. **Goal** — What this task achieves and why it matters in the project
2. **Background** — Relevant context the agent needs (what was built before, what depends on this)
3. **Detailed requirements** — Specific fields, parameters, behaviors, edge cases, validation rules. Pull these directly from the PRD or chat context — don't summarize, be explicit
4. **Implementation guidance** — Which patterns, libraries, or conventions to follow. Reference specific files to read for existing patterns
5. **Constraints** — What NOT to do, common pitfalls, things to avoid
6. **Acceptance definition** — What "done" looks like in concrete terms beyond the automated success_criteria

### Example: Weak vs Strong subagent_prompt

**Weak (don't do this):**
```
"subagent_prompt": "Create the Genome TypeScript interface and Prisma schema."
```

**Strong (do this):**
```
"subagent_prompt": "Create the Genome data model that represents a kart's AI brain parameters.\n\n## Background\nIn Genetic Kart, each kart is driven by a 'genome' — a set of 11 numerical parameters that control steering, throttle, and braking behavior. These genomes are mutated between races via genetic algorithms. The User model (T004) is already complete and lives in shared/types/User.ts — follow the same export pattern.\n\n## Requirements\nCreate a TypeScript interface in shared/types/Genome.ts with these exact fields:\n- id: string (UUID)\n- userId: string (references User.id)\n- name: string (user-assigned label, max 50 chars)\n- generation: number (starts at 1, incremented on mutation)\n- parameters: object containing:\n  - steerFromCenter: number (0-1, how aggressively the kart steers away from track center)\n  - steerToCheckpoint: number (0-1, weight of steering toward next checkpoint)\n  - throttleBase: number (0.3-1.0, minimum throttle applied)\n  - throttleStraight: number (0-1, additional throttle on straights)\n  - brakeAngle: number (0-90, angle threshold to trigger braking)\n  - brakePower: number (0-1, how hard to brake)\n  - lookahead: number (1-5, how many checkpoints ahead to consider)\n  - driftTendency: number (0-1, willingness to drift)\n  - recoveryAggression: number (0-1, how aggressively to correct off-track)\n  - riskTolerance: number (0-1, willingness to take tight lines)\n  - topSpeedBias: number (0-1, preference for top speed vs acceleration)\n- fitness: number (calculated after race, nullable)\n- createdAt: Date\n- updatedAt: Date\n\nAlso add a Prisma model in prisma/schema.prisma. The parameters object should be stored as a Json field in Prisma. Add a relation to User (one User has many Genomes).\n\n## Patterns to follow\n- Read shared/types/User.ts for the export pattern (named export, not default)\n- Read shared/types/index.ts and add Genome to the barrel export\n- Prisma schema should use @id, @default(uuid()), @relation decorators matching existing models\n\n## Constraints\n- Do NOT add API routes or service logic — those are separate tasks\n- Do NOT create migration files — T010 handles migrations\n- Parameter ranges are documentation only at the type level; validation happens in the API layer (T017)"
```

### Prompt length guidance

| Complexity | Prompt length |
|------------|---------------|
| trivial | 100-200 words |
| simple | 200-400 words |
| moderate | 400-700 words |
| complex | 700-1200 words |

### Referencing requirements

- **From PRD file**: Quote or paraphrase specific PRD sections. Include field names, validation rules, and behaviors verbatim.
- **From chat context**: Reconstruct the specific details discussed. Reference CONTEXT.md sections.
- **Always**: Name the exact files to read for patterns, the exact files to create/modify, and the exact fields/parameters/behaviors expected.

---

## Status Transitions

```
pending → in_progress → completed
              ↓
           blocked → pending (after unblocked)
              ↓
           skipped (if no longer needed)
```

---

## Validation Rules

1. **IDs must be unique** - T001, T002, etc.
2. **depends_on must reference existing tasks** - No forward references
3. **depends_on tasks must come earlier** - Enforce ordering
4. **At least one success_criterion required** - Every task must be verifiable
5. **output_files should not overlap** - Avoid conflicts between tasks
6. **context_files must exist** - Or be created by prior task
