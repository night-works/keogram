#  MIT License
#
#  Copyright (c) 2023 Night Works
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#

import logging
from os import PathLike, path, makedirs, listdir
from typing import Union

from PIL import Image

logger = logging.getLogger(__name__)

valid_images = [".jpg", ".gif", ".png", ".jpeg"]


def create(source: Union[str, PathLike], destination: Union[str, PathLike], keogram_file: str = "keogram.jpg") -> None:
    """
    Creates a Keogram from all the image files found in the source directory and saves the resulting image in
    destination/keogram_file.

    Args:
        source: location of the images to be processed
        destination: destination directory to save the resulting keogram
        keogram_file: file name for the resulting image defaults to keogram.jpg

    Raises:
        NotADirectoryError: if the source is a file or the directory can not be found
    """
    if path.exists(source):
        logger.debug('%s exists on the file system', source)
        if path.isfile(source):
            logger.error('%s is not a directory', source)
            raise NotADirectoryError('%s is not a directory', source)
        else:
            if not path.exists(destination):
                logger.debug('%s does not exist, creating directories', destination)
                makedirs(destination)
            logger.debug('source and destination directories exist beginning to process images')
            process_images(source, destination, keogram_file)
    else:
        logger.error('%s does not exist', source)
        raise NotADirectoryError('%s does not exist', source)


def process_images(source: Union[str, PathLike], destination: Union[str, PathLike], file_name: str) -> None:
    keogram_image = Image.new("RGB", (0, 0))

    sorted_files = sorted(listdir(source))
    logger.debug(f"source directory contains {len(sorted_files)} files")

    for file_item in sorted_files:
        if not valid_image(file_item):
            logger.warning(f"{file_item} is not a valid image type")
            continue
        current_image = Image.open(path.join(source, file_item))
        image_middle = int(current_image.width / 2)
        center_slice = (image_middle, 0, image_middle + 1, current_image.height)
        current_image = current_image.crop(center_slice)
        keogram_image = concat_images(keogram_image, current_image)

    file_destination = f"{destination}/{file_name}"
    keogram_image.save(file_destination)


def valid_image(file: Union[str, PathLike]) -> bool:
    file_extension = path.splitext(file)[1]
    logger.debug(f"checking image type of {file} with extension of {file_extension}")
    return file_extension.lower() in valid_images


def concat_images(left_image: Image, right_image: Image) -> Image:
    logger.debug("concatenating base image with new image slice")
    logger.debug(f"base image size {left_image.width} x {left_image.height}")
    new_image = Image.new('RGB', (left_image.width + right_image.width, right_image.height))
    new_image.paste(left_image, (0, 0))
    new_image.paste(right_image, (left_image.width, 0))
    logger.debug(f"new image size {new_image.width} x {new_image.height}")
    return new_image
