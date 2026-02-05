# Changelog

## 2026-01-23 - UPDATED: Automatic Detailed AI Summaries (BREAKING CHANGE)

### What Changed

**MAJOR UPDATE:** The `obsidian-email` skill now **ALWAYS generates detailed AI summaries automatically**. No longer requires a two-step workflow.

### New Default Behavior

**Single-Step Processing:**
1. Run `process_email.py` → Automatically generates comprehensive detailed summary
2. Processing takes 30-60 seconds for AI analysis
3. Falls back to enhanced basic summary only if AI unavailable

### Detailed Summary Features

Every email processing now includes:
- ✅ Comprehensive multi-paragraph overview with full context
- ✅ Technical issue breakdown with root causes and specific details
- ✅ Stakeholder mapping organized by role
- ✅ Action items with owners, deadlines, and checkboxes
- ✅ Process breakdown and communication gap analysis
- ✅ Tables for ticket tracking
- ✅ Timeline of events with timestamps
- ✅ Specific technical details (serial numbers, configs, error messages)
- ✅ Customer impact assessment with quotes
- ✅ Root cause summary (technical + process failures)
- ✅ Prioritized next steps

### Example Output

```
✓ Extracted 15 unique participants
✓ Updated 2 profiles with email addresses
✓ Updated Participants section
⏳ Generating detailed AI summary (this may take 30-60 seconds)...
✓ Generated detailed AI summary
✓ Updated email note
```

### Performance

- **Processing time:** 30-60 seconds for AI analysis
- **Content analyzed:** Up to 30KB of email chain content
- **Fallback:** Enhanced basic summary if AI unavailable

### Breaking Changes

- ⚠️ **Processing time increased** from instant to 30-60 seconds
- ⚠️ **Requires AI capabilities** (anthropic library recommended)
- ✅ **Much more detailed output** automatically

### Migration

No migration needed - existing functionality enhanced automatically.

---

## 2026-01-23 - Enhanced Summary Generation

### What Changed

Updated the `obsidian-email` skill to support detailed email summaries through an interactive workflow with GitHub Copilot CLI.

### New Workflow

1. **Initial Processing** (Automated)
   - Run `process_email.py` to extract participants and generate enhanced basic summary
   - Enhanced summary includes: tickets, dates, urgency, customer names
   
2. **Detailed Analysis** (Interactive via Copilot CLI)
   - After initial processing, request: "I would like more details from the messages in the summary"
   - GitHub Copilot generates comprehensive analysis with:
     - Technical issue breakdown with root causes
     - Stakeholder mapping by role
     - Action items organized by timeline with owners
     - Process breakdown analysis
     - Tables for ticket tracking
     - Specific technical details (serial numbers, configs, etc.)

### Enhanced Basic Summary

The auto-generated summary now includes:
- ✅ Customer/project name extraction from subject
- ✅ Urgency indicators (HIGH PRIORITY, meeting scheduled)
- ✅ Referenced tickets as Obsidian links
- ✅ Key dates mentioned in thread
- ✅ Participant count and stakeholder involvement
- ✅ Structured action item section

### Files Updated

- `scripts/process_email.py` - Enhanced summary generation logic
- `SKILL.md` - Updated documentation for new workflow
- `examples.md` - Added Example 7 showing interactive workflow
- `CHANGELOG.md` - This file

### Backward Compatibility

✅ Fully backward compatible - existing functionality unchanged
✅ Enhanced summaries generated automatically
✅ Detailed summaries requested interactively as needed
