#!/usr/bin/env python3
"""
Process Obsidian email chain notes.

Usage:
    python process_email.py <email_note_file.md>

This script:
1. Extracts unique participants from email From headers
2. Creates missing People profiles with email addresses
3. Updates Participants section with linked names
4. Generates summary from email chain content
5. Updates Summary section in the note
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional


def extract_participants(email_chain: str) -> List[Tuple[str, str]]:
    """
    Extract unique senders from email chain.
    
    Returns list of (name, email) tuples in order of first appearance.
    Name format: "Last, First" or "Last, First Middle"
    """
    participants = []
    seen_emails = set()
    seen_names = set()
    
    # Pattern to match From headers (both plain and bold)
    # Matches: "From: Last, First <email@domain.com>"
    # Or: "**From:** Last, First <email@domain.com>"
    from_pattern = r'\*?\*?From:\*?\*?\s+([^<\n]+?)\s*<([^>]+)>'
    
    for match in re.finditer(from_pattern, email_chain):
        name_raw = match.group(1).strip()
        email_raw = match.group(2).strip()
        
        # Clean email - handle markdown links [email](mailto:email)
        # Extract just the email address
        email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', email_raw)
        if not email_match:
            continue
        email = email_match.group(1)
        
        # Skip if we've seen this email before
        if email in seen_emails:
            continue
        
        # Clean name - remove role descriptions in parentheses
        # e.g., "McKee, Heidi L (GreenLake Manager)" -> "McKee, Heidi L"
        name = re.sub(r'\s*\([^)]+\)\s*', '', name_raw).strip()
        
        # Validate name format (should contain comma for "Last, First")
        if ',' not in name:
            continue
        
        # Skip if we've seen this name before (avoid duplicates)
        if name in seen_names:
            continue
        
        seen_emails.add(email)
        seen_names.add(name)
        participants.append((name, email))
    
    return participants


def format_name_for_link(name: str) -> Tuple[str, str]:
    """
    Convert "Last, First" to ("Last, First", "First Last").
    Handles middle names: "Last, First Middle" -> "First Middle Last"
    """
    if ',' not in name:
        return name, name
    
    parts = [p.strip() for p in name.split(',', 1)]
    last_name = parts[0]
    first_parts = parts[1] if len(parts) > 1 else ""
    
    # Display format: "First Middle Last"
    display_name = f"{first_parts} {last_name}".strip()
    
    return name, display_name


def check_profile_exists(name: str, people_dir: Path) -> Optional[Path]:
    """Check if a People profile exists for the given name."""
    profile_path = people_dir / f"{name}.md"
    return profile_path if profile_path.exists() else None


def create_people_profile(name: str, email: str, people_dir: Path) -> bool:
    """Create a new People profile with email address."""
    profile_path = people_dir / f"{name}.md"
    
    _, display_name = format_name_for_link(name)
    
    content = f"""---
tags:
  - person
---

# {name}

## Contact
- Email: {email}

## Aliases
- [[{name}|{display_name}]]
"""
    
    try:
        with open(profile_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"ERROR: Failed to create profile for {name}: {e}")
        return False


def add_email_to_profile(profile_path: Path, email: str) -> bool:
    """Add email to existing profile if not already present."""
    try:
        with open(profile_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if email already exists
        if email in content:
            return False
        
        # Check if Contact section exists
        if '## Contact' in content:
            # Add email to existing Contact section
            content = re.sub(
                r'(## Contact\n)',
                f'\\1- Email: {email}\n',
                content,
                count=1
            )
        else:
            # Add Contact section after the heading
            name_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            if name_match:
                insert_pos = content.find('\n', name_match.end())
                content = (content[:insert_pos + 1] + 
                          f'\n## Contact\n- Email: {email}\n' +
                          content[insert_pos + 1:])
        
        with open(profile_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"ERROR: Failed to add email to profile: {e}")
        return False


def update_participants_section(content: str, participants: List[Tuple[str, str]]) -> str:
    """Update the Participants section with linked names."""
    # Build participant list
    participant_lines = []
    for name, _ in participants:
        full_name, display_name = format_name_for_link(name)
        participant_lines.append(f"- [[{full_name}|{display_name}]]")
    
    participant_text = '\n'.join(participant_lines)
    
    # Replace Participants section
    pattern = r'(# Participants\n)\s*(\n# )'
    replacement = f'\\1\n{participant_text}\n\\2'
    
    new_content = re.sub(pattern, replacement, content)
    
    return new_content


def generate_summary_with_ai(email_chain: str, participants: List[Tuple[str, str]]) -> str:
    """
    Generate a detailed AI-powered summary.
    
    Always attempts to generate comprehensive detailed summary.
    Falls back to enhanced basic summary only if AI generation fails.
    """
    import subprocess
    import tempfile
    import os
    
    # Extract subject for context
    subject_match = re.search(r'Subject:\s*(.+?)(?:\n|$)', email_chain, re.IGNORECASE)
    subject = subject_match.group(1).strip() if subject_match else "Email Discussion"
    
    print("⏳ Generating detailed AI summary (this may take 30-60 seconds)...")
    
    # Prepare comprehensive prompt for detailed analysis
    prompt = f"""Analyze this email chain from Obsidian notes and generate a COMPREHENSIVE, DETAILED summary.

