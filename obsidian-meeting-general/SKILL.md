---
name: obsidian-meeting-general
description: Process general (non-standup) Obsidian meeting notes. **Use when** router delegates non-standup meeting processing. Handles attendee extraction from screenshots, People profile creation, transcript cleaning (4 format variants), Microsoft Copilot Summary detection, and meeting summary generation.
---

# Obsidian General Meeting Processor

Process regular meeting notes (non-standup meetings) with attendee extraction, transcript cleanup, and summary generation.

## Capabilities

1. **Attendee Extraction** - Process Teams screenshots to identify participants
2. **People Profile Creation** - Generate linked profiles with avatars and aliases
3. **Known People Lookup** - Find attendees mentioned in content when no screenshot available
4. **Transcript Cleaning** - Handle 4 different Teams transcript formats
5. **Copilot Summary Detection** - Recognize and preserve Microsoft Copilot summaries
6. **Summary Generation** - Create structured meeting notes from transcripts
7. **Summary Augmentation** - Enhance existing summaries with transcript details

## Processing Workflow

### Step 1: Extract Attendees

**Option A: From Screenshot (Preferred)**

If meeting has attendee screenshot reference (`![[SCR-*.png]]`):

1. View image from `~/Documents/Obsidian/HPE/Media/`
2. Extract names in "Last, First" format
3. Extract individual avatars (40x40 pixels) using sips:
   ```bash
   cd ~/Documents/Obsidian/HPE/Media
   # First attendee
   sips -c 40 40 --cropOffset 12 12 SCR-YYYYMMDD-xxxxx.png --out Last-First-avatar.png
   # Second attendee (~54 pixels down)
   sips -c 40 40 --cropOffset 66 12 SCR-YYYYMMDD-xxxxx.png --out Last-First-avatar.png
   ```
4. Create People profiles with avatars
5. Update ## Attendees section with linked list
6. Remove screenshot reference after extraction

**Option B: Known People Lookup (No Screenshot)**

If no screenshot available:

1. Extract potential names from meeting content:
   ```bash
   grep -oE "\b[A-Z][a-z]+\b" "meeting-file.md" | sort -u
   ```
2. Search People profiles for matches:
   ```bash
   cd ~/Documents/Obsidian/HPE/People
   for name in Yogesh Kyu Darra; do
     ls -1 *.md | grep -i "$name"
   done
   ```
3. Verify matches by checking aliases
4. Build attendee list from verified matches

### Step 2: Create People Profiles

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

**Important:**
- Only add avatar if profile doesn't already have one
- Check for existing `![[` image reference first
- Use exact format: filename `{Last}, {First}.md`, alias `{First} {Last}`

### Step 3: Update Meeting Attendees

Replace image reference with linked attendee list:

```markdown
## Attendees

## In Meeting (5)
- [[Tronkowski, Kevin|Kevin Tronkowski]]
- [[Pahwa, Kashish|Kashish Pahwa]]

## Invited/Other Participants (3)
- [[Luna, Gabriella|Gabriella Luna]]
```

Include counts in section headers: `## In Meeting (5)`

### Step 4: Check for Copilot Summary

**Check if `## Copilot Summary` section exists with content:**

- **If present**: Skip transcript cleanup and summary generation
- **If absent or empty**: Proceed with transcript processing

**Copilot Summary Characteristics:**
- Section header: `## Copilot Summary`
- Structured subsections: `# Decisions`, `# Open question`, `# Agenda`, `# Meeting notes`
- Already formatted (no cleanup needed)
- Often present WITHOUT transcript

**When Copilot Summary exists:**
1. ✅ Process attendees normally
2. ✅ Keep Copilot-generated content intact
3. ❌ Skip transcript cleanup
4. ❌ Skip summary generation
5. ✅ Optionally augment if transcript also present

### Step 5: Clean Transcript (if no Copilot Summary)

Use appropriate script based on transcript format:

#### Format 1: Direct Teams Paste
**Characteristics:**
- Speaker names on own line: `Last, First`
- Verbose timestamp: `0 minutes 3 seconds0:03`
- Profile image URLs
- Separator lines `____`

