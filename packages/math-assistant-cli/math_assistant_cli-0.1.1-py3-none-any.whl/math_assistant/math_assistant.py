"""Main Math Assistant implementation."""

import anthropic
from typing import Optional, Dict, List, Union, Any
from pathlib import Path
from .config import Config
from .exceptions import APIError, ConfigurationError
from .image_processor import ImageProcessor
from .formatters import ResponseFormatter


class MathAssistant:
    """A class to help with mathematics problems using Claude API."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Math Assistant.

        Args:
            api_key: Optional API key. If not provided, will use environment variable.
        """
        self.api_key = api_key or Config.ANTHROPIC_API_KEY
        if not self.api_key:
            raise ConfigurationError("No API key provided")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.conversation_history: List[Dict[str, Any]] = []
        Config.initialize()

    def _get_explanation(
        self, image_path: Union[str, Path], additional_text: str
    ) -> dict:
        """Internal method to get explanation from API."""
        try:
            encoded_image, _ = ImageProcessor.process_image(image_path)

            message = self.client.messages.create(
                model=Config.DEFAULT_MODEL,
                max_tokens=Config.DEFAULT_MAX_TOKENS,
                temperature=0,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": encoded_image,
                                },
                            },
                            {
                                "type": "text",
                                "text": f"""Please help me with this math problem. {additional_text}

                                Provide:
                                1. Concepts being tested
                                2. Step-by-step solution
                                3. Key points to remember
                                4. Common mistakes to avoid""",
                            },
                        ],
                    }
                ],
            )

            return message.content

        except anthropic.APIError as e:
            raise APIError(f"API error: {str(e)}")

    def _generate_problems(
        self, image_path: Union[str, Path], num_problems: int
    ) -> dict:
        """Internal method to generate similar problems."""
        try:
            encoded_image, _ = ImageProcessor.process_image(image_path)

            message = self.client.messages.create(
                model=Config.DEFAULT_MODEL,
                max_tokens=Config.DEFAULT_MAX_TOKENS * 2,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": encoded_image,
                                },
                            },
                            {
                                "type": "text",
                                "text": f"""Generate {num_problems} similar practice problems that test
                                the same concepts. For each problem, provide:
                                1. Problem statement
                                2. Complete solution
                                3. Difficulty level compared to original
                                4. Key concepts being tested""",
                            },
                        ],
                    }
                ],
            )

            return message.content

        except anthropic.APIError as e:
            raise APIError(f"API error: {str(e)}")

    def _check_solution(
        self, image_path: Union[str, Path], student_solution: str
    ) -> dict:
        """Internal method to check solution."""
        try:
            encoded_image, _ = ImageProcessor.process_image(image_path)

            message = self.client.messages.create(
                model=Config.DEFAULT_MODEL,
                max_tokens=Config.DEFAULT_MAX_TOKENS,
                temperature=0,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": encoded_image,
                                },
                            },
                            {
                                "type": "text",
                                "text": f"""Review this solution:

                                Student solution:
                                {student_solution}

                                Please provide:
                                1. Correctness assessment
                                2. Detailed feedback on each step
                                3. Suggestions for improvement
                                4. Alternative solution methods
                                5. Conceptual understanding assessment""",
                            },
                        ],
                    }
                ],
            )

            return message.content

        except anthropic.APIError as e:
            raise APIError(f"API error: {str(e)}")

    def explain_problem(
        self,
        image_path: Union[str, Path],
        additional_text: str = "",
        format_output: bool = True,
        format_style: str = "basic",
    ) -> Union[Dict, str]:
        """Get explanation for a math problem from an image.

        Args:
            image_path: Path to the image file
            additional_text: Optional additional context or questions
            format_output: Whether to format the output (default: True)
            format_style: Formatting style ('basic', 'pretty', or 'rich')

        Returns:
            Formatted explanation if format_output=True, otherwise raw response
        """
        response = self._get_explanation(image_path, additional_text)

        if not format_output:
            return response

        if format_style == "pretty":
            ResponseFormatter.pretty_print(response)
        elif format_style == "rich":
            ResponseFormatter.rich_print(response, title="Math Problem Explanation")
        else:
            return ResponseFormatter.clean_text(response)

    def generate_similar_problems(
        self,
        image_path: Union[str, Path],
        num_problems: int = 3,
        format_output: bool = True,
        format_style: str = "basic",
    ) -> Union[List[Dict], str]:
        """Generate similar practice problems based on an image.

        Args:
            image_path: Path to the image file
            num_problems: Number of similar problems to generate
            format_output: Whether to format the output (default: True)
            format_style: Formatting style ('basic', 'pretty', or 'rich')

        Returns:
            Formatted problems if format_output=True, otherwise raw response
        """
        response = self._generate_problems(image_path, num_problems)

        if not format_output:
            return response

        if format_style == "pretty":
            ResponseFormatter.pretty_print(response)
        elif format_style == "rich":
            ResponseFormatter.rich_print(response, title="Similar Problems")
        else:
            return ResponseFormatter.clean_text(response)

    def check_solution(
        self,
        image_path: Union[str, Path],
        student_solution: str,
        format_output: bool = True,
        format_style: str = "basic",
    ) -> Union[Dict, str]:
        """Check a student's solution against a problem from an image.

        Args:
            image_path: Path to the image file
            student_solution: The student's attempted solution
            format_output: Whether to format the output (default: True)
            format_style: Formatting style ('basic', 'pretty', or 'rich')

        Returns:
            Formatted feedback if format_output=True, otherwise raw response
        """
        response = self._check_solution(image_path, student_solution)

        if not format_output:
            return response

        if format_style == "pretty":
            ResponseFormatter.pretty_print(response)
        elif format_style == "rich":
            ResponseFormatter.rich_print(response, title="Solution Feedback")
        else:
            return ResponseFormatter.clean_text(response)

    def start_conversation(
        self, image_path: Optional[str] = None, format_style: str = "rich"
    ) -> str:
        """Start a new conversation about a math problem.

        Args:
            image_path: Optional path to problem image
            format_style: Output formatting style

        Returns:
            Initial response from assistant
        """
        self.conversation_history = []

        if image_path:
            return self.ask_about_problem(
                image_path, "Can you explain this problem?", format_style=format_style
            )

        response = "Conversation started. How can I help you with mathematics today?"
        if format_style == "rich":
            ResponseFormatter.rich_print(response, title="Conversation Start")
        elif format_style == "pretty":
            ResponseFormatter.pretty_print(response)
        else:
            return ResponseFormatter.clean_text(response)
        return response

    def ask_about_problem(
        self, image_path: str, question: str, format_style: str = "rich"
    ) -> str:
        """Ask a specific question about a problem.

        Args:
            image_path: Path to problem image
            question: User's question
            format_style: Output formatting style
        """
        try:
            encoded_image, _ = ImageProcessor.process_image(image_path)

            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": question})

            message = self.client.messages.create(
                model=Config.DEFAULT_MODEL,
                max_tokens=Config.DEFAULT_MAX_TOKENS,
                temperature=0,
                messages=[
                    *self.conversation_history,
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": encoded_image,
                                },
                            },
                            {"type": "text", "text": question},
                        ],
                    },
                ],
            )

            response = message.content
            self.conversation_history.append({"role": "assistant", "content": response})

            if format_style == "pretty":
                ResponseFormatter.pretty_print(response)
            elif format_style == "rich":
                ResponseFormatter.rich_print(response)
            else:
                return ResponseFormatter.clean_text(response)

            return response

        except Exception as e:
            raise APIError(f"Error: {str(e)}")

    def continue_conversation(self, question: str, format_style: str = "rich") -> str:
        """Continue the conversation with a follow-up question.

        Args:
            question: User's follow-up question
            format_style: Output formatting style
        """
        try:
            self.conversation_history.append({"role": "user", "content": question})

            message = self.client.messages.create(
                model=Config.DEFAULT_MODEL,
                max_tokens=Config.DEFAULT_MAX_TOKENS,
                temperature=0,
                messages=[*self.conversation_history],
            )

            response = message.content
            self.conversation_history.append({"role": "assistant", "content": response})

            if format_style == "pretty":
                ResponseFormatter.pretty_print(response)
            elif format_style == "rich":
                ResponseFormatter.rich_print(response)
            else:
                return ResponseFormatter.clean_text(response)

            return response

        except Exception as e:
            raise APIError(f"Error: {str(e)}")

    def save_conversation(self, filename: str) -> None:
        """Save the current conversation to a file.

        Args:
            filename: Path where to save the conversation
        """
        with open(filename, "w") as f:
            for message in self.conversation_history:
                role = message["role"].upper()
                if isinstance(message["content"], str):
                    content = message["content"]
                else:
                    # Handle cases where content might be a list of message parts
                    content = str(message["content"])
                f.write(f"{role}: {content}\n\n")

    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the current conversation history.

        Returns:
            List of conversation messages
        """
        return self.conversation_history
