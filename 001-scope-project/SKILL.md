---
name: 001-scope-project
description: Comprehensive project scoping through iterative discovery. Guides users through structured questioning phases to capture every detail needed for software work — whether building new products, adding features, auditing security, optimizing performance, fixing bugs, or migrating systems. Use when user wants to plan any software project or needs help structuring requirements before implementation.
---

# Scope Project — Iterative Discovery

Capture everything needed to execute software work through natural conversation and targeted questions.

---

## Step 1: Open with a Simple Prompt

**Do NOT use AskUserQuestion first.** Start with an open prompt:

> "What are we working on today?"

Or if context suggests they have something in mind:

> "Tell me about what you're trying to build/fix/improve."

**Let them describe it in their own words.** This could be:
- A full product idea
- A single feature
- A bug they encountered
- A refactor they're considering
- A vague notion they want to explore

Don't assume scope. Let them tell you.

---

## Step 2: Acknowledge and Start Drilling Down

After they describe their intent, acknowledge what you heard and start asking targeted questions using AskUserQuestion.

**Example flow:**

User: "I want to build a simple app that helps me track my reading habits"

You: "Got it — a reading tracker. Let me understand this better."

Then use AskUserQuestion to drill down:

```json
{
  "questions": [{
    "question": "What's the core thing you want to track?",
    "header": "Core Feature",
    "options": [
      {"label": "Books read", "description": "Track completed books"},
      {"label": "Reading progress", "description": "Track pages/chapters as you go"},
      {"label": "Reading time", "description": "Track how long you read"},
      {"label": "All of the above", "description": "Comprehensive tracking"}
    ],
    "multiSelect": false
  }]
}
```

---

## Step 3: Iterative Questioning

**Keep asking questions until you have everything needed.**

### Questioning Principles

- **React to their answers** — Each question should follow from what they just said
- **Follow threads** — When an answer reveals complexity, go deeper
- **Use AskUserQuestion for choices** — When there are reasonable options to pick from
- **Use open prompts for exploration** — When you need them to describe something
- **Confirm assumptions** — State what you're assuming and check
- **Don't over-question simple things** — A small script doesn't need a full PRD

### Adapt to Scope

**Small scope** (script, quick fix, simple feature):
- 2-5 questions might be enough
- Focus on: what it does, any constraints, how to know it works

**Medium scope** (feature, integration, refactor):
- 5-15 questions
- Add: who uses it, edge cases, tech approach

**Large scope** (new product, major system):
- Many questions across multiple turns
- Cover: users, workflows, tech stack, data model, auth, deployment, etc.

---

## Step 4: Required Outcomes

Before generating a document, ensure you've captured what's needed for the scope:

### Always Capture (any size):

| What | Why |
|------|-----|
| **What it does** | Core functionality |
| **Success criteria** | How we know it works |
| **Constraints** | Limitations, requirements |

### Also Capture (medium+ scope):

| What | Why |
|------|-----|
| **Who uses it** | Target users/personas |
| **Key workflows** | How people use it |
| **Tech approach** | Stack, architecture |
| **UI/UX requirements** | Visual design, layout, interactions (see UI/UX section below) |
| **External dependencies** | Backend, APIs, payments (see below) |
| **Edge cases** | What could go wrong |

### Also Capture (large scope):

| What | Why |
|------|-----|
| **Data model** | Entities, relationships |
| **Auth/permissions** | Who can do what |
| **Integrations** | External systems |
| **Deployment** | Where/how it runs |
| **Rollout plan** | How to release safely |

### UI/UX Requirements (medium+ scope, always capture when project has a UI):

**This section is mandatory for any project with a user interface.** UI/UX decisions must always make it into the PRD — they directly shape task generation and implementation quality.

**Step 1: Determine if this is a new or existing project**

```json
{
  "questions": [{
    "question": "Does this project have an existing UI?",
    "header": "UI Status",
    "options": [
      {"label": "New project", "description": "Building UI from scratch"},
      {"label": "Existing UI", "description": "There's already a frontend to work with"},
      {"label": "No UI needed", "description": "CLI, API-only, or backend service"}
    ],
    "multiSelect": false
  }]
}
```

If **No UI needed**, skip this section entirely.

**Step 2a: New project — Establish UI direction**

```json
{
  "questions": [
    {
      "question": "What kind of visual style are you going for?",
      "header": "Style",
      "options": [
        {"label": "Clean & minimal", "description": "Lots of whitespace, simple layouts, subtle colors"},
        {"label": "Bold & modern", "description": "Strong colors, large typography, gradient accents"},
        {"label": "Data-dense", "description": "Dashboards, tables, compact information display"},
        {"label": "Match a reference", "description": "I have a site or design I want to look like"}
      ],
      "multiSelect": false
    },
    {
      "question": "What's the primary layout pattern?",
      "header": "Layout",
      "options": [
        {"label": "Sidebar + content", "description": "Navigation sidebar with main content area"},
        {"label": "Top nav + pages", "description": "Header navigation with full-width pages"},
        {"label": "Single page app", "description": "One scrolling page or modal-driven"},
        {"label": "Not sure", "description": "Help me decide based on the use case"}
      ],
      "multiSelect": false
    }
  ]
}
```

Follow up with:

```json
{
  "questions": [
    {
      "question": "What UI component library or approach?",
      "header": "Components",
      "options": [
        {"label": "shadcn/ui (Recommended)", "description": "Radix primitives + Tailwind, copy-paste components"},
        {"label": "Material UI", "description": "Google's design system for React"},
        {"label": "Chakra UI", "description": "Composable component library"},
        {"label": "Custom / Tailwind only", "description": "Build from scratch with utility classes"}
      ],
      "multiSelect": false
    },
    {
      "question": "Any specific UX patterns needed?",
      "header": "UX Patterns",
      "options": [
        {"label": "Forms & validation", "description": "Multi-step forms, inline validation, error states"},
        {"label": "Real-time updates", "description": "Live data, notifications, optimistic UI"},
        {"label": "Data tables", "description": "Sorting, filtering, pagination, bulk actions"},
        {"label": "Drag & drop", "description": "Reordering, kanban boards, file uploads"}
      ],
      "multiSelect": true
    }
  ]
}
```

If user selected **"Match a reference"**, ask:
> "Share the URL or describe the site/design you'd like to reference. I'll note the key visual patterns to match."

**Step 2b: Existing project — Assess current UI and desired changes**

First, examine the existing codebase:
> "Let me look at your current UI setup."

Check for:
- Component library in use (package.json)
- CSS approach (Tailwind, CSS modules, styled-components)
- Existing layout patterns
- Design tokens or theme files

Then present findings:

> "Your current UI uses [library] with [CSS approach]. The layout is [pattern]. Here's what I found:"
> - [Key UI observations]

```json
{
  "questions": [{
    "question": "How should the UI change for this work?",
    "header": "UI Changes",
    "options": [
      {"label": "Keep current style", "description": "Match existing look and feel exactly"},
      {"label": "Evolve the style", "description": "Improve while staying consistent with existing UI"},
      {"label": "Redesign needed", "description": "Significant visual changes required"},
      {"label": "New section only", "description": "New pages/features can have fresh style, leave existing alone"}
    ],
    "multiSelect": false
  }]
}
```

If **Evolve** or **Redesign**:

```json
{
  "questions": [{
    "question": "What specifically should change about the UI?",
    "header": "UI Updates",
    "options": [
      {"label": "Colors & theme", "description": "Update color palette, dark/light mode"},
      {"label": "Layout & navigation", "description": "Restructure navigation, page layouts"},
      {"label": "Component quality", "description": "Better loading states, animations, responsiveness"},
      {"label": "Accessibility", "description": "WCAG compliance, keyboard nav, screen readers"}
    ],
    "multiSelect": true
  }]
}
```

**Step 3: Responsive & accessibility baseline**

```json
{
  "questions": [{
    "question": "What devices and accessibility level should we target?",
    "header": "Targets",
    "options": [
      {"label": "Desktop only", "description": "Internal tool or desktop-focused app"},
      {"label": "Desktop + mobile", "description": "Responsive design for all screen sizes"},
      {"label": "Mobile first", "description": "Primary mobile experience, desktop secondary"},
      {"label": "WCAG AA compliance", "description": "Full accessibility support required"}
    ],
    "multiSelect": true
  }]
}
```

