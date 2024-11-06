import matplotlib.pyplot as plt
import numpy as np

class MPLContext:
    """Allow overriding default style parameters using decorator classes
    """
    
    def __init__(self, arg):
        self._arg = arg
    
    def __call__(self, *args, **kwargs):
        with self:
            retval = self._arg(*args, **kwargs)
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
        plt.rc('axes', titleweight='bold')
        plt.rc('axes', edgecolor='Green')
        plt.rc('axes', linewidth=10)
        plt.rc('axes.spines', bottom=False)
        plt.rc('axes', labelcolor='green')
        plt.rc('axes', edgecolor='none')
        plt.rc('xtick', bottom=False, labelbottom=False)
        plt.rc('ytick', left=False, labelleft=False)

        





# Create a sample image
image = np.random.rand(10, 10)

# Apply NoAxes and BoldTitle decorators
# @BoldTitle
@NoAxes
def show_image1(ax):
    ax.imshow(image, cmap='viridis')
    ax.set_title('hi there')
    
def show_image2(ax):
    ax.imshow(image, cmap='viridis')
    ax.set_title('hi there')
    

# Test the decorated function

# fig, ax = plt.subplots(1, 2)

fig, ax = plt.gcf(), plt.gca()
show_image1(ax)
plt.show()

show_image2(ax)

plt.show()