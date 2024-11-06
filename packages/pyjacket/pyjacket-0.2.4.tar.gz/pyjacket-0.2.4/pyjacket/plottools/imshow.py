import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
from typing import Tuple
from matplotlib.figure import Figure
from matplotlib.axis import Axis

from pyjacket import filetools

class MPLContext:
    """Allow overriding default style parameters using decorator classes
    """
    def __init__(self, func):
        self._func = func
    
    def __call__(self, *args, **kwargs):
        with self:  # > calls self.__enter__
            retval = self._func(*args, **kwargs)
        return retval
    
    def __enter__(self):
        self.previous_rc = plt.rcParams.copy()
        self.rc()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        plt.rcParams.update(self.previous_rc)
        
    def rc(self):
        """Make the changes here""" 
        # plt.rc('key', value)   
 
class BoldTitle(MPLContext):
    def rc(self):
        plt.rc('axes', titleweight='bold')
        
class NoAxes(MPLContext):
    def rc(self):
        plt.rc('axes', edgecolor='none')
        plt.rc('xtick', bottom=False, labelbottom=False)
        plt.rc('ytick', left=False, labelleft=False)



# Typing
Handle = Tuple[Figure, Axis]

lognorm = colors.SymLogNorm(linthresh=0.015)

fm = filetools.FileManager(
    r'E:\Data\EMSA', 
    r'C:\Users\arfma005\Scripts\EMSA_analysis\out', 
    '240605_ASb1500', 
    CSV_SEP=','
    )
img = fm.read_img('20240605-ASb1500-[Cy3]-2.tif')

@NoAxes
def imshow(arr, handle: Handle=None, colorbar=False, *args, **kwargs):
        fig, ax = handle or (plt.gcf(), plt.gca())
        im = ax.imshow(arr, *args, **kwargs)
        if colorbar: fig.colorbar(im, ax=ax, extend='both')   
        return fig, ax
    


fig, ax = plt.subplots(1, 2)
imshow(img, (fig, ax[0]))
imshow(img, (fig, ax[1]), norm=lognorm)
plt.show()