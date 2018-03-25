import Math


class Bitmap:
    """simple bitmap class for heightmaps, etc"""
    def __init__(self, x, y = None, data_type = Uint16Array):
        self.width = x
        self.height = y or x
        self.data = __new__(data_type(self.width * self.height))
        self.data_type  = data_type

    def get(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        return self.data[x + y * self.width]

    def set(self, x, y, val):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise KeyError('Bitmap address out of bounds')
        self.data[x + y * self.width] = val




    # these work as literals -- but not apparently if <addr> is supplied by a loop?
    # see https://github.com/QQuick/Transcrypt/issues/508

    def __getitem__(self, addr):
        x, y = addr
        return self.get(x,y)

    def __setitem__(self, addr, val):
        print ("__setitem__", addr, val)
        x, y = addr
        self.set(x, y, val)

    def range(self, xmin, ymin, xmax, ymax):
        """iterator that yields all the addresses in the range (inclusive on lower bound, exclusive on upper!)"""
        for x in range(xmin, xmax):
            for y in range (ymin, ymax):
                yield x, y

    def map_function(self, func, bounds = None):
        """run the callable func on every address within <bounds> on this image and (optionally) <image2>, returning a new image"""


        if bounds is None:
            bounds = (0,0, self.width, self.height)

        result = Bitmap(bounds[2], bounds[3], self.data_type)
        for address in self.range(bounds[0], bounds[1], bounds[2], bounds[3] ):
            r = func(self, address)
            result.set(address[0], address[1], float(abs(r)))

        return result

    def convolve (self, kernel, bounds = None):
        """run kernel on every address within <bounds> on this image and (optionally) <image2>, returning a new image"""
        # note my python instinct is to use __call__, but that does not work without a pragma
        # which defeas

        if bounds is None:
            bounds = (0,0, self.width, self.height)

        result = Bitmap(bounds[2], bounds[3], self.data_type)
        for address in self.range(bounds[0], bounds[1], bounds[2], bounds[3] ):
            r = kernel(self, address)
            print(address, r)
            result.set(address[0], address[1], r)

        return result



def create_kernel( width, height, data):

    """returns a function object with associated weights for convolving a pixel"""

    assert (len(data) == width * height, "Kernel data must include width  * height elements")
    assert (width / 2.0 != Math.floor(width / 2.0), "Kernel must have an odd number of columns")
    assert (height / 2.0 != Math.floor(height / 2.0), "Kernel must have an odd number of rows")

    margin_w =  Math.floor(width / 2.0)
    margin_h = Math.floor(height / 2.0)


    def _kernel_(bitmap, address):
        """
        return the result of this kernel applied to bitmap pixel x, y
        """
        x, y = address

        x_min = x - margin_w
        x_max = x + margin_w + 1
        ymin = y - margin_h
        ymax = y + margin_h + 1

        total = 0

        fallback = self.reference_value * bitmap.get(x, y)

        kernel_y = 0
        for y_pixel in range(ymin, ymax):
            kernel_x = 0
            for x_pixel in range(x_min, x_max):
                source = bitmap.get(x_pixel, y_pixel)
                if source is not None:
                    multiplier = data[kernel_y * width + kernel_x]
                    total += source * multiplier
                kernel_x += 1
            kernel_y += 1
        return total

    return _kernel_




