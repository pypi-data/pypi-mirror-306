from fractions import Fraction
import tifffile

class ExifTag:
    name: None 
    value: None


def read_exif(filename):
    tif = tifffile.TiffFile(filename)
    exif = tif.pages[0].tags
    return exif

class Metadata:
    EXIF_READER = {
        'tif': read_exif,
    }

    def __init__(self, filename):
        self.filename = filename
        ext = filename.split('.')[-1]
        self.exif: dict[int, ExifTag] = self.EXIF_READER.get(ext, read_exif)(filename)
        
        self._resolution = (None, None)
        
    def get(self, i: int, default=None):
        x = self.exif.get(i)
        x = x.value if x is not None else default
        return x
    
    @property
    def shape(self):
        x = self.get(256) # tuple or None
        y = self.get(257) # tuple or None
        return (y, x)
        
   
    @property
    def bits(self):  # 258
        return self.get(258) # tuple or None
        
    @property
    def resolution(self):  # 282 and 283
        x = self.get(282) # tuple or None
        y = self.get(283) # tuple or None
        x = float(Fraction(*x)) if x else 1
        y = float(Fraction(*y)) if y else 1
        return (y, x)
    
    @property
    def resolution_unit(self):  # 296
        return self.get(296) # tuple or None
        
        
            
    # @property        
    # def exposure_time(self): ...
    
    # @property
    # def light_intensity(self): ...
    
    # @property
    # def period(self): ...
    
    # @property
    # def fps(self): ...
    
    # @property
    # def total_duration(self): ...
    
    
    @property
    def dict(self):
        return {t.name: t.value for i, t in self.exif.items() if i in TAGS}
    
    def __repr__(self):
        return f"Metadata({dir(self)})"
    