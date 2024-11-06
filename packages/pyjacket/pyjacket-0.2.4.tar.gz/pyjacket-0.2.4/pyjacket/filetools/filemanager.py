from dataclasses import dataclass
import os
import pickle
# import pims
import numpy as np
from matplotlib.figure import Figure
from imageio import mimwrite

import matplotlib.pyplot as plt
from matplotlib import cm
from PIL import Image, ImageDraw

from pyjacket import filetools, arrtools
import pandas as pd
import warnings


class Writeable:
    def write(self):
        raise NotImplementedError()
    
    def save(self):
        raise NotImplementedError()


@dataclass
class FileManager:
    """Make it easy to read/write files"""
    src_root: str
    dst_root: str
    rel_path: str = ''
    base: str = ''  # provide base name of file to wrap all results in an additional folder
    CSV_SEP: str = ';'

    @property
    def src_folder(self):
        return os.path.join(self.src_root, self.rel_path)

    @property
    def dst_folder(self):
        return os.path.join(self.dst_root, self.rel_path, self.base)
    
    def src_path(self, filename='', folder=''):
        """Absolute path to a file in the src directory"""
        return os.path.join(self.src_folder, folder, filename).rstrip('\\')
    
    def dst_path(self, filename=None, folder=None):
        """Absolute path to a file in the dst directory"""
        filename = filename or ''
        folder = folder or ''
        return os.path.join(self.dst_folder, folder, filename).rstrip('\\')
    
    def delete(self, filename):
        abs_path = self.dst_path(filename)
        if os.path.exists(abs_path):
            os.remove(abs_path)
            print('Deleted', filename)



    def read_before(self, filename: str, folder: str, dst: bool, valid_extensions: list):
        """Prepare the filepath for reading a file
        
        filename: str
        
        folder: str
        
        dst: bool
        
        valid_extensions: list
          the first element of this list will be used as default.
        """
        filename = self.handle_extension(filename, valid_extensions)
        filepath = self.dst_path if dst else self.src_path  
        return filepath(filename, folder)
            
    # def read_after(self):
    #     """what to do after a file is read"""
    
    def write_before(self, filename: str, folder: str, valid_extensions: list):
        """Finds the absolute path and creates folders when necessary """
        if valid_extensions:
            filename = self.handle_extension(filename, valid_extensions)
        filepath = self.dst_path(filename, folder)
        self.ensure_exists(filepath)
        return filepath
        
    def write_after(self, filepath):
        """..."""
        rel_path = os.path.relpath(filepath, self.dst_folder)
        print(f'Saved: {rel_path}')
        
        
    def read(self, filename: str, *args, folder: str='', dst: bool=False, **kwargs):
        """Read files of a standard format such as .txt"""
        filepath = self.read_before(filename, folder, dst, [])
        with open(filepath, 'r') as f:
            return f.read(*args, **kwargs)
        
    def write(self, filename: str, data: Writeable, *args, folder: str='', **kwargs):
        """Writes any object that implements a write function"""
        filepath = self.write_before(filename, folder, [])
        if hasattr(data, 'write'):
            data.write(filepath, *args, **kwargs)
        elif hasattr(data, 'save'):
            data.save(filepath, *args, **kwargs)
        else:
            raise ValueError(f'Expected data obj that implements .read or .write, instead got data of type: {type(data)}. ')
        self.write_after(filepath)
         
    def read_pickle(self, filename: str, *args, folder: str='', dst: bool=False, **kwargs):
        """Read a python object from a pickle file.
        
        dst_folder: bool
          read a file in the dst path rather than the src path
        """
        filepath = self.read_before(filename, folder, dst, ['.pkl'])
        with open(os.path.join(filepath), 'rb') as f:
            return pickle.load(f, *args, **kwargs)

    def write_pickle(self, filename: str, data: object, *args, folder: str='', **kwargs):
        """Write a python object to a pickle file."""
        filepath = self.write_before(filename, folder, ['.pkl'])
        with open(filepath, 'wb') as f:
            pickle.dump(data, f, *args, **kwargs)
        self.write_after(filepath)
            
    def read_csv(self, filename: str, folder: str='', dst: bool=False, **kwargs):
        """Read csv data into a pandas dataframe"""
        filepath = self.read_before(filename, folder, dst, ['.csv'])
        kwargs.setdefault('sep', self.CSV_SEP)
        # return pd.read_csv(filepath, *args, **kwargs)
        return filetools.read_csv(filepath, **kwargs)

    def write_csv(self, filename: str, data: pd.DataFrame, folder: str='', **kwargs):
        """Save a csv data to a csv file"""
        filepath = self.write_before(filename, folder, ['.csv'])
        kwargs.setdefault('sep', self.CSV_SEP)
        # data.to_csv(filepath, *args, **kwargs)
        filetools.write_csv(filepath, data, **kwargs)
        self.write_after(filepath)
        
    def read_img(self, filename, *args, folder='', dst=False, **kwargs):
        """Read image data into a numpy.ndarray of shape:
            (frames, t, y, x, channels)
        """
        valid_extensions = [
            '.tif', 
            '.tiff', 
            '.png', 
            '.jpg',
            '.avi',
            '.mov',
            '.mp4',
            '.bmp',
            '',  # allow folders to be specified
            ]
        filepath = self.read_before(filename, folder, dst, valid_extensions)
        print(f'Reading: {filepath}')
        return filetools.read_img(filepath, *args, **kwargs)
    
    def read_img_meta(self, filename, folder='', dst_folder=False):
        """Get the Exif (meta)data for an image file. 
        This contains various acquisition details such as exposure time
        """
        getter = self.dst_path if dst_folder else self.src_path  
        filepath = getter(filename, folder)
        return filetools.read_img_meta(filepath)
    
    def write_img(self, filename, data: np.ndarray, *args, folder='', **kwargs):
        """Write numpy.ndarray data to img file format
        
        TODO: allow log scale display
        """
        valid_extensions = [
            '.tif', 
            '.tiff', 
            '.png', 
            '.jpg',
            '.avi',
            '.mov',
            '.mp4',
            '.bmp',
            ]
        filepath = self.write_before(filename, folder, valid_extensions)
        filetools.write_img(filepath, data, **kwargs)
        self.write_after(filepath)
        
    def savefig(self, filename, handle=None, folder='', dst=False):
        """Called 'save' rather than 'write' because the original data cannot be retrieved from the file."""
        fig, _ = handle or plt.gcf(), plt.gca()
        # img_path = self.dst_path(filename, folder)

        filepath = self.write_before(filename, folder, ['.png'])

        self.ensure_exists(filepath)
        fig.savefig(filepath, dpi=300)
        plt.close(fig)

        self.write_after(filepath)

        # print(f'Saved: {folder}/{filename}')
            

    """Useful Methods"""
    def iter_dir(self, ext: str='', dst_folder=False):
        directory = self.dst_path() if dst_folder else self.src_path()
        for file in os.listdir(directory):
            if file and not file.endswith(ext): continue
            yield file

    def list_dir(self, ext: str='', dst_folder=False, **kwargs):
        return list(self.iter_dir(ext, dst_folder, **kwargs))
    
    @staticmethod
    def explode(p, sep=os.sep):
        """Convert path a/b/c into list [a, b, c]"""
        return os.path.normpath(p).split(sep)

    @staticmethod
    def ensure_endswith(s, extension):
        # print('checking end:', s)
        return s if s.endswith(extension) else s + extension

    @staticmethod
    def ensure_exists(path): 
        folder = os.path.dirname(path)
        # print('folder:', folder)
        if not os.path.exists(folder):
            os.makedirs(folder)
            print("Created", folder)

    @staticmethod
    def handle_extension(filename: str, valid_extensions: list):
        default_ext = valid_extensions[0]
        _, ext = os.path.splitext(filename)

        if ext not in valid_extensions:
            if ext == '':  # no extension is provided
                filename = filename + default_ext
            else:  # non-supported extension
                warnings.warn(Warning(f'Unsupported file format ({ext}): {filename}, using {default_ext} instead.'))
                filename = filename + default_ext

        return filename



if __name__ == "__main__":
    # c = FileManager('data', 'results', '2023', 'test001')
    c = FileManager.from_path('data', 'C::/idk/results/2023/test001')

    print(c.src_root)
    print(c.dst_root)
    print(c.rel_path)
    print(c.experiment)

    print(c.abs_path('haha.md'))