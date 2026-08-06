# Lessons Learned

This document captures engineering lessons throughout the project's life.

---

## Lesson 001

### Keep the Runtime Small

Reason

The runtime should coordinate components rather than contain business logic.

Benefit

Easier testing and cleaner architecture.

---

## Lesson 002

### Depend on Interfaces

Reason

Providers and storage systems should be replaceable without changing the runtime.

Benefit

Scalability and flexibility.

---

## Lesson 003

### Documentation Evolves with Code

Reason

Outdated documentation becomes a liability.

Benefit

Developers can trust the documentation.
