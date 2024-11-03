# Math Assistant CLI

A command-line tool that uses Claude AI to help with math problems. Just show it a picture of your math problem and get explanations, similar practice problems, and solution checking.

## Installation

```bash
pip install math-assistant-cli
```

You'll need an Anthropic API key. Set it as an environment variable:
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

## Quick Start

1. Explain a problem:
```bash
math-assist explain problem.jpg
```

2. Interactive mode:
```bash
math-assist
```

3. Different formatting:
```bash
math-assist explain problem.jpg --format rich
```

## Features

- 📸 Upload images of math problems
- 💬 Get step-by-step explanations
- 🏋️ Generate similar practice problems
- ✅ Check your solutions
- 💾 Save conversations for later
- 🎨 Multiple output formats

## Interactive Commands

When in interactive mode:
- `image: path/to/image.jpg` - Load a new problem
- `save` - Save the conversation
- `quit` - Exit

## Examples

1. Quick explanation:
```bash
math-assist explain calc_problem.jpg
```

2. Interactive session:
```bash
math-assist
> image: integral.jpg
> Can you explain the first step?
> How do I know which substitution to use?
> save conversation.txt
> quit
```

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT License - see [LICENSE](LICENSE) for details.
