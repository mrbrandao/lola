# Lola - Loading Lazy Contexts

Lola lets you package AI contexts (personas, workflows, scripts, templates)
into reusable modules that can be shared and installed across projects.
Instead of writing monolithic prompts, you build modular, efficient AI programs.

**Think of it this way:**

- The LLM is a **non-deterministic CPU**
- Your prompts are the **assembly language**
- Lola modules are **libraries** that get loaded only when needed
- Context injection is **lazy loading** for AI instructions

## How Lazy Context Loading Works

To manage AI context as installable modules for LLM assistants,
Lola implements **lazy context loading** - a meta-programming technique for
optimizing LLM workflows through modular, on-demand context injection.

Traditional approach: Load everything into a massive prompt

```
You are a chef and developer and writer and...
[Thousands of tokens of instructions]
```

Lazy context loading approach: Load only what you need, when you need it

```
Main context monitors triggers
User says "chocolate cake"
Load chef persona + baking workflow
Execute step-by-step instructions
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
# Install the module chef-buddy to a test directory
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

When you start your AI assistant:

- Acts as an enthusiastic baking chef (persona loaded) - say `hello` and start
  to interact with the `Chef Baking Buddy`
- Provides step-by-step recipes when you say "chocolate cake" (context injected)
- Creates blog posts when you say "new blog post" (workflow executed)

## LoLas

Well we need a way to share all those cool, contexts, that's why
Lola Modules were created. modules are called **LoLas** from `Load Lazy`

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

Also check the [Chef Baking Buddy Module](modules/chef-buddy) as example, with a
module that makes your LLM become a cooking chef using a lola module.

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

[GPL-2.0-or-later](https://spdx.org/licenses/GPL-2.0-or-later.html)

## Author

Igor Brandao

---

_The AI is a CPU. Prompts are the assembly. Lazy context loading is your
build system._