IMPORTANT: Extract SPECIFIC details from the emails - serial numbers, configurations, error messages, exact quotes, deadlines, etc. Be thorough and precise.

Required Structure:

## Overview
- Detailed 2-3 paragraph overview explaining what this thread is about
- Include: customer/project name, timeline, urgency level, type of discussion
- Context: why this email thread exists, what triggered it

## Technical Issues Identified (if applicable)
- Break down EACH distinct technical issue or topic separately
- For each issue include:
  * Problem statement
  * Root cause (technical details)
  * Affected systems/components (with serial numbers, models, etc.)
  * Solution/fix plan
  * Current status
- Use subsections (### Issue #1, ### Issue #2) for clarity
- Include tables for ticket tracking if multiple issues discussed
- Extract ALL technical specifics mentioned in emails

## Process & Communication Issues (if applicable)
- Identify process breakdowns or communication gaps
- What are leadership concerns?
- Questions raised that need answers
- Team coordination problems

## Action Items & Responsibilities
Organize by timeline with SPECIFIC owners and deadlines:
### Immediate Actions (with deadlines if mentioned)
- [x] Completed items
- [ ] Pending items with owner name and deadline

### Short-Term Actions
- [ ] Items with owner names

### Long-Term Actions
- [ ] Strategic items

## Progress Updates (if applicable)
- Timeline of what has been tried/completed
- Current status vs. expected status
- Blockers and challenges
- Specific metrics if mentioned (e.g., "11 to 12 devices")

## Key Stakeholders
Group by role with BRIEF description of their involvement:
### Engineering Leadership
- Name - Role/involvement

### Engineering Teams  
- Team Name:
  - Person - specific role

### Support/QA
- Name - involvement

### Customer Success
- Name - involvement

## Root Cause Summary (if applicable)
### Technical Failures
- Concise list of what went wrong technically

### Process Failures  
- What process/communication broke down

### Why Not Caught Earlier
- Analysis of why this persisted

### Customer Impact Duration
- How long has this affected the customer

## Next Steps
- Clear, prioritized list of what needs to happen next
- Include dependencies if mentioned

## Additional Context (if needed)
- Any other important observations
- Patterns or systemic issues identified

Email subject: {subject}
Number of participants: {len(participants)}

Email chain (analyzing first 30KB):
{email_chain[:30000]}

GENERATE THE DETAILED SUMMARY NOW. Use markdown formatting with bold, tables, checkboxes. Extract SPECIFIC details and quotes from the emails."""

    try:
        # Try multiple approaches to generate AI summary
        
        # Approach 1: Use python subprocess to call AI directly
        # This works in Copilot CLI context where AI is available
        result = subprocess.run(
            ['python3', '-c', f'''
import sys
import os

# Attempt to use available AI capabilities
prompt = {repr(prompt)}

# Try to import and use anthropic if available
try:
    import anthropic
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=6000,
        temperature=0.3,
        messages=[{{"role": "user", "content": prompt}}]
    )
    print(message.content[0].text)
    sys.exit(0)
except ImportError:
    pass
except Exception:
    pass

# If anthropic not available, indicate need for fallback
print("AI_UNAVAILABLE", file=sys.stderr)
sys.exit(1)
'''],
            capture_output=True,
            text=True,
            timeout=120,
            env={**os.environ, 'ANTHROPIC_API_KEY': os.environ.get('ANTHROPIC_API_KEY', '')}
        )
        
        if result.returncode == 0 and len(result.stdout.strip()) > 500:
            # Successfully generated AI summary
            output = result.stdout.strip()
            # Clean up any preamble
            if output.startswith(('Here', 'I will', 'I\'ll', 'Let me', 'Sure')):
                lines = output.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith('##'):
                        output = '\n'.join(lines[i:])
                        break
            print("✓ Generated detailed AI summary")
            return output
        
    except subprocess.TimeoutExpired:
        print("⚠ AI summary generation timed out, using enhanced basic summary")
    except Exception as e:
        print(f"⚠ AI generation failed ({type(e).__name__}), using enhanced basic summary")
    
    # Fallback to enhanced basic summary
    print("ℹ Using enhanced basic summary (AI unavailable)")
    return generate_basic_summary(email_chain, participants)


def generate_basic_summary(email_chain: str, participants: List[Tuple[str, str]]) -> str:
    """
    Generate an enhanced basic summary when AI is unavailable.
    Extracts key information from the email chain.
    """
    # Extract subject line
    subject_match = re.search(r'Subject:\s*(.+?)(?:\n|$)', email_chain, re.IGNORECASE)
    subject = subject_match.group(1).strip() if subject_match else "Email Discussion"
    
    # Count emails
    num_emails = len(participants)
    
    # Extract mentioned issues/tickets
    tickets = re.findall(r'GLCP-\d+|\[\[GLCP-\d+\]\]', email_chain)
    unique_tickets = sorted(list(set([t.replace('[[', '').replace(']]', '') for t in tickets])))
    
    # Extract dates mentioned
    dates = re.findall(r'\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}(?:,?\s+\d{4})?\b', email_chain)
    
    # Extract key action words/urgency indicators
    urgency_words = []
    if re.search(r'\b(?:urgent|critical|escalat|asap|immediately|priority)\b', email_chain, re.IGNORECASE):
        urgency_words.append("HIGH PRIORITY")
    if re.search(r'\b(?:meeting|call|sync)\b.*\b(?:today|tomorrow|noon)\b', email_chain, re.IGNORECASE):
        urgency_words.append("Imminent meeting scheduled")
    
    # Extract customer/project names
    customers = re.findall(r'\b([A-Z][A-Z]+)\b(?:\s+\([^)]+\))?', subject)
    
    # Build enhanced summary
    summary = f"""## Overview
Email thread regarding: {subject}

Thread contains {num_emails} messages from {len(participants)} unique participants.
"""
    
    if customers:
        summary += f"\n**Customer/Project:** {', '.join(set(customers))}\n"
    
    if urgency_words:
        summary += f"**Status:** {', '.join(urgency_words)}\n"
    
    summary += "\n## Key Points\n"
    summary += "- Discussion involves multiple stakeholders across teams\n"
    
    if unique_tickets:
        summary += f"\n**Referenced Tickets:**\n"
        for ticket in unique_tickets:
            summary += f"- [[{ticket}]]\n"
    
    if dates:
        summary += f"\n**Key Dates Mentioned:** {', '.join(set(dates[:5]))}\n"
    
    summary += """
## Action Items
- Review email chain for specific action items and deadlines
- Follow up on open issues discussed
- Note: Run this script again to attempt AI-generated detailed summary

## Context
See full email chain below for complete discussion details.

---
*Note: This is a basic summary. For detailed analysis including technical issues, stakeholder breakdown, and comprehensive action items, ensure AI capabilities are configured.*
"""
    
    return summary


def generate_summary(email_chain: str, participants: List[Tuple[str, str]]) -> str:
    """
    Generate a detailed summary of the email chain using AI when available.
    Falls back to enhanced basic summary otherwise.
    """
    return generate_summary_with_ai(email_chain, participants)


def update_summary_section(content: str, summary: str) -> str:
    """Update the Summary section with generated content."""
    pattern = r'(# Summary\n)\s*(\n# )'
    replacement = f'\\1\n{summary}\n\\2'
    
    new_content = re.sub(pattern, replacement, content)
    
    return new_content


def extract_email_chain(content: str) -> Optional[str]:
    """Extract the Email Chain section content."""
    match = re.search(r'# Email Chain\n(.+)', content, re.DOTALL)
    return match.group(1) if match else None


def main():
    if len(sys.argv) != 2:
        print("Usage: process_email.py <email-note-file.md>")
        sys.exit(1)
    
    filepath = Path(sys.argv[1])
    
    if not filepath.exists():
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)
    
    # Determine People directory
    # Assuming structure: .../Obsidian/HPE/Notes/file.md -> .../Obsidian/HPE/People/
    people_dir = filepath.parent.parent / "People"
    
    if not people_dir.exists():
        print(f"ERROR: People directory not found: {people_dir}")
        sys.exit(1)
    
    # Read the note file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract email chain
    email_chain = extract_email_chain(content)
    if not email_chain:
        print("ERROR: No email chain section found")
        sys.exit(1)
    
    # Extract participants
    participants = extract_participants(email_chain)
    
    if not participants:
        print("ERROR: No participants extracted from email chain")
        print("Ensure emails have 'From: Name <email>' format")
        sys.exit(1)
    
    print(f"✓ Extracted {len(participants)} unique participants")
    for name, email in participants:
        print(f"  - {name} ({email})")
    
    # Process participants - create/update profiles
    new_profiles = 0
    updated_profiles = 0
    
    for name, email in participants:
        profile_path = check_profile_exists(name, people_dir)
        
        if profile_path:
            # Profile exists, check if email needs to be added
            if add_email_to_profile(profile_path, email):
                updated_profiles += 1
        else:
            # Create new profile
            if create_people_profile(name, email, people_dir):
                new_profiles += 1
    
    if new_profiles > 0:
        print(f"✓ Created {new_profiles} new People profiles")
    if updated_profiles > 0:
        print(f"✓ Updated {updated_profiles} profiles with email addresses")
    
    # Update Participants section
    content = update_participants_section(content, participants)
    print("✓ Updated Participants section")
    
    # Generate and update summary
    summary = generate_summary(email_chain, participants)
    content = update_summary_section(content, summary)
    
    # Count summary sections
    summary_sections = len(re.findall(r'^##', summary, re.MULTILINE))
    print(f"✓ Generated summary ({summary_sections} sections)")
    
    # Write updated content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Updated {filepath.name}")


if __name__ == '__main__':
    main()
