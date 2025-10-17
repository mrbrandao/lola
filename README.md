# Lola - Loading Lazy Contexts

A tool to manage AI context as installable modules for LLM assistants. 
Lola implements **lazy context loading** - a meta-programming technique for 
optimizing LLM workflows through modular, on-demand context injection.

## What is Lola?

Lola lets you package AI contexts (personas, workflows, scripts, templates) 
into reusable modules that can be shared and installed across projects. 
Instead of writing monolithic prompts, you build modular, efficient AI programs.

**Think of it this way:**
- The LLM is a **non-deterministic CPU**
- Your prompts are the **assembly language**
- Lola modules are **libraries** that get loaded only when needed
- Context injection is **lazy loading** for AI instructions

## How Lazy Context Loading Works

Traditional approach: Load everything into a massive prompt

```
You are a chef and developer and writer and...
[Thousands of tokens of instructions]
```

Lazy context loading approach: Load only what you need, when you need it

```
Main context monitors triggers ’
User says "chocolate cake" ’
Load chef persona + baking workflow ’
Execute step-by-step instructions ’
Unload when done
```

## Installation

```bash
# Clone the repository
git clone https://github.com/mrbrandao/lola
cd lola

# Install with uv
uv pip install -e .

# Or with pip
pip install -e .
```

## Quick Start

### 1. List available modules

```bash
lola mod ls
```

### 2. Install a module

```bash
# Install to a test directory
lola mod install chef-buddy -d /tmp/test
```

This creates:
- `.lolas/chef-buddy/` - Module assets (contexts, scripts, templates)
- `AGENTS.md` - Main context file (for Cursor)

### 3. Test the module

```bash
cd /tmp/test
cursor .
```

Now your AI assistant:
- Acts as an enthusiastic baking chef (persona loaded)
- Provides step-by-step recipes when you say "chocolate cake" (context injected)
- Creates blog posts when you say "new blog post" (workflow executed)

## How It Works

Lola modules use a structured approach to context management:

### 1. Main Context File

The entry point - like a `main()` function:

```markdown
**Name**: Chef Buddy
**Persona**: Load from `.lolas/chef-buddy/context/persona.context`

**Triggers**:
- "chocolate cake" => Load `.lolas/chef-buddy/context/chocolate-cake.context`
- "new blog post" => Load `.lolas/chef-buddy/context/blog.context`
```

**Main context files by AI assistant:**
- `AGENTS.md` - For Cursor
- `CLAUDE.md` - For Claude CLI
- `GEMINI.md` - For Gemini CLI

### 2. Context Files

Specialized instructions loaded on-demand:

```markdown
**Name**: chocolate-cake.context
**Description**: Step-by-step chocolate cake baking

## Execution Workflow
1. Preheat oven to 350°F
   __WAIT_USER_RESPONSE__
2. Mix dry ingredients
   __WAIT_USER_RESPONSE__
3. Add wet ingredients
   ...
```

### 3. Helper Scripts

Scripts do the heavy lifting (date calculations, API calls, file operations):

```bash
#!/bin/bash
# Returns clean JSON for LLM to use
echo '{"today": "2025-01-01T00:00:00Z", "file": "blog/post.md"}'
```

### 4. Workflow Control

Contexts use special syntax for control flow:

- `__WAIT_USER_RESPONSE__` - Pause and wait for user input
- `$VARIABLE = __USER_LAST_RESPONSE__` - Store user responses
- `IF/ELSE` - Conditional logic
- `=> run script.sh` - Execute helper scripts

## LoLas Modules

Well we need to have a way to share all those cool, contexts, that's why
Lola Modules were created. Lola modules are called **LoLas** from `Load Lazy`

Now that you know how Lola works, what about help us to extend lola with you own
modules?

Here's the quick overview on how to create your own modules.

1. Create module structure in `modules/your-module/`
2. Define module in `modules/lolamod.yml`
3. Create main context file (AGENTS.md, CLAUDE.md, or GEMINI.md)
4. Add persona and workflow contexts
5. Add helper scripts and templates
6. Test and share

See the complete guide on **[Creating Lola Modules](docs/modules.md)**

Also check the [Chef Baking Buddy Module](modules/chef-buddy) as example

## Further Reading

- **[Creating Lola Modules](docs/modules.md)** - Complete guide to building modules
- **[Chef Buddy Example](modules/chef-buddy/)** - Working example module
- **[Vision and Roadmap](docs/roadmap.md)** - Future plans for Lola

## Contributing

Lola is an experimental project exploring lazy context loading patterns. 
Contributions welcome:

1. Create new context modules
2. Improve existing modules
3. Add features to the CLI
4. Share your use cases

## License

[Add your license here]

## Author

Igor Brandao

---

_The AI is a CPU. Prompts are the assembly. Lazy context loading is your 
build system._
