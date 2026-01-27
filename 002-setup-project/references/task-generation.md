# Task Generation Methodology

## Principles

### 1. Tasks Must Be Atomic
A task should be completable in a single agent session (~15-30 min of work).

**Too big**: "Build the authentication system"
**Right size**: "Create User model and Prisma schema"

### 2. Tasks Must Be Verifiable
Every task needs automated success criteria. If you can't test it, break it down further.

**Bad**: "Make the UI look good"
**Good**: "Create Button component with hover state" + file_exists criterion

### 3. Tasks Must Be Sequential
Each task builds on the previous. No parallel work—agents work one task at a time.

### 4. Dependencies Must Be Explicit
If Task B needs files from Task A, `depends_on: ["A"]` must be set.

---

## Task Breakdown Process

### Step 1: Identify Phases from PRD

Map PRD sections to development phases:

| PRD Section | Phase |
|-------------|-------|
| Technical Stack | foundation |
| Data Models | data-layer |
| Functional Requirements | core |
| API Contracts | api |
| UI/UX | ui |
| Non-Functional (testing) | testing |

### Working from Chat Context (No PRD File)

If requirements came from conversation rather than a saved PRD file:

1. **Summarize key requirements** in CONTEXT.md under "Project Summary"
2. **Map discussed features to phases** using the same logic as PRD sections
3. **Reference "chat context"** in task descriptions rather than "PRD section X"
4. **Set `requirements_source: "chat"`** in tasks.json project metadata
5. **Omit `requirements_path`** from tasks.json (only used with `"file"` source)

Example task description when working from chat:
```
"description": "Create User model with fields discussed: id, email, name, createdAt.
See CONTEXT.md for full requirements summary."
```

The phase mapping still applies — just derive phases from what was discussed:
- Stack decisions mentioned → foundation
- Entities/data mentioned → data-layer
- Features/behavior described → core, api, ui

**How to detect which source to use:**
- If `.claude/PRD.md` exists → `requirements_source: "file"`
- If user says "requirements are from our discussion" or "don't save a PRD" → `requirements_source: "chat"`
- If user provides a different file path → `requirements_source: "file"` with that path

### Step 2: Extract Components per Phase

For each phase, list distinct components:

**foundation**:
- Monorepo/project setup
- TypeScript configuration
- Linting/formatting setup
- Database connection
- Auth provider setup

**data-layer**:
- Each entity = 1 task
- Migrations = 1 task
- Seed data = 1 task

**core**:
- Each algorithm/business rule = 1 task
- State machine implementation = 1 task

**api**:
- Each endpoint group = 1 task
- Validation layer = 1 task

**ui**:
- Each screen = 1-2 tasks
- Each complex component = 1 task

### Step 3: Order by Dependency

```
foundation → data-layer → core → api → ui → testing → polish
```

Within phases, order by what depends on what:
1. Types/interfaces first
2. Models/schemas second
3. Services/logic third
4. Controllers/routes fourth
5. UI components last

### Step 4: Write Success Criteria

For each task, ask: "How do I prove this is done?"

| Task Type | Typical Criteria |
|-----------|------------------|
| Setup | command_succeeds (npm install, build) |
| Model | file_exists + type_checks |
| Logic | test_passes |
| API | server_responds |
| UI | file_exists + type_checks |
| Integration | test_passes + server_responds |

---

## Standard Task Templates

### Project Initialization
```json
{
  "id": "T001",
  "name": "Initialize project structure",
  "description": "Create base project with package.json, tsconfig, and directory structure",
  "category": "setup",
  "phase": "foundation",
  "depends_on": null,
  "estimated_complexity": "simple",
  "success_criteria": [
    {"type": "file_exists", "target": "package.json"},
    {"type": "file_exists", "target": "tsconfig.json"},
    {"type": "command_succeeds", "command": "npm install"}
  ]
}
```

### Database Schema
```json
{
  "id": "T00X",
  "name": "Create [Entity] model",
  "description": "Define Prisma schema for [Entity] with fields: [list fields]",
  "category": "data",
  "phase": "data-layer",
  "depends_on": ["T00Y"],
  "estimated_complexity": "simple",
  "success_criteria": [
    {"type": "file_contains", "target": "prisma/schema.prisma", "pattern": "model [Entity]"},
    {"type": "command_succeeds", "command": "npx prisma validate"}
  ]
}
```

