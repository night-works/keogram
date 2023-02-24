import pytest
from PIL import Image
import os
from keogram.keogram import valid_image, concat_images, create


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

@pytest.mark.parametrize("valid_format", ["jpg", "gif", "png", "jpeg", "JPG", "GIF", "PNG", "JPEG"])
def test_valid_image_formats(valid_format):
    assert valid_image(f"/something/test.{valid_format}")


@pytest.mark.parametrize("invalid_format", ["tif", "dng", "raw", "pdf", "tiff", "TIF", "DNG", "RAW", "TIFF"])
def test_invalid_image_formats(invalid_format):
    assert not valid_image(f"/something/test.{invalid_format}")


def test_concat_images():
    first = Image.new("RGB", (10, 10))
    second = Image.new("RGB", (15, 10))
    result = concat_images(first, second)
    assert result.width == 25
    assert result.height == 10


def test_concat_second_image_taller():
    first = Image.new("RGB", (10, 10))
    second = Image.new("RGB", (15, 30))
    result = concat_images(first, second)
    assert result.width == 25
    assert result.height == 30


def test_concat_first_image_taller():
    first = Image.new("RGB", (10, 50))
    second = Image.new("RGB", (15, 30))
    result = concat_images(first, second)
    assert result.width == 25
    assert result.height == 30


def test_source_not_file():
    with pytest.raises(NotADirectoryError):
        create(f"{ROOT_DIR}/test_keogram.py", "")


def test_source_directory_not_exist():
    with pytest.raises(NotADirectoryError):
        create(f"{ROOT_DIR}/not_found/", "")
