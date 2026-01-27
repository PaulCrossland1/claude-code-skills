# Questioning Guide

Reference for effective discovery questioning. Use these patterns to gather complete requirements.

---

## Questioning Principles

### 1. Start Broad, Then Narrow

```
"What are you building?" → "A scheduling app"
"Who uses it?" → "Small businesses"
"What's their biggest pain?" → "Double-bookings"
"How do they handle that today?" → "Manual spreadsheets"
```

### 2. Follow the Thread

When an answer reveals complexity, dive deeper before moving on:

```
"How do users authenticate?" → "OAuth with Google"
"Just Google, or other providers too?" → "Maybe GitHub later"
"Do you need different permission levels?" → "Yes, admin and regular users"
"What can admins do that regular users can't?" → [deeper...]
```

### 3. Offer Options When Defaults Exist

Don't ask open-ended questions when there are common patterns:

**Bad**: "What database should we use?"

**Good**:
```json
{
  "question": "What database fits your needs?",
  "options": [
    {"label": "PostgreSQL (Recommended)", "description": "Relational, robust, great ecosystem"},
    {"label": "MongoDB", "description": "Document store, flexible schema"},
    {"label": "SQLite", "description": "Simple, file-based, good for small apps"},
    {"label": "Other", "description": "I have specific requirements"}
  ]
}
```

### 4. Confirm Assumptions

State what you're assuming and verify:

```json
{
  "question": "I'm assuming: React frontend, Node backend, PostgreSQL database, deployed to Vercel. Correct?",
  "options": [
    {"label": "Yes, proceed", "description": "That stack works"},
    {"label": "Mostly right", "description": "Small adjustments needed"},
    {"label": "Different approach", "description": "Let me explain"}
  ]
}
```

### 5. Track What's Decided

Never re-ask something that's been confirmed. Keep a mental checklist:

- ✓ Problem: Double-booking pain for small businesses
- ✓ Users: Business owners, their clients
- ✓ Auth: Google OAuth, admin/user roles
- ○ Tech stack: Need to confirm
- ○ Data model: Not yet discussed

---

## Question Patterns by Topic

### Understanding the Problem

- "What specific problem are you solving?"
- "Who experiences this problem?"
- "How do they cope with it today?"
- "Why is now the right time to fix this?"
- "What happens if we don't build this?"

### Understanding Users

- "Who's the primary user?"
- "What's their context when using this?" (mobile, desktop, stressed, casual)
- "What motivates them?"
- "Who else might use it differently?"
- "Who is this explicitly NOT for?"

### Defining Success

- "How will you know this is working?"
- "What metrics matter?"
- "What must NOT get worse?"
- "What's the minimum viable outcome?"

### Scoping Functionality

- "What are the must-have features for v1?"
- "What's explicitly out of scope?"
- "What's deferred to v2?"
- "Walk me through the core user workflow"

### Technical Decisions

- "Any existing tech stack constraints?"
- "Preferences for frontend/backend/database?"
- "How will users authenticate?"
- "Any third-party services needed?" (payments, email, analytics)
- "Where will this be deployed?"

### Edge Cases & Risks

- "What if [unusual situation]?"
- "What could go wrong?"
- "What happens when [dependency] fails?"
- "How do we handle [edge case]?"

---

## Multi-Question Patterns

### For Tech Stack (when user has preferences):

```json
{
  "questions": [
    {
      "question": "Frontend framework?",
      "header": "Frontend",
      "options": [
        {"label": "React/Next.js", "description": "Most popular, great ecosystem"},
        {"label": "Vue/Nuxt", "description": "Simpler learning curve"},
        {"label": "Svelte", "description": "Compiled, fast"},
        {"label": "Other", "description": "Different preference"}
      ]
    },
    {
      "question": "Backend approach?",
      "header": "Backend",
      "options": [
        {"label": "Node.js", "description": "JavaScript everywhere"},
        {"label": "Python", "description": "FastAPI, Django"},
        {"label": "Go", "description": "Performance-critical"},
        {"label": "Serverless", "description": "Edge functions, no server"}
      ]
    }
  ]
}
```

### For Authentication:

```json
{
  "questions": [
    {
      "question": "How should users log in?",
      "header": "Auth Method",
      "options": [
        {"label": "OAuth (Google, GitHub)", "description": "Social login, no passwords"},
        {"label": "Email + Password", "description": "Traditional credentials"},
        {"label": "Magic Link", "description": "Passwordless via email"},
        {"label": "No auth needed", "description": "Public or anonymous use"}
      ],
      "multiSelect": true
    },
    {
      "question": "Different permission levels?",
      "header": "Roles",
      "options": [
        {"label": "Single role", "description": "All users equal"},
        {"label": "Admin + User", "description": "Two-tier permissions"},
        {"label": "Multiple roles", "description": "Complex RBAC needed"},
        {"label": "Team-based", "description": "Permissions by organization"}
      ]
    }
  ]
}
```

### For Scope Boundaries:

```json
{
  "questions": [
    {
      "question": "What's the absolute minimum for v1?",
      "header": "MVP",
      "options": [
        {"label": "Core flow only", "description": "Just the happy path"},
        {"label": "Core + auth", "description": "Basic features with login"},
        {"label": "Full v1 vision", "description": "Complete initial feature set"}
      ]
    },
    {
      "question": "Any hard constraints?",
      "header": "Constraints",
      "options": [
        {"label": "Timeline", "description": "Must ship by date X"},
        {"label": "Budget", "description": "Cost limits"},
        {"label": "Compliance", "description": "GDPR, HIPAA, etc."},
        {"label": "No major constraints", "description": "Flexible"}
      ],
      "multiSelect": true
    }
  ]
}
```

---

## When to Stop Asking

You have enough when you can confidently fill every section of the output document without guessing.

**Checklist before generating:**

- [ ] I understand WHY we're building this
- [ ] I know WHO will use it
- [ ] I can describe the core WORKFLOW
- [ ] I know the TECH STACK (or constraints)
- [ ] I understand what SUCCESS looks like
- [ ] I know what's IN and OUT of scope
- [ ] I've identified major RISKS

If any of these are unclear, keep asking.