### API Endpoint
```json
{
  "id": "T00X",
  "name": "Implement [Resource] API endpoints",
  "description": "Create GET/POST/PUT/DELETE endpoints for [Resource]",
  "category": "api",
  "phase": "api",
  "depends_on": ["T00Y"],
  "estimated_complexity": "moderate",
  "success_criteria": [
    {"type": "file_exists", "target": "src/app/api/[resource]/route.ts"},
    {"type": "type_checks", "command": "npx tsc --noEmit"},
    {"type": "test_passes", "command": "npm test -- [resource].test"}
  ]
}
```

### React Component
```json
{
  "id": "T00X",
  "name": "Create [Component] component",
  "description": "Build [Component] with states: default, loading, error, empty",
  "category": "ui",
  "phase": "ui",
  "depends_on": ["T00Y"],
  "estimated_complexity": "moderate",
  "success_criteria": [
    {"type": "file_exists", "target": "src/components/[Component]/index.tsx"},
    {"type": "type_checks", "command": "npx tsc --noEmit"},
    {"type": "lint_passes", "command": "npm run lint"}
  ]
}
```

### Integration Task
```json
{
  "id": "T00X",
  "name": "Integrate [Service] authentication",
  "description": "Set up [Service] provider with login/logout flows",
  "category": "integration",
  "phase": "integration",
  "depends_on": ["T00Y"],
  "estimated_complexity": "complex",
  "success_criteria": [
    {"type": "env_var_set", "variable": "[SERVICE]_API_KEY"},
    {"type": "file_exists", "target": "src/lib/auth/[service].ts"},
    {"type": "server_responds", "url": "/api/auth/session", "expected_status": 200}
  ]
}
```

---

## Complexity Estimation

| Complexity | Typical Duration | Criteria |
|------------|------------------|----------|
| trivial | < 5 min | Single file, copy/paste, config change |
| simple | 5-15 min | Few files, straightforward logic |
| moderate | 15-30 min | Multiple files, some decisions |
| complex | 30-60 min | Many files, significant logic, integration |

If a task is >60 min, break it down further.

---

## Example: PRD to Tasks (Genetic Kart)

From the Genetic Kart PRD, extract ~25 tasks:

**Foundation (T001-T005)**:
1. Initialize monorepo structure
2. Configure TypeScript and linting
3. Set up Phaser.js in client
4. Configure Supabase connection
5. Set up environment variables

**Data Layer (T006-T010)**:
6. Create User model
7. Create Genome model
8. Create LeaderboardEntry model
9. Create VideoExport model
10. Run initial migrations

**Core Logic (T011-T015)**:
11. Implement KartBrain decision function
12. Implement genetic mutation algorithm
13. Implement selection logic
14. Implement race timeout rules
15. Implement physics simulation

**API (T016-T019)**:
16. Implement auth endpoints
17. Implement genome CRUD endpoints
18. Implement leaderboard endpoints
19. Implement export endpoints

**UI (T020-T023)**:
20. Create GenomeEditor component
21. Create RaceCanvas component
22. Create ResultsPanel component
23. Create LeaderboardModal component

**Testing (T024-T025)**:
24. Write unit tests for KartBrain
25. Write integration tests for API

---

## Anti-Patterns

### Don't: Create catch-all tasks
**Bad**: "Implement the frontend"
**Good**: Separate task per component/screen

### Don't: Skip success criteria
Every task MUST have at least one automated check.

### Don't: Create circular dependencies
Task A depends on B, B depends on A = deadlock.

### Don't: Mix concerns in one task
**Bad**: "Create User model and authentication endpoints"
**Good**: Separate model task and endpoint task

### Don't: Assume implicit knowledge
Each task description should be self-contained. Agent may not have context from previous tasks.

### Don't: Leave subagent_prompt null
Every task must have a rich `subagent_prompt` generated at setup time. This is the primary brief the executing agent reads. Include the goal, background, explicit requirements (fields, parameters, behaviors), implementation patterns to follow, constraints, and what "done" looks like. The more specific you are, the fewer retries needed. See [task-schema.md](task-schema.md#subagent-prompt--rich-task-prompts) for full guidance.
