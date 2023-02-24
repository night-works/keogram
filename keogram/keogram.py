import argparse
import logging
import time
from os import PathLike, path, makedirs, listdir
from typing import Union

from PIL import Image

logger = logging.getLogger(__name__)

valid_images = [".jpg", ".gif", ".png", ".jpeg"]


def create(source: Union[str, PathLike], destination: Union[str, PathLike], keogram_file: str = "keogram.jpg") -> None:
    if path.exists(source):
        logger.debug(f"{source} exists on the file system")
        if not path.exists(destination):
            logger.debug(f"{source} doesn't exists with create path.")
            makedirs(destination)
        if path.isfile(source):
            message = f"{source} is not a directory"
            logger.error(message)
            raise NotADirectoryError(message)
        else:
            logger.debug("source and destination directories exist beginning to process images")
            process_images(source, destination, keogram_file)
    else:
        message = f"{source} doesn't exist"
        logger.error(message)
        raise NotADirectoryError(message)


def process_images(source, destination, file_name):
    start = time.perf_counter()
    keogram = Image.new("RGB", (0, 0))

    sorted_files = sorted(listdir(source))
    logger.debug(f"source directory contains {len(sorted_files)} files")
    invalid_files = 0

    for file_item in sorted_files:
        if not valid_image(file_item):
            logger.warning(f"{file_item} is not a valid image type")
            invalid_files += 1
            continue
        image_open = Image.open(path.join(source, file_item))
        image_middle = int(image_open.width / 2)
        crop_rectangle = (image_middle, 0, image_middle + 1, image_open.height)
        image_open = image_open.crop(crop_rectangle)
        keogram = concat_images(keogram, image_open)

    file_destination = f"{destination}/{file_name}"
    keogram.save(file_destination)
    end = time.perf_counter()
    logger.debug(f"completed\t: {file_destination}")
    logger.debug(f"time\t\t: {end - start:0.4f} seconds")
    logger.debug(f"size\t\t: {keogram.width} x {keogram.height}")
    logger.debug(f"total files\t: {len(sorted_files)}")
    logger.debug(f"non images\t: {invalid_files}")
    logger.debug(f"images\t\t: {len(sorted_files) - invalid_files}")


def valid_image(file_item) -> bool:
    ext = path.splitext(file_item)[1]
    logger.debug(f"checking image type of {file_item} with extension of {ext}")
    return ext.lower() in valid_images


def concat_images(im1, im2):
    logger.debug("concatenating base image with new image slice")
    logger.debug(f"base image size {im1.width} x {im1.height}")
    dst = Image.new('RGB', (im1.width + im2.width, im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    logger.debug(f"new image size {dst.width} x {dst.height}")
    return dst


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, required=True)
    parser.add_argument('--destination', type=str, required=True)
    parser.add_argument('--loglevel', type=int, default=20)
    args = parser.parse_args()

    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        logger.setLevel("INFO")

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=args.loglevel)
    logger.setLevel(args.loglevel)

    try:
        logger.debug(f"--source : {args.source}")
        logger.debug(f"--destination :{args.destination}")
        create(args.source, args.destination)
    except OSError as e:
        logger.fatal(e)
