<div align="center">

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/night-works/keogram/build.yml?style=for-the-badge)
![Codecov](https://img.shields.io/codecov/c/gh/night-works/keogram?style=for-the-badge)
![Sonar Quality Gate](https://img.shields.io/sonar/quality_gate/night-works_keogram?server=https%3A%2F%2Fsonarcloud.io&style=for-the-badge)
![GitHub](https://img.shields.io/github/license/night-works/keogram?color=g&style=for-the-badge)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/night-works/keogram?style=for-the-badge)

</div>

# Keogram

A Keogram is generated from the center slice 1px wide from a series of images and stitched together to generate an image
that shows the
sky throughout the captured period. A keogram is a way of displaying the intensity of an auroral display, taken from a
narrow part of a
screen recorded by a camera, more specifically and ideally in practice a "whole sky camera". This allows one to easily
realize the general activity of the display that night, whether it had been interrupted by weather conditions or not,
and allows the determination of the regions in which the aurora was seen in terms of latitude and longitude of the area.

However, the initial case that this module was created was to create a keogram of general night skies to judge how clear
the
night sky was on the night.

## Features

* Generates a keogram from a sorted list of files from a given directory.
* Saves information about the keogram alongside the image in json format.
* Can generate a keogram from a mixture of image formats ignoring non image formats.

## Installing

```shell
pip install keogram
```

## Usage

To generate a keogram with checks on the source directory, and creation of the destination directory call the following.
The first parameter is the folder that contains the images that you want to use for the keogram, the second parameter
is the destination folder for the keogram. The third parameter (optional) is the filename of the resulting keogram
image. Be sure to include the file type extension. The default is "keogram.jpg"
The final parameter is weather to save a metadata json file alongside the generated keogram, this is optional and
defaults to
**False**. The method returns the MetaData of the file, even if not asked to save it locally.

```python
import keogram

metadata = keogram.create("input_directory", "output_directory", "filename", True)
```

## Running Tests

There are a few ways to run the tests the usual way is to use __tox__ from the top level of the repository

```shell
tox
```

If you already have the dependencies in your python environment you can just use __pytest__ if extra arguments for code
coverage

```shell
pytest --cov=src
```

## Contributing

Please first raise an issue then fork the repository referencing the issue in commits and raise a Pull Request.

## License

Licensed under the MIT.
Copyright 2023 Night Works. [Copy of the license](LICENSE.md).

A list of the Licenses of the dependencies of the project can be found at
the bottom of the [Libraries Summary](https://libraries.io/pypi/keogram).