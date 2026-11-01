# Observability Standards

This document defines logging, metrics, and error reporting practices.

## Logging

### Log Levels
- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages (something unexpected but not error)
- **ERROR**: Error events (something went wrong)
- **CRITICAL**: Critical errors (system may not recover)

### When to Use Each Level

#### DEBUG
- Detailed execution flow
- Variable values for debugging
- Performance metrics (detailed)

#### INFO
- Application lifecycle events (startup, shutdown)
- Significant state changes
- User actions (audit trail)
- Successful operations

#### WARNING
- Deprecated feature usage
- Retryable failures
- Configuration issues (non-critical)
- Unexpected but handled situations

#### ERROR
- Unhandled exceptions
- Failed operations
- External service failures
- Data corruption issues

#### CRITICAL
- System cannot continue
- Data loss
- Security breaches
- Complete service outage

### Log Format

#### Structured Logging
Use structured logging (JSON format) for production:
```python
import logging
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "context": getattr(record, "context", {}),
        }
        return json.dumps(log_obj)
```

#### Standard Fields
Every log should include:
- timestamp
- level
- logger name
- message
- correlation ID (if applicable)
- user ID (if applicable)

### Logging Best Practices

#### DO
- Log at appropriate level
- Include context (user ID, request ID, etc.)
- Use structured data
- Log entry/exit of important functions
- Log security events

#### DON'T
- Log sensitive data (passwords, tokens, PII)
- Log at DEBUG level in production
- Log too frequently (performance impact)
- Log in tight loops
- Log large objects

### Example
```python
import logging

logger = logging.getLogger(__name__)

def submit_idea(command: SubmitIdeaCommand) -> Idea:
    logger.info("Submitting idea", extra={"user_id": command.author_id})

    try:
        idea = Idea(
            title=command.title,
            description=command.description,
            author_id=command.author_id,
        )
        logger.debug("Idea created", extra={"idea_id": idea.id})
        return idea
    except EmptyTitleError as e:
        logger.warning("Empty title submitted", extra={"user_id": command.author_id})
        raise
    except Exception as e:
        logger.error("Failed to submit idea", extra={"user_id": command.author_id}, exc_info=True)
        raise
```

## Metrics

### What to Measure

#### Business Metrics
- Ideas submitted per day
- Approval rate
- User signups
- Feature usage

#### Technical Metrics
- Request latency (p50, p95, p99)
- Error rate
- Throughput (requests per second)
- Database query time

#### Resource Metrics
- CPU usage
- Memory usage
- Disk usage
- Network I/O

### Metric Naming
Use consistent naming:
- `feature_action_unit`
- Examples: `ideas_submitted_total`, `request_duration_seconds`

### Tools
Consider:
- Prometheus for metrics collection
- Grafana for visualization
- StatsD for simple metrics

## Error Reporting

### Error Categories
- **Transient**: Temporary failures (retryable)
- **Permanent**: Non-retryable failures
- **Expected**: Expected error conditions
- **Unexpected**: Bugs, unexpected failures

### Error Handling Strategy
1. Log the error with context
2. Classify the error
3. Determine retry strategy
4. Return appropriate response to user
5. Alert if critical

### Error Response Format
```json
{
  "error": {
    "type": "EmptyTitleError",
    "message": "Idea title cannot be empty",
    "details": {},
    "request_id": "abc-123"
  }
}
```

## Distributed Tracing

### Correlation IDs
Generate and pass correlation IDs through the system:
```python
import uuid

correlation_id = str(uuid.uuid4())
# Pass through logs, headers, etc.
```

### Span Creation
For operations that span multiple services:
- Create a span for the operation
- Add child spans for sub-operations
- Include timing information

## Performance Monitoring

### Key Metrics
- Response time (p50, p95, p99)
- Error rate
- Throughput
- Resource utilization

### Thresholds
Define alerting thresholds: <!-- inferred: confirm -->
- p95 latency > 500ms: Warning
- p95 latency > 1s: Critical
- Error rate > 1%: Warning
- Error rate > 5%: Critical

## Health Checks

### Health Endpoint
Implement a `/health` endpoint that checks:
- Database connectivity
- External service availability
- Disk space
- Memory usage

### Response Format
```json
{
  "status": "healthy",
  "checks": {
    "database": "ok",
    "cache": "ok",
    "disk": "warning"
  }
}
```

## Alerting

### When to Alert
- Critical errors
- High error rates
- Performance degradation
- Security incidents
- Data integrity issues

### Alert Severity
- **P1**: Critical (wake someone up)
- **P2**: High (respond within 1 hour)
- **P3**: Medium (respond within 4 hours)
- **P4**: Low (respond within 24 hours)

### Alert Content
Include in alerts:
- What happened
- When it happened
- Impact
- Relevant metrics/logs
- Suggested actions

## Review Checklist

When reviewing observability code, check:
- [ ] Appropriate log level used
- [ ] Sensitive data not logged
- [ ] Context included in logs
- [ ] Errors are logged with stack traces
- [ ] Metrics are properly named
- [ ] Health checks implemented
- [ ] Correlation IDs used
- [ ] Performance monitored
