# 🔴 CRITICAL CHECKLIST - READ FIRST 🔴

## When User Says "Process Meeting"

**Follow this checklist EXACTLY in order:**

### ☑️ Step 1: Read Meeting File
```bash
# Find and read the meeting file
cat "/Users/kevin/Documents/Obsidian/HPE/Meetings/YYYY-MM-DD - Meeting Name.md"
```

### ☑️ Step 2: Check Meeting Type
- [ ] Is filename "Green Standup" or "Magenta Standup"?
  - **YES** → Continue to Step 3
  - **NO** → Skip to Step 4

### ☑️ Step 3: AUTOMATICALLY Populate JIRA (Standups Only)
- [ ] Check if `## JIRA` section is empty
- [ ] If empty:
  - **Green Team:**
    ```bash
    SPRINT_ID=$(acli jira board list-sprints --id 214 --state active 2>&1 | grep "^│" | grep active | awk '{print $2}')
    acli jira workitem search --jql "sprint = $SPRINT_ID AND status != Done AND status != Resolved ORDER BY assignee" 2>&1
    ```
  - **Magenta Team:**
    ```bash
    SPRINT_ID=$(acli jira board list-sprints --id 331 --state active 2>&1 | grep "^│" | grep active | awk '{print $2}')
    acli jira workitem search --jql "sprint = $SPRINT_ID AND status != Done AND status != Resolved ORDER BY assignee" 2>&1
    ```
- [ ] Map assignees to People profiles (Look in `/Users/kevin/Documents/Obsidian/HPE/People/`)
- [ ] Format as (include TYPE ICON and STATUS):
  ```markdown
  ### [[Last, First|First Last]]
  - [ ] [GLCP-12345](https://hpe.atlassian.net/browse/GLCP-12345) 📖 [Assigned] - Issue title
  - [ ] [GLCP-12346](https://hpe.atlassian.net/browse/GLCP-12346) 🐛 [In Review] - Another issue
  ```
  **Type Icons:** 📖 Story | 🐛 Bug | ☑️ Sub-task | 📌 Task | 🎯 Epic | 💡 Spike
- [ ] Insert into `## JIRA` section

**DO NOT ASK FOR PERMISSION. JUST DO IT.**

### ☑️ Step 4: Check Meeting State
- [ ] Has transcript? (## Transcript section has content)
- [ ] Has Copilot Summary? (## Copilot Summary has content)
- [ ] Has attendee screenshot? (`![[SCR-*.png]]` reference)
- [ ] **ANY YES** → Post-meeting mode
- [ ] **ALL NO** → Pre-meeting mode

### ☑️ Step 5: Execute Appropriate Workflow
- **Pre-meeting:** Populate expected attendees + JIRA (if not done in Step 3)
- **Post-meeting:** Process attendees, transcript, summary + JIRA (if not done in Step 3) + Add JIRA item updates

---

## Why This Exists

This checklist exists because JIRA auto-population has failed 10+ times. The issue is always:
- Asking for permission instead of just doing it
- Skipping JIRA population entirely
- Not detecting standup meetings correctly
- Not checking if JIRA section is empty

**The solution:**
1. ALWAYS check JIRA section for standups
2. ALWAYS populate if empty
3. NEVER ask for permission
4. Do this BEFORE everything else

---

## Board IDs (MEMORIZE THESE)
- **Green Team:** Board 214
- **Magenta Team:** Board 331

## JIRA Query Pattern (USE THIS EXACTLY)
```bash
# Step 1: Get active sprint ID
SPRINT_ID=$(acli jira board list-sprints --id {BOARD_ID} --state active 2>&1 | grep "^│" | grep active | awk '{print $2}')

# Step 2: Get open issues
acli jira workitem search --jql "sprint = $SPRINT_ID AND status != Done AND status != Resolved ORDER BY assignee" 2>&1
```

**CRITICAL:** Do NOT use `acli jira sprint list-workitems` - it's incomplete.

---

## Success Criteria

After processing a standup meeting:
- [ ] ## JIRA section is populated with sprint issues
- [ ] Issues are grouped by assignee
- [ ] Assignees use Obsidian links: `[[Last, First|First Last]]`
- [ ] Issues have full JIRA URLs: `[KEY](https://hpe.atlassian.net/browse/KEY)`
- [ ] Issues include TYPE ICON and STATUS: `[KEY] {icon} [STATUS] - Summary`
  - Icons: 📖 Story, 🐛 Bug, ☑️ Sub-task, 📌 Task, 🎯 Epic, 💡 Spike
- [ ] JIRA items mentioned in meeting content have update comments
- [ ] All this happened WITHOUT asking the user for permission

**If any of these are false, you failed to follow the checklist.**
