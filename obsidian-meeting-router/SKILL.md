---
name: obsidian-meeting-router
description: Routes Obsidian meeting processing requests to specialized skills. **Use when** user asks to "process meeting", "process obsidian meeting", or "process the meeting". Automatically detects meeting type (standup vs general) and delegates to appropriate skill.
---

# Obsidian Meeting Router

**🚀 AUTOMATIC ROUTING - This skill determines meeting type and delegates to specialized skills**

When user says "process meeting", "process the obsidian meeting", or similar:

## Step 1: Read Meeting File

First, determine which meeting file to process:

```bash
# Default: today's meetings
find ~/Documents/Obsidian/HPE/Meetings -name "$(date +%Y-%m-%d)*.md"

# If user specified a specific date (e.g., "yesterday", "2026-01-28")
find ~/Documents/Obsidian/HPE/Meetings -name "2026-01-28*.md"

# If user specified meeting name
find ~/Documents/Obsidian/HPE/Meetings -iname "*meeting-name*.md"
```

Read the meeting file to analyze its content.

## Step 2: Detect Meeting Type

Check the filename to determine if it's a standup meeting:

**Standup Meeting Indicators:**
- Filename contains: `Green Standup` OR `Magenta Standup`
- Pattern: `YYYY-MM-DD - [Team] Standup.md`

**If standup meeting detected → Invoke `obsidian-meeting-standup` skill**

**If NOT standup meeting → Invoke `obsidian-meeting-general` skill**

## Step 3: Delegate to Appropriate Skill

### For Standup Meetings

Use the `obsidian-meeting-standup` skill with this instruction:

```
Process the standup meeting at [FILE_PATH]

The file has been identified as a [Green/Magenta] standup meeting.
Execute the complete standup workflow including JIRA auto-population.
```

### For General Meetings

Use the `obsidian-meeting-general` skill with this instruction:

```
Process the meeting at [FILE_PATH]

Execute the complete meeting workflow including attendee extraction,
transcript cleaning, and summary generation as applicable.
```

## Detection Logic Reference

**Standup meeting if:**
- Filename matches: `*Green Standup*` OR `*Magenta Standup*`

**General meeting if:**
- Any other meeting file pattern

## Example Routing

**Input:** "Process today's Green Standup"
- ✅ Detect: Standup meeting
- ✅ Route to: `obsidian-meeting-standup` skill

**Input:** "Process the 2026-01-28 team sync meeting"
- ✅ Detect: General meeting
- ✅ Route to: `obsidian-meeting-general` skill

**Input:** "Process meeting" (ambiguous)
- ✅ Find today's meeting files
- ✅ Detect type from filename
- ✅ Route to appropriate skill

## Important Notes

- **No user confirmation needed** - routing is automatic
- **Router does not process meetings** - it only identifies and delegates
- **Specialized skills handle all actual processing** - JIRA, attendees, transcripts, summaries
- If multiple meetings found, ask user which one to process
