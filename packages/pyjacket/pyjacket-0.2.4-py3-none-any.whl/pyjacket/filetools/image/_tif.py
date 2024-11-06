# import cv2 as cv
# from skimage import io
import tifffile
import numpy as np
import os

from typing import Union
from .image_handle import ImageHandle
from pyjacket import arrtools


class TifImageHandle(ImageHandle):
    
    data: tifffile.TiffPage
    
    @property
    def ndim(self):
        n = self.data.ndim 
        if self.channels > 1:
            n += 1
        return n
    
    @property
    def shape(self):
        """Sizes of each of the dimensions"""
        if self.ndim < 4:
            return self.data.shape
        
        else:
            # Ensure channel becomes last dimension
            # This is needed to interface with imageJ format
            if len(self.data.shape) == 3:
                t, y, x = self.data.shape 
                t //= self.channels
                c = self.channels
                
            else:
                t, c, y, x = self.data.shape
            
            
            
            return (t, y, x, c)
    
    @property
    def dtype(self):
        return self.data.dtype
    
    def get_data(self):

        self.file = tifffile.TiffFile(self.filename)

        series = self.file.series
        page = series[0]
        return page
    
    def close(self):
        self.file.close()
    
    def get(self, i):
        """Go to the desired frame number. O(1)"""
        N = self.shape[0]
        if not (-N < i <= N):
            raise IndexError("Frame index out of range")
        
        if self.ndim == 4:
            # 4d data is really stored in a 3d format for some reason
            # So we need to unzip the channels
            num_channels = self.shape[3]
            i *= num_channels
            
            # stack all of the color channels
            stack = [self.data.asarray(key=i+di) for di in range(num_channels)]
            frame = np.stack(stack, axis=-1)
        else:
            frame = self.data.asarray(key=i) 
        return frame
    
class MMStack(ImageHandle):
    """Read a folder of ome.tif files"""
    
    data: list[tifffile.TiffFile]
    page_counts: list[int]

    def open(self):
        ome_files = [f for f in os.listdir(self.filename) if f.endswith('.ome.tif')]
        ome_files.sort()
        files = [os.path.join(self.filename, f) for f in ome_files]
        return [tifffile.TiffFile(f) for f in files]
    
    def close(self):
        for tif in self.data:
            tif.close()        
        
    def get(self, i):
        """Get the i-th frame across all files."""
        if not (0 <= i < self.max_shape[0]):
            raise IndexError("Frame index out of range")
        
        i *= self.channels
        
        t, p = relative_index(self.page_counts, i)
        frame = self.data[t].pages[p].asarray()
        
        if self.channels == 1:
            return frame
        
        # in case of unzipping the data, stack the color channels
        stack = np.empty((*frame.shape, self.channels), dtype=frame.dtype)
        stack[..., 0] = frame
        for di in range(1, self.channels):
            t, p = relative_index(self.page_counts, i+di)
            stack[..., di] = self.data[t].pages[p].asarray()
            
        return stack
        
    def get_max_shape(self):
        # number of frames
        self.page_counts = [len(tif.pages) for tif in self.data]
        num_frames = sum(self.page_counts) // self.channels
        
        # Frames shape
        frame_shape = self.data[0].pages[0].shape
        
        if self.channels == 1:
            return (num_frames, *frame_shape)
        return (num_frames, *frame_shape, self.channels)      


def slice_length(s: slice, n: int):
    """Compute how many elements belong to a slice of an iterable of size n"""
    start, stop, step = s.indices(n)
    if step > 0:
        return max(0, (stop - start + (step - 1)) // step)
    elif step < 0:
        return max(0, (start - stop - (step + 1)) // (-step))
    else:
        raise ValueError("Slice step cannot be zero")

def relative_index(sizes, i):
    for j, size in enumerate(sizes):
        if i < size:
            return j, i   
        i -= size
    raise IndexError()

def percentile(hist: np.ndarray, p, color=False):
    if color:
        hist = np.cumsum(hist, axis=0)
        i = np.stack(
            [np.searchsorted(hist[:, i], p, side='right') \
                for i in range(hist.shape[-1])]).T
    else:
        hist = np.cumsum(hist)
        i = np.searchsorted(hist, p, side='right')
    return i.T

def intensity_histogram(a: ImageHandle, color=True, normalize=True) -> np.ndarray:
    if color:
        shape = (arrtools.type_max(a.dtype)+1, a.shape[-1])  # e.g. (256, 3)
        hist = np.zeros(shape, dtype=np.int64)
        for rgb in a:
            for i in range(shape[-1]):
                frame = rgb[..., i]
                unique, counts = np.unique(frame, return_counts=True)
                hist[unique, i] += counts
        if normalize:  hist = hist / np.sum(hist, axis=0)
                
    else:
        shape = arrtools.type_max(a.dtype)+1  # e.g. (256, )
        hist = np.zeros(shape, dtype=np.int64)
        for frame in a:
            unique, counts = np.unique(frame, return_counts=True)
            hist[unique] += counts
        if normalize:  hist = hist / np.sum(hist)
        
    return hist 
   

def read(filepath, transpose=True):
    data = tifffile.imread(filepath)

    # Ensure channels are in last dimension
    if transpose and data.ndim == 4:
        data = np.transpose(data, (0, 2, 3, 1))

    return data









# def write(filepath, data: Union[np.ndarray], meta=None, **kwargs):
#     # if isinstance(data, TifImageHandle):
#     #     pass
#     # elif isinstance(data, np.ndarray):
#     #     pass
#     # else:
#     #     raise ValueError(f'Unexpected data type: {type(data)}')
    
#     # Tif expects dimensions order (frames, ch, y, x)
#     # But we provide order (frames, y, x, ch), so need to adjust this
#     if data.ndim == 4:
#         data = np.transpose(data, (0, 3, 1, 2))
    
#     kwargs.setdefault('imagej', True)
#     return tifffile.imwrite(filepath, data, metadata=meta, **kwargs)






def write(filepath, data: Union[np.ndarray, ImageHandle], meta=None, **kwargs):

    if data.ndim not in [3, 4]:
        raise ValueError(f'Cannot write .tif with {data.ndim} dimensions')
    
    elif data.ndim == 3:
        # 3 dimensions: assume (t, h, w)
        # add the last dimension
        ...
    else:
        # 3 dimensions: assume (t, h, w, ch)
        # Tif expects dimensions order (frames, ch, y, x)
        # But we provide order (frames, y, x, ch), so need to adjust this

        data = np.transpose(data, (0, 3, 1, 2))
    #     ...

    
    kwargs.setdefault('imagej', True)
    return tifffile.imwrite(filepath, data, metadata=meta, **kwargs)
    
    

         
# def read_exif(filename):
#     tif = tifffile.TiffFile(filename)
#     exif = tif.pages[0].tags
#     return exif


# def imwrite_tif(file: str, arr):
#     x = io.imsave(file, arr)
#     return x