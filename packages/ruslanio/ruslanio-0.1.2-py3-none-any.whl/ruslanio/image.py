from pathlib import Path
import numpy as np
import cv2


def imread(path: Path | str) -> np.ndarray:
    img = cv2.imread(str(path))
    assert img is not None, f'Cannot read from {path}'
    return img[:, :, ::-1].copy()


def imwrite(path: Path | str, image: np.ndarray) -> None:
    # Validate the path argument
    if not isinstance(path, (str, Path)):
        raise ValueError("Invalid 'path' argument. Expected a string or Path object.")
    path = Path(path)
    if not path.parent.exists():
        raise ValueError("Invalid 'path' argument. Parent directory does not exist.")
    if path.is_dir():
        raise ValueError("Invalid 'path' argument. Expected a file path, not a directory.")

    # Validate the image array
    if not isinstance(image, np.ndarray):
        raise ValueError("Invalid 'image' argument. Expected a NumPy array.")
    if len(image.shape) != 3 or image.shape[2] != 3:
        raise ValueError("Invalid 'image' argument. Expected a 3-dimensional array with shape (height, width, 3).")
    if not np.issubdtype(image.dtype, np.uint8):
        raise ValueError("Invalid 'image' argument. Expected a NumPy array with data type np.uint8.")

    # Save the image
    cv2.imwrite(str(path), image[:, :, ::-1].copy())
