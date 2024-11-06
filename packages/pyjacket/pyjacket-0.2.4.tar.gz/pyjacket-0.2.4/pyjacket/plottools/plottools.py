import matplotlib as mpl
from matplotlib.pyplot import *
import matplotlib.pyplot as plt
from functools import wraps
from os import path

from matplotlib.axes import Axes

defaults = {
    'hist': {
        'edgecolor': 'black',
        'linewidth': 1.4,
        'rwidth': 1.00,
    },
    }

def custom_imshow(f):
    @wraps(f)
    def wrapper(self: Axes, *a, **kw):
        self.axis('off')
        kw = {**defaults.get('imshow', {}), **kw}
        return f(self, *a, **kw)
    return wrapper

  
def custom__hist(f):
    @wraps(f)
    def wrapper(*a, **kw):
        kw = {**defaults.get('hist', {}), **kw}
        return f(*a, **kw)
    return wrapper

    
Axes.imshow = custom_imshow(Axes.imshow)
Axes.hist = custom__hist(Axes.hist)



def set_style(name: str):
    name = name.lower()
    if name == 'default':
        mpl.rcParams.update(mpl.rcParamsDefault)
        return
    here = path.dirname(__file__)
    file = path.join(here, 'styles', f'{name}.mplstyle')
    style.use(file)
set_style('test')



    
    
if __name__ == '__main__':
    set_style('sprakel')