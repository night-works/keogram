from os import PathLike, path, makedirs, listdir
from typing import Union
import argparse

from PIL import Image

valid_images = [".jpg", ".gif", ".png", ".jpeg"]


def create(source: Union[str, PathLike], destination: Union[str, PathLike], keogram_file: str = "keogram.jpg") -> None:
    if path.exists(source):
        if not path.exists(destination):
            makedirs(destination)
        if path.isfile(source):
            raise NotADirectoryError("Directory required to load source files for keogram")
        else:
            process_images(source, destination, keogram_file)
    else:
        raise NotADirectoryError("Directory required to load source files for keogram not found")


def process_images(source, destination, file_name):
    keogram = Image.new("RGB", (0, 0))

    for file_item in sorted(listdir(source)):
        if not valid_image(file_item):
            continue
        image_open = Image.open(path.join(source, file_item))
        image_middle = int(image_open.width / 2)
        crop_rectangle = (image_middle, 0, image_middle + 1, image_open.height)
        image_open = image_open.crop(crop_rectangle)
        keogram = concat_images(keogram, image_open)
    keogram.save(f"{destination}/{file_name}")


def valid_image(file_item) -> bool:
    ext = path.splitext(file_item)[1]
    return ext.lower() in valid_images


def concat_images(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, required=True)
    parser.add_argument('--destination', type=str, required=True)
    args = parser.parse_args()

    try:
        create(args.source, args.destination)
    except OSError as e:
        print(e)
