# ADR-0001

## Title

Runtime-Centered Architecture

## Status

Accepted

## Context

Multiple interfaces (CLI, API, Desktop, Mobile) need a shared execution engine.

Without a runtime, business logic becomes duplicated across interfaces.

## Decision

Create a Runtime responsible for:

- Session lifecycle
- Assistant execution
- Memory access
- Provider interaction
- Tool execution

Every external interface communicates only with the Runtime.

## Consequences

Advantages

- Single execution path
- Easier testing
- Better scalability
- Cleaner architecture

Trade-offs

- Slightly more abstraction
- More classes
