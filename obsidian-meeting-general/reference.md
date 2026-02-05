# Obsidian Markdown Syntax Reference

## Meeting Note Format

Meeting files use format: `YYYY-MM-DD - meeting name.md` in `~/Documents/Obsidian/HPE/Meetings/`

### Standard Sections

```markdown
## Attendees

## In Meeting (5)
- [[Last, First|First Last]]

## Invited/Other Participants (2)
- [[Last, First|First Last]]

## Notes

[Meeting notes or generated summary]

## Copilot Summary

[Microsoft Copilot-generated summary if available]

## Transcript

[Cleaned Teams transcript]
```

## Link Formats

### People Links (Obsidian Wikilinks)

**Format:** `[[File Name|Display Text]]`

**People Profile Links:**
- File: `People/Last, First.md`
- Link: `[[Last, First|First Last]]`
- Display: "First Last" (clickable)

**Examples:**
```markdown
- [[Tronkowski, Kevin|Kevin Tronkowski]]
- [[Pahwa, Kashish|Kashish Pahwa]]
- [[Luna, Gabriella|Gabriella Luna]]
```

### Image References

**Format:** `![[filename.png]]`

**Examples:**
```markdown
![[SCR-20260113-jshz.png]]
![[Tronkowski-Kevin-avatar.png]]
```

## People Profile Structure

**Location:** `~/Documents/Obsidian/HPE/People/{Last}, {First}.md`

**Format:**
```markdown
---
aliases:
  - {First} {Last}
tags:
  - People
---
![[{Last}-{First}-avatar.png]]

[Additional notes about person]
```

**Example:** `Pahwa, Kashish.md`
```markdown
---
aliases:
  - Kashish Pahwa
tags:
  - People
---
![[Pahwa-Kashish-avatar.png]]
```

## Transcript Cleaning

### Input (Unclean Transcript)

```markdown
## Transcript

____

![](https://nam.loki.delve.office.com/api/v2/personaphoto?AadObjectId=...)

Luna, Gabriella

0 minutes 8 seconds0:08

Luna, Gabriella 0 minutes 8 seconds

No worries. Um, so I know we want to touch base on.
```

### Output (Clean Transcript)

```markdown
## Transcript

**Luna, Gabriella** [0:08]: No worries. Um, so I know we want to touch base on.
```

## Avatar Extraction

**Source:** Teams screenshot (`SCR-*.png`)

**Extraction using sips:**
```bash
cd ~/Documents/Obsidian/HPE/Media

# First attendee (top of list)
sips -c 40 40 --cropOffset 12 12 SCR-20260113-jshz.png \
  --out Tronkowski-Kevin-avatar.png

# Second attendee (~54 pixels down)
sips -c 40 40 --cropOffset 66 12 SCR-20260113-jshz.png \
  --out De-Anirban-avatar.png
```

**Naming Convention:** `{Last}-{First}-avatar.png`

**Typical Layout:**
- Avatars: ~40x40 pixels
- Left offset: ~12 pixels from edge
- Vertical spacing: ~52-54 pixels
- First avatar: ~12-20 pixels from top

## Summary Structure

### Generated Summary Format

```markdown
## Notes

### Decisions
- Decision item 1
- Decision item 2

### Action Items
- [ ] Action item with checkbox
- [ ] Another action

### Open Questions
- Question 1?
- Question 2?

### Key Discussion Points
- Discussion point 1
- Discussion point 2
```

### Copilot Summary Format (Preserve As-Is)

```markdown
## Copilot Summary

# Decisions
- Decision item

# Open question
- Question item

# Meeting notes
### Topic
- Note details
```

## File Paths

```
~/Documents/Obsidian/HPE/
├── Meetings/
│   └── 2026-01-28 - Team Sync.md
├── People/
│   ├── Tronkowski, Kevin.md
│   └── Pahwa, Kashish.md
└── Media/
    ├── SCR-20260128-abcd.png
    ├── Tronkowski-Kevin-avatar.png
    └── Pahwa-Kashish-avatar.png
```
