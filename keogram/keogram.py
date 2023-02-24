from os import PathLike, path, makedirs, listdir
from typing import Union

from PIL import Image


def create(source: Union[str, PathLike], destination: Union[str, PathLike], keogram_file: str = "keogram.jpg") -> None:
    if path.exists(source):
        if not path.exists(destination):
            makedirs(destination)
        if path.isfile(source):
            print(f"Source is a file")
        else:
            process_images(source, destination, keogram_file)
    else:
        raise FileNotFoundError


def process_images(source, destination, file_name):
    p: Image = Image.new("RGB", (0, 0))
    valid_images = [".jpg", ".gif", ".png", ".tga"]
    image_number = 1
    for f in sorted(listdir(source)):
        ext = path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        image_open = Image.open(path.join(source, f))
        image_middle = int(image_open.width / 2)
        crop_rectangle = (image_middle, 0, image_middle + 1, image_open.height)
        image_open = image_open.crop(crop_rectangle)
        print(f"Processing Image {image_number}")
        image_number += 1
        p = get_concat_h_cut(p, image_open)
    p.save(f"{destination}/{file_name}")


def get_concat_h_cut(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


if __name__ == '__main__':
    in_directory = "/home/joseph/Repos/night-works/night-sky-pi/data/observations/2023-02-10/stills/"
    out_directory = "/home/joseph/Repos/night-works/night-sky-pi/data/observations/2023-02-10/keogram/"

    create(in_directory, out_directory)
