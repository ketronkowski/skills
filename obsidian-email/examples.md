# Email Chain Processing Examples

## Example 1: Basic Email Chain Processing

### Input File

```markdown
---
when: 2026-01-23
tags:
  - note
---
# Participants


# Summary



# Email Chain

From: Smith, John <john.smith@hpe.com>
Date: Monday, January 20, 2026 at 2:30 PM
To: Team <team@hpe.com>
Subject: Project Update

Hello team,

Just wanted to provide a quick update on the project status.

Thanks,
John

---

**From:** Johnson, Alice <alice.johnson@hpe.com>
**Sent:** Monday, January 20, 2026 3:45 PM
**To:** Smith, John <john.smith@hpe.com>
**Subject:** RE: Project Update

Thanks John,

Can you provide more details on the timeline?

Best,
Alice
```

### After Processing

```markdown
---
when: 2026-01-23
tags:
  - note
---
# Participants

- [[Smith, John|John Smith]]
- [[Johnson, Alice|Alice Johnson]]

# Summary

## Overview
Email thread regarding: Project Update

Thread contains 2 messages from 2 participants.

## Key Points
- Discussion involves multiple stakeholders across teams

## Action Items
- Review email chain for specific action items and deadlines
- Follow up on open issues discussed

## Context
See full email chain below for complete discussion details.


# Email Chain

[Same content as before]
```

### Created People Profiles

**File: `~/Documents/Obsidian/HPE/People/Smith, John.md`**
```markdown
---
tags:
  - person
---

# Smith, John

## Contact
- Email: john.smith@hpe.com

## Aliases
- [[Smith, John|John Smith]]
```

**File: `~/Documents/Obsidian/HPE/People/Johnson, Alice.md`**
```markdown
---
tags:
  - person
---

# Johnson, Alice

## Contact
- Email: alice.johnson@hpe.com

## Aliases
- [[Johnson, Alice|Alice Johnson]]
```

## Example 2: Email with Multiple Names and Tickets

### Input File

```markdown
---
when: 2026-01-23
tags:
  - note
---
# Participants


# Summary



# Email Chain

From: Vobbilisetty, Suresh <suresh.vobbilisetty@hpe.com>
Date: Friday, January 23, 2026 at 7:43 AM
To: Yun, Stella <xiaoyang.yun@hpe.com>
Subject: Re: DGTS Sustainability - OpsRamp

Stella - please check with the team on this.

We need an update by noon today regarding [[GLCP-322691]].

Thanks,
Suresh.

---

**From:** Yun, Stella <xiaoyang.yun@hpe.com>
**Sent:** Friday, January 23, 2026 8:15 AM
**To:** Vobbilisetty, Suresh <suresh.vobbilisetty@hpe.com>
**Subject:** RE: DGTS Sustainability - OpsRamp

Hi Suresh,

Working on it now. Will have update before the meeting.

Best,
Stella
```

### Processing Output

```
✓ Extracted 2 unique participants
  - Vobbilisetty, Suresh (suresh.vobbilisetty@hpe.com)
  - Yun, Stella (xiaoyang.yun@hpe.com)
✓ Updated 2 profiles with email addresses
✓ Updated Participants section
✓ Generated summary (4 sections)
✓ Updated 2026-01-23 - DGTS Sustainability.md
```

### After Processing

```markdown
---
when: 2026-01-23
tags:
  - note
---
# Participants

- [[Vobbilisetty, Suresh|Suresh Vobbilisetty]]
- [[Yun, Stella|Stella Yun]]

# Summary

## Overview
Email thread regarding: Re: DGTS Sustainability - OpsRamp

Thread contains 2 messages from 2 participants.

## Key Points
- Discussion involves multiple stakeholders across teams
- References tickets: [[GLCP-322691]]

## Action Items
- Review email chain for specific action items and deadlines
- Follow up on open issues discussed

## Context
See full email chain below for complete discussion details.


# Email Chain

[Same content as before]
```

## Example 3: Long Email Chain with Multiple Participants

