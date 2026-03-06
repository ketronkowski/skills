---
name: create-pr
description: Automate GitHub Pull Request creation following team conventions with JIRA ID or conventional commit formats. **REQUIRED** Invoke this skill when user asks to create a PR, push and create a PR, or mentions opening/making a pull request. Handles PR status validation, JIRA work item discovery, and proper title/description formatting.
---

# Create PR

Automate GitHub Pull Request creation with team conventions, JIRA integration, and proper formatting.

## PR Creation Workflow

Follow these steps when creating a PR:

### 1. Validate Existing PR Status

**CRITICAL**: Before updating an existing PR, check its status:

```bash
gh pr view <number> --json state,mergedAt
```

- If PR is **merged or closed**: Create a new PR instead of updating
- Only update PRs that are currently **open**

### 2. Check for Previous PRs on Branch

Look for previous merged PRs to reuse JIRA IDs:

```bash
gh pr list --state merged --author @me --head $(git branch --show-current)
```

Offer to reuse the JIRA ID from the most recent merged PR on this branch.

### 3. Push Branch (if needed)

Ensure the current branch is pushed to origin before creating the PR:

```bash
# Check if branch has a remote tracking branch
git status -sb

# Push if not yet pushed (set upstream on first push)
git push -u origin $(git branch --show-current)
```

### 4. Query Open JIRA Work Items

Check open work items in the current Green Team sprint:

```bash
# Get active sprint ID for board 214
SPRINT_ID=$(acli jira board list-sprints --id 214 --state active 2>&1 | grep "^│" | grep active | awk '{print $2}')

# List open work items assigned to current user
acli jira sprint list-workitems --sprint $SPRINT_ID --board 214 --jql "assignee = currentUser() AND status not in (Resolved, Done)"
```

Present these as JIRA ID options to the user.

### 5. Prompt for Title Format

Offer two title format options:

**Option 1: JIRA ID format**
- Use suggestions from previous PRs or current sprint work items
- Example: `GLCP-313119: Add deployment configuration`

**Option 2: Conventional commit prefix**
- Valid prefixes: `feat`, `fix`, `chore`, `docs`, `style`, `refactor`, `test`, `perf`, `ci`, `build`
- Example: `feat: add new API endpoint`

### 6. Format PR Title and Description

#### JIRA ID Format

**Title**: `{JIRA-ID}: {description}`
- Example: `GLCP-313119: Add deployment configuration for staging environment`

**Description**: Include JIRA link
```markdown
Implements deployment configuration for staging environment.

Jira: https://hpe.atlassian.net/browse/GLCP-313119
```

#### Conventional Commit Format

**Title**: `{prefix}: {description}`
- Example: `feat: add new API endpoint`

**Description**: Standard PR description without JIRA link

### 7. Create or Update the PR

**Create a new PR:**
```bash
gh pr create \
  --title "{title}" \
  --body "{description}" \
  --base main
```

**Update an existing open PR:**
```bash
gh pr edit <number> \
  --title "{title}" \
  --body "{description}"
```

## Commit Message Format

Use conventional commit format for all commits:

**Format**: `{type}: {description}`

**Valid types**: feat, fix, chore, docs, style, refactor, test, perf, ci, build

**Examples**:
- `feat: add authentication endpoint`
- `fix: resolve null pointer exception`
- `chore: update dependencies`
- `docs: update README`
