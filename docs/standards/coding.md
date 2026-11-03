# Coding Standards

This document defines the coding style and conventions for this repository.

## Language-Specific Standards

### Python

#### Style
- **Formatter**: ruff (uses ruff-format)
- **Linter**: ruff
- **Type Checker**: pyright (`just types`, standard mode)
- **Docstring Format**: Google style

#### Naming Conventions
- **Classes**: PascalCase (e.g., `Idea`, `SubmitIdea`)
- **Functions/Methods**: snake_case (e.g., `submit_idea`, `get_user`)
- **Variables**: snake_case (e.g., `user_id`, `idea_count`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_RETRIES`, `DEFAULT_TIMEOUT`)
- **Private members**: Leading underscore (e.g., `_ideas`, `_validate`)

#### Type Hints
- All functions must have type hints
- Use `|` for union types (Python 3.10+)
- Use `typing` module for complex types
- Return types are required for all functions

#### Imports
- Group imports: standard library, third-party, local
- Use absolute imports for local modules
- Order: stdlib, third-party, local (each group separated by blank line)
- No wildcard imports (`from module import *`)

#### File Organization
- One class per file unless closely related
- Keep files under 300 lines <!-- inferred: confirm -->
- Related functions grouped together
- Docstrings for all public functions/classes

#### Error Handling
- Use custom exception classes for domain errors
- Catch specific exceptions, not bare `except:`
- Log errors at appropriate level
- Never silently swallow exceptions

#### Code Structure
<!-- inferred: confirm -->
- Maximum nesting depth: 4
- Maximum function length: 50 lines
- Maximum parameter count: 7 (use dataclasses for more)
- Cyclomatic complexity: < 10

## General Principles

### Readability
- Code should be self-documenting
- Comments explain "why", not "what"
- Avoid cleverness in favor of clarity
- Use meaningful names

### DRY
- Don't Repeat Yourself
- Extract common patterns to functions
- Use composition over inheritance where appropriate

### YAGNI
- You Aren't Gonna Need It
- Don't add features "just in case"
- Implement what's needed now

### SOLID
- Single Responsibility
- Open/Closed
- Liskov Substitution
- Interface Segregation
- Dependency Inversion

## Tooling

### Running Formatters
```bash
ruff format .
```

### Running Linter
```bash
ruff check .
```

### All at Once
```bash
ruff format --check . && ruff check .
```

## Violations

The CI will fail if:
- ruff format produces changes
- ruff check reports errors

Fix these before committing.
