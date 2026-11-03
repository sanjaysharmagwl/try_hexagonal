# Testing Standards

This document defines the testing approach and expectations for this repository.

## Test Pyramid

```
        /\
       /E2E\       (Few, slow, expensive)
      /------\
     /Integration\ (More, medium)
    /------------\
   /   Unit Tests \ (Many, fast, cheap)
  /----------------\
```

### Unit Tests
- **Location**: `packages/core/tests/`
- **What to test**: Domain entities, services, pure functions
- **Speed**: < 1 second each
- **Coverage**: Target 90%+ for domain layer <!-- inferred: confirm -->

### Integration Tests
- **Location**: `apps/api/tests/` (repository/storage integrations may add their own under `packages/*/tests/`)
- **What to test**: HTTP routes through TestClient, adapters with real implementations
- **Speed**: 1-10 seconds each
- **Coverage**: Critical paths only

### End-to-End Tests
- **Location**: `apps/api/tests/`
- **What to test**: Full system through HTTP
- **Speed**: 10+ seconds each
- **Coverage**: Happy path + critical edge cases

## Test Organization

### File Structure
```
packages/core/tests/      # domain + service tests
├── test_domain.py
└── test_service.py
apps/api/tests/           # HTTP tests (TestClient + dependency_overrides)
└── test_ideas_api.py
docs/checks/tests/        # tooling tests
└── test_checks.py
```

### Naming Conventions
- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Test Organization
- One test class per module/class
- Related tests grouped together
- Descriptive test names (test_user_cannot_approve_own_idea)

## Writing Tests

### Given-When-Then Pattern
```python
def test_idea_status_transition():
    # Given
    idea = Idea(title="Test", description="...", author_id="user-1")

    # When
    idea.start_review()

    # Then
    assert idea.status == IdeaStatus.UNDER_REVIEW
```

### Assertions
- Use specific assertions (`assert result == expected`)
- Avoid multiple assertions in one test
- Use pytest fixtures for setup

### Fixtures
- Use fixtures for common test data
- Keep fixtures simple
- Use `conftest.py` for shared fixtures

## Coverage

### Targets
<!-- inferred: confirm -->
- **Overall**: 80%
- **Domain layer**: 90%
- **Application layer**: 80%
- **Adapters**: 70%

### Rules
- CI reports coverage on every run (`just cov` = `pytest --cov=core --cov=api --cov-report=term-missing`)
- Coverage must not decrease relative to `main`
- The 80% overall target is provisional <!-- inferred: confirm -->

### Exceptions
- Legacy code: Documented exception
- Generated code: Not required
- Configuration: Not required

### Measuring Coverage
```bash
just cov   # or: pytest --cov=core --cov=api --cov-report=html
```

## Test Data

### Factories
Use factories or fixtures for test data:
```python
@pytest.fixture
def idea():
    return Idea(title="Test", description="...", author_id="user-1")
```

### Avoid Magic Numbers
Use constants or fixtures:
```python
# Bad
assert response.status_code == 200

# Good
assert response.status_code == status.HTTP_200_OK
```

## Running Tests

### All Tests
```bash
just test
```

### Core (Domain/Service) Tests Only
```bash
just test packages/core/tests
```

### With Coverage
```bash
just cov
```

### Specific Test
```bash
just test packages/core/tests/test_domain.py::test_idea_status
```

## Async Tests

pytest-asyncio is **not installed**. If async tests are needed, add it via an OpenSpec change and document usage here.

## Mocking

### When to Mock
- External services (APIs, databases)
- Time-dependent code
- Slow operations

### When NOT to Mock
- Domain entities
- Value objects
- Pure functions

### Mocking Style
pytest-mock is **not installed**. Use `unittest.mock` from the standard library; add pytest-mock via an OpenSpec change if needed.

## Flaky Tests

Flaky tests (intermittent failures) are not acceptable. If a test is flaky:
1. Fix the test (timing, ordering, etc.)
2. If unfixable, disable and file issue
3. Never merge flaky tests

## CI Requirements

CI will run:
- All unit tests
- Coverage report (coverage must not decrease; 80% overall target <!-- inferred: confirm -->)
- Integration tests if configured

Tests must pass before merging.

## Review Checklist

When reviewing tests, check:
- [ ] Test follows Given-When-Then pattern
- [ ] Test is readable and understandable
- [ ] Test is independent (no coupling)
- [ ] Test has meaningful name
- [ ] Assertions are specific
- [ ] Fixtures used appropriately
- [ ] No magic numbers
- [ ] Mocks used correctly