**Step 4: Record in PRD**

All UI/UX decisions must be captured in a dedicated `## UI/UX Requirements` section of the PRD, including:
- Visual style direction
- Layout pattern
- Component library
- Key UX patterns needed
- Responsive targets
- Accessibility requirements
- For existing projects: what changes vs what stays the same
- Reference designs or screenshots if provided

This section feeds directly into task generation in 002 — UI tasks without clear UX requirements produce vague, unverifiable work.

---

### External Dependencies & Integrations (medium+ scope):

For projects that need external services, use a **broad-to-specific** questioning approach:

**Step 1: Broad intent gathering**

```json
{
  "questions": [{
    "question": "What kinds of external services will this project need?",
    "header": "Services",
    "options": [
      {"label": "Database/Backend", "description": "Data storage, auth, real-time"},
      {"label": "APIs/Integrations", "description": "Third-party services, webhooks"},
      {"label": "Payments", "description": "Stripe, PayPal, etc."},
      {"label": "None/Unsure", "description": "Self-contained or need suggestions"}
    ],
    "multiSelect": true
  }]
}
```

**Step 2: Dial into specific providers based on selections**

If **Database/Backend** selected:

```json
{
  "questions": [{
    "question": "Which backend/database approach?",
    "header": "Backend",
    "options": [
      {"label": "Supabase (Recommended)", "description": "Postgres + Auth + Realtime + Storage"},
      {"label": "Firebase", "description": "NoSQL + Auth + Realtime + Hosting"},
      {"label": "PlanetScale", "description": "Serverless MySQL"},
      {"label": "Self-hosted/Other", "description": "Custom setup or different provider"}
    ],
    "multiSelect": false
  }]
}
```

If **APIs/Integrations** selected:

```json
{
  "questions": [{
    "question": "What types of integrations do you need?",
    "header": "Integrations",
    "options": [
      {"label": "AI/LLM", "description": "OpenAI, Anthropic, etc."},
      {"label": "Email/Notifications", "description": "SendGrid, Resend, Twilio"},
      {"label": "Analytics", "description": "Posthog, Mixpanel, Plausible"},
      {"label": "Other/Custom", "description": "Specific APIs you'll integrate"}
    ],
    "multiSelect": true
  }]
}
```

Then follow up with specific provider questions for each category.

If **Payments** selected:

```json
{
  "questions": [{
    "question": "Which payment provider?",
    "header": "Payments",
    "options": [
      {"label": "Stripe (Recommended)", "description": "Cards, subscriptions, invoices"},
      {"label": "LemonSqueezy", "description": "Digital products, merchant of record"},
      {"label": "PayPal", "description": "Wide consumer adoption"},
      {"label": "Other/Multiple", "description": "Different provider or combination"}
    ],
    "multiSelect": false
  }]
}
```

If **None/Unsure** selected, offer suggestions based on project type:

> "Based on what you're building, here are common patterns:"
> - **SaaS app**: Supabase (DB + Auth) + Stripe (payments) + Resend (email)
> - **Content site**: Supabase or Firebase + Analytics
> - **Internal tool**: Supabase + your existing auth provider
> - **Mobile app**: Firebase or Supabase + push notifications

**Step 3: Capture specific details**

For each selected provider, gather:
- Do you have an account/API keys already?
- Any specific features you know you'll need?
- Existing data to migrate?

**Record in dependencies section of PRD and `.claude/skills.json`:**

```json
{
  "projectSkills": {
    "aesthetic": ["brand-guidelines"],
    "dependencies": {
      "backend": {
        "provider": "supabase",
        "features": ["auth", "database", "realtime"],
        "notes": "User already has Supabase project set up"
      },
      "payments": {
        "provider": "stripe",
        "features": ["subscriptions", "customer-portal"],
        "notes": "Monthly subscription model"
      },
      "integrations": [
        {"name": "openai", "purpose": "AI features", "notes": "GPT-4 for content generation"},
        {"name": "resend", "purpose": "Transactional email", "notes": "Welcome emails, receipts"}
      ]
    }
  }
}
```

