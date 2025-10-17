# Creating Lola Modules

This guide shows you how to create your own Lola modules using lazy context loading principles.

## What is a Lola Module?

A Lola module is a **lazy context** - a package of AI instructions, personas, workflows, scripts, and templates that get loaded only when needed. Think of it as a library or module for your AI assistant.

## Module Structure

It's important to mention that modules Lolas are flexible, that means
you are not forced to use all contexts for example a persona, you can have
modules for specific tasks for example, a context for a tool, or for a set of
specific commands.

With that in mind Lola module follows this structure:

```
modules/your-module/
├── AGENTS.md              # Main context for Cursor (required)
├── CLAUDE.md              # Main context for Claude CLI
├── GEMINI.md              # Main context for Gemini CLI
├── README.md              # Module documentation
├── context/               # Context files (.context)
│   ├── persona.context    # Persona definition
│   └── workflow.context   # Workflow instructions
├── scripts/               # Helper scripts
│   └── helper.sh          # Script for heavy lifting
├── templates/             # Templates for generation
│   └── template.md
└── commands/              # AI assistant commands (WIP)
    ├── cursor/            # Cursor-specific commands
    ├── claude/            # Claude CLI commands
    └── gemini/            # Gemini CLI commands
```

**Main Context Files:**
- `AGENTS.md` - For Cursor
- `CLAUDE.md` - For Claude CLI
- `GEMINI.md` - For Gemini CLI

You can create one or multiple main context files depending on which AI assistants you want to support.


## Step 1: Define Your Module in lolamod.yml

Add your module to `modules/lolamod.yml`:

```yaml
version: 0.1.0
lolas:
  - name: your-module
    desc: "Brief description of what this module does"
    path: "./your-module"
    main: AGENTS.md
    dest:
      - cursor
      - claude-cli
      - gemini-cli
    assets:
      - "context"
      - "scripts"
      - "templates"
      - "commands"      # Commands support (work in progress)
```

**Fields:**
- `name`: Module identifier (used for installation)
- `desc`: Short description
- `path`: Relative path from modules directory
- `main`: Main entry file (AGENTS.md for Cursor, CLAUDE.md for Claude CLI, etc.)
- `dest`: Compatible AI assistants
- `assets`: Directories to copy during installation

**Note**: Commands support in Lola is a work in progress and planned for future implementation. When implemented, commands will be automatically installed to the appropriate AI assistant's command directory.

## Step 2: Create Main Context Files

Create main context files for each AI assistant you want to support. The structure is the same across all assistants.

### Example: AGENTS.md (for Cursor)

```markdown
**Name**: Your Module Name
**Version**: 1.0.0
**Description**: What your module does

**Persona**: Load and assume the role from `.lolas/your-module/context/persona.context`

**CRITICAL:**

Monitor user messages for these triggers and inject the appropriate context,
always following the .context files workflows strictly.

**Triggers**:

- "trigger phrase" => Read, Load and execute `.lolas/your-module/context/workflow.context`
- "another trigger" => Read, Load and execute `.lolas/your-module/context/another.context`
```

**Tips:**
 Use `CLAUDE.md` for Claude CLI and `GEMINI.md` for Gemini CLI with the same structure as AGENTS.md.

**Key principles:**
- Define clear triggers for context loading
- Point to specific context files in `.lolas/your-module/`
- Instruct the LLM to follow workflows strictly

## Step 3: Create Persona Context

Define the personality and behavior in `context/persona.context`:

```markdown
**Name**: Your Persona Name
**Description**: Brief persona description

## Persona

You are [role description].

**Your personality:**
- Trait 1
- Trait 2
- Trait 3

**Your communication style:**
- Style guideline 1
- Style guideline 2

**Your expertise:**
- Expertise area 1
- Expertise area 2
```

## Step 4: Create Workflow Contexts

Workflow contexts define step-by-step instructions. Create `context/workflow.context`:

```markdown
**Name**: workflow.context
**Description**: What this workflow does
**Triggers**: List trigger phrases here

## Execution Workflow

1. First step instruction
   __WAIT_USER_RESPONSE__
   => save response as $VARIABLE_NAME = __USER_LAST_RESPONSE__

2. Second step instruction
   Run .lolas/your-module/scripts/helper.sh $VARIABLE_NAME
   => Returns data description

3. Third step based on returned data
   __WAIT_USER_RESPONSE__
   IF $USER_LAST_RESPONSE = "yes" => action
   ELSE IF $USER_LAST_RESPONSE = "no" => other action

4. Final step
```

**Workflow syntax:**
- `__WAIT_USER_RESPONSE__`: Pause and wait for user input
- `$VARIABLE_NAME`: Store user responses or data
- `=>`: Indicates what happens next
- `IF/ELSE`: Conditional logic
- Script calls return structured data (JSON recommended)

## Step 5: Add Helper Scripts (Optional)

Scripts do the heavy lifting - date calculations, API calls, file operations:

```bash
#!/bin/bash
# scripts/helper.sh
# Does complex computation that would waste LLM tokens

# Return clean JSON for LLM to use
echo "{\"key\": \"value\", \"data\": \"result\"}"
```

**Best practices:**
- Let scripts handle computational tasks
- Return structured data (JSON)
- Keep LLM focused on user interaction
- Scripts reduce token usage significantly

## Step 6: Add Templates (Optional)

Templates provide structured formats for content generation:

```markdown
# templates/blog-template.md
---
title: {{TITLE}}
date: {{DATE}}
---

{{CONTENT}}
```

**Note**: There's plans to have commands support, in the future,
those are currently a work in progress.

As a example for a full working module, check the [Chef Buddy
module](../modules/chef-buddy/).

## Installing Your Module

Once created, install it to a directory:

```bash
lola mod install your-module -d /tmp/test
```

This creates:
- `.lolas/your-module/` - Module assets (contexts, scripts, templates, commands)
- `AGENTS.md` (or CLAUDE.md/GEMINI.md) - Main context file for the AI assistant

## Testing Your Module

### For Cursor:

```bash
cd /tmp/test
cursor . # or your preferred project
```

Verify:
- Persona loads correctly
- Triggers activate the right contexts
- Workflows execute step-by-step
- Scripts return proper data
- Wait points work as expected

## Key Concepts

### Lazy Context Loading

Only load instructions when needed. The main context monitors triggers and injects specialized contexts dynamically.

### Context as Functions

Think of contexts as function calls:
- Main context (AGENTS.md/CLAUDE.md/GEMINI.md) = `main()` function
- Workflow contexts = function calls
- Scripts = inline assembly for performance

## Best Practices

1. **Keep contexts focused** - One context, one purpose
2. **Use scripts for heavy lifting** - Date math, API calls, file ops
3. **Clear triggers** - Make trigger phrases obvious
4. **Step-by-step workflows** - Use `__WAIT_USER_RESPONSE__`
5. **Structured data** - Scripts return JSON
6. **Document everything** - Clear README for users
7. **Test thoroughly** - Verify all triggers and workflows
8. **Multi-assistant support** - Create AGENTS.md, CLAUDE.md, and GEMINI.md

## Sharing Your Module

Lola modules are designed to be shared. Once you create a useful module:

1. Document it well
2. Test all workflows across different AI assistants
3. Share via Git repository
4. Others can use your lazy contexts

## Community Context Libraries

The vision is to build standardized, reusable context libraries that can be:
- Downloaded and installed
- Shared across projects
- Community-driven and battle-tested
- Versioned and maintained

Your module contributes to this ecosystem.

## Security Considerations

Context files are powerful - they control LLM behavior:
- Review context files before installation
- Be cautious with scripts from untrusted sources
- Understand what contexts do before loading
- Audit logs can track context loading

## Further Reading

- [Chef Buddy Example Module](../modules/chef-buddy/)
- [Main README](../README.md)

---

_You're not just writing prompts - you're building programs that program the AI._
