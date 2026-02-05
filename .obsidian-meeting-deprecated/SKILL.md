---
name: obsidian-meeting
description: **[READ CRITICAL-CHECKLIST.md FIRST]** **AUTOMATICALLY** processes Obsidian meeting notes with intelligent pre/post-meeting detection. **Use when** user asks to "process meeting", "process obsidian meeting", "clean up transcript", "extract attendees", "summarize meeting". **CRITICAL:** When processing standup files, **FIRST CHECK AND AUTO-POPULATE JIRA SECTION IF EMPTY** (no asking, no exceptions), then execute appropriate workflow. **NO USER CONFIRMATION NEEDED** - detection and execution are fully automatic.
---

# Obsidian Meeting Attendee Processor

**🔴 BEFORE DOING ANYTHING: Read [CRITICAL-CHECKLIST.md](CRITICAL-CHECKLIST.md) 🔴**

**🤖 FULLY AUTOMATIC PROCESSING** - This skill detects meeting state and executes the complete workflow without asking for confirmation.

Extract attendees from Teams screenshots, create People profiles with aliases, update meeting notes with linked lists, clean up Microsoft Teams transcripts, and generate meeting summaries.

## 🔴 MANDATORY FIRST STEP - READ THIS BEFORE ANYTHING ELSE 🔴

**WHEN USER SAYS "PROCESS MEETING" OR "PROCESS THE OBSIDIAN MEETING":**

```
STEP 1: Read the meeting file IMMEDIATELY
STEP 2: Check if JIRA section is empty (standup meetings only)
STEP 3: If JIRA section is empty → AUTOMATICALLY populate it (no questions, no confirmation)
STEP 4: Then continue with rest of processing
```

**🚨 CRITICAL: IF STANDUP MEETING HAS EMPTY JIRA SECTION 🚨**

**YOU MUST AUTOMATICALLY:**
1. ✅ Detect team (Green=214, Magenta=331) from filename
2. ✅ Get active sprint ID for that team's board
3. ✅ Query all open sprint issues
4. ✅ Format with Obsidian links and JIRA URLs
5. ✅ Populate ## JIRA section
6. ❌ DO NOT ask for permission
7. ❌ DO NOT skip this step
8. ❌ DO NOT wait for user confirmation

**This happens BEFORE everything else. Non-negotiable. No exceptions.**

## Quick Start

**🚨 CRITICAL RULE: WHEN USER SAYS "PROCESS MEETING" 🚨**

**DO THIS IMMEDIATELY:**
1. ✅ Read the meeting file
2. ✅ Check if JIRA section is empty (for standups)
3. ✅ **AUTOMATICALLY populate JIRA if empty** (NO QUESTIONS ASKED)
4. ✅ Check if it matches pre-meeting criteria (empty transcript/attendees)
5. ✅ **AUTOMATICALLY** execute the full appropriate workflow
6. ❌ **DO NOT** ask which mode to use
7. ❌ **DO NOT** stop after partial completion
8. ❌ **DO NOT** skip any mandatory steps

**"Process the obsidian meeting"** or **"Process meeting"** = **Intelligent workflow that detects pre-meeting vs post-meeting automatically**:

**🚨 CRITICAL: AUTOMATIC MODE DETECTION 🚨**

**ALWAYS CHECK MEETING FILE STATE FIRST** - The very first action when processing any meeting is to:
1. Read the meeting file
2. **IF STANDUP WITH EMPTY JIRA SECTION → POPULATE JIRA AUTOMATICALLY (NO ASKING)**
3. Determine if it's pre-meeting or post-meeting based on detection logic below
4. **AUTOMATICALLY execute the appropriate workflow** - DO NOT ask the user which mode to use

**Detection Logic** - Check meeting file state to determine mode:

