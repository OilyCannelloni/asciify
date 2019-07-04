from PIL import Image
import cv2
import os


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

    @staticmethod
    def linear(ax, b):
        return lambda x: ax*x+b

    @staticmethod
    def poly(*args):
        return lambda x: sum([args[i]*x**i for i in range(len(args))])

    @staticmethod
    def homographic(a, b, c, d):
        return lambda x: (a*x+b)/(c*x+d)


class ImageAsciifier:
    def __init__(self, func=None, charmap=None, symbols=None):
        """
        Class initializer
        :param func: Preset tone curve function (see IACurves)
        :type func: LambdaType
        :param charmap: Predefined threshold map
        :type charmap: {threshold: symbol} dict
        :param symbols: List of symbols used to draw
        """
        self.data = None
        self.image = None
        self.image_width = 0
        self.image_height = 0
        self.image_length = 0
        self.ascii = []

        # Set of symbols in order from darkest to brightest
        self.symbols = symbols or [' ', '`', "'", '.', '"', ',', '-', '^', '>', '=', '+', '*', 'c', 'u', 'r', 'o',
                                   'h', 'i', 'e', 'a', 'x', 'w', '?', 'O', 'D', 'N', 'S', 'M', 'X', 'W', '@', '#']

        self.func = func or (lambda x: x)
        self.charmap = charmap or self.define_tone_curve(self.func)

    def define_tone_curve(self, func):
        """
        Applies a given tone curve function to the set
        of symbols, thus creating a threshold map
        :param func: The mapping function
        :type func: LambdaType
        :return: {threshold: symbol} dict
        """
        if func is not None:
            l = len(self.symbols)
            self.func = func
            self.charmap = {func(x): sym for x, sym in zip(range(l, 255 + 255 % l, int(255 / l)), self.symbols)}
            self.charmap[256] = '#'
        return self.charmap

    def to_grayscale(self, load, resize):
        """
        Reads and converts an image file to grayscale
        :param load: Path to file OR PIL image object
        :param resize: Resize multiplier, 0.12=12% of original
        :return: resized image converted to grayscale
        """
        img = Image.open(load) if type(load) is str else load
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

    def load(self, img, resize=None):
        """
        Reads an image file, resizes it and converts to grayscale
        :param img: Path to file OR PIL image object
        :param resize: Resize multiplier
        :return: None
        """
        self.image = self.to_grayscale(img, resize)
        self.image_width, self.image_height = self.image.size
        self.image_length = self.image_width*self.image_height
        self.data = list(self.image.getdata())
        self.data = [self.data[r:r+self.image_width] for r in range(0, self.image_length, self.image_width)]

    def img_to_ascii(self, load=None, resize=None, draw=False, file=None):
        """
        Converts an image to ASCII Art
        :param path: Path to image, if not given the loaded image is taken
        :param resize: Resize multiplier, if not given the image is not resized
        :param draw: if True prints the image to console
        :return: List of strings containing frame
        """
        # TODO file printing
        self.ascii = []
        if load is not None:
            self.load(load, resize)
        for row in range(self.image_height):
            out = []
            for pix in self.data[row]:
                for threshold in self.charmap.keys():
                    if pix <= threshold:
                        out.append(self.charmap[threshold])
                        out.append(self.charmap[threshold])
                        break
            self.ascii.append("".join(out))
        self.print_ascii(draw, file)
        return self.ascii

    def print_ascii(self, draw, file):
        """
        Prints the stored image to console
        :return: None
        """
        if file is not None:
            try:
                with open(file, 'w') as f:
                    for line in self.ascii:
                        f.write(line)
            except Exception as e:
                print("Invalid path!: {}".format(e))
        if draw:
            for line in self.ascii:
                print(line)





class VideoAsciifier(ImageAsciifier):
    def __init__(self, func=None, charmap=None, symbols=None, fps=10):
        super().__init__(func, charmap, symbols)
        self.fps = fps
        self.vc = cv2.VideoCapture(0)

    def cam_capture(self):
        cv2.imwrite("frame.jpg", self.vc.read()[1])
        return Image.open("frame.jpg")

    def start_preview(self, fps=None, resize=None):
        self.fps = fps or self.fps
        try:
            while True:
                frame=self.cam_capture()
                self.img_to_ascii(load=frame, resize=resize, draw=False)
                os.system("cls")
                print("Press ESC to stop preview\n")
                self.print_ascii(True, None)
        except KeyboardInterrupt:
            self.vc.release()
