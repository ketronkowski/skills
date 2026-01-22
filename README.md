# GitHub Copilot Skills

A collection of specialized skills that extend GitHub Copilot's capabilities with domain-specific knowledge, workflows, and best practices.

## What are Skills?

Skills are modular, self-contained packages that transform GitHub Copilot from a general-purpose agent into a specialized expert equipped with procedural knowledge, workflows, and tools for specific domains. Think of them as "onboarding guides" that teach Copilot how to handle specialized tasks.

## Available Skills

### Project-Specific Skills

- **[create-pr](create-pr/)** - Automate GitHub Pull Request creation following team conventions with JIRA ID or conventional commit formats. Handles PR status validation, JIRA work item discovery, and proper title/description formatting.

- **[gh-glcp](gh-glcp/)** - GitHub CLI best practices for GLCP organization. Prefer `gh` CLI over GitHub MCP server tools for glcp org to avoid 404 errors and access issues.

- **[git-commit](git-commit/)** - Standards and formatting for creating git commit messages using conventional commit format with type prefixes and descriptions.

- **[jira-glcp](jira-glcp/)** - Work with Jira and Atlassian for the GLCP project using Atlassian MCP server tools. Handles querying issues, sprints, boards, and creating/updating GLCP stories.

- **[sd-repos](sd-repos/)** - Quick reference for SD/SIC (Sustainability Dashboard/Sustainability Insight Center) repositories. Helps identify ADS apps, locate repositories, and understand repository categorization.

### Obsidian Workflow Skills

- **[obsidian-vault](obsidian-vault/)** - Context for Obsidian vault structure, organization, and search strategies. Navigation guide for notes, meetings, people profiles, and documentation.

- **[obsidian-meeting](obsidian-meeting/)** - Process Obsidian meeting notes from Teams transcripts. Handles attendee extraction from screenshots, People profile creation, transcript cleaning/formatting, and meeting summary generation.

- **[obsidian-daily-summary](obsidian-daily-summary/)** - Generate daily summaries for Obsidian daily notes by aggregating content from meetings, notes, and conversations associated with a specific day.

### Meta Skill

- **[skill-creator](skill-creator/)** - Guide for creating effective skills. Use when you want to create a new skill or update an existing skill that extends GitHub Copilot's capabilities.

## Usage

These skills are designed to work with GitHub Copilot CLI and compatible AI assistants. Each skill directory contains:

- `SKILL.md` - The main skill definition with instructions and workflows
- Supporting files - References, examples, scripts, and documentation
- `.skill-definition` - Metadata files (where applicable)

## Contributing

Feel free to submit issues or pull requests to improve existing skills or add new ones.

## License

See individual skill directories for specific license information. Most skills are available for use as reference material.
