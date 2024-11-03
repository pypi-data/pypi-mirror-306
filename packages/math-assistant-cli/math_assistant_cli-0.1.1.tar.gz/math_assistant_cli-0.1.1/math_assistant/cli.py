"""Command Line Interface for Math Assistant."""

import click
import sys
import os
import time
from pathlib import Path
from typing import Optional, List
from click.core import Context
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from .math_assistant import MathAssistant
from .exceptions import ConfigurationError, ImageProcessingError

# Initialize rich console
console = Console()


class CLIError(Exception):
    """Base exception for CLI errors."""

    pass


def check_environment() -> None:
    """Verify environment setup."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ConfigurationError(
            "No API key found. Please set your ANTHROPIC_API_KEY environment variable."
        )


def print_welcome() -> None:
    """Print welcome message and instructions."""
    welcome_text = """
# Math Assistant

Welcome! Here's how to use the assistant:

## Commands:
- `image: path/to/image.jpg` - Load and analyze a math problem
- `practice` - Get similar practice problems (after loading an image)
- `check` - Check a solution (after loading an image)
- `save: filename.txt` - Save conversation
- `help` - Show these instructions
- `quit` - Exit the program

## Example:
```
> image: calculus_problem.jpg
> Can you explain the first step?
> What formula should I use here?
> practice
> save: my_session.txt
```
    """
    console.print(Markdown(welcome_text))


def handle_error(error: Exception) -> None:
    """Handle different types of errors with user-friendly messages."""
    if isinstance(error, ConfigurationError):
        console.print(
            Panel(
                """[red]API Key Error:[/red]
Please set your Anthropic API key:

1. Export as environment variable:
   [yellow]export ANTHROPIC_API_KEY='your-api-key'[/yellow]

Get your API key at: https://console.anthropic.com/
            """,
                title="🔑 API Key Required",
                border_style="red",
            )
        )

    elif isinstance(error, ImageProcessingError):
        console.print(
            Panel(
                f"""[red]Image Error:[/red] {str(error)}

Supported formats: JPG, JPEG, PNG
Maximum size: 2048x2048 pixels

Tips:
• Verify the file exists and is readable
• Check the file format
• Try reducing image size if too large
            """,
                title="🖼️ Image Processing Error",
                border_style="red",
            )
        )

    elif "rate limit" in str(error).lower():
        console.print(
            Panel(
                "[yellow]Rate limit reached. Waiting 5 seconds...[/yellow]",
                title="⏱️ Rate Limit",
                border_style="yellow",
            )
        )
        time.sleep(5)
        return

    else:
        console.print(
            Panel(
                f"[red]Error:[/red] {str(error)}", title="❌ Error", border_style="red"
            )
        )


def handle_image_command(assistant: MathAssistant, image_path: str) -> bool:
    """Handle loading and processing an image."""
    try:
        path = Path(image_path.strip())
        if not path.exists():
            raise ImageProcessingError(f"Image not found: {path}")

        if path.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
            raise ImageProcessingError("Unsupported format. Use JPG or PNG.")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(description="Analyzing image...", total=None)
            try:
                assistant.ask_about_problem(str(path), "Can you explain this problem?")
                console.print("[green]✓ Image processed successfully[/green]")
                return True
            except Exception as e:
                if "rate limit" in str(e).lower():
                    handle_error(e)
                    # Retry once after rate limit
                    assistant.ask_about_problem(
                        str(path), "Can you explain this problem?"
                    )
                    return True
                raise

    except Exception as e:
        handle_error(e)
        return False


def get_multiline_input(prompt: str) -> str:
    """Get multiline input from user."""
    console.print(f"\n{prompt} (Press Ctrl+D or Ctrl+Z when finished):")
    lines: List[str] = []
    try:
        while True:
            line = input()
            lines.append(line)
    except (EOFError, KeyboardInterrupt):
        return "\n".join(lines)


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx: Context) -> None:
    """Math Assistant CLI - Get help with math problems using AI."""
    try:
        check_environment()
        if ctx.invoked_subcommand is None:
            ctx.invoke(interactive)
    except Exception as e:
        handle_error(e)
        sys.exit(1)


@main.command()
def interactive() -> None:
    """Start an interactive session."""
    try:
        assistant = MathAssistant()
        current_image: Optional[str] = None
        print_welcome()

        while True:
            try:
                # Show appropriate prompt
                if current_image:
                    prompt = f"\n[Current image: {current_image}]\nYour command"
                else:
                    prompt = "\nYour command"

                command = click.prompt(prompt, prompt_suffix=" > ")

                # Handle commands
                if command.lower() == "quit":
                    console.print("[blue]Goodbye! 👋[/blue]")
                    break

                elif command.lower() == "help":
                    print_welcome()

                elif command.lower().startswith("image:"):
                    image_path = command.split(":", 1)[1].strip()
                    if handle_image_command(assistant, image_path):
                        current_image = image_path

                elif command.lower().startswith("save:"):
                    try:
                        filename = command.split(":", 1)[1].strip()
                        assistant.save_conversation(filename)
                        console.print(
                            f"[green]✓ Conversation saved to {filename}[/green]"
                        )
                    except Exception as e:
                        console.print(f"[red]Error saving file:[/red] {str(e)}")

                elif command.lower() == "practice":
                    if current_image:
                        with Progress(
                            SpinnerColumn(),
                            TextColumn("[progress.description]{task.description}"),
                        ) as progress:
                            progress.add_task(
                                description="Generating practice problems...",
                                total=None,
                            )
                            assistant.generate_similar_problems(current_image)
                    else:
                        console.print(
                            "[red]Please load an image first using 'image: path/to/image.jpg'[/red]"
                        )

                elif command.lower() == "check":
                    if current_image:
                        solution = get_multiline_input("Enter your solution")
                        with Progress(
                            SpinnerColumn(),
                            TextColumn("[progress.description]{task.description}"),
                        ) as progress:
                            progress.add_task(
                                description="Checking solution...", total=None
                            )
                            assistant.check_solution(current_image, solution)
                    else:
                        console.print(
                            "[red]Please load an image first using 'image: path/to/image.jpg'[/red]"
                        )

                else:
                    if current_image:
                        assistant.continue_conversation(command)
                    else:
                        console.print(
                            "[red]Please load an image first using 'image: path/to/image.jpg'[/red]"
                        )

            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'quit' to exit properly[/yellow]")
            except Exception as e:
                handle_error(e)

    except Exception as e:
        handle_error(e)
        sys.exit(1)


@main.command()
@click.argument("image", type=click.Path(exists=True))
@click.option(
    "--format",
    "-f",
    type=click.Choice(["basic", "pretty", "rich"]),
    default="rich",
    help="Output format style",
)
def explain(image: str, format: str) -> None:
    """Explain a math problem from an image."""
    try:
        assistant = MathAssistant()
        with Progress(
            SpinnerColumn(), TextColumn("[progress.description]{task.description}")
        ) as progress:
            progress.add_task(description="Analyzing problem...", total=None)
            assistant.explain_problem(image, format_style=format)
    except Exception as e:
        handle_error(e)
        sys.exit(1)
