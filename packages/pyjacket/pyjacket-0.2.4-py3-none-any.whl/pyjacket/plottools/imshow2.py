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

# Decorator to optionally apply NoAxes context manager
def NoAxesDecorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with NoAxes() as no_axes:
            return func(*args, **kwargs)
    return wrapper

# Decorator to make the title bold
def BoldTitleDecorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        plt.rcParams['axes.titleweight'] = 'bold'
        result = func(*args, **kwargs)
        plt.rcParams['axes.titleweight'] = 'normal'
        return result
    return wrapper

# Create a sample image
image = np.random.rand(10, 10)

# Function to display the image with imshow
def show_image():
    plt.imshow(image, cmap='viridis')
    plt.title('Sample Image')
    plt.show()
    
# Apply NoAxes and BoldTitle decorators
@NoAxesDecorator
# @BoldTitleDecorator
def show_image():
    plt.imshow(image, cmap='viridis')
    plt.title('Sample Image')
    plt.show()

# Test the decorated function
show_image()