---

### Aesthetic & Design Skills (when UI/frontend involved):

If the project involves UI, frontend, visual design, or presentations, check `~/.claude/aesthetic-preferences.json` for user preferences. If mode is `select-per-project`, offer skill selection:

```json
{
  "questions": [{
    "question": "This project has visual/UI elements. Which design skills should guide the work?",
    "header": "Design Skills",
    "options": [
      {"label": "brand-guidelines", "description": "Apply brand colors, typography, visual identity"},
      {"label": "vercel-react-best-practices", "description": "React/Next.js performance patterns (if applicable)"},
      {"label": "web-design-guidelines", "description": "UI/UX compliance review"},
      {"label": "canvas-design", "description": "Visual art & design philosophy"}
    ],
    "multiSelect": true
  }]
}
```

**Only show skills that are installed** (check `~/.claude/aesthetic-preferences.json` for `installedSkills`).

**Only ask if relevant** — a CLI tool or backend service doesn't need aesthetic skills.

---

## Step 5: Completeness Check

Before generating, briefly summarize what you've gathered:

> "Here's what I've got:
> - [Core functionality]
> - [Key decisions]
> - [Technical approach]
>
> Anything to add before I write this up?"

For small things, this might be 3 bullet points.
For large projects, this might be a full summary.

---

## Step 6: Generate Document

**Match the document to the scope:**

| Scope | Output |
|-------|--------|
| Tiny (script, one-liner) | Maybe no document needed — just do it |
| Small (quick feature, bug fix) | Brief spec in chat or short markdown |
| Medium (feature, integration) | Focused requirements doc |
| Large (new product, major system) | Full PRD with all sections |

Use [prd-template.md](references/prd-template.md) as a guide, but only include sections that are relevant.

**Saving:**
- Tiny/Small: May not need a file — just proceed to implementation
- Medium+: Save as `.claude/PRD.md` — this becomes input for `/002-setup-project`

**Note for `/002-setup-project`:** When you save a PRD file, `/002-setup-project` will set `requirements_source: "file"` in tasks.json. If the user declines to save a PRD (preferring to keep requirements in chat context), `/002-setup-project` should set `requirements_source: "chat"` and summarize requirements in CONTEXT.md instead.

**Project `.env` File:**

Based on the dependencies selected and `~/.claude/services.json` (from `/000-install`), create a project-specific `.env` file:

```bash
# Check which services user has configured globally
cat ~/.claude/services.json
```

Create `.env` with the services needed for this project:

