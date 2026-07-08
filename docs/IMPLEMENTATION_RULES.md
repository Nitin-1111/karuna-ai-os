# Karuna AI OS
# Implementation Rules
Version 1.0

---

# Purpose

This document defines the implementation workflow for Karuna AI OS.

It complements `ENGINEERING_STANDARD.md`.

`ENGINEERING_STANDARD.md` defines **how code should be written.**

`IMPLEMENTATION_RULES.md` defines **how work should be performed.**

Both documents must be followed.

---

# Project Philosophy

Karuna AI OS is built incrementally.

Each phase should implement only the functionality assigned to that phase.

Do not anticipate future phases.

Do not redesign the architecture.

Preserve existing design decisions.

Generate production-quality code.

---


# Prompt Contract

Every implementation prompt is assumed to require the following workflow unless explicitly overridden.

Before writing any code:

1. Read:
   - docs/ENGINEERING_STANDARD.md
   - docs/IMPLEMENTATION_RULES.md
   - docs/ARCHITECTURE.md

2. Inspect the existing repository.

3. Understand the current implementation.

4. Reuse existing modules whenever possible.

5. Preserve the architecture.

6. Implement ONLY the requested phase.

7. Do not implement future phases.

8. Follow the default verification suite.

9. Commit and push after successful verification.

10. Stop immediately after completing the requested phase.
---

# Existing Repository

Before writing any code:

1. Inspect the current repository.
2. Read all relevant modules.
3. Understand existing implementations.
4. Reuse existing utilities.
5. Reuse existing exceptions.
6. Reuse existing logging.
7. Reuse existing configuration.
8. Reuse existing validation.

The existing repository is the source of truth.

---

# Scope Control

Implement ONLY the requested phase.

Never implement future phases.

Never partially implement future phases.

Never add "helpful" features outside the requested scope.

If a requested feature depends on a future phase, create only the minimum interface required.

Do not implement the dependency itself.

---

# Architecture Preservation

Do not redesign.

Do not rename folders unnecessarily.

Do not move files unnecessarily.

Do not replace existing implementations without justification.

Maintain backwards compatibility.

Preserve package boundaries.

Respect existing abstractions.

---

# Reuse First

Always prefer:

Reuse

over

Rewrite.

Do not duplicate:

- validation
- logging
- configuration
- exceptions
- utilities
- helper methods
- provider logic

---

# Providers

Current supported providers:

- Groq
- Google Gemini

Do not introduce additional providers unless explicitly requested.

Do not hardcode model names.

Continue using the provider abstraction.

Continue using Settings.

---

# Dependencies

Do not introduce unnecessary dependencies.

Prefer Python standard library whenever practical.

Only add third-party libraries when required.

Every dependency must have a clear justification.

---

# File Modifications

Modify existing files only when necessary.

Avoid unnecessary edits.

Create new files only when required.

Avoid changing unrelated modules.

---

# Code Generation

Generate production-ready code.

Avoid placeholders except when explicitly required.

Avoid TODO comments.

Avoid unfinished implementations.

Avoid commented-out code.

Avoid dead code.

---

# Documentation

Write clear docstrings.

Use type hints.

Document public classes.

Document public methods.

Document non-obvious behaviour.

---

# Validation

Validate inputs.

Fail fast.

Raise meaningful exceptions.

Reuse shared exception classes.

Never silently ignore errors.

---

# Logging

Reuse the shared logging system.

Do not use print().

Use structured logging.

Log important events.

Do not over-log.

---

# Testing

Every phase must include verification.

Before completion:

Run Ruff.

Run MyPy.

Run compileall.

Run smoke tests.

Fix every reported issue.

Remove unused imports.

Remove dead code.

Check circular imports.

Ensure package imports work.

---

# Default Verification Suite

Unless explicitly overridden, every implementation phase must execute the following verification steps.

## Static Analysis

- Ruff
- MyPy

## Compilation

- python -m compileall

## Import Validation

- Verify package imports.
- Verify no circular imports.

## Smoke Tests

Run manual smoke tests demonstrating:

- Primary functionality
- Validation
- Error handling

## Quality Checks

Ensure:

- No unused imports
- No dead code
- No TODO comments
- No placeholder implementations unless explicitly requested
- Production-quality code
---

# Prompt Optimization

Implementation prompts should contain only phase-specific objectives.

Do not repeat project-wide engineering rules already defined in:

- ENGINEERING_STANDARD.md
- IMPLEMENTATION_RULES.md
- ARCHITECTURE.md

These documents are considered the permanent source of truth.

Future prompts should reference these documents instead of duplicating their contents.
---

# Output Requirements

Do not paste generated code unless requested.

Return only:

Files Created

Files Modified

Verification Summary

Manual Test Commands

Definition of Done

---

# Manual Testing

Generate manual verification commands for every phase.

Prefer commands using:

python -m

rather than direct executable paths.

Smoke tests should demonstrate:

- primary functionality
- validation
- error handling

---

# Token Efficiency

Avoid regenerating existing code.

Avoid repeating unchanged implementations.

Modify only what is required.

Reuse existing modules whenever possible.

Keep responses concise while maintaining engineering quality.

---

# Git Workflow

Unless explicitly instructed otherwise, every completed phase must:

1. Stage all generated changes.

2. Commit using a descriptive phase-specific commit message.

Example:

Phase 6 - LangGraph Orchestration

3. Push to the default branch.

4. Include the commit hash in the final summary.

If any files remain intentionally uncommitted, explicitly explain why.

The repository should remain in a clean state after every completed phase.

---

# Context Management

To maximize implementation quality and reduce context usage:

- Avoid regenerating existing code.
- Read existing modules before modifying them.
- Prefer modifying existing implementations over creating new ones.
- Avoid repeating instructions already defined in project documentation.

If the context window approaches approximately 85% utilization:

1. Complete the current implementation phase.
2. Commit and push all verified changes.
3. Start a fresh Codex conversation.
4. Reload:
   - docs/ENGINEERING_STANDARD.md
   - docs/IMPLEMENTATION_RULES.md
   - docs/ARCHITECTURE.md
5. Continue with the next phase.

Do not begin a new implementation phase in an almost full context window.
---
# Completion Criteria

A phase is complete only when:

- Requested functionality is implemented.
- No future functionality is implemented.
- Verification passes.
- Smoke tests pass.
- Code follows ENGINEERING_STANDARD.md.
- Existing architecture is preserved.
- Shared infrastructure is reused.
- Output requirements are satisfied.

After completing the assigned phase, stop immediately.

Do not continue into the next phase.