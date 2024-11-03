import pytest
from pathlib import Path
from math_assistant.image_processor import ImageProcessor
from math_assistant.exceptions import ImageProcessingError


class TestImageProcessor:
    @pytest.fixture
    def test_image(self):
        return Path(__file__).parent / "test_files" / "test_problem.jpg"

    def test_validate_image_valid(self, test_image):
        path = ImageProcessor.validate_image(test_image)
        assert isinstance(path, Path)
        assert path.exists()

    def test_validate_image_nonexistent(self):
        with pytest.raises(ImageProcessingError):
            ImageProcessor.validate_image("nonexistent.jpg")

    def test_validate_image_unsupported_format(self):
        with pytest.raises(ImageProcessingError):
            ImageProcessor.validate_image("test.gif")

    def test_process_image(self, test_image):
        encoded, size = ImageProcessor.process_image(test_image)
        assert isinstance(encoded, str)
        assert len(encoded) > 0
        assert isinstance(size, tuple)
        assert len(size) == 2

    def test_process_image_resize(self, test_image):
        encoded, size = ImageProcessor.process_image(test_image)
        assert max(size) <= 2048  # Max size from config
