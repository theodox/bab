import Math
import Random


class BitmapBase:
    """bitmap class"""

    DATA_TYPE = Uint8Array

    def __init__(self, x, y=None):
        self.width = x
        self.height = y or x
        self.data = __new__(self.DATA_TYPE(self.width * self.height))

    def get(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        return self.data[x + y * self.width]

    def set(self, x, y, val):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise KeyError('Bitmap address out of bounds')
        self.data[x + y * self.width] = val

    def region(self, xmin, ymin, xmax, ymax):
        """
        iterator that yields all the addresses in the range (inclusive on lower bound, exclusive on upper!)
        """
        for x in range(xmin, xmax):
            for y in range(ymin, ymax):
                yield x, y

    def map_function(self, func, bounds=None):
        """
        run the callable func on every address within <bounds> on this image and (optionally) <image2>, returning a new image
        """
        bounds = bounds or (0, 0, self.width, self.height)

        result = self.__class__(bounds[2], bounds[3])
        for address in self.region(bounds[0], bounds[1], bounds[2], bounds[3]):
            r = func(self, address)
            result.set(address[0], address[1], float(abs(r)))

        return result

    def convolve(self, kernel, bounds=None):
        """
        run kernel on every address within <bounds> on this image and (optionally) <image2>, returning a new image

        kernel is a callable which takes a bitmap and a tuple pixel address
        """

        bounds = bounds or (0, 0, self.width, self.height)

        result = self.__class__(bounds[2], bounds[3])
        for address in self.region(bounds[0], bounds[1], bounds[2], bounds[3]):
            r = kernel(self, address)
            result.set(address[0], address[1], r)

        return result

    def validate(self, value):
        '''override in derived classes to make sure values are good'''
        if value < 0:
            return 0
        if value > 255:
            return 255
        return Math.floor(value)


class BitmapUint16(BitmapBase):
    DATA_TYPE = Uint16Array

    def validate(self, value):
        if value < 0:
            return 0
        if value > 65535:
            return 65535
        return Math.floor(value)


class BitmapFloat32(BitmapBase):
    DATA_TYPE = Float32Array

    def validate(self, value):
        return value


def create_kernel(width, height, data, multiplier=1):
    """
    returns a function object with associated weights for convolving a pixel
    """

    assert (len(data) == width * height,
            "Kernel data must include width  * height elements")
    assert (width / 2.0 != Math.floor(width / 2.0),
            "Kernel must have an odd number of columns")
    assert (height / 2.0 != Math.floor(height / 2.0),
            "Kernel must have an odd number of rows")

    margin_w = Math.floor(width / 2.0)
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
        kernel_y = 0
        for y_pixel in range(ymin, ymax):
            kernel_x = 0
            for x_pixel in range(x_min, x_max):
                source = bitmap.get(x_pixel, y_pixel)
                if source is not None:
                    value = data[(kernel_y * width) + kernel_x]
                    total += (source * value)
                kernel_x += 1
            kernel_y += 1

        return total * multiplier

    return _kernel_


def box_blur_kernel():
    return create_kernel(3, 3, [1, 1, 1, 1, 1, 1, 1, 1, 1], (1 / 9.0))


def test_bitmap():
    console.time("create bitmap")
    b = BitmapFloat32(1024, 1024)
    console.timeEnd("create bitmap")
    console.time("fill bitmap")
    for u in range(1024):
        for v in range(1024):
            b.set(u, v, int(Random.random() * 10000))
    b.set(0, 0, 99.99)
    console.timeEnd("fill bitmap")
    print (b.get(0, 0))

    k = box_blur_kernel()
    console.time("convolve")
    b.convolve(k)
    console.timeEnd("convolve")
