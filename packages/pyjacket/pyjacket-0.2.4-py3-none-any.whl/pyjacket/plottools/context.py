import matplotlib.pyplot as plt

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