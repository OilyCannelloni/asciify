from PIL import Image

class IACurves:
    """
    Set of tone curve functions which are
    used to map symbols to grayscale
    """
    CONTRAST_L = lambda x: -100000/(1/2*x+165)+600
    CONTRAST_M = lambda x: -75000/(2/3*x+150)+500
    CONTRAST_H = lambda x: -50000/(x+130)+384
    DEFAULT = lambda x: x

    @staticmethod
    def shift(val):
        return lambda x: x+val


class ImageAsciifier:
    def __init__(self, func=None, chars=None):
        self.data = None
        self.image = None
        self.image_width = 0
        self.image_height = 0
        self.image_length = 0
        self.ascii = []

        # Set of symbols in order from darkest to brightest
        # TODO make this overrideable
        self.symbols = [' ', '`', "'", '.', '"', ',', '-', '^', '>', '=', '+', '*', 'c', 'u', 'r', 'o',
                        'h', 'i', 'e', 'a', 'x', 'w', '?', 'O', 'D', 'N', 'S', 'M', 'X', 'W', '@', '#']

        self.func = func or (lambda x: x)
        self.chars = chars or self.define_tone_curve(self.func)

    def define_tone_curve(self, func):
        """
        Applies a given tone curve function to the set
        of symbols, thus creating a threshold map
        :param func: The mapping function
        :type func: LambdaType
        :return: {threshold: symbol} dict
        """
        l = len(self.symbols)
        self.func = func
        self.chars = {func(x): sym for x, sym in zip(range(l, 255 + 255 % l, int(255/l)), self.symbols)}
        self.chars[256] = '#'
        return self.chars

    def to_grayscale(self, path, resize):
        """
        Reads and converts an image file to grayscale
        :param path: Path to file
        :param resize: Resize multiplier, 0.12=12% of original
        :return: resized image converted to grayscale
        """
        img = Image.open(path)
        if resize is not None:
            img = self.resize(img, resize)
        return img.convert('L')

    @staticmethod
    def resize(image, percentage):
        """
        Resizes the image
        :param image: PIL Image object
        :param percentage: Resize multiplier
        :return: Resized image
        """
        w, h = [int(percentage*i) for i in image.size]
        return image.resize((w, h), Image.ANTIALIAS)

    def load(self, path, resize=None):
        """
        Reads an image file, resizes it and converts to grayscale
        :param path: Path to file
        :param resize: Resize multiplier
        :return: None
        """
        self.image = self.to_grayscale(path, resize)
        self.image_width, self.image_height = self.image.size
        self.image_length = self.image_width*self.image_height
        self.data = list(self.image.getdata())
        self.data = [self.data[r:r+self.image_width] for r in range(0, self.image_length, self.image_width)]

    def to_ascii(self, path=None, resize=None, draw=False):
        """
        Converts an image to ASCII Art
        :param path: Path to image, if not given the loaded image is taken
        :param resize: Resize multiplier, if not given the image is not resized
        :param draw: if True prints the image to console
        :return:
        """
        # TODO file printing
        if path is not None:
            self.load(path, resize)
        for row in range(self.image_height):
            out = []
            for pix in self.data[row]:
                for threshold in self.chars.keys():
                    if pix <= threshold:
                        out.append(self.chars[threshold])
                        out.append(self.chars[threshold])
                        break
            self.ascii.append("".join(out))
        if draw:
            self.print_ascii()
        return self.ascii

    def print_ascii(self):
        """
        Prints the stored image to console
        :return: None
        """
        for line in self.ascii:
            print(line)