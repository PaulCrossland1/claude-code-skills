---
name: code-simplifier
description: Simplifies recently modified code for clarity, consistency, and maintainability while preserving all functionality. Trigger this skill after completing a coding task or writing a logical chunk of code (implementing a new feature, fixing a bug, refactoring for performance, or completing any code modification). Focuses only on recently modified code unless instructed otherwise.
---

# Code Simplifier

Expert code simplification focused on enhancing clarity, consistency, and maintainability while preserving exact functionality. Prioritize readable, explicit code over overly compact solutions.

## Refinement Process

1. Identify recently modified code sections
2. Analyze for opportunities to improve clarity and consistency
3. Apply project-specific best practices (from CLAUDE.md if present)
4. Ensure all functionality remains unchanged
5. Verify the refined code is simpler and more maintainable

## Simplification Principles

### Preserve Functionality
Never change what the code does—only how it does it. All original features, outputs, and behaviors must remain intact.

### Enhance Clarity
- Reduce unnecessary complexity and nesting
- Eliminate redundant code and abstractions
- Use clear variable and function names
- Consolidate related logic
- Remove comments that describe obvious code
- **Avoid nested ternary operators**—prefer switch statements or if/else chains
- Choose clarity over brevity

### Apply Project Standards
Follow established coding standards from CLAUDE.md when present:
- ES modules with proper import sorting and extensions
- Prefer `function` keyword over arrow functions
- Explicit return type annotations for top-level functions
- React components with explicit Props types
- Proper error handling (avoid try/catch when possible)
- Consistent naming conventions

### Maintain Balance
Avoid over-simplification that could:
- Reduce clarity or maintainability
- Create overly clever solutions
- Combine too many concerns into single functions
- Remove helpful abstractions
- Prioritize "fewer lines" over readability
- Make code harder to debug or extend

## Scope

Focus only on recently modified code unless explicitly instructed to review broader scope.