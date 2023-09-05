"""Code to load all the library."""
import importlib.util
import json
import os
import pathlib
import typing

import PIL.Image

path: typing.TypeAlias = pathlib.Path | str | os.PathLike
pure_image: typing.TypeAlias = PIL.Image.Image
image: typing.TypeAlias = path | pure_image
message: typing.TypeAlias = typing.AnyStr | typing.Any
secret: typing.TypeAlias = typing.AnyStr


def load_path(paths: path) -> pathlib.Path:
    """Load any PathLike object as pathlib.Path"""
    if isinstance(paths, str) or isinstance(paths, os.PathLike):
        return pathlib.Path(paths)
    return paths


def load_image(paths: path) -> PIL.Image.Image:
    """Convert path to PIL.Image.Image instance."""
    images = PIL.Image.open(paths)
    return images


def get_script_path() -> pathlib.Path:
    """Get the Path of where the current file locate"""
    return pathlib.Path(os.path.dirname(os.path.abspath(__file__)))


# def get_execute_path() -> pathlib.Path:
#     """Get the Path of where the script executed"""
#     return pathlib.Path(os.getcwd())


def get_library(paths: path) -> dict[str, path]:
    """Retrieve all library path in the sub-directory from a specific path."""
    directory = os.listdir(paths)
    return_dictionary = {}
    for item in directory:
        if len(item.split('.')) == 1 and \
                item not in ['__pycache__'] and \
                os.path.isfile(pathlib.Path(paths, item, 'manifest.json')):
            return_dictionary[item] = pathlib.Path(paths, item)
    return return_dictionary


def get_library_class(paths: path) -> dict[str, typing.Callable]:
    """Retrieve the library class on the certain path."""
    library_list = get_library(paths)
    return_dict = {}
    for library in library_list:
        try:
            manifest_path = pathlib.Path(library_list[library], 'manifest.json')
            with open(manifest_path, 'r') as f:
                data = json.load(f)
                spec = importlib.util.spec_from_file_location(library,
                                                              pathlib.Path(library_list[library], data['location'][0]))
                library_instance = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(library_instance)
                return_dict[library] = getattr(library_instance, data['location'][1])
        except AttributeError:  # noqa: E722
            pass
    return return_dict


if __name__ == '__main__':
    print(get_library(get_script_path()))
    print(get_library_class(get_script_path()))
