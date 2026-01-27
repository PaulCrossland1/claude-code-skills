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
  "subagent_prompt": null,
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
  "subagent_prompt": null,
  "status": "pending",
  "started_at": null,
  "completed_at": null,
  "blocked_reason": null,
  "notes": null
}
```

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
