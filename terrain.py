import Math


class Array2D:

	def __init__(self, x, y = None):
		self.width = x
		self.height = y or x
		self.data = __new__(Uint16Array)(self.width * self.height)

	def get(self, x, y):
		w = self.width
		addr = (max(min(y, self.height), 0) * w) + max(min(x, w), 0)
		return self.data[addr]

	def set(self, x, y, val):
		w = self.width
		addr = (max(min(y, self.height), 0) * w) + max(min(x, w), 0)
		self.data[addr] = val

	def range(self, xmin, ymin, xmax, ymax):
		for x in range(xmin, xmax):
			for y in range (ymin, ymax):
				yield x, y


	def __getitem__(self, addr):
		x, y = addr
		return self.get(x,y)


	def __setitem__(self, addr, val):
		x, y = addr
		self.set(x, y, val)


	def map(self, func, image2 = None, bounds = None):

		if image2 is None:
			image2 = self

		if bounds is None:
			bounds = (0,0, self.width, self.height)

		result = Array2D(bounds[2], bounds[3])

		for address in self.range(bounds[0], bounds[1], bounds[2], bounds[3] ):
			result[address] = Math.floor(func(self, image2, address))

		return result

def test_blur(image1, image2, address):
	x, y  = address
	total = 0
	total += image1[x-1, y-1]
	total += image1[x+1, y-1]
	total += image1[x-1, y+1]
	total += image1[x+1, y+1]
	total += image1[x-1, y] * 2
	total += image1[x+1, y] * 2
	total += image1[x, y-1] * 2
	total += image1[x, y+1] * 2
	total += image1[x, y] * 8
	return total / 16

	

	