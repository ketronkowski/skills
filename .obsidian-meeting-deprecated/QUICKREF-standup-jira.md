# Stand-up JIRA Quick Reference

## 🔴 CRITICAL: AUTO-POPULATION RULE 🔴

**WHEN PROCESSING ANY STANDUP MEETING:**

```
STEP 1: Check if ## JIRA section is empty
STEP 2: If empty → AUTOMATICALLY populate it (NO ASKING)
STEP 3: Continue with rest of processing
```

**DO NOT ask "should I populate JIRA?" - JUST DO IT.**

This has failed 10+ times. It must be automatic now.

---

## When It Triggers
- Meeting filename contains: `*Green Standup*` OR `*Magenta Standup*`
- Has a `## JIRA` section in the file

## What It Does
1. Detects stand-up type (Green or Magenta)
2. Queries JIRA for open sprint issues for that team
3. Groups issues by assignee
4. Maps assignees to Obsidian People profiles
5. Formats as markdown with clickable JIRA links
6. Inserts into `## JIRA` section

## Output Format
```markdown
## JIRA

### [[Last, First|First Last]]
- [GLCP-12345](https://hpe.atlassian.net/browse/GLCP-12345) - Issue title
- [GLCP-12346](https://hpe.atlassian.net/browse/GLCP-12346) - Another issue

### Unassigned
- [GLCP-12347](https://hpe.atlassian.net/browse/GLCP-12347) - Unassigned work
```

## Team Mapping
| Meeting Type | Team Name | Board ID |
|-------------|-----------|----------|
| Green Standup | Green | 214 |
| Magenta Standup | Magenta | 317 |

## JIRA Query
**Recommended: Board-Based Sprint Query**
```bash
# 1. Get active sprint ID for the team's board
SPRINT_ID=$(acli jira board list-sprints --id {BOARD_ID} --state active 2>&1 | grep "^│" | grep active | awk '{print $2}')

# 2. Get ALL open issues in that sprint (CRITICAL: Use this method)
acli jira workitem search --jql "sprint = $SPRINT_ID AND status != Done AND status != Resolved ORDER BY assignee" 2>&1
```

**Board IDs:**
- Green Team: Board 214
- Magenta Team: Board 331

**CRITICAL:** Do NOT use `acli jira sprint list-workitems` - it does not return all open items. Always use `acli jira workitem search`.

## Usage Examples

### Pre-Meeting Processing (JIRA Only)
```
"Pre-meeting processing for 2026-01-28 Green Standup"
"Populate JIRA only for today's Magenta Standup"
```
**Result:** Populates `## JIRA` section only, skips attendees/transcript/summary

### Full Meeting Processing
```
"Process the 2026-01-28 Green Standup"
"Process today's Magenta Standup"
```
**Result:** Complete workflow including JIRA, attendees, transcript, and summary

## Processing Modes

### Pre-Meeting Mode (Stand-alone)
- ✅ Populates `## JIRA` section only
- ✅ No attendee screenshot needed
- ✅ No transcript needed
- ✅ Can run before meeting starts
- ⚡ Fast - just JIRA query and formatting

### Full Processing Mode
- ✅ Populates `## JIRA` section (if empty)
- ✅ Extracts `## Attendees` (if screenshot present)
- ✅ Cleans `## Transcript` (if present)
- ✅ Generates summary (if needed)

## What Gets Updated
- ✅ `## Attendees` section (if screenshot present)
- ✅ `## JIRA` section (populated with sprint issues)
- ✅ `## Transcript` section (cleaned if present)
- ✅ `## Notes` or `## Copilot Summary` (generated if needed)

## Files Updated
- `/Users/kevin/obsidian-meeting/SKILL.md` - Main documentation
- `/Users/kevin/obsidian-meeting/examples.md` - Example stand-up
- `/Users/kevin/obsidian-meeting/reference-standup-jira.md` - Implementation guide

## See Also
- [SKILL.md](SKILL.md#jira-section-auto-population-stand-ups) - Full documentation
- [examples.md](examples.md#example-4-processed-stand-up-meeting-green-standup) - Complete example
- [reference-standup-jira.md](reference-standup-jira.md) - Implementation details
- [jira-glcp skill](../skills/jira-glcp/SKILL.md) - JIRA query tools