```bash
# .env (project root)
# Generated by /001-scope-project
# ⚠️  DO NOT COMMIT — add to .gitignore

# ===================
# Backend: Supabase
# ===================
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_KEY=

# ===================
# Payments: Stripe
# ===================
STRIPE_SECRET_KEY=
STRIPE_PUBLISHABLE_KEY=
STRIPE_WEBHOOK_SECRET=

# ===================
# AI: OpenAI
# ===================
OPENAI_API_KEY=

# ===================
# App Config
# ===================
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

**Auto-populate from global config if user approves:**

```json
{
  "questions": [{
    "question": "You have some of these API keys configured globally. Copy them to the project .env?",
    "header": "API Keys",
    "options": [
      {"label": "Yes, copy configured keys (Recommended)", "description": "Pre-fill .env with your existing keys"},
      {"label": "No, I'll add them manually", "description": "Create .env with empty placeholders"},
      {"label": "Use environment variables", "description": "Don't create .env, rely on shell env"}
    ],
    "multiSelect": false
  }]
}
```

Also create `.env.example` (safe to commit) with placeholder values:

```bash
# .env.example
SUPABASE_URL=your-project-url
SUPABASE_ANON_KEY=your-anon-key
STRIPE_SECRET_KEY=sk_test_...
```

Ensure `.gitignore` includes `.env`:

```bash
# Add to .gitignore if not present
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
```

---

**Project-Scoped Skills Configuration:**

If aesthetic/design skills or dependencies were selected, create `skills.json` inside the `.claude/` directory:

```json
{
  "projectSkills": {
    "aesthetic": [
      "brand-guidelines",
      "vercel-react-best-practices"
    ],
    "notes": {
      "brand-guidelines": "Use for all UI components and documentation",
      "vercel-react-best-practices": "Apply to all React components"
    }
  },
  "createdBy": "001-scope-project",
  "createdAt": "2024-01-15T10:30:00Z"
}
```

This file tells subsequent skills (`/002-setup-project`, `/003-execute-tasks`) which aesthetic guidelines to apply during implementation.

---

## Key Behaviors

1. **Start open** — Let them describe intent before structuring
2. **Match their energy** — Small ask = simple questions. Big vision = thorough discovery.
3. **Follow the thread** — Each question reacts to what they just said
4. **Don't over-engineer** — A 10-line script doesn't need a PRD
5. **Use AskUserQuestion strategically** — For choices, not for open exploration

---

## Example: Small Scope

**User**: "I need a script that renames files in a folder based on their creation date"

**You**: "Simple enough. A few quick questions:"

```json
{
  "questions": [{
    "question": "What format for the new names?",
    "header": "Format",
    "options": [
      {"label": "2024-01-15-filename.txt", "description": "Date prefix"},
      {"label": "filename-2024-01-15.txt", "description": "Date suffix"},
      {"label": "2024/01/15/filename.txt", "description": "Date folders"}
    ]
  }]
}
```

Then maybe one more question about handling duplicates, and you're done. No PRD needed.

---

## Example: Large Scope

**User**: "I want to build a marketplace for freelance developers"

**You**: "That's a substantial project. Let me understand the vision."

Then many rounds of AskUserQuestion covering:
- Target users (who's buying, who's selling)
- Core workflows (finding work, hiring, payments)
- Differentiators (what makes this different from Upwork)
- Tech preferences
- MVP scope vs full vision
- And so on...

This warrants a full PRD with all sections.

---

## Example: Project with UI (Aesthetic Skills)

**User**: "I want to build a dashboard for monitoring our API usage"

**You**: "Got it — an API monitoring dashboard. Let me understand what you need."

After gathering core requirements, since this involves UI:

```json
{
  "questions": [{
    "question": "This dashboard has visual/UI elements. Which design skills should guide the work?",
    "header": "Design Skills",
    "options": [
      {"label": "brand-guidelines", "description": "Apply your brand colors & typography"},
      {"label": "vercel-react-best-practices", "description": "React performance patterns"},
      {"label": "web-design-guidelines", "description": "UI/UX best practices review"}
    ],
    "multiSelect": true
  }]
}
```

If user selects `brand-guidelines` + `vercel-react-best-practices`, create `.claude/skills.json`:

```json
{
  "projectSkills": {
    "aesthetic": ["brand-guidelines", "vercel-react-best-practices"],
    "notes": {
      "brand-guidelines": "Dashboard should match company visual identity",
      "vercel-react-best-practices": "Optimize for performance with real-time data updates"
    }
  }
}
```

This configuration persists with the project and informs `/002-setup-project` and `/003-execute-tasks`.

---

## Example: Project with External Dependencies

**User**: "I want to build a SaaS for scheduling social media posts"

**You**: "A social media scheduler — that'll need some external services. Let me understand the scope."

After gathering core requirements:

```json
{
  "questions": [{
    "question": "What kinds of external services will this project need?",
    "header": "Services",
    "options": [
      {"label": "Database/Backend", "description": "Data storage, auth, real-time"},
      {"label": "APIs/Integrations", "description": "Third-party services, webhooks"},
      {"label": "Payments", "description": "Stripe, PayPal, etc."}
    ],
    "multiSelect": true
  }]
}
```

User selects all three. Follow up for each:

**Backend:**
```json
{
  "questions": [{
    "question": "Which backend/database approach?",
    "header": "Backend",
    "options": [
      {"label": "Supabase (Recommended)", "description": "Postgres + Auth + Realtime + Storage"},
      {"label": "Firebase", "description": "NoSQL + Auth + Realtime"},
      {"label": "Self-hosted", "description": "Custom setup"}
    ]
  }]
}
```

User selects Supabase.

**Integrations** (specific to social media scheduler):
> "For a social media scheduler, you'll likely need APIs for the platforms you're posting to. Which ones?"

```json
{
  "questions": [{
    "question": "Which social platforms will you support?",
    "header": "Platforms",
    "options": [
      {"label": "Twitter/X", "description": "Twitter API v2"},
      {"label": "LinkedIn", "description": "LinkedIn Marketing API"},
      {"label": "Instagram", "description": "Meta Graph API"},
      {"label": "Other/Multiple", "description": "Additional platforms"}
    ],
    "multiSelect": true
  }]
}
```

**Payments:**
```json
{
  "questions": [{
    "question": "Which payment provider?",
    "header": "Payments",
    "options": [
      {"label": "Stripe (Recommended)", "description": "Cards, subscriptions"},
      {"label": "LemonSqueezy", "description": "Handles tax/compliance as MoR"}
    ]
  }]
}
```

**Generate project `.env`:**

Check `~/.claude/services.json` — user has Supabase and Stripe configured globally.

```json
{
  "questions": [{
    "question": "You have Supabase and Stripe keys configured. Copy them to project .env?",
    "header": "API Keys",
    "options": [
      {"label": "Yes, copy configured keys (Recommended)", "description": "Pre-fill with existing keys"},
      {"label": "No, I'll add manually", "description": "Empty placeholders"}
    ]
  }]
}
```

User selects "Yes". Create `.env`:

```bash
# .env
# Generated by /001-scope-project for: Social Media Scheduler
# ⚠️  DO NOT COMMIT

# Backend: Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_KEY=eyJ...

# Payments: Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=

# Social Platform APIs (add your keys)
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_BEARER_TOKEN=
LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=
META_APP_ID=
META_APP_SECRET=

# App Config
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

Also create `.env.example` and update `.gitignore`.

**Final `.claude/skills.json`:**

```json
{
  "projectSkills": {
    "aesthetic": ["brand-guidelines", "vercel-react-best-practices"],
    "dependencies": {
      "backend": {
        "provider": "supabase",
        "features": ["auth", "database", "storage"],
        "notes": "Store scheduled posts, user accounts, media assets"
      },
      "payments": {
        "provider": "stripe",
        "features": ["subscriptions"],
        "notes": "Monthly plans with usage tiers"
      },
      "integrations": [
        {"name": "twitter-api", "purpose": "Post scheduling", "notes": "Twitter API v2, need elevated access"},
        {"name": "linkedin-api", "purpose": "Post scheduling", "notes": "Marketing API"},
        {"name": "meta-graph-api", "purpose": "Instagram posting", "notes": "Business account required"}
      ]
    },
    "envFile": ".env",
    "envConfigured": ["SUPABASE_URL", "SUPABASE_ANON_KEY", "STRIPE_SECRET_KEY"],
    "envNeeded": ["TWITTER_API_KEY", "LINKEDIN_CLIENT_ID", "META_APP_ID"]
  }
}
```

---

## AskUserQuestion Patterns

**Drilling into specifics:**
```json
{
  "question": "You mentioned user authentication. What approach?",
  "options": [
    {"label": "Email + password", "description": "Traditional"},
    {"label": "OAuth only", "description": "Google, GitHub, etc."},
    {"label": "Magic link", "description": "Passwordless"},
    {"label": "Not sure yet", "description": "Help me decide"}
  ]
}
```

**Confirming understanding:**
```json
{
  "question": "So the core flow is: user uploads file → system processes → user downloads result. Right?",
  "options": [
    {"label": "Yes, exactly", "description": "Move on"},
    {"label": "Close but...", "description": "Small correction"},
    {"label": "Not quite", "description": "Let me clarify"}
  ]
}
```

**Gauging scope:**
```json
{
  "question": "How big is this project in your mind?",
  "options": [
    {"label": "Quick thing", "description": "Hour or less of work"},
    {"label": "Small feature", "description": "A day or two"},
    {"label": "Significant feature", "description": "A week+"},
    {"label": "Full product", "description": "Major undertaking"}
  ]
}
```
