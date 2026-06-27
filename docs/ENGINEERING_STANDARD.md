# Karuna AI OS Engineering Standard

Version: 1.0

---

# Purpose

This document defines the engineering standards for Karuna AI OS.

All future implementation phases must follow this document.

These standards are considered mandatory unless explicitly overridden.

---

# Project Vision

Karuna AI OS is a production-oriented AI Operating System backend.

The project is built incrementally in implementation phases.

Every phase must preserve the existing architecture.

The goal is long-term maintainability, scalability, and production-quality code.

---

# Architecture Principles

The architecture is locked.

Do not redesign the project.

Do not move modules unnecessarily.

Do not rename packages without explicit instruction.

Respect existing boundaries.

Future phases must integrate with previous phases instead of replacing them.

---

# Development Workflow

Every implementation follows this sequence:

1. Implement only the requested phase.
2. Verify the implementation.
3. Fix issues.
4. Run quality checks.
5. Commit to Git.
6. Push to GitHub.
7. Begin the next phase.

Never implement multiple phases at once.

---

# Scope Control

Every implementation must remain inside the requested phase.

Do not generate future functionality.

If a requested feature belongs to a future phase, do not implement it.

---

# Python Standards

Python Version

3.12

Follow:

* PEP 8
* Strong type hints
* Clean imports
* Modular design

Avoid:

* Global state
* Circular imports
* Magic strings
* Duplicate logic

---

# Code Quality

Generate production-quality code.

Never generate:

* TODO comments
* Placeholder implementations
* Fake implementations
* Incomplete files

Every generated file must be complete.

---

# Folder Structure

Preserve the existing project structure.

Only create files required by the current phase.

Do not create unnecessary modules.

---

# Configuration

Configuration must always come from the shared configuration system.

Never hardcode:

* API keys
* Models
* Provider names
* Environment values
* Paths

Use environment variables.

---

# Logging

Use the shared logging system.

Do not create custom logging systems.

Every module should use the common logger.

---

# Exceptions

Use the shared exception hierarchy.

Do not create duplicate exception systems.

Raise meaningful exceptions.

---

# LLM Design Principles

The system is provider-agnostic.

Agents must never know which provider is being used.

Providers must never know about agents.

Future providers should be addable without modifying existing business logic.

---

# Supported Providers (Current Version)

Only:

* Groq
* Google Gemini

Do not implement:

* Anthropic
* OpenAI
* OpenRouter
* Ollama
* Hugging Face
* Azure

unless a future implementation phase explicitly requests them.

---

# Model Policy

Never hardcode model names.

Providers must accept any valid model identifier supplied by configuration.

Changing models must never require changing Python code.

Only configuration should change.

---

# Dependency Rules

Reuse existing modules.

Do not duplicate functionality.

If functionality already exists, import it.

---

# Documentation

Every phase must update documentation only if required.

Do not rewrite existing documentation unnecessarily.

---

# Testing

Every implementation should be verifiable.

Use:

* Ruff
* MyPy
* Compilation checks
* Manual verification

Generate unit tests only when requested by the current phase.

---

# Verification Checklist

Before completing a phase verify:

* Imports
* Configuration
* Logging
* Type checking
* Linting
* Compilation
* No circular imports

---

# Git Workflow

Every completed phase should follow:

git status

git add .

git commit

git push

Use descriptive commit messages.

Example:

Phase 1 - Project Foundation

Phase 2 - Configuration & Infrastructure

Phase 3 - Provider Layer

---

# Output Requirements

Every implementation phase must provide:

* Files created
* Files modified
* Verification summary
* Manual test commands
* Definition of Done

Stop immediately after completing the requested phase.

Do not continue into future phases.

---

# Engineering Philosophy

Build software incrementally.

Prefer simplicity over cleverness.

Prefer maintainability over shortcuts.

Preserve architecture.

Minimize coupling.

Maximize cohesion.

Generate code suitable for production deployment.
