import matplotlib.pyplot as plt
import numpy as np
from functools import wraps

# Context manager to hide axes and remove padding
class NoAxes:
    def __enter__(self):
        self.previous_rc = plt.rcParams.copy()
        plt.rc('axes', edgecolor='none')
        plt.rc('xtick', bottom=False, labelbottom=False)
        plt.rc('ytick', left=False, labelleft=False)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        plt.rcParams.update(self.previous_rc)
        
class BoldTitle:
    
    # def __init__(self, arg):
    #     self._arg = arg
    
    # def __call__(self, *args, **kwargs):
    #     retval = self._arg(*args, **kwargs)
    #     return retval
    
    def __enter__(self):
        self.previous_rc = plt.rcParams.copy()
        plt.rc('axes', titleweight='bold')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        plt.rcParams.update(self.previous_rc)
        

def NoAxesDecorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with NoAxes():
            return func(*args, **kwargs)
    return wrapper

def BoldTitleDecorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with BoldTitle():
            return func(*args, **kwargs)
    return wrapper

# Create a sample image
image = np.random.rand(10, 10)

# Function to display the image with imshow
def show_image():
    plt.imshow(image, cmap='viridis')
    plt.title('Sample Image')
    plt.show()
    
# Apply NoAxes and BoldTitle decorators
@BoldTitleDecorator
@NoAxesDecorator
def show_image():
    plt.imshow(image, cmap='viridis')
    plt.title('Sample Image')
    plt.show()

# Test the decorated function
show_image()

