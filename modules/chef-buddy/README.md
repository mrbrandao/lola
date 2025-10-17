# Chef Buddy

A Lola module demonstrating lazy context loading - transforms your AI assistant into an enthusiastic baking chef who guides you through recipes step-by-step.

## What is it?

Chef Buddy is a lazy context module that loads a professional chef persona with interactive baking workflows. This module demonstrates key concepts of lazy context loading:

- **On-demand context injection** - Persona and workflows load only when triggered
- **Workflow control** - Step-by-step execution with wait points
- **Script integration** - Helper scripts handle heavy lifting
- **Modular contexts** - Reusable, focused context files

The assistant stays in character, provides recipe guidance, and even helps create blog posts about your baking adventures.

## Features

- **Interactive Baking**: Step-by-step chocolate cake recipe with wait points
- **Blog Creation**: Automated blog post generation with templates
- **Chef Persona**: Enthusiastic, encouraging personality that never breaks character
- **Context Workflows**: Trigger-based context loading for different tasks

## Installation

This module is designed for Cursor. Install it to your project directory:

```bash
lola mod install chef-buddy -d /tmp/test
```

This installs the module to `/tmp/test/.lolas/chef-buddy/` and copies `AGENTS.md` to `/tmp/test/`.

## Testing

```bash
cd /tmp/test
cursor .
```

Cursor will load the chef-buddy context and you can start interacting with your baking assistant.

## Usage

Once installed, your AI assistant will recognize these triggers:

- **"chocolate cake"** - Launches interactive chocolate cake baking guide
- **"new blog post"** - Creates a new blog entry with templates
- **General chat** - Maintains chef persona for baking questions

The assistant automatically loads contexts from `.lolas/chef-buddy/context/` based on your requests.

## How Lazy Context Loading Works

Chef Buddy demonstrates the lazy context loading pattern:

1. **Main Context** (`AGENTS.md`) - Monitors for trigger phrases
2. **Persona Loading** - Loads `context/persona.context` for chef personality
3. **Trigger Detection** - User says "chocolate cake"
4. **Context Injection** - Loads `context/chocolate-cake.context` on-demand
5. **Workflow Execution** - Follows step-by-step instructions
6. **Wait Points** - `__WAIT_USER_RESPONSE__` pauses between steps
7. **Script Integration** - Helper scripts return structured data

This approach reduces token usage and creates focused, efficient AI interactions.

## Structure

```
.lolas/chef-buddy/
├── context/           # Persona and workflow definitions
├── templates/         # Blog post templates
└── scripts/           # Helper scripts for blog management
```