### Command Line Usage

```bash
# Find email notes
find ~/Documents/Obsidian/HPE/Notes -iname "*ops*ramp*email*.md"

# Process the email
python ~/skills/obsidian-email/scripts/process_email.py \
  ~/Documents/Obsidian/HPE/Notes/2026-01-23\ -\ Ops\ Ramp\ Issues\ Email.md
```

### Output

```
✓ Extracted 5 unique participants
  - Vobbilisetty, Suresh (suresh.vobbilisetty@hpe.com)
  - Sadananda, Ravi Kiran Srirangam (ravikiransrirangam.sadananda@hpe.com)
  - Daniel, Binu (binu.daniel@hpe.com)
  - Vanteru, Bhanu (bhanu.vanteru@hpe.com)
  - Yun, Stella (xiaoyang.yun@hpe.com)
✓ Created 4 new People profiles
✓ Updated 1 profiles with email addresses
✓ Updated Participants section
✓ Generated summary (4 sections)
✓ Updated 2026-01-23 - Ops Ramp Issues Email.md
```

## Example 4: Handling Middle Names

### Input From Header

```
From: Van Der Berg, Jan Willem <jan.vandeberg@hpe.com>
```

### Generated Links

```markdown
- [[Van Der Berg, Jan Willem|Jan Willem Van Der Berg]]
```

### Profile Created

```markdown
---
tags:
  - person
---

# Van Der Berg, Jan Willem

## Contact
- Email: jan.vandeberg@hpe.com

## Aliases
- [[Van Der Berg, Jan Willem|Jan Willem Van Der Berg]]
```

## Example 5: Mixed Email Format (Outlook + Plain)

### Input Email Chain

```markdown
# Email Chain

From: Lee, Sarah <sarah.lee@hpe.com>
Date: Wednesday, January 15, 2026 at 9:00 AM
To: Team <team@hpe.com>

Initial message here.

---

**From:** Chen, Michael <michael.chen@hpe.com>
**Sent:** Wednesday, January 15, 2026 10:30 AM
**To:** Lee, Sarah <sarah.lee@hpe.com>

Reply message here.
```

### Result

Both formats are correctly parsed:
```
✓ Extracted 2 unique participants
  - Lee, Sarah (sarah.lee@hpe.com)
  - Chen, Michael (michael.chen@hpe.com)
```

## Example 7: Automatic Detailed AI Summary (DEFAULT BEHAVIOR)

### Processing Email - Automatic Detailed Analysis

When you process an email, the script **automatically generates a comprehensive detailed summary**:

```bash
python process_email.py "2026-01-23 - DGTS Email.md"
```

**Output:**
```
✓ Extracted 15 unique participants
✓ Updated 2 profiles with email addresses
✓ Updated Participants section
⏳ Generating detailed AI summary (this may take 30-60 seconds)...
✓ Generated detailed AI summary
✓ Updated email note
```

