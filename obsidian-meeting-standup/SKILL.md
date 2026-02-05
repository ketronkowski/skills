---
name: obsidian-meeting-standup
description: Process standup meeting notes (Green/Magenta) with automatic JIRA population. **Use when** router delegates standup meeting processing. **AUTOMATICALLY** populates JIRA section if empty (no asking, no exceptions), then handles pre/post-meeting workflows. **CRITICAL:** JIRA auto-population runs first, always, for all standups.
---

# Obsidian Standup Meeting Processor

**🔴 CRITICAL: Read this entire section before processing ANY standup meeting 🔴**

## 🚨 ABSOLUTE RULE - JIRA AUTO-POPULATION 🚨

**WHEN PROCESSING ANY STANDUP MEETING (Green or Magenta):**

```
STEP 1: Read the meeting file
STEP 2: Check if ## JIRA section is empty
STEP 3: If empty → IMMEDIATELY populate it with sprint issues (NO ASKING, NO EXCEPTIONS)
STEP 4: Then continue with appropriate workflow (pre-meeting or post-meeting)
```

**DO NOT:**
- Ask permission to populate JIRA
- Ask which mode to use
- Skip JIRA population
- Wait for explicit "pre-meeting" instruction
- Make excuses about why you can't do it

**THIS IS NON-NEGOTIABLE. THIS MUST HAPPEN AUTOMATICALLY.**

## Team Detection

Detect team from filename:
- **Green Standup** → Green Team (Board ID: 214)
- **Magenta Standup** → Magenta Team (Board ID: 331)

## Processing Modes

### Mode Detection (Automatic)

After handling JIRA population, check meeting file state:

**Pre-Meeting Mode** - Execute if ALL are true:
- JIRA section populated (just did this in Step 3 above)
- No transcript present (## Transcript section empty)
- No Copilot Summary present (## Copilot Summary empty or absent)
- No attendee screenshot (`![[SCR-*.png]]` not found)
- **→ Execute pre-meeting workflow**

**Post-Meeting Mode** - Execute if ANY are true:
- Transcript present (## Transcript has content)
- Copilot Summary present (## Copilot Summary has content)
- Attendee screenshot present (`![[SCR-*.png]]` found)
- **→ Execute post-meeting workflow**

## Pre-Meeting Workflow

**Execute ALL steps automatically:**

### 1. Populate Expected Attendees (REQUIRED)

Find 3-5 most recent meetings with same team name:
```bash
find ~/Documents/Obsidian/HPE/Meetings -name "*Green Standup*.md" -o -name "*Magenta Standup*.md" | sort -r | head -5
```

Extract unique attendees from those meetings and populate:
```markdown
## Attendees

### Expected (based on recent meetings)
- [[Last, First|First Last]]
- [[Last, First|First Last]]
```

### 2. Populate JIRA Section (Already Done)

This was already completed in Step 3 of the absolute rule above.

**Validation:**
- [ ] ## Attendees populated with expected attendees
- [ ] ## JIRA populated with current sprint items
- [ ] All links use proper Obsidian format

## Post-Meeting Workflow

**Execute ALL steps in order:**

### 1. Extract/Update Attendees

**If screenshot present** (`![[SCR-*.png]]`):
- Extract attendees from Teams screenshot
- Create missing People profiles with avatars
- Update ## Attendees section with actual participants
- Remove screenshot reference after extraction

**If no screenshot**:
- Keep expected attendees from pre-meeting (if exists)
- OR search meeting content for names and link to People profiles

### 2. Ensure JIRA Populated

JIRA section should already be populated from Step 3 of absolute rule.
If somehow missing, populate it now (should never happen).

### 3. Process Transcript (if present and no Copilot Summary)

**Check for Copilot Summary first:**
- If `## Copilot Summary` has content → Skip transcript cleanup and summary generation
- If no Copilot Summary → Clean transcript and generate summary

**Clean transcript:**
```bash
# Use the transcript cleaning script
python3 ~/.copilot/skills/obsidian-meeting-standup/scripts/clean_transcript_simple.py "meeting-file.md"
```

**Generate summary from transcript:**
- Analyze cleaned transcript for key points
- Insert structured summary in ## Notes section
- Include: Decisions, Action Items, Open Questions

### 4. Add JIRA Item Updates (if JIRA section populated)

**CRITICAL: This step runs AFTER meeting content processing (transcript/summary)**

**Objective:** Link meeting discussions to specific JIRA items by adding update comments.

**Requirements:**
- JIRA section must be populated with items grouped by user
- Meeting content must exist (Copilot Summary, Notes, or Transcript)

**Process:**
1. Extract all JIRA keys from the `## JIRA` section (e.g., GLCP-12345)
2. Search meeting content for mentions of each JIRA key in:
   - `## Copilot Summary` section
   - `## Meeting notes` section (if present)
   - `## Notes` section
   - `# Decisions` subsection
   - `# Follow-up tasks` table
3. For each JIRA item with mentions:
   - Extract relevant context about that specific JIRA item
   - Add indented comment on next line after the JIRA item
   - Format: `	- **Update (YYYY-MM-DD):** [extracted context]`
   - Use meeting date for timestamp
4. Combine related mentions into a single coherent update comment

**Format Example:**
```markdown
### [[Last, First|First Last]]
- [ ] [GLCP-12345](https://hpe.atlassian.net/browse/GLCP-12345) 📖 [In Review] - Feature implementation
	- **Update (2026-01-30):** Code review completed. Awaiting approval from Alex. Deployment planned for Monday.
- [ ] [GLCP-12346](https://hpe.atlassian.net/browse/GLCP-12346) 🐛 [Assigned] - Bug fix
```

**Extraction Guidelines:**
- Focus on actionable updates: status changes, blockers, decisions, timelines
- Include relevant names/approvers mentioned
- Combine multiple mentions into single coherent update
- Prioritize information from Decisions section and Meeting notes
- Skip generic mentions without substantive updates

**What NOT to include:**
- Vague mentions without context
- Duplicate information already in the JIRA item title
- Unrelated discussion that just mentions the key

### 5. Validation Checklist

**Verify all steps completed:**
- [ ] ## Attendees updated with actual participants (or expected if pre-meeting)
- [ ] ## JIRA populated with sprint items grouped by assignee
- [ ] ## Transcript cleaned (if present and no Copilot Summary)
- [ ] ## Notes or ## Copilot Summary contains meeting summary
- [ ] JIRA items have update comments where mentioned in meeting content
- [ ] All People profiles created for new attendees
- [ ] All links use Obsidian format: `[[Last, First|First Last]]`
- [ ] All JIRA links include URLs: `[KEY](https://hpe.atlassian.net/browse/KEY)`

## JIRA Population Implementation

### Query Commands (MANDATORY PATTERN)

```bash
# For Green Team (board 214):
SPRINT_ID=$(acli jira board list-sprints --id 214 --state active 2>&1 | grep "^│" | grep active | awk '{print $2}')
acli jira workitem search --jql "sprint = $SPRINT_ID AND status != Done AND status != Resolved ORDER BY assignee" 2>&1

# For Magenta Team (board 331):
SPRINT_ID=$(acli jira board list-sprints --id 331 --state active 2>&1 | grep "^│" | grep active | awk '{print $2}')
acli jira workitem search --jql "sprint = $SPRINT_ID AND status != Done AND status != Resolved ORDER BY assignee" 2>&1
```

**CRITICAL:** Do NOT use `acli jira sprint list-workitems` - it's incomplete. Always use `acli jira workitem search` with full JQL.

### Output Format

Group issues by assignee with **checkboxes**, **type icon**, and **status** (not bullets):

```markdown
## JIRA

### [[Last, First|First Last]]
- [ ] [GLCP-12345](https://hpe.atlassian.net/browse/GLCP-12345) 📖 [Assigned] - Issue title
- [ ] [GLCP-12346](https://hpe.atlassian.net/browse/GLCP-12346) 🐛 [In Review] - Another issue

### [[Last, First|First Last]]
- [ ] [GLCP-12347](https://hpe.atlassian.net/browse/GLCP-12347) ☑️ [In Test] - Their issue

### Unassigned
- [ ] [GLCP-12348](https://hpe.atlassian.net/browse/GLCP-12348) 📖 [New] - Unassigned work
```

**CRITICAL:** 
- Use `- [ ]` (checkbox) NOT `-` (bullet) for each JIRA item
- Include **emoji icon** for TYPE and `[STATUS]` from JIRA: `[KEY] {icon} [STATUS] - Summary`
- Type icons (from JIRA Type column):
  - **Story** → 📖
  - **Bug** → 🐛
  - **Sub-task** → ☑️
  - **Task** → 📌
  - **Epic** → 🎯
  - **Spike** → 💡
- Status comes from the Status column (Assigned, In Review, In Test, New, etc.)

### Assignee Mapping

1. Extract assignee displayName from JIRA (format: "First Last")
2. Search People profiles: `~/Documents/Obsidian/HPE/People/`
3. Find matching profile: `ls -1 *.md | grep -i "Last, First"`
4. Format as: `[[Last, First|First Last]]`
5. Fallback: If no profile found, use plain text

## Finding Meeting Files

```bash
# Today's standup
find ~/Documents/Obsidian/HPE/Meetings -name "$(date +%Y-%m-%d)*Standup*.md"

# Specific team today
find ~/Documents/Obsidian/HPE/Meetings -name "$(date +%Y-%m-%d)*Green Standup*.md"
find ~/Documents/Obsidian/HPE/Meetings -name "$(date +%Y-%m-%d)*Magenta Standup*.md"

# Specific date
find ~/Documents/Obsidian/HPE/Meetings -name "2026-01-28*Standup*.md"
```

## Common Failure Modes (AVOID THESE)

❌ **Asking for permission** to populate JIRA
❌ **Skipping JIRA** population entirely
❌ **Not detecting** standup meetings correctly
❌ **Not checking** if JIRA section is empty
❌ **Stopping halfway** through workflow

✅ **Always check** JIRA section for standups
✅ **Always populate** if empty
✅ **Never ask** for permission
✅ **Complete** all workflow steps

## Example Workflows

### Example 1: Empty Standup File (Pre-Meeting)

**Input:** "Process 2026-01-28 - Green Standup.md"

**File state:** Empty file, just template

**Actions:**
1. ✅ Read file → Detect Green Standup
2. ✅ Check JIRA section → Empty
3. ✅ Query Green Team board 214 for sprint issues
4. ✅ Populate ## JIRA with grouped issues
5. ✅ Detect pre-meeting mode (no transcript/screenshot)
6. ✅ Find recent Green Standups
7. ✅ Extract expected attendees
8. ✅ Populate ## Attendees section
9. ✅ Done

### Example 2: Standup After Meeting (Post-Meeting)

**Input:** "Process 2026-01-28 - Magenta Standup.md"

**File state:** Has transcript and screenshot

**Actions:**
1. ✅ Read file → Detect Magenta Standup
2. ✅ Check JIRA section → Empty
3. ✅ Query Magenta Team board 331 for sprint issues
4. ✅ Populate ## JIRA with grouped issues
5. ✅ Detect post-meeting mode (has transcript + screenshot)
6. ✅ Extract attendees from screenshot
7. ✅ Create missing People profiles
8. ✅ Update ## Attendees section
9. ✅ Clean ## Transcript section
10. ✅ Generate meeting summary
11. ✅ Add update comments to JIRA items mentioned in meeting
12. ✅ Done

## Success Criteria

After processing, verify:
- [ ] ## JIRA section is populated
- [ ] Issues grouped by assignee with Obsidian links
- [ ] All JIRA IDs have full URLs
- [ ] JIRA items mentioned in meeting have update comments
- [ ] ## Attendees populated (expected or actual)
- [ ] Transcript cleaned if present
- [ ] Summary generated if no Copilot Summary
- [ ] All happened WITHOUT asking user for permission

**If any criteria is false, the workflow was not completed correctly.**

## Additional Resources

- [scripts/README.md](scripts/README.md) - Transcript cleaning scripts
- [examples.md](examples.md) - Complete standup examples
- [reference.md](reference.md) - JIRA query patterns and team mappings
