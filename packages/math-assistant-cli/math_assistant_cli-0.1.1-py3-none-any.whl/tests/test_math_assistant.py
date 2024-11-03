import pytest
from pathlib import Path
from math_assistant import MathAssistant
from math_assistant.exceptions import ConfigurationError, ImageProcessingError


class TestMathAssistant:
    @pytest.fixture
    def assistant(self):
        return MathAssistant()

    @pytest.fixture
    def test_image(self):
        return Path(__file__).parent / "test_files" / "test_problem.jpg"

    def test_initialization_without_api_key(self):
        with pytest.raises(ConfigurationError):
            MathAssistant(api_key=None)

    def test_explain_problem(self, assistant, test_image):
        explanation = assistant.explain_problem(test_image)
        assert explanation is not None
        assert isinstance(explanation, dict)

    def test_generate_similar_problems(self, assistant, test_image):
        problems = assistant.generate_similar_problems(test_image)
        assert problems is not None
        assert isinstance(problems, list)
        assert len(problems) > 0

    def test_check_solution(self, assistant, test_image):
        feedback = assistant.check_solution(test_image, "Test solution")
        assert feedback is not None
        assert isinstance(feedback, dict)

    def test_invalid_image_path(self, assistant):
        with pytest.raises(ImageProcessingError):
            assistant.explain_problem("nonexistent.jpg")

    def test_unsupported_image_format(self, assistant):
        with pytest.raises(ImageProcessingError):
            assistant.explain_problem("test.gif")