**Script:**
```bash
python3 ~/.copilot/skills/obsidian-meeting-general/scripts/clean_transcript.py "meeting-file.md"
```

#### Format 2: Downloaded from Teams
**Characteristics:**
- Combined speaker/timestamp: `**Bennett, Ryan**   0:03`
- Embedded image references
- Meeting header (title, date, duration)

**Script:**
```bash
python3 ~/.copilot/skills/obsidian-meeting-general/scripts/clean_transcript_downloaded.py "meeting-file.md"
```

#### Format 3: .docx Exported
**Characteristics:**
- Plain text (no bold): ` Last, First   timestamp content`
- Leading space before name
- No image references

**Script:**
```bash
python3 ~/.copilot/skills/obsidian-meeting-general/scripts/clean_transcript_docx.py "meeting-file.md"
```

#### Format 4: Simple/Generic
**Characteristics:**
- Basic formatting, minimal metadata

**Script:**
```bash
python3 ~/.copilot/skills/obsidian-meeting-general/scripts/clean_transcript_simple.py "meeting-file.md"
```

### Step 6: Generate Summary (if no Copilot Summary)

Analyze cleaned transcript and create structured meeting notes:

**If existing summary sections found** (e.g., `# Decisions`, `# Open questions`):
- Augment with additional detail from transcript
- Preserve existing structure

**If no existing summary:**
- Insert new structured summary in `## Notes` section
- Include: Decisions, Action Items, Open Questions, Key Discussion Points

## Finding Meeting Files

```bash
# Today's meetings
find ~/Documents/Obsidian/HPE/Meetings -name "$(date +%Y-%m-%d)*.md"

# Specific date
find ~/Documents/Obsidian/HPE/Meetings -name "2026-01-05*.md"

# By name (case-insensitive)
find ~/Documents/Obsidian/HPE/Meetings -iname "*aruba*interlock*.md"

# Date range (last week)
find ~/Documents/Obsidian/HPE/Meetings -name "*.md" -newermt "$(date -v-7d +%Y-%m-%d)" ! -newermt "$(date +%Y-%m-%d)"
```

## Common Usage Patterns

**"Process the meeting with transcript"**
- Extract attendees (screenshot or known people lookup)
- Create missing People profiles
- Clean transcript (detect format automatically)
- Generate summary from cleaned transcript

**"Process today's aruba meeting"**
- Find matching meeting file
- Full workflow: attendees → profiles → transcript → summary

**"Just clean up the transcript"**
- Skip attendee processing
- Only clean transcript section
- Detect format and use appropriate script

**"Find the people from obsidian people and list them"**
- When no screenshot available
- Extract first names from content
- Search People profiles
- Update attendee list with found profiles

## Validation Checklist

After processing, verify:
- [ ] ## Attendees updated with participants (actual or from content)
- [ ] People profiles created for new attendees (with avatars if screenshot)
- [ ] ## Transcript cleaned (if present and no Copilot Summary)
- [ ] ## Notes or ## Copilot Summary contains meeting summary
- [ ] All links use Obsidian format: `[[Last, First|First Last]]`
- [ ] Screenshot reference removed after extraction
- [ ] Existing Copilot Summaries preserved (not overwritten)

## Important Rules

- Always check existing profiles before creating
- Preserve existing profile content when found
- Use exact format: filename `{Last}, {First}.md`, alias `{First} {Last}`
- Include counts in section headers: `## In Meeting (5)`
- Check for Copilot Summary before cleaning transcript
- Preserve Copilot-generated summaries
- Only generate summaries when no Copilot Summary exists
- Remove screenshot reference after attendee extraction

## Directory Structure

```
~/Documents/Obsidian/HPE/
├── Meetings/YYYY-MM-DD - name.md
├── People/{Last}, {First}.md
└── Media/SCR-YYYYMMDD-xxxxx.png
```

## Additional Resources

- [scripts/README.md](scripts/README.md) - Documentation for transcript cleaning scripts
- [examples.md](examples.md) - Complete meeting examples
- [reference.md](reference.md) - Obsidian markdown syntax reference
