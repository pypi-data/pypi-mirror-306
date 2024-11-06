import numpy as np
import os
from typing import Union, Callable, Type
from .metadata import Metadata
from .image_handle import ImageHandle
from . import _mp4, _tif, _nd2, _avi, _png, _jpg

"""Convention:
All arrays must be of shape
 - (height, width)
 - (frames, height, width)
 - (frames, height, width, colors)
"""

ReaderLazy = Callable[..., ImageHandle]
Reader = Callable[..., np.ndarray]

def read_img(filepath: str, lazy=False, **kwargs):
    """Read image data into a numpy array.

    Args:
        filepath (str): Location of the image file
        lazy (bool, optional): Read lazy to save memory. Defaults to False.
        channels (int, optional): Unzip first dimension into multiple channels. Defaults to 1.

    Raises:
        ValueError: _description_
        NotImplementedError: _description_

    Returns:
        np.ndarray: _description_
    """

    # Check whether we are dealing with a file, or a folder of files
    folder = False
    if os.path.isdir(filepath):
        print(f'Folder detected!')
        folder = True

    # Get the file extension (folders get '')
    _, ext = os.path.splitext(filepath)  # ext may be missing
    ext = ext.lstrip('.')

    if lazy:
        read_function_lazy: ReaderLazy = {
            '': _tif.MMStack if folder else _tif.TifImageHandle,
            'tif': _tif.TifImageHandle,
            'tiff': _tif.TifImageHandle,
        }.get(ext)

        if read_function_lazy is None:
            raise ValueError(f'Cannot lazy-read data of type {ext}')
        h = read_function_lazy(filepath, **kwargs)
        return h
  
    elif not lazy:
        read_function: Reader = {
            '': None if folder else _tif.read,
            'tif': _tif.read,
            'tiff': _tif.read,
            'nd2': _nd2.read,
            'avi': _avi.read,
        }.get(ext)

        if read_function is None:
            raise NotImplementedError(f'Cannot read data of type {ext}')
        arr = read_function(filepath)      
        return arr

def read_img_meta(filename):
    return Metadata(filename)

def write_img(filepath: str, data: Union[np.ndarray, ImageHandle], meta: Metadata=None, **kwargs):
    """Write image data. Supports tif, nd2"""

    # Get the file extension (folders get '')
    _, ext = os.path.splitext(filepath)  # ext may be missing
    ext = ext.lstrip('.')

    if not ext:  ValueError(f"missing extension in filename: {filepath}")

    write_function = {
        'tif': _tif.write,
        'mp4': _mp4.write,
    }.get(ext)
    
    if not write_function:
        raise NotImplementedError(f'Cannot write image of type {ext}')
    
    return write_function(filepath, data, meta, **kwargs)