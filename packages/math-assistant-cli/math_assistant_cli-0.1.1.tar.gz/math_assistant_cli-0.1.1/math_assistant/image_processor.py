"""Image processing utilities for Math Assistant."""

from PIL import Image
import io
import base64
from pathlib import Path
from typing import Union, Tuple, Optional, List, ClassVar, TypedDict, Literal
from .exceptions import ImageProcessingError
from .config import Config

# Type aliases
ImagePath = Union[str, Path]
ImageSize = Tuple[int, int]
ImageMode = Literal["RGB", "RGBA"]
EncodedImage = str


class ImageInfo(TypedDict):
    """Type definition for image information dictionary."""

    dimensions: ImageSize
    format: str
    mode: str
    estimated_size: int
    issues: List[str]


class ImageProcessor:
    """Handles image processing operations."""

    # Class variables with explicit types
    VALID_MODES: ClassVar[List[ImageMode]] = ["RGB", "RGBA"]
    DEFAULT_QUALITY: ClassVar[int] = 95

    @staticmethod
    def validate_image(image_path: ImagePath) -> Path:
        """Validate image file exists and has supported format."""
        try:
            path: Path = Path(image_path)
            if not path.exists():
                raise ImageProcessingError(f"Image file not found: {path}")
            if path.suffix.lower() not in Config.SUPPORTED_FORMATS:
                raise ImageProcessingError(
                    f"Unsupported image format: {path.suffix}. "
                    f"Supported formats: {', '.join(Config.SUPPORTED_FORMATS)}"
                )
            return path
        except Exception as e:
            raise ImageProcessingError(f"Error validating image: {str(e)}")

    @staticmethod
    def process_image(
        image_path: ImagePath,
        max_size: Optional[int] = None,
        quality: Optional[int] = None,
    ) -> Tuple[EncodedImage, ImageSize]:
        """Process and encode image for API submission."""
        try:
            # Validate image path
            path: Path = ImageProcessor.validate_image(image_path)

            # Use default values if not specified
            max_size = max_size or Config.MAX_IMAGE_SIZE
            quality = quality or ImageProcessor.DEFAULT_QUALITY

            with Image.open(path) as img:
                # Convert to RGB if necessary
                if img.mode not in ImageProcessor.VALID_MODES:
                    img = img.convert("RGB")

                # Get original size
                width: int
                height: int
                width, height = img.size

                # Resize if needed, maintaining aspect ratio
                if width > max_size or height > max_size:
                    ratio: float = min(max_size / width, max_size / height)
                    new_size: ImageSize = (int(width * ratio), int(height * ratio))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)

                # Convert to JPEG format for consistency
                buffer: io.BytesIO = io.BytesIO()
                img.save(
                    buffer,
                    format="JPEG",
                    quality=quality,
                    optimize=True,
                )

                # Encode to base64
                encoded: EncodedImage = base64.b64encode(buffer.getvalue()).decode(
                    "utf-8"
                )

                return encoded, img.size

        except Exception as e:
            raise ImageProcessingError(f"Error processing image {image_path}: {str(e)}")

    @staticmethod
    def estimate_file_size(image_path: ImagePath) -> int:
        """Estimate file size after processing."""
        try:
            path: Path = ImageProcessor.validate_image(image_path)
            with Image.open(path) as img:
                buffer: io.BytesIO = io.BytesIO()
                img.save(buffer, format="JPEG", quality=ImageProcessor.DEFAULT_QUALITY)
                return len(buffer.getvalue())
        except Exception as e:
            raise ImageProcessingError(f"Error estimating file size: {str(e)}")

    @staticmethod
    def check_image(image_path: ImagePath) -> ImageInfo:
        """Check image properties and potential issues."""
        try:
            path: Path = ImageProcessor.validate_image(image_path)
            with Image.open(path) as img:
                info: ImageInfo = {
                    "dimensions": img.size,
                    "format": str(img.format),
                    "mode": str(img.mode),
                    "estimated_size": path.stat().st_size,
                    "issues": [],
                }

                # Check potential issues
                if max(img.size) > Config.MAX_IMAGE_SIZE:
                    info["issues"].append(
                        f"Image will be resized (max dimension: {Config.MAX_IMAGE_SIZE})"
                    )
                if img.mode not in ImageProcessor.VALID_MODES:
                    info["issues"].append(
                        f"Image will be converted to RGB (current mode: {img.mode})"
                    )

                return info

        except Exception as e:
            raise ImageProcessingError(f"Error checking image: {str(e)}")
