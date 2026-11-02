# ideas Specification

## Purpose

Describes the current behavior of the ideas capability: submitting ideas over HTTP and the domain rules governing an idea's lifecycle status. This is a baseline spec capturing what the code does today.

## Requirements

### Requirement: Idea Submission

The system SHALL accept new ideas via `POST /ideas` with a JSON body containing `title` (required, 1–200 characters), `description` (optional, defaults to empty string, max 5000 characters), and `author_id` (required). The system SHALL store the idea via the configured repository and respond with `201 Created` containing the idea's `id`, `title`, `description`, `author_id`, `status`, and `created_at`.

#### Scenario: Successful submission

- **WHEN** a client posts `{"title": "New idea", "description": "Details", "author_id": "u1"}` to `/ideas`
- **THEN** the system responds `201 Created` with a body containing a generated UUID `id`, `status` equal to `submitted`, and a `created_at` timestamp

#### Scenario: Description omitted

- **WHEN** a client posts an idea body without a `description` field
- **THEN** the idea is created with an empty description

#### Scenario: Title violates request schema

- **WHEN** a client posts an idea with an empty `title`, a `title` longer than 200 characters, or a missing `title`
- **THEN** the system responds `422 Unprocessable Entity`

#### Scenario: Blank title rejected by domain

- **WHEN** a client posts an idea whose `title` contains only whitespace
- **THEN** the system responds `422 Unprocessable Entity` with a detail explaining the title cannot be empty

#### Scenario: Title is normalized

- **WHEN** a client posts an idea whose `title` has leading or trailing whitespace
- **THEN** the stored and returned `title` has the whitespace stripped

### Requirement: Idea Initial State

The system SHALL create each new idea with a generated UUID identifier, status `submitted`, and a UTC creation timestamp.

#### Scenario: New idea defaults

- **WHEN** an idea is created by any submission path
- **THEN** its `status` is `submitted`, its `id` is a unique UUID, and `created_at` is set at creation time

### Requirement: Idea Status Transitions

The domain SHALL allow an idea to move from `submitted` to `under_review` via review start, and from `under_review` to `approved` via approval. The domain SHALL reject any other transition with an `InvalidStatusTransitionError`.

#### Scenario: Start review from submitted

- **WHEN** `start_review` is called on an idea in `submitted` status
- **THEN** the idea's status becomes `under_review`

#### Scenario: Approve from under_review

- **WHEN** `approve` is called on an idea in `under_review` status
- **THEN** the idea's status becomes `approved`

#### Scenario: Approve without review is rejected

- **WHEN** `approve` is called on an idea that is not in `under_review` status
- **THEN** an `InvalidStatusTransitionError` is raised and the status is unchanged

#### Scenario: Start review again is rejected

- **WHEN** `start_review` is called on an idea that is not in `submitted` status
- **THEN** an `InvalidStatusTransitionError` is raised and the status is unchanged
