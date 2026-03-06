---
name: git-commit
description: Standards and formatting for creating git commit messages. **REQUIRED** Invoke this skill BEFORE creating any git commit to ensure proper conventional commit format with type prefixes and descriptions. Use when committing changes or when user asks about commit message format.
---

# Git Commit

Create properly formatted git commit messages following conventional commit standards.

## Commit Message Format

Use conventional commit format: `{type}({scope}): {description}`

The scope is optional but encouraged when the change is scoped to a specific component, module, or package.

### Valid Types

- **feat** - New feature or functionality
- **fix** - Bug fix
- **chore** - Maintenance tasks (dependencies, config, etc.)
- **docs** - Documentation changes
- **style** - Code style/formatting (no logic changes)
- **refactor** - Code restructuring (no behavior changes)
- **test** - Adding or updating tests
- **perf** - Performance improvements
- **ci** - CI/CD pipeline changes
- **build** - Build system or external dependencies

### Breaking Changes

Append `!` after the type/scope to signal a breaking change:

```
feat!: remove deprecated API endpoints
feat(auth)!: change token format from JWT to opaque
```

Or include a `BREAKING CHANGE:` footer in the commit body:

```
feat(api)!: rename user endpoint

BREAKING CHANGE: /api/user is now /api/users — update all clients
```

### Examples

```
feat: add new authentication endpoint
feat(auth): implement JWT-based login flow
fix: resolve null pointer exception in API handler
fix(payments): handle declined card response correctly
chore: update dependencies
chore(deps): upgrade Spring Boot to 3.2.0
docs: update README with deployment instructions
refactor(validation): extract logic into separate service
test(user-service): add unit tests for registration flow
perf(db): optimize user query with index
ci: add automated deployment workflow
```

### Multi-line Commits

When a single-line description isn't enough, add a blank line then a body:

```
feat(auth): implement OAuth2 PKCE flow

Replaces the implicit grant flow with PKCE for better security.
Refresh tokens are now rotated on each use.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

## Best Practices

- Keep the subject line concise (72 chars or fewer)
- Use imperative mood ("add" not "added" or "adds")
- Start description with lowercase after the colon
- No period at the end of the subject line
- Put the "why" and context in the body, not the subject
- Always include `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer when Copilot assisted