**Automatically Generated Detailed Summary:**
```markdown
# Summary

## Overview
This email thread discusses critical issues with the Sustainability Insight Center (SIC) setup for DGTS (Deloitte) customer that have been ongoing for approximately 5 months. The thread involves escalated communication between HPE Engineering (OpsRamp team), SIC team, Customer Success, and leadership regarding data integration problems.

**Timeline:** January 15-23, 2026 (peak escalation), with issues dating back ~5 months  
**Key Meeting:** January 23, 2026 at 12:00 PM (noon)  
**Customer:** DGTS (Deloitte)

## Technical Issues Identified

Bhanu Vanteru provided detailed analysis of **2 distinct root cause issues** affecting **4 GLCP Jira tickets**:

### Customer Environment
- **Server:** One DL385 Gen11 server (Serial# 3M1D1J13N0) monitored via Redfish integration
- **Components:** Contains two power supplies (Serial# 5XLNR0LLLJIKC9 and 5XLNR0LLLJIKFL)

### Issue #1: Power Supply Data Misrepresentation
**Problem:** OpsRamp is sending SIC data with power supply serial numbers, causing them to appear as separate devices instead of components within the server.

**Solution Required:**
- Send parent resource information in the data feed to SIC
- Requires changes on both OpsRamp AND SIC sides

### Issue #2: Computer System Chassis - Missing Data (CRITICAL BUG)
**Problem:** OpsRamp is sending SIC data for Computer System Chassis with device type UNKNOWN and NO serial number.

**Root Cause:** Missing resource type definition in Redfish integration  
**Fix Plan:** Planned for SH/CON 3.3 release (priority item)

### Affected GLCP Tickets

| Ticket | Summary | Status | Environment |
|--------|---------|--------|-------------|
| [[GLCP-271413]] | Redfish Integration doesn't send data properly | Reopened | Production |
| [[GLCP-280098]] | OpsRamp data not reflected in SIC | Reopened | Production |
| [[GLCP-293364]] | OpsRamp Redfish issue in Aquila | New | Aquila |
| [[GLCP-323815]] | Duplicate Chassis entry without serial# | Assigned | Aquila |

## Process & Escalation Issues

### Communication Breakdown
- **No PI tickets** found despite 5-month customer issue
- Issue discovered during **routine ticket review**, not escalation
- Engineering was unaware of customer pain

## Action Items & Responsibilities

### Immediate Actions (Due: Jan 23, 2026 by Noon)
- [x] **Stella Yun & Bhanu Vanteru:** Sync on next steps
- [x] **Bhanu:** Provide ETA for Chassis bug fix
- [ ] **Binu/Nithin:** Audit support process breakdown

### Short-Term Actions
- [ ] **Bhanu:** Schedule call with SIC team
- [ ] **Engineering:** Implement fixes in SH/CON 3.3

## Key Stakeholders

### Engineering Leadership
- **Suresh Vobbilisetty:** Leading escalation
- **Bhanu Vanteru:** Engineering lead providing analysis
- **Latha Vishnubhotla:** Executive sponsor

### Customer Success
- **Jennifer Evanko:** Escalating customer frustration ("5 full months")
- **David Cagin:** Hands-on configuration work
```

### AI Summary Features

The AI-powered summary extracts:
- ✅ **Specific technical details** (serial numbers, models, configurations)
- ✅ **Root cause analysis** for each issue
- ✅ **Affected tickets in tables** for easy scanning
- ✅ **Stakeholder roles and responsibilities**
- ✅ **Action items with owners and deadlines**
- ✅ **Timeline of events**
- ✅ **Process breakdowns** identified
- ✅ **Customer impact** and urgency

### Fallback Mode

If AI is unavailable (no API keys configured), generates enhanced basic summary:
```markdown
# Summary

## Overview
Email thread regarding: Re: DGTS Sustainability Insight Center set up

**Customer/Project:** DGTS  
**Status:** HIGH PRIORITY, Imminent meeting scheduled

## Key Points
- Discussion involves multiple stakeholders across teams

**Referenced Tickets:**
- [[GLCP-322691]]
- [[GLCP-323815]]
- [[GLCP-271413]]

**Key Dates Mentioned:** Friday, January 23, 2026, January 16, 2026

## Action Items
- Review email chain for specific action items and deadlines
- Note: Run this script again to attempt AI-generated detailed summary

---
*Note: This is a basic summary. For detailed analysis, ensure AI capabilities are configured.*
```

## Example 8: Adding Email to Existing Profile

If profile already exists but without email:

### Existing Profile
```markdown
---
tags:
  - person
---

# Smith, John

## Aliases
- [[Smith, John|John Smith]]
```

### After Processing
```markdown
---
tags:
  - person
---

# Smith, John

## Contact
- Email: john.smith@hpe.com

## Aliases
- [[Smith, John|John Smith]]
```

### Output
```
✓ Extracted 1 unique participants
  - Smith, John (john.smith@hpe.com)
✓ Updated 1 profiles with email addresses
✓ Updated Participants section
✓ Generated summary (4 sections)
```
