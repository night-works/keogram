from keogram.keogram import valid_image
import pytest


@pytest.mark.parametrize("valid_format", ["jpg", "gif", "png", "jpeg"])
def test_valid_image_formats(valid_format):
    assert valid_image(f"/something/test.{valid_format}")


@pytest.mark.parametrize("invalid_format", ["tif", "dng", "raw"])
def test_invalid_image_formats(invalid_format):
    assert not valid_image(f"/something/test.{invalid_format}")