**Pre-meeting mode** - Execute automatically if ALL of these are true:
   - Meeting is a standup (filename contains "Green Standup" or "Magenta Standup")
   - JIRA section is empty (will be auto-populated first)
   - No transcript present (## Transcript section is empty or contains only whitespace)
   - No Copilot Summary present (## Copilot Summary section is empty or absent)
   - No attendee screenshot reference (no `![[SCR-*.png]]` in Attendees section)
   - **→ AUTOMATICALLY execute pre-meeting processing workflow below**

**Post-meeting mode** - Execute automatically if ANY of these are true:
   - Transcript present (## Transcript section has content)
   - Copilot Summary present (## Copilot Summary section has content)
   - Attendee screenshot present (`![[SCR-*.png]]` reference found)
   - **→ AUTOMATICALLY execute post-meeting processing workflow below**

**Pre-Meeting Processing Workflow** (Standup meetings only, when file is empty):

**🚨 EXECUTE ALL STEPS AUTOMATICALLY - DO NOT SKIP ANY STEP 🚨**

1. **Populate Expected Attendees** (REQUIRED):
   - Find 3-5 most recent meetings with same meeting name pattern
   - Extract unique attendees from those meetings
   - Populate ## Attendees section with "### Expected (based on recent meetings)" heading
   - Format as Obsidian-linked list: `- [[Last, First|First Last]]`

2. **Populate JIRA Section** (REQUIRED):
   - Detect stand-up meeting type from filename (Green or Magenta)
   - Query the team's board (Green: 214, Magenta: 331) for current active sprint
   - Get all issues in that team's sprint (team-specific filtering)
   - Group issues by status: In Progress, New, Recently Completed (Resolved/Verified)
   - Format as linked list with JIRA URLs: `- [ISSUE-KEY](https://hpe.atlassian.net/browse/ISSUE-KEY) - Summary (Assignee) - Status`
   - Populate ## JIRA section with all sprint items

**BOTH STEPS ARE MANDATORY** - Do not stop after just attendees or just JIRA. Complete the full pre-meeting workflow.

**Post-Meeting Processing Workflow** (When transcript, screenshot, or Copilot Summary exists):

**🚨 EXECUTE ALL STEPS IN ORDER - FOLLOW THE COMPLETE WORKFLOW 🚨**

1. Extract attendees from Teams screenshot (if available)
   - **If no screenshot**: Attempt known people lookup from meeting content
2. Create missing People profiles
3. Update meeting note with linked attendee list
4. **Populate JIRA section** (for Green/Magenta stand-ups only, if not already populated):
   - Detect stand-up meeting type from filename (Green or Magenta)
   - Query the team's board (Green: 214, Magenta: 331) for current sprint
   - Get all issues in that team's sprint (team-specific filtering)
   - Group issues by status: In Progress, New, Recently Completed
   - Format as linked list with JIRA URLs
5. Check for Copilot Summary section:
   - If present with content: Skip transcript cleanup and summary generation (already done by Microsoft Copilot)
   - If absent or empty: Proceed with transcript processing
6. Clean up transcript (if no Copilot Summary exists)
7. Generate meeting summary from transcript (if no Copilot Summary exists):
   - **If existing summary sections found** (e.g., `# Decisions`, `# Open questions`, `# Meeting notes`): Augment them with additional detail from transcript
   - **If no existing summary found**: Insert new structured summary in `## Notes` section

**COMPLETE ALL APPLICABLE STEPS** - Do not stop halfway through the workflow.

## ✅ Validation Checklist

**After completing pre-meeting processing, verify:**
- [ ] ## Attendees section populated with expected attendees from recent meetings
- [ ] ## JIRA section populated with current sprint items grouped by status
- [ ] All attendee links use Obsidian format: `[[Last, First|First Last]]`
- [ ] All JIRA links include full URLs: `[ISSUE-KEY](https://hpe.atlassian.net/browse/ISSUE-KEY)`

**After completing post-meeting processing, verify:**
- [ ] ## Attendees section updated with actual meeting participants (or known people if no screenshot)
- [ ] ## JIRA section populated (for standups only)
- [ ] ## Transcript section cleaned up (if no Copilot Summary)
- [ ] ## Notes or ## Copilot Summary section contains meeting summary
- [ ] All People profiles created for new attendees

**If any checklist item is incomplete, you did not finish the workflow correctly.**

---

## 🔴 EMERGENCY OVERRIDE: JIRA AUTO-POPULATION 🔴

**THIS SECTION EXISTS BECAUSE THIS HAS FAILED 10+ TIMES. READ IT CAREFULLY.**

**ABSOLUTE RULE - NO EXCEPTIONS:**

When processing ANY standup meeting (Green or Magenta):

```
1. Read the file first
2. Look at ## JIRA section
3. Is it empty or has only whitespace?
   → YES: IMMEDIATELY populate it with sprint issues
   → NO: Continue with normal processing

DO NOT:
- Ask permission to populate JIRA
- Ask which mode to use
- Skip JIRA population
- Wait for explicit "pre-meeting" instruction
- Make excuses about why you can't do it
```

**JIRA Population Command Sequence (MANDATORY):**

```bash
# For Green Team (board 214):
SPRINT_ID=$(acli jira board list-sprints --id 214 --state active 2>&1 | grep "^│" | grep active | awk '{print $2}')
acli jira workitem search --jql "sprint = $SPRINT_ID AND status != Done AND status != Resolved ORDER BY assignee" 2>&1

# For Magenta Team (board 331):
SPRINT_ID=$(acli jira board list-sprints --id 331 --state active 2>&1 | grep "^│" | grep active | awk '{print $2}')
acli jira workitem search --jql "sprint = $SPRINT_ID AND status != Done AND status != Resolved ORDER BY assignee" 2>&1
```

**Format as:**
```markdown
## JIRA

### [[Last, First|First Last]]
- [GLCP-12345](https://hpe.atlassian.net/browse/GLCP-12345) - Issue title
```

**This is NOT optional. This is NOT a suggestion. This MUST happen automatically.**

---

This is the default behavior - processing mode is determined automatically based on file state.

**"Pre-meeting processing"** or **"Populate JIRA only"** = Pre-meeting preparation (stand-ups only):
1. Detect stand-up meeting type from filename (Green or Magenta)
2. Query the team's board (Green: 214, Magenta: 331) for current sprint ID
3. Get all issues in that team's sprint backlog
4. Group issues by assignee with Obsidian profile links
5. Format as linked list with JIRA URLs
6. Populate ## JIRA section only (skip attendees, transcript, summary)

Use this mode before the meeting starts to see what work items the team will discuss.

**Meeting File Name Patterns for Pre-Meeting Processing:**
- Files named with pattern `YYYY-MM-DD - [Team] Standup.md` (e.g., `2026-01-28 - Magenta Standup.md`, `2026-01-28 - Green Standup.md`)
- Can be processed even when empty (no transcript, no attendees yet)
- Pre-meeting processing populates JIRA section in preparation for the meeting

## Capabilities

1. **Intelligent Mode Detection**: Automatically determine pre-meeting vs post-meeting processing based on file state
2. **Pre-Meeting Preparation**: Populate JIRA section before meeting starts (stand-ups only)
3. **Extract Attendees**: Process Teams screenshots to identify meeting participants
4. **Known People Lookup**: Find and link attendees mentioned in meeting content when no screenshot is available
5. **Create People Profiles**: Generate linked profiles with proper aliases
6. **Populate JIRA Sections**: Auto-populate sprint issues for Green/Magenta stand-up meetings
7. **Handle Copilot Summaries**: Recognize and preserve Microsoft Copilot-generated meeting summaries
8. **Clean Transcripts**: Format Microsoft Teams transcripts for Obsidian readability (when no Copilot Summary exists)
9. **Generate Summaries**: Analyze cleaned transcript and create structured meeting notes (when no Copilot Summary exists)
10. **Augment Existing Summaries**: Enhance pre-existing summary sections with additional detail from transcript analysis

## Additional Resources

- **[reference.md](reference.md)** - Obsidian markdown syntax reference for meeting notes
- **[reference-standup-jira.md](reference-standup-jira.md)** - JIRA section auto-population implementation guide
- **[examples.md](examples.md)** - Complete examples of formatted meeting notes
- **[scripts/README.md](scripts/README.md)** - Documentation for utility scripts

## Finding Meetings

Meeting files use format: `YYYY-MM-DD - meeting name.md` in `~/Documents/Obsidian/HPE/Meetings/`

### Find by date reference

```bash
# Today's meetings
find ~/Documents/Obsidian/HPE/Meetings -name "$(date +%Y-%m-%d)*.md"

# Specific date
find ~/Documents/Obsidian/HPE/Meetings -name "2026-01-05*.md"

# Date range (last week)
find ~/Documents/Obsidian/HPE/Meetings -name "*.md" -newermt "$(date -v-7d +%Y-%m-%d)" ! -newermt "$(date +%Y-%m-%d)"

# Date range (specific week)
find ~/Documents/Obsidian/HPE/Meetings -name "*.md" -newermt "2026-01-01" ! -newermt "2026-01-08"
```

### Find by name

```bash
# Case-insensitive search
find ~/Documents/Obsidian/HPE/Meetings -iname "*aruba*interlock*.md"
```

### Batch processing

For multiple meetings, process each sequentially, reporting progress.

## Processing Workflow

### Step 0: Detect Processing Mode (Automatic)

**Before starting any processing**, examine the meeting file to determine the appropriate mode:

```bash
# Check for standup meeting type
filename=$(basename "$meeting_file")
is_standup=false
if [[ "$filename" == *"Green Standup"* ]] || [[ "$filename" == *"Magenta Standup"* ]]; then
  is_standup=true
fi

# Check for post-meeting indicators
has_transcript=$(grep -A 5 "^## Transcript" "$meeting_file" | grep -v "^## Transcript" | grep -q "^[^#]" && echo true || echo false)
has_screenshot=$(grep -q "!\[\[SCR-.*\.png\]\]" "$meeting_file" && echo true || echo false)
has_copilot_summary=$(grep -A 5 "^## Copilot Summary" "$meeting_file" | grep -v "^## Copilot Summary" | grep -q "^[^#]" && echo true || echo false)

# Determine mode
if [ "$is_standup" = true ] && [ "$has_transcript" = false ] && [ "$has_screenshot" = false ] && [ "$has_copilot_summary" = false ]; then
  mode="pre-meeting"
  echo "Detected: Pre-meeting mode (empty standup file) - will populate JIRA section only"
else
  mode="post-meeting"
  echo "Detected: Post-meeting mode - will run full workflow"
fi
```

**Pre-Meeting Mode**: Jump to "Step 4a: Populate JIRA Section (Stand-ups Only)" and exit
**Post-Meeting Mode**: Continue with Step 1 below

### Step 1: Extract Attendees from Image (When Available)

1. Locate image reference: `![[SCR-YYYYMMDD-xxxxx.png]]` (in "Notable Attendees" section)
2. View image from `~/Documents/Obsidian/HPE/Media/`
3. Extract names in "Last, First" format:
   - **In Meeting**: Present attendees (green checkmarks in image)
   - **Invited/Other**: Invited/declined/mentioned in transcript

### Step 1 (Alternative): Known People Lookup (No Screenshot)

When no attendee screenshot is available, search for people mentioned in the meeting content:

1. **Extract potential names** from meeting sections:
   ```bash
   # Scan Copilot Summary and Notes for first names
   grep -oE "\b[A-Z][a-z]+\b" "meeting-file.md" | sort -u
   ```

2. **Search People profiles** for matches:
   ```bash
   cd ~/Documents/Obsidian/HPE/People
   # For each potential name (e.g., Yogesh, Kyu, Darra)
   ls -1 *.md | grep -iE "(Yogesh|Kyu|Darra)"
   ```

3. **Verify matches** by checking aliases:
   ```bash
   # Example: Check if "Kumar, Yogesh.md" has alias "Yogesh Kumar"
   for file in "Kumar, Yogesh.md" "Oh, Kyu.md"; do
     head -7 "$file" | grep "aliases:" -A 1
   done
   ```

4. **Build attendee list** from verified matches (see Step 4b for format)

### Step 2: Extract Avatar Images

Extract individual avatar images from the screenshot for each attendee:

1. Get image dimensions: `sips -g pixelWidth -g pixelHeight SCR-YYYYMMDD-xxxxx.png`
2. Extract each avatar using sips crop (avatars are typically ~40x40 pixels):
   ```bash
   # Example for first attendee
   sips -c 40 40 --cropOffset Y_OFFSET X_OFFSET SCR-YYYYMMDD-xxxxx.png \
     --out Last-First-avatar.png
   ```
3. Typical layout in Teams screenshots:
   - Avatars are on the left side (~16 pixels from left edge)
   - Spaced vertically (typically ~52-54 pixels between avatars)
   - First avatar starts around y=12-20 pixels from top
4. Save avatars with naming convention: `{Last}-{First}-avatar.png` in Media folder

**Example extraction commands:**
```bash
cd ~/Documents/Obsidian/HPE/Media

# First attendee (top of list)
sips -c 40 40 --cropOffset 12 12 SCR-20260113-jshz.png \
  --out Tronkowski-Kevin-avatar.png

# Second attendee (~54 pixels down)
sips -c 40 40 --cropOffset 66 12 SCR-20260113-jshz.png \
  --out De-Anirban-avatar.png

# Third attendee (~54 pixels down)
sips -c 40 40 --cropOffset 120 12 SCR-20260113-jshz.png \
  --out Holden-Edward-avatar.png
```

### Step 3: Create People Profiles with Avatars

Check `~/Documents/Obsidian/HPE/People/{Last}, {First}.md` - create if missing:

```markdown
---
aliases:
  - {First} {Last}
tags:
  - People
---
![[{Last}-{First}-avatar.png]]
```

**Important**: Only add avatar if the profile doesn't already have one. Check for existing `![[` image reference in the file first.

Example: `Pahwa, Kashish.md` → alias "Kashish Pahwa" + avatar image

### Step 4: Update Meeting Note

Replace image reference with attendee list using link format `[[{Last}, {First}|{First} {Last}]]`:

```markdown
# Attendees

## In Meeting (5)
- [[Tronkowski, Kevin|Kevin Tronkowski]]
- [[Pahwa, Kashish|Kashish Pahwa]]

## Invited/Other Participants (3)
- [[Luna, Gabriella|Gabriella Luna]]
```

**Important**: Remove the `![[SCR-YYYYMMDD-xxxxx.png]]` image reference after extracting attendees.

### Step 4b: Known People Lookup (No Screenshot Available)

When a meeting has no attendee screenshot but mentions people in the Copilot Summary or meeting notes, automatically find and link them:

1. **Extract names** from content sections:
   - Scan `## Copilot Summary` section
   - Scan `## Notes` section  
   - Scan `# Meeting notes` subsection
   - Look for first names mentioned in content (e.g., "Yogesh", "Kyu", "Darra")

2. **Search People profiles** for matches:
   ```bash
   cd ~/Documents/Obsidian/HPE/People
   # Search for each name found
   ls -1 *.md | grep -i "{FirstName}"
   ```

3. **Build attendee list** from matches:
   - Use the "Last, First" filename format for canonical names
   - Check the alias field to get "First Last" display format
   - Count the matches

4. **Update meeting note** with discovered attendees:
   ```markdown
   ## Attendees
   
   ## In Meeting (4)
   - [[Kumar, Yogesh|Yogesh Kumar]]
   - [[Oh, Kyu|Kyu Oh]]
   - [[Zhou, Shikuang|Shikuang Zhou]]
   - [[Ricks, Darra|Darra Ricks]]
   ```

**When to use:**
- Meeting has empty `## Attendees` section (no screenshot was available)
- Copilot Summary or Notes sections mention team members by first name
- User explicitly requests: "find the people from obsidian people and list them"

**Example workflow:**
```bash
# 1. Find names mentioned in meeting content
grep -oE "\b[A-Z][a-z]+\b" meeting-file.md | sort -u

# 2. Search for matching profiles (first names)
cd ~/Documents/Obsidian/HPE/People
for name in Yogesh Kyu Shikuang Darra; do
  ls -1 *.md | grep -i "$name"
done

# 3. Verify matches and extract aliases
for file in "Kumar, Yogesh.md" "Oh, Kyu.md"; do
  grep "^  - " "$file" | head -1  # Get alias
done

# 4. Update meeting note with linked list
```

## Directory Structure

```
~/Documents/Obsidian/HPE/
├── Meetings/YYYY-MM-DD - name.md
├── People/{Last}, {First}.md
└── Media/SCR-YYYYMMDD-xxxxx.png
```

## JIRA Section Auto-Population (Stand-ups)

### When to Use

Automatically populate the `## JIRA` section when processing **Green Standup** or **Magenta Standup** meetings.

This can be done:
- **Pre-meeting**: Before the meeting starts (even with empty meeting file)
- **During full processing**: As part of the complete meeting workflow

### Detection Logic

The skill detects stand-up meetings by checking the meeting filename:
- **Green Standup**: `*Green Standup*` → Maps to Green Team (Board ID: 214)
- **Magenta Standup**: `*Magenta Standup*` → Maps to Magenta Team (Board ID: 317)

Files matching this pattern can be processed for JIRA population even when:
- No transcript exists yet
- No attendee information available
- File only contains the empty template structure

### Query Approach

Uses the **acli jira** command to query open issues in the current sprint:

**Step 1: Get active sprint ID**
```bash
# For Green Team (board 214)
SPRINT_ID=$(acli jira board list-sprints --id 214 --state active 2>&1 | grep "^│" | grep active | awk '{print $2}')

# For Magenta Team (board 331)
SPRINT_ID=$(acli jira board list-sprints --id 331 --state active 2>&1 | grep "^│" | grep active | awk '{print $2}')
```

**Step 2: Query all open items in the sprint**
```bash
# This query gets ALL open items (not Done/Resolved) and orders by assignee
acli jira workitem search --jql "sprint = $SPRINT_ID AND status != Done AND status != Resolved ORDER BY assignee" 2>&1
```

**CRITICAL:** Do NOT use `acli jira sprint list-workitems` with a `--jql` parameter, as it does not return all open items correctly. Always use `acli jira workitem search` with the full JQL query including the sprint ID.

### Output Format

Group issues by assignee, with each assignee as a subsection:

```markdown
## JIRA

### [[Tronkowski, Kevin|Kevin Tronkowski]]
- [GLCP-313119](https://hpe.atlassian.net/browse/GLCP-313119) - Add deployment configuration
- [GLCP-313120](https://hpe.atlassian.net/browse/GLCP-313120) - Fix authentication bug

### [[Smith, Jane|Jane Smith]]
- [GLCP-313121](https://hpe.atlassian.net/browse/GLCP-313121) - Update API documentation

### Unassigned
- [GLCP-313122](https://hpe.atlassian.net/browse/GLCP-313122) - Investigation spike
```

### Assignee Mapping

1. **Extract assignee displayName** from JIRA response (format: "First Last")
2. **Search People profiles** in `~/Documents/Obsidian/HPE/People/`:
   ```bash
   # Search for profile matching display name
   ls -1 ~/Documents/Obsidian/HPE/People/*.md | grep -i "Last, First"
   ```
3. **Format as Obsidian link**: `[[Last, First|First Last]]`
4. **Fallback**: If no profile found, use plain text: `First Last` (no link)

### Edge Cases

- **Unassigned issues**: Group under `### Unassigned` heading
- **No People profile**: Use plain display name without link
- **No open issues**: Display message: `No open issues in current sprint`

### Example Workflow

```bash
# 1. Detect stand-up type
filename="2026-01-28 - Green Standup.md"
if [[ $filename == *"Green Standup"* ]]; then
  team="Green"
  board_id=214
fi

# 2. Query JIRA (using Atlassian MCP tools)
# Use Atlassian-searchJiraIssuesUsingJql

# 3. Group issues by assignee
# Sort and organize results

# 4. Map assignees to People profiles
cd ~/Documents/Obsidian/HPE/People
for assignee in "${assignees[@]}"; do
  # Search for matching profile
  profile=$(ls -1 *.md | grep -i "$assignee")
done

# 5. Format and insert into ## JIRA section
```

## Common Patterns

**"Process the obsidian meeting"** or **"Process meeting"**
- **Intelligently detects** pre-meeting vs post-meeting mode based on file state
- **Pre-meeting** (empty standup file): Populates JIRA section only
- **Post-meeting** (has transcript/screenshot/Copilot Summary): Full workflow (attendees + profiles + JIRA + transcript)
- Finds most recent meeting or prompts for clarification
- If no screenshot: Attempts known people lookup from content
- **For stand-ups**: Auto-populates JIRA section with current sprint issues
- Example: "Process the obsidian meeting" → detects mode and processes accordingly

**"Process the Green Standup"** or **"Process the Magenta Standup"**
1. Find: `find ~/Documents/Obsidian/HPE/Meetings -name "YYYY-MM-DD*Green Standup*.md"`
2. **Automatic mode detection**:
   - If file is empty (no transcript/screenshot): Pre-meeting mode (JIRA only)
   - If file has content: Post-meeting mode (full workflow)
3. **Pre-meeting** (empty file):
   - Populate JIRA section with current sprint open issues for the team
   - Group by assignee with Obsidian profile links
   - Format JIRA IDs as clickable links
4. **Post-meeting** (has content):
   - Extract attendees (if screenshot available)
   - Populate JIRA section (if not already done)
   - Process transcript (if available)
5. Example output in JIRA section:
   ```markdown
   ## JIRA
   
   ### [[Tronkowski, Kevin|Kevin Tronkowski]]
   - [GLCP-313119](https://hpe.atlassian.net/browse/GLCP-313119) - Story title
   ```

**"Find the people from obsidian people and list them"**
- When no attendee screenshot is available
- Extracts first names from Copilot Summary or meeting notes
- Searches People profiles for matches
- Updates attendee list with found profiles
- Example: Meeting mentions "Yogesh", "Kyu", "Darra" → finds and links their profiles

**"Process the meeting with transcript from ~/Downloads/Meeting.docx"**
1. Convert .docx to text: `textutil -convert txt ~/Downloads/Meeting.docx -output ~/tmp/transcript.txt`
2. Add transcript to meeting file's `## Transcript` section
3. Run full workflow (extract attendees, create profiles, clean transcript, generate summary)
4. Use Format 3 cleaner (`clean_transcript_docx.py`) for plain text format

**"Process today's aruba meeting"**
1. Find: `find ~/Documents/Obsidian/HPE/Meetings -name "$(date +%Y-%m-%d)*aruba*.md"`
2. Extract attendees from image
3. Create missing People profiles
4. Update meeting note
5. Clean up transcript

**"Process all meetings from last week"**
1. Find: `find ~/Documents/Obsidian/HPE/Meetings -name "*.md" -newermt "$(date -v-7d +%Y-%m-%d)"`
2. Process each meeting sequentially (full workflow)
3. Report: "Processed 5 meetings, created 12 new profiles, cleaned 5 transcripts"

**"Process the 2026-01-05 aruba interlock meeting"**
1. Find: `find ~/Documents/Obsidian/HPE/Meetings -name "2026-01-05*aruba*.md"`
2. Single meeting - full workflow

**"Just clean up the transcript"** (specific step only)
1. Skip attendee processing
2. Only clean transcript section

**"Pre-meeting processing for 2026-01-28 Green Standup"** or **"Populate JIRA only"** (stand-ups only)
1. Detect Green Standup meeting type (from filename pattern `*Green Standup*` or `*Magenta Standup*`)
2. Query open issues in Green Team's current sprint
3. Group issues by assignee
4. Map assignees to Obsidian People profiles
5. Format and populate `## JIRA` section
6. Skip attendee extraction, transcript, and summary
7. Works with empty meeting files (pre-meeting) or existing files

**"Process the 2026-01-28 Green Standup"** (after meeting with transcript)
1. Pre-meeting: Populate JIRA section (if empty)
2. Extract attendees from screenshot
3. Create missing People profiles
4. Clean transcript
5. Generate summary

## Important Rules

- Always check existing profiles before creating
- Preserve existing profile content when found
- Use exact format: filename `{Last}, {First}.md`, alias `{First} {Last}`
- Include counts in section headers: `## In Meeting (5)`
- Process meetings in date order when batch processing
- **For stand-ups (Green/Magenta)**: Auto-populate `## JIRA` section with current sprint open issues
- **JIRA format**: Group by assignee, use Obsidian profile links, include full JIRA URLs
- **Check for `## Copilot Summary` section** - if present with content, skip transcript cleanup and summary generation
- Preserve Copilot-generated summaries (already formatted by Microsoft Copilot)
- Only generate summaries from transcripts when no Copilot Summary exists

---

## Copilot Summary Section

The "Copilot Summary" section contains meeting summaries generated by Microsoft Copilot during Teams meetings. This is a pre-generated summary that appears when the meeting organizer or participant used Microsoft Copilot's meeting recap feature.

### Copilot Summary Characteristics

- Section header: `## Copilot Summary`
- Contains structured subsections: `# Decisions`, `# Open question`, `# Agenda`, `# Meeting notes`, `# Follow-up tasks`
- Already formatted and cleaned (no transcript cleanup needed)
- Often present WITHOUT a transcript (since Copilot generates summary directly from meeting audio)

### Processing Copilot Summary

When a "Copilot Summary" section is detected:

1. **Treat it as an existing summary** - Do NOT generate a new summary from transcript
2. **Keep all Copilot-generated content intact** - It's already well-formatted
3. **Extract attendees normally** from the screenshot in "Attendees" section
4. **Skip transcript cleanup** - If there's no transcript, skip this step entirely
5. **Optionally augment** - Only add additional details if a transcript is ALSO present

### Example Meeting with Copilot Summary

```markdown
## Attendees

![[SCR-20260120-kbwa.png]]

## Copilot Summary
# Decisions

- Cancel the sprint review meeting due to lack of demoable items.
- Communicate to Will and others that there is no intent to push to production.

# Open question

- Clarify tracking and visibility for unaccounted-for stories and technical debt.

# Meeting notes

### Project status updates

- Drew explained that the current story will not be completed today due to required rework.

## Transcript

[Empty or omitted when Copilot Summary is present]
```

### Detection Logic

```bash
# Check if meeting has Copilot Summary
grep -q "## Copilot Summary" "meeting-file.md"

# If found:
# - Process attendees as normal
# - Skip transcript cleanup (or only clean if transcript is present)
# - Do NOT generate new summary (Copilot Summary is sufficient)
```

## Transcript Cleanup

Clean up Microsoft Teams transcripts by removing profile pictures, metadata, and formatting for Obsidian readability.

**Note**: If a `## Copilot Summary` section exists, transcript cleanup is typically not needed since the meeting likely has no transcript.

### Transcript Formats

Meeting transcripts can come from multiple sources with different formatting:

#### Format 1: Direct Paste from Teams (Original Format)
**Source**: Copy-paste directly from Teams meeting transcript view

**Characteristics**:
- Speaker names on their own line: `Last, First`
- Timestamp line with verbose format: `0 minutes 3 seconds0:03`
- Duplicate speaker+timestamp line: `Last, First 0 minutes 3 seconds`
- Profile image URLs on separate lines
- Metadata and navigation text
- Separator lines `____`

**Example:**
```markdown
## Transcript

____

![](https://nam.loki.delve.office.com/api/v2/personaphoto?AadObjectId=...)

Luna, Gabriella

0 minutes 8 seconds0:08

Luna, Gabriella 0 minutes 8 seconds

No worries. Um, so I know we want to touch base on.
```

**Script**: `clean_transcript.py` (existing)

#### Format 2: Downloaded/Exported from Teams (New Format)
**Source**: Downloaded VTT file converted to text, or exported from Teams

**Characteristics**:
- Combined speaker and timestamp on one line: `**Bennett, Ryan**   0:03`
- Embedded image references before each speaker: `![](file:////Users/kevin/Library/Group%20Containers/...)`
- Meeting header info (title, date, duration)
- No separator lines
- Content follows immediately after speaker line

**Example:**
```markdown
## Transcript

**Green and Magenta Design Discussion-20260113_133528-Meeting Recording**

January 13, 2026, 6:35PM

1h 16m 5s

![](file:////Users/kevin/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image002.jpg)**Bennett, Ryan** started transcription

![](file:////Users/kevin/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image004.jpg)**Bennett, Ryan**   0:03  
Yeah, well, the recording has begun.  
Recording has begun.

![](file:////Users/kevin/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image006.jpg)**Tronkowski, Kevin**   0:08  
Alright, let's look at those pages.
```

**Script**: `clean_transcript_downloaded.py` (new - for downloaded format)

#### Format 3: Plain Text from .docx Export (Converted Format)
**Source**: Teams transcript exported to .docx, then converted to plain text via `textutil` or similar

**Characteristics**:
- Plain text format (NO bold markdown): ` Last, First   timestamp content`
- Leading space before speaker name
- Meeting header info (title, date, duration) at top
- No image references (stripped during conversion)
- Content on same line as speaker and timestamp
- May have "started/stopped transcription" markers

**Example:**
```markdown
## Transcript

Forecasting Sync-20260114_210016UTC-Meeting Recording
January 14, 2026, 9:00PM
27m 18s
 Willmschen, Royce   0:09 Thank you.
 Oh, Kyu   0:12 Erase.
    0:43 Hello.
 Tronkowski, Kevin   1:03 OK.
 Willmschen, Royce stopped transcription
```

**Script**: `clean_transcript_docx.py` (new - for .docx converted format)

#### Format 4: Google Recorder (Bracket Format)
**Source**: Transcript generated from Google Recorder app

**Characteristics**:
- Speaker names in brackets: `[First Last]`
- No timestamps (Google Recorder doesn't provide precise timestamps)
- Content follows immediately after speaker line or on next lines
- No image references or metadata
- Simple, clean format but needs speaker linking

**Example:**
```markdown
## Transcript

[Stella Yun]
And.

[Kevin Tronkowski]
Started feeling. Better. Again, not perfect, but better.

[Stella Yun]
Good good? All right, I have. I'm gonna all the potential project. That we can take home.

[Kevin Tronkowski]
Okay,
```

**Processing approach**: Use `clean_transcript_google_recorder.py` script
- Pattern: `\[(.*?)\]` to extract speaker names
- Convert "First Last" to "[[Last, First|First Last]]" format using attendee mapping
- No timestamps to extract or format
- Combine multi-line content for same speaker into paragraphs

**Script**: `clean_transcript_google_recorder.py` (for Google Recorder format)

**Example cleaned output:**
```markdown
## Transcript

**[[Yun, Stella|Stella Yun]]**

And.

**[[Tronkowski, Kevin|Kevin Tronkowski]]**

Started feeling. Better. Again, not perfect, but better.

**[[Yun, Stella|Stella Yun]]**

Good good? All right, I have. I'm gonna all the potential project. That we can take home.
```

### When to Use

- User requests "clean up transcript", "process transcript", or "format transcript"
- Meeting note contains raw Teams transcript with image URLs and metadata
- After processing attendees, offer to clean transcript

### Transcript Cleanup Workflow

**Auto-detect format and use appropriate script:**

```bash
# For Format 1 (direct paste from Teams)
python ~/.copilot/skills/obsidian-meeting/scripts/clean_transcript.py "meeting-file.md"

# For Format 2 (downloaded/exported)
python ~/.copilot/skills/obsidian-meeting/scripts/clean_transcript_downloaded.py "meeting-file.md"

# For Format 3 (.docx converted to text)
python ~/.copilot/skills/obsidian-meeting/scripts/clean_transcript_docx.py "meeting-file.md"

# For Format 4 (Google Recorder - bracket format)
python ~/.copilot/skills/obsidian-meeting/scripts/clean_transcript_google_recorder.py "meeting-file.md"
```

**Detection logic:**
1. Check for pattern `\[.*?\]` (brackets with names) → Format 4 (Google Recorder)
2. Check for pattern `**Last, First**   timestamp` → Format 2 (downloaded with markdown bold)
3. Check for pattern ` Last, First   timestamp content` (leading space, no bold) → Format 3 (.docx converted)
4. Check for pattern `Last, First` on own line + timestamp on next line → Format 1 (direct paste)
5. If unsure, try Format 4 first, then Format 2, then Format 3, then Format 1

The script automatically:
1. Extracts the transcript section
2. Parses speakers, timestamps, and content
3. Removes all metadata, images, and unwanted formatting
4. Replaces the transcript with clean formatted output
5. Removes separator lines (`____`)

**What the script does:**
- Reads attendee list to build speaker name mapping
- Parses raw Teams transcript block-by-block
- Extracts clean timestamps from complex format (e.g., "0 minutes 3 seconds0:03" → "0:03")
- Skips all unwanted content (images, metadata, duplicates, separators)
- Formats as: `**[[Last, First|First Last]]** timestamp` + content
- Writes back to original file

**Example usage:**
```bash
# Process single meeting
python ~/.copilot/skills/obsidian-meeting/scripts/clean_transcript.py \
  ~/Documents/Obsidian/HPE/Meetings/2026-01-08\ -\ SIC-PCE\ Syncup.md

# Output:
# ✓ Cleaned transcript: 15 entries formatted
#   - Will Colton at 0:03
#   - Kashish Pahwa at 2:51
#   - Will Colton at 2:54
#   ... and 12 more
```

### Transcript Format Rules

- **Speaker format**: `**[[Last, First|First Last]]** timestamp`
- **Timestamp format**: Keep original clean timestamp (e.g., `0:03`, `2:26`, `28:56`)
- **Paragraph breaks**: Blank line between speakers
- **Multi-paragraph speeches**: Blank line between paragraphs from same speaker at same timestamp
- **Section header**: Use `## Transcript` (not `# Transcript`)
- **No separators**: Remove all `____` lines
- **No images**: Remove all profile picture URLs and attendee screenshot references

### Items to Remove from Raw Transcript

- Profile picture image URLs (`![](https://nam.loki.delve.office.com/api/v2/personaphoto?...`)
- Navigation text ("Transcript. Use arrow keys to navigate...")
- Metadata lines ("AI-generated content may be incorrect")
- "started transcription" / "stopped transcription" markers
- Duplicate timestamp labels (e.g., "0 minutes 3 seconds0:03")
- Duplicate "Speaker timestamp" lines (e.g., "Luna, Gabriella 0 minutes 8 seconds")
- Speaker initials without context (e.g., "PK", "SM")
- Separator lines (`____`)
- Empty blocks

### Example: Before and After

**Before (Raw Teams):**
```markdown
## Transcript

____

Transcript. Use arrow keys...

AI-generated content may be incorrect

![](https://nam.loki.delve.office.com/api/v2/personaphoto?AadObjectId=...)

Luna, Gabriella

0 minutes 8 seconds0:08

Luna, Gabriella 0 minutes 8 seconds

No worries. Um, so I know we want to touch base on.

![](https://nam.loki.delve.office.com/api/v2/personaphoto?AadObjectId=...)

Colton, Will

0 minutes 19 seconds0:19

Colton, Will 0 minutes 19 seconds

And had some things they want it cleaned up.
```

**After (Cleaned):**
```markdown
## Transcript

**[[Luna, Gabriella|Gabriella Luna]]** 0:08

No worries. Um, so I know we want to touch base on.

**[[Colton, Will|Will Colton]]** 0:19

And had some things they want it cleaned up.
```

### Processing Combined Workflow

**Default behavior** when user says "process meeting" or "process the obsidian meeting":

**Step 0: Automatic Mode Detection**
1. Check if meeting is a standup (filename contains "Green Standup" or "Magenta Standup")
2. Check for post-meeting indicators:
   - Transcript content in `## Transcript` section
   - Screenshot reference `![[SCR-*.png]]` in Attendees section
   - Content in `## Copilot Summary` section
3. **Determine mode**:
   - **Pre-meeting**: Standup file with no transcript, screenshot, or Copilot Summary → Populate JIRA only (skip to step 10)
   - **Post-meeting**: Any transcript, screenshot, or Copilot Summary present → Full workflow (continue below)

**Steps 1-9: Post-Meeting Processing** (only when post-meeting mode detected)
1. Extract and process attendees from screenshot (if available)
2. **Extract individual avatar images** from screenshot for each attendee
3. Create missing People profiles with avatars (only add if not already present)
4. Update meeting note with attendee list
5. **Remove attendee screenshot** reference from meeting note
6. **Populate JIRA section** (for Green/Magenta stand-ups, if not already populated - jump to step 10)
7. **Check for Copilot Summary section**:
   - If `## Copilot Summary` exists with content, skip transcript cleanup and summary generation (Copilot Summary is already present)
   - If `## Copilot Summary` is empty or absent, proceed with transcript processing
8. **Run transcript cleaner script** (if no Copilot Summary and transcript exists): `python ~/.copilot/skills/obsidian-meeting/scripts/clean_transcript.py "meeting-file.md"`
9. **Generate meeting summary from cleaned transcript** (if no Copilot Summary):
   - **Check for existing summary sections** (`# Decisions`, `# Open questions`, `# Agenda`, `# Meeting notes`, etc.)
   - **If found**: Augment existing sections with additional detail, add new subsections as needed
   - **If not found**: Insert new structured summary in `# Notes` section

**Step 10: JIRA Population** (for stand-ups only, referenced from steps above)
- See "Step 4a: Populate JIRA Section (Stand-ups Only)" below for detailed implementation

**Individual steps** only performed when specifically requested:
- "Just extract attendees" → skip transcript cleanup and summary
- "Just clean up the transcript" → only run transcript cleaner script
- "Just summarize the meeting" → only generate summary from existing transcript
- "Augment the meeting summary" → enhance existing summary sections with transcript analysis
- "Create people profiles" → only profile creation

**Expected Results:**
- Attendee list with linked profiles and counts
- Individual avatar images extracted for each attendee (saved as `{Last}-{First}-avatar.png`)
- People profiles updated with avatars (only if they don't already have one)
- **If Copilot Summary present**: Preserved as-is (no transcript cleanup or summary generation)
- **If no Copilot Summary**: Clean, formatted transcript with speaker links and timestamps
- **If no Copilot Summary**: Comprehensive meeting summary (either new or augmented)
- No image references (attendee screenshots or speaker profile images)
- No temporary files (script cleans up automatically)
- All existing summary content preserved when augmenting

Use the full workflow by default unless the user explicitly requests a single step.

---

## Meeting Summary Generation

When a transcript is present, automatically generate a summary and insert/augment it in the Notes section.

**Note**: If a `## Copilot Summary` section exists with content, skip summary generation entirely. The Copilot Summary is already a high-quality, structured summary generated by Microsoft Copilot during the meeting.

### Summary Workflow

1. **Check for Copilot Summary first**:
   - If `## Copilot Summary` section exists with content (e.g., `# Decisions`, `# Meeting notes`), treat it as the meeting summary
   - Skip transcript cleanup and summary generation
   - Proceed only with attendee processing
2. **If no Copilot Summary**, proceed with transcript-based summary:
   - Read cleaned transcript (after cleanup step completes)
   - **Analyze content** to identify:
     - Meeting purpose/topic
     - Key discussion points and decisions
     - Technical details and requirements
     - Action items and follow-ups
     - Important context or background
   - **Check for existing summary content**:
     - Look for existing sections: `# Decisions`, `# Open questions`, `# Agenda`, `# Meeting notes`, `# Notes`, `# Take Aways`, `# Actions`
     - Identify which sections already exist and contain content
   - **Generate structured summary** in markdown format
   - **Augment or insert** based on existing content (see Augmentation Strategy below)
   - Meeting purpose/topic
   - Key discussion points and decisions
   - Technical details and requirements
   - Action items and follow-ups
   - Important context or background
3. **Check for existing summary content**:
   - Look for existing sections: `# Decisions`, `# Open questions`, `# Agenda`, `# Meeting notes`, `# Notes`, `# Take Aways`, `# Actions`
   - Identify which sections already exist and contain content
4. **Generate structured summary** in markdown format
5. **Augment or insert** based on existing content (see Augmentation Strategy below)

### Augmentation Strategy: Handling Existing Summaries

**Detection**: Check if any of these sections already exist with content:
- `# Decisions`
- `# Open questions`  
- `# Agenda`
- `# Meeting notes` (with subsections like `### Meeting tools and automation`)
- `# Notes` (with content beyond templates)
- `# Take Aways`
- `# Actions`

**When existing summary sections are found:**

1. **Keep all existing sections intact** - Do not replace or remove them
2. **Analyze existing content** to understand what's already covered
3. **Generate supplementary content** from the transcript that:
   - Adds detail to existing bullet points
   - Identifies topics not yet covered in existing sections
   - Extracts additional decisions, questions, or action items
4. **Augment each existing section** by:
   - Adding new items discovered from transcript analysis
   - Expanding brief items with additional context from transcript
   - Preserving all original content (never remove existing items)
5. **Fill in template sections** if they exist but are empty (e.g., `# Subject`, `# Take Aways`, `# Actions`)

**When NO existing summary sections are found:**

Insert a new structured summary in the `# Notes` section (standard workflow):

```markdown
# Notable Attendees

## In Meeting (5)
- [[Tronkowski, Kevin|Kevin Tronkowski]]
...

# Subject
- 

# Notes

## Meeting Purpose
[Generated summary content starts here]

## Key Discussion Points
...

## Media
-
```

### Augmentation Example

**Before augmentation:**
```markdown
# Decisions

- Enable facilitator agent for meeting recording.
- Merge secret scanning feature.

# Open questions

- Agreement needed on CXL cluster usage.

# Meeting notes

### Security automation

- Will confirmed changes were implemented.
```

**After augmentation (from transcript analysis):**
```markdown
# Decisions

- Enable facilitator agent for meeting recording and automated notes.
- Merge secret scanning feature and use Copilot for repo integration.
- Create separate story for secret scanning in all repos.
- Test agent-side work and coordinate for further development.
- Submit I18N header PR and hold review until implementation is ready.

# Open questions

- Agreement needed on CXL cluster usage for forecasting.
- Resolve ML pipeline build failures due to runner disk space.
- Investigate separating user input from prompts to pass Amazon guardrails.
- Analyze prompt aspects that trigger Amazon guardrails.

# Meeting notes

### Security automation

- Will confirmed that the changes based on Ryan's feedback have been implemented and successfully tested, and the secret scanning job received final approval from Kevin.

### Forecasting updates

- Kyu relayed the forecasting update to the green and magenta teams and noted ongoing discussions about using the CXL cluster
- Kyu reported that the ML forecasting PR checks are failing due to build space issues, and Thomas is working on adjustments to resolve this
```

**Note**: Items are added or enhanced, never removed. Original content is preserved.

### Summary Format Template

**For meetings WITHOUT existing summaries:**

```markdown
# Notes

## Meeting Purpose
[Brief 1-2 sentence overview of meeting topic]

## Key Discussion Points

### [Topic Area 1]
- **Current state**: [What exists now]
- **Requirements**: [What's needed]
- **Proposed solution**: [Approach discussed]
- **Status**: [Current progress/decisions]

### [Topic Area 2]
[Repeat structure for additional topics]

### [Team/Participant Context]
- Key stakeholders and their roles
- Relevant organizational information

### Follow-up Plans
- Action items with owners
- Timeline commitments
- Dependencies or blockers noted

### Additional Context
- Travel issues or attendance notes
- Related discussions or background
```

**For meetings WITH existing summaries (augmentation mode):**

Preserve existing section structure and add/enhance content within those sections:

```markdown
# Decisions
[Existing items kept as-is]
[New decisions extracted from transcript added below]

# Open questions
[Existing questions kept as-is]
[New questions from transcript added below]

# Agenda
[Usually kept as-is since it's pre-meeting]

# Meeting notes
[Existing subsections kept as-is]
[Enhance with additional detail from transcript]
[Add new subsections for topics not yet covered]

# Subject
[Fill in if empty, otherwise keep existing]

# Take Aways
[Fill in if empty or augment with key learnings from transcript]

# Actions
[Keep existing, add action items discovered in transcript]
```

### Summary Guidelines

- **Detect existing content**: Always check for pre-existing summary sections before generating
- **Augment, don't replace**: When existing sections are found, add to them rather than replacing
- **Be comprehensive**: Capture all significant discussion points from the transcript
- **Use bullet points**: Easy to scan and reference
- **Include specifics**: Names, systems, requirements, timelines
- **Maintain structure**: Use consistent heading hierarchy matching existing format
- **Preserve technical details**: System names, technologies, requirements
- **Note action items**: Who, what, when
- **Keep context**: Background information that adds understanding
- **Match existing style**: If existing summaries use a certain bullet format or structure, maintain consistency

### Example Summary Structure

Based on actual meeting (OpsRamp Collector - 2026-01-05):

```markdown
# Notes

## Meeting Purpose
Discussion about using OpsRamp Collector for SIC (Sustainability Insight Center) to collect power consumption data from non-centrally managed Aruba devices.

## Key Discussion Points

### OpsRamp Collector for SIC
- **Current state**: SIC already supports Aruba devices through Aruba Central
- **New requirement**: Need to support Aruba devices NOT managed by Aruba Central
- **Proposed solution**: Use OpsRamp Collector as lightweight solution
- **Status**: Very early stage - need POC to validate feasibility

### SIC Engineering Context
- Royce Willmschen: Engineering Manager for SIC
- Active roadmap item for non-central managed Aruba device support

### Follow-up Plans
- Schedule follow-up meeting in early February to review POC results
- Royce and Kevin (SIC team) to work on POC
```
