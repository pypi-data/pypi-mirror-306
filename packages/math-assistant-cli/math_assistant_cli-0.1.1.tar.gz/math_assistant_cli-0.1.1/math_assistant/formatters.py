"""Formatting utilities for Math Assistant responses."""

from typing import Union, Dict, List, Any, Optional, ClassVar
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.theme import Theme
import re
from datetime import datetime

ResponseType = Union[str, Dict[str, Any], List[Any]]


class ResponseFormatter:
    """Handles formatting of responses from the Math Assistant."""

    BOLD: ClassVar[str] = "\033[1m"
    RESET: ClassVar[str] = "\033[0m"

    def __init__(self) -> None:
        """Initialize formatter with custom theme."""
        self.theme: Theme = Theme(
            {
                "info": "cyan",
                "warning": "yellow",
                "error": "red",
                "success": "green",
                "header": "blue bold",
            }
        )
        self.console: Console = Console(theme=self.theme)

    @staticmethod
    def clean_text(response: ResponseType) -> str:
        """Extract and clean text from response."""
        if isinstance(response, str):
            # Extract text from TextBlock if present
            if "TextBlock" in response:
                match = re.search(r'text="([^"]*)"', response, re.DOTALL)
                if match:
                    text = match.group(1)
                else:
                    text = response
            else:
                text = response
        else:
            text = str(response)

        # Clean up the text
        text = text.replace("\\n", "\n")
        text = re.sub(r"\n\s+", "\n", text)  # Remove excess whitespace

        # Remove TextBlock wrapper if present
        text = re.sub(r'\[TextBlock\(text="|", type=\'text\'\)\]', "", text)

        return text.strip()

    @staticmethod
    def format_steps(text: str) -> str:
        """Format step-by-step solutions with proper spacing."""
        lines = text.split("\n")
        formatted_lines = []
        in_step_by_step = False

        for line in lines:
            line = line.strip()

            # Check if we're entering step-by-step section
            if "Step-by-step solution:" in line:
                in_step_by_step = True
                formatted_lines.append("\n" + line + "\n")
                continue

            # Format lettered steps in step-by-step section
            if in_step_by_step and re.match(r"^[a-z]\)", line):
                formatted_lines.append("\n" + line)
                continue

            # Handle numbered sections (1, 2, 3, 4)
            if re.match(r"^\d+\s+[A-Z]", line):
                formatted_lines.append("\n" + line)
                continue

            # Handle bullet points
            if line.startswith("•"):
                formatted_lines.append("  " + line)
                continue

            # Handle regular text
            if line:
                formatted_lines.append(line)

        text = "\n".join(formatted_lines)

        # Fix spacing around major sections
        text = re.sub(r"(\d+\s+[A-Z][^:]+:)", r"\n\1\n", text)

        # Add space between bullet points and next section
        text = re.sub(r"(•[^\n]+)\n(\d+\s+[A-Z])", r"\1\n\n\2", text)

        return text.strip()

    @classmethod
    def rich_print(
        cls,
        response: ResponseType,
        title: str = "Math Assistant Response",
        style: str = "blue",
    ) -> None:
        """Print response using rich formatting with colors and boxes."""
        console: Console = Console()

        # Clean and format the text
        text = cls.clean_text(response)
        text = cls.format_steps(text)

        # Convert to markdown
        md: Markdown = Markdown(text)

        # Create panel with proper styling
        panel: Panel = Panel(
            md,
            title=title,
            border_style=style,
            padding=(1, 2),
            title_align="left",
        )

        # Print with proper spacing
        console.print()
        console.print(panel)
        console.print()

    @classmethod
    def pretty_print(cls, response: ResponseType, show_sections: bool = True) -> None:
        """Format and print response with sections and formatting."""
        text: str = cls.clean_text(response)

        # Format steps if present
        if "Step " in text or "• " in text:
            formatted_text = cls.format_steps(text)
        else:
            formatted_text = text

        print(formatted_text)

    @classmethod
    def to_markdown(
        cls, response: ResponseType, include_frontmatter: bool = False
    ) -> str:
        """Convert response to markdown format for saving or further processing."""
        text: str = cls.clean_text(response)

        # Format steps if present
        if "Step " in text or "• " in text:
            text = cls.format_steps(text)

        # Add frontmatter if requested
        if include_frontmatter:
            frontmatter: str = f"""---
title: Math Assistant Response
date: {datetime.now().strftime('%Y-%m-%d')}
---

"""
            text = frontmatter + text

        return text.strip() + "\n"

    def print_error(self, message: str) -> None:
        """Print error message in red."""
        self.console.print(f"[error]Error: {message}[/error]")

    def print_success(self, message: str) -> None:
        """Print success message in green."""
        self.console.print(f"[success]{message}[/success]")

    def print_warning(self, message: str) -> None:
        """Print warning message in yellow."""
        self.console.print(f"[warning]Warning: {message}[/warning]")
