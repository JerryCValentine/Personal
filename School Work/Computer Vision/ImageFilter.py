import io
import math
from PIL import Image, ImageFilter
import glob
import numpy as np
from copy import deepcopy as copy

scunchDict = {
    -255: 0, 
    -254: 0,
    -253: 1, 
    -252: 1,
    -251: 2, 
    -250: 2,
    -249: 3, 
    -248: 3,
    -247: 4, 
    -246: 4,
    -245: 5, 
    -244: 5,
    -243: 6, 
    -242: 6,
    -241: 7, 
    -240: 7,
    -239: 8, 
    -238: 8,
    -237: 9, 
    -236: 9,
    -235: 10, 
    -234: 10,
    -233: 11, 
    -232: 11,
    -231: 12, 
    -230: 12,
    -229: 13, 
    -228: 13,
    -227: 14, 
    -226: 14,
    -225: 15, 
    -224: 15,
    -223: 16, 
    -222: 16,
    -221: 17, 
    -220: 17,
    -219: 18, 
    -218: 18,
    -217: 19, 
    -216: 19,
    -215: 20, 
    -214: 20,
    -213: 21, 
    -212: 21,
    -211: 22, 
    -210: 22,
    -209: 23, 
    -208: 23,
    -207: 24, 
    -206: 24,
    -205: 25, 
    -204: 25,
    -203: 26, 
    -202: 26,
    -201: 27, 
    -200: 27,
    -199: 28, 
    -198: 28,
    -197: 29, 
    -196: 29,
    -195: 30, 
    -194: 30,
    -193: 31, 
    -192: 31,
    -191: 32, 
    -190: 32,
    -189: 33, 
    -188: 33,
    -187: 34, 
    -186: 34,
    -185: 35, 
    -184: 35,
    -183: 36, 
    -182: 36,
    -181: 37, 
    -180: 37,
    -179: 38, 
    -178: 38,
    -177: 39, 
    -176: 39,
    -175: 40, 
    -174: 40,
    -173: 41, 
    -172: 41,
    -171: 42, 
    -170: 42,
    -169: 43, 
    -168: 43,
    -167: 44, 
    -166: 44,
    -165: 45, 
    -164: 45,
    -163: 46, 
    -162: 46,
    -161: 47, 
    -160: 47,
    -159: 48, 
    -158: 48,
    -157: 49, 
    -156: 49,
    -155: 50, 
    -154: 50,
    -153: 51, 
    -152: 51,
    -151: 52, 
    -150: 52,
    -149: 53, 
    -148: 53,
    -147: 54, 
    -146: 54,
    -145: 55, 
    -144: 55,
    -143: 56, 
    -142: 56,
    -141: 57, 
    -140: 57,
    -139: 58, 
    -138: 58,
    -137: 59, 
    -136: 59,
    -135: 60, 
    -134: 60,
    -133: 61, 
    -132: 61,
    -131: 62, 
    -130: 62,
    -129: 63, 
    -128: 63,
    -127: 64, 
    -126: 64,
    -125: 65, 
    -124: 65,
    -123: 66, 
    -122: 66,
    -121: 67, 
    -120: 67,
    -119: 68, 
    -118: 68,
    -117: 69, 
    -116: 69,
    -115: 70, 
    -114: 70,
    -113: 71, 
    -112: 71,
    -111: 72, 
    -110: 72,
    -109: 73, 
    -108: 73,
    -107: 74, 
    -106: 74,
    -105: 75, 
    -104: 75,
    -103: 76, 
    -102: 76,
    -101: 77, 
    -100: 77,
    -99: 78, 
    -98: 78,
    -97: 79, 
    -96: 79,
    -95: 80, 
    -94: 80,
    -93: 81, 
    -92: 81,
    -91: 82, 
    -90: 82,
    -89: 83, 
    -88: 83,
    -87: 84, 
    -86: 84,
    -85: 85, 
    -84: 85,
    -83: 86, 
    -82: 86,
    -81: 87, 
    -80: 87,
    -79: 88, 
    -78: 88,
    -77: 89, 
    -76: 89,
    -75: 90, 
    -74: 90,
    -73: 91, 
    -72: 91,
    -71: 92, 
    -70: 92,
    -69: 93, 
    -68: 93,
    -67: 94, 
    -66: 94,
    -65: 95, 
    -64: 95,
    -63: 96, 
    -62: 96,
    -61: 97, 
    -60: 97,
    -59: 98, 
    -58: 98,
    -57: 99, 
    -56: 99,
    -55: 100, 
    -54: 100,
    -53: 101, 
    -52: 101,
    -51: 102, 
    -50: 102,
    -49: 103, 
    -48: 103,
    -47: 104, 
    -46: 104,
    -45: 105, 
    -44: 105,
    -43: 106, 
    -42: 106,
    -41: 107, 
    -40: 107,
    -39: 108, 
    -38: 108,
    -37: 109, 
    -36: 109,
    -35: 110, 
    -34: 110,
    -33: 111, 
    -32: 111,
    -31: 112, 
    -30: 112,
    -29: 113, 
    -28: 113,
    -27: 114, 
    -26: 114,
    -25: 115, 
    -24: 115,
    -23: 116, 
    -22: 116,
    -21: 117, 
    -20: 117,
    -19: 118, 
    -18: 118,
    -17: 119, 
    -16: 119,
    -15: 120, 
    -14: 120,
    -13: 121, 
    -12: 121,
    -11: 122, 
    -10: 122,
    -9: 123, 
    -8: 123,
    -7: 124, 
    -6: 124,
    -5: 125, 
    -4: 125,
    -3: 126, 
    -2: 126,
    -1: 127, 
    0: 127,
    1: 128,
    2: 128,
    3: 129, 
    4: 129,
    5: 130, 
    6: 130,
    7: 131, 
    8: 131,
    9: 132, 
    10: 132,
    11: 133,
    12: 133,
    13: 134, 
    14: 134,
    15: 135, 
    16: 135,
    17: 136, 
    18: 136,
    19: 137, 
    20: 137,
    21: 138,
    22: 138,
    23: 139, 
    24: 139,
    25: 140, 
    26: 140,
    27: 141, 
    28: 141,
    29: 142, 
    30: 142,
    31: 143,
    32: 143,
    33: 144, 
    34: 144,
    35: 145, 
    36: 145,
    37: 146, 
    38: 146,
    39: 147, 
    40: 147,
    41: 148,
    42: 148,
    43: 149, 
    44: 149,
    45: 150, 
    46: 150,
    47: 151, 
    48: 151,
    49: 152, 
    50: 152,
    51: 153,
    52: 153,
    53: 154, 
    54: 154,
    55: 155, 
    56: 155,
    57: 156, 
    58: 156,
    59: 157, 
    60: 157,
    61: 158,
    62: 158,
    63: 159, 
    64: 159,
    65: 160, 
    66: 160,
    67: 161, 
    68: 161,
    69: 162, 
    70: 162,
    71: 163,
    72: 163,
    73: 164, 
    74: 164,
    75: 165, 
    76: 165,
    77: 166, 
    78: 166,
    79: 167, 
    80: 167,
    81: 168,
    82: 168,
    83: 169, 
    84: 169,
    85: 170, 
    86: 170,
    87: 171, 
    88: 171,
    89: 172, 
    90: 172,
    91: 173,
    92: 173,
    93: 174, 
    94: 174,
    95: 175, 
    96: 175,
    97: 176, 
    98: 176,
    99: 177, 
    100: 177,
    101: 178,
    102: 178,
    103: 179, 
    104: 179,
    105: 180, 
    106: 180,
    107: 181, 
    108: 181,
    109: 182, 
    110: 182,
    111: 183,
    112: 183,
    113: 184, 
    114: 184,
    115: 185, 
    116: 185,
    117: 186, 
    118: 186,
    119: 187, 
    120: 187,
    121: 188,
    122: 188,
    123: 189, 
    124: 189,
    125: 190, 
    126: 190,
    127: 191, 
    128: 191,
    129: 192, 
    130: 192,
    131: 193,
    132: 193,
    133: 194, 
    134: 194,
    135: 195, 
    136: 195,
    137: 196, 
    138: 196,
    139: 197, 
    140: 197,
    141: 198,
    142: 198,
    143: 199, 
    144: 199,
    145: 200, 
    146: 200,
    147: 201, 
    148: 201,
    149: 202, 
    150: 202,
    151: 203,
    152: 203,
    153: 204, 
    154: 204,
    155: 205, 
    156: 205,
    157: 206, 
    158: 206,
    159: 207, 
    160: 207,
    161: 208,
    162: 208,
    163: 209, 
    164: 209,
    165: 210, 
    166: 210,
    167: 211, 
    168: 211,
    169: 212, 
    170: 212,
    171: 213,
    172: 213,
    173: 214, 
    174: 214,
    175: 215, 
    176: 215,
    177: 216, 
    178: 216,
    179: 217, 
    180: 217,
    181: 218,
    182: 218,
    183: 219, 
    184: 219,
    185: 220, 
    186: 220,
    187: 221, 
    188: 221,
    189: 222, 
    190: 222,
    191: 223,
    192: 223,
    193: 224, 
    194: 224,
    195: 225, 
    196: 225,
    197: 226, 
    198: 226,
    199: 227, 
    200: 227,
    201: 228,
    202: 228,
    203: 229, 
    204: 229,
    205: 230, 
    206: 230,
    207: 231, 
    208: 231,
    209: 232, 
    210: 232,
    211: 233,
    212: 233,
    213: 234, 
    214: 234,
    215: 235, 
    216: 235,
    217: 236, 
    218: 236,
    219: 237, 
    220: 237,
    221: 238,
    222: 238,
    223: 239, 
    224: 239,
    225: 240, 
    226: 240,
    227: 241, 
    228: 241,
    229: 242, 
    230: 242,
    231: 243,
    232: 243,
    233: 244, 
    234: 244,
    235: 245, 
    236: 245,
    237: 246, 
    238: 246,
    239: 247, 
    240: 247,
    241: 248,
    242: 248,
    243: 249, 
    244: 249,
    245: 250, 
    246: 250,
    247: 251, 
    248: 251,
    249: 252, 
    250: 252,
    251: 253,
    252: 253,
    253: 254, 
    254: 254,
    255: 255,
    }

class KeyPoint():
    def __init__(self, _location=(-1,-1), _scale=-1, _orientation=-1, _descriptor=[]):
        self.location = _location
        self.scale = _scale
        self.orientation = _orientation
        self.descriptor = _descriptor

def combineOriginalAndSobel(_originalImage, _sobelImage, _weightOne, _weightTwo): # Assumes they are the same size.
    xSize = _originalImage.size[0]
    ySize = _originalImage.size[1]
    addedImage = Image.new('RGBA', (xSize, ySize), color = 'white')
    addedImageFilter = addedImage.load()
    
    for x in range(xSize):
        for y in range(ySize):
            addedImageFilter[x, y] = (int(((_weightOne * _originalImage.getpixel((x, y))[0]) + (_weightTwo * _sobelImage.getpixel((x, y))))), 
                                    int(((_weightOne * _originalImage.getpixel((x, y))[1]) + (_weightTwo * _sobelImage.getpixel((x, y))))), 
                                    int(((_weightOne * _originalImage.getpixel((x, y))[2]) + (_weightTwo * _sobelImage.getpixel((x, y)))))
                                    )

    return addedImage

def combineSobelXY(_edgeMapOne, _edgeMapTwo): # Assumes they are the same size.
    xSize = len(_edgeMapOne)
    ySize = len(_edgeMapOne[0])
    addedImage = Image.new('L', (xSize, ySize), color = 'white')
    addedImageFilter = addedImage.load()
    
    for x in range(xSize):
        for y in range(ySize):
            addedImageFilter[x, y] = int(round(math.sqrt(_edgeMapOne[x][y]**2 + _edgeMapTwo[x][y]**2)))

    return addedImage

def convolve(_image, _kernel, _mode=0): # 0 - color, 1 - sobel, 2 - sobelIncludingNegitives, 3 greyscale
    posX = 0
    posY = 0
    
    pixelImage = _image.load()
    xSize = _image.size[0]
    ySize = _image.size[1]
    if(_mode is 0):
        newImage = Image.new('RGBA', (xSize, ySize), color = 'white')
        newPixelImage = newImage.load()
    elif(_mode is 1 or _mode is 3):
        newImage = Image.new('L', (xSize, ySize), color = 'white')
        newPixelImage = newImage.load()
    else:
        newImage = []
        for x in range(xSize):
            newImage.append([])
            for y in range(ySize):
                newImage[x].append(0)
        


    while (posY < ySize):
        red = 0
        green = 0
        blue = 0
        intensity = 0
        pixelAverageScale = 0
        for x in range(int(len(_kernel)/-2), int((len(_kernel)/2) + 1)):
            for y in range(int(len(_kernel[0])/-2), int((len(_kernel[0])/2) + 1)):
                if((posX + x) >= 0 and (posX + x) < xSize and (posY + y) >= 0 and (posY + y) < ySize):
                    if(_mode is 0):
                        red += _kernel[x + int(len(_kernel)/2+.5)-1][y + int((len(_kernel[0])/2)+.5)-1] * pixelImage[posX + x, posY + y][0]
                        green += _kernel[x + int(len(_kernel)/2+.5)-1][y + int((len(_kernel[0])/2)+.5)-1] * pixelImage[posX + x, posY + y][1]
                        blue += _kernel[x + int(len(_kernel)/2+.5)-1][y + int((len(_kernel[0])/2)+.5)-1] * pixelImage[posX + x, posY + y][2]
                    else:
                        intensity += _kernel[x + int(len(_kernel)/2+.5)-1][y + int((len(_kernel[0])/2)+.5)-1] * pixelImage[posX + x, posY + y]
                    pixelAverageScale += abs(_kernel[x + int(len(_kernel)/2+.5)-1][y + int((len(_kernel[0])/2)+.5)-1])
                else:
                    if(_mode is 0):
                        red += _kernel[x + int(len(_kernel)/2+.5)-1][y + int((len(_kernel[0])/2)+.5)-1] * 0
                        green += _kernel[x + int(len(_kernel)/2+.5)-1][y + int((len(_kernel[0])/2)+.5)-1] * 0
                        blue += _kernel[x + int(len(_kernel)/2+.5)-1][y + int((len(_kernel[0])/2)+.5)-1] * 0
                    else:
                        intensity += _kernel[x + int(len(_kernel)/2+.5)-1][y + int((len(_kernel[0])/2)+.5)-1] * 0
                    pixelAverageScale += abs(_kernel[x + int(len(_kernel)/2+.5)-1][y + int((len(_kernel[0])/2)+.5)-1])

        if(_mode is 0): 
            newPixelImage[posX, posY] = (int(abs(red) / pixelAverageScale), int(abs(green) / pixelAverageScale), int(abs(blue) / pixelAverageScale))
        elif(_mode is 1):
            newPixelImage[posX, posY] = scunchDict[int(intensity / pixelAverageScale)]
        elif(_mode is 3):
            newPixelImage[posX, posY] = int(abs(intensity) / pixelAverageScale)
        else:
            newImage[posX][posY] = int(intensity / pixelAverageScale)

        if(posX < xSize-1):
            posX += 1
        else:
            posX = 0
            posY += 1

    if(_mode != 2):
        newImage.save(".\\School Work\\Computer Vision\\Processed Images\\ConvoledImage.png") # For testing only
    return newImage

def getEdgeMapMagnitudes(_image):
    horizontalEdgeMapValues = getEdgeXMapValues(_image)
    verticalEdgeMapValues = getEdgeYMapValues(_image)
    edgemap = combineSobelXY(horizontalEdgeMapValues, verticalEdgeMapValues)
    edgemap.save(".\\School Work\\Computer Vision\\Processed Images\\EdgeMap.png")
    return edgemap

def getEdgeXMapValues(_image):
    horizontalSobelKernel = [
        [1, 0, -1],
        [2, 0, -2],
        [1, 0, -1]
    ]
    imageGreyScale = _image.convert('L')
    horizontalEdgeMap = convolve(imageGreyScale, horizontalSobelKernel, 2)
    # horizontalEdgeMap.save(".\\School Work\\Computer Vision\\Processed Images\\horizontalEdge.png")
    return horizontalEdgeMap

def getEdgeYMapValues(_image):
    verticalSobelKernel = [
        [1, 2, 1],
        [0, 0, 0],
        [-1, -2, -1]
    ]
    imageGreyScale = _image.convert('L')
    verticalEdgeMap = convolve(imageGreyScale, verticalSobelKernel, 2)
    # verticalEdgeMap.save(".\\School Work\\Computer Vision\\Processed Images\\verticalEdge.png")
    return verticalEdgeMap

def getEdgeDirectionMap(_image):
    xSize = _image.size[0]
    ySize = _image.size[1]
    horizontalEdgeMapValues = getEdgeXMapValues(_image)
    verticalEdgeMapValues = getEdgeYMapValues(_image)
    edgeDirectionMap = []

    for y in range(ySize):
        edgeDirectionMap.append([])
        for x in range(xSize):
            deltaX = horizontalEdgeMapValues[x][y]
            deltaY = verticalEdgeMapValues[x][y]
            theta = math.atan2(deltaX, deltaY)
            edgeDirectionMap[y].append(theta)

def sharpen(_image):
    bluredImage = convolve(_image, gaussianKernelGenerator(5, 1), 0)
    sharpenedImage = combineOriginalAndSobel(bluredImage, getEdgeMapMagnitudes(_image), 1, 1)
    sharpenedImage.save(".\\School Work\\Computer Vision\\Processed Images\\Sharpened.png")
    return sharpenedImage

def gaussianEquation(_x, _y, _sigma):
    return 1 / (2*np.pi*(_sigma**2)) * np.exp(-(_x**2 + _y**2)/(2* _sigma**2))

def gaussianKernelGenerator(_size, _sigma):
    kernel = np.zeros((_size, _size), np.float32)
    m = _size//2
    for x in range(-m, m+1):
        for y in range(-m, m+1):
            kernel[x+m, y+m] = gaussianEquation(x, y, _sigma)
    scaleFactor = 1 / kernel[0,0] # Gets scale to convert to int
    for x in range(len(kernel)):
        for y in range(len(kernel[x])):
             kernel[x,y] = round(kernel[x,y] * scaleFactor)
    return kernel

def decreaseSize(_image, _factor):
    smallImage = copy(_image)
    smallImage.thumbnail((int(_image.size[0]/_factor),  int(_image.size[1]/_factor)))
    return smallImage

def generateImagesForScaleSpace(_image):
    for scale in range(2, 16, 4):
        for size in range(5, 18, 6):
            kernel = gaussianKernelGenerator(size, 4)
            image = decreaseSize(_image, scale)
            image = image.convert('L')
            image = convolve(image, kernel, 3)
            image.save(".\\School Work\\Computer Vision\\Scaled-Blured Images\\image-" + str(scale) + "-" + str(size) + ".png" )

    for size in range(5, 18, 6):
        kernel = gaussianKernelGenerator(size, 4)
        image = decreaseSize(_image, 1)
        image = image.convert('L')
        image = convolve(image, kernel, 3)
        image.save(".\\School Work\\Computer Vision\\Scaled-Blured Images\\image-" + str(1) + "-" + str(size) + ".png" )

def createDifferenceOfGaussian(_imageOne, _imageTwo):
    xSize = _imageOne.size[0]
    ySize = _imageOne.size[1]
    newImage = Image.new('L', (xSize, ySize), color = 'white')
    newImageFilter = newImage.load()
    
    for x in range(xSize):
        for y in range(ySize):
            newImageFilter[x, y] = _imageOne.getpixel((x,y)) - _imageTwo.getpixel((x,y)) 

    return newImage

def computeDoG(_images):
    DoG = []
    for i in range(len(_images)):
        DoG.append([])
        for j in range(len(_images[i])):
            if(not len(_images[i]) == j + 1):
                dogImage = createDifferenceOfGaussian(_images[i][j], _images[i][j+1])
                dogImage.save(".\\School Work\\Computer Vision\\Scaled-Blured Images\\DoG\\DoG-" + str(i) + "-" + str(j) + ".png")
                DoG[i].append(dogImage)
    return DoG

def paintKeyPoints(_image, _keyPoints):
    pixelImage = _image.load()
    for keyPoint in _keyPoints:
        pixelImage[keyPoint.location[0],keyPoint.location[1]] = (0,255,0)
    _image.save(".\\School Work\\Computer Vision\\Scaled-Blured Images\\test.png")

def findLocalMaxs(_images):
    listOfKeyPoints = []
    xSize = _images[0].size[0]
    ySize = _images[0].size[1]
    localMax = (-1,-1)
    isKeyPointAlready = False

    for x in range(xSize):
        for y in range(ySize):
            for imageIndex in range(2):
                for i in range(-1,2):
                    for j in range(-1,2):
                        if(x + i >= 0 and x + i < xSize and y + j >= 0 and y + j < ySize):
                            if(localMax == (-1,-1)):
                                localMax = ((x+i,y+j), _images[imageIndex].getpixel((x+i,y+j)))
                            if(localMax[1] < _images[imageIndex].getpixel((x+i,y+j))):
                                localMax = ((x+i,y+j), _images[imageIndex].getpixel((x+i,y+j)))
            
            if(localMax[1] > 15):
                isKeyPoint = False
                for keyPoint in listOfKeyPoints: # Searching if already keypoint or not
                    if(keyPoint.location is localMax[0]):
                        isKeyPointAlready = True
                        break
                if(not isKeyPointAlready):
                    listOfKeyPoints.append(KeyPoint(localMax[0],1,0,localMax[1]))
            localMax = (-1,-1)
    paintKeyPoints(Image.open("School Work\\Computer Vision\\images\\room1.jpeg"), listOfKeyPoints)
    return listOfKeyPoints

def sift(_image):
    ## Create scalespace
    generateImagesForScaleSpace(_image)

    ## Compute DoG
    # Grab all of the images in the scalespace
    images = []
    stringHolder = []
    previousNumber = -1
    index = -1
    for fileName in glob.iglob(".\\School Work\\Computer Vision\\Scaled-Blured Images\\image-*"):
        stringHolder = fileName.split('-')
        if(int(stringHolder[2]) is int(previousNumber)):
            images[index].append(Image.open(fileName))
        else:
            images.append([])
            index += 1
            images[index].append(Image.open(fileName))
            previousNumber = stringHolder[2]

    dogImages = computeDoG(images)

    ## Find local Maximums
    
    keyPoints = findLocalMaxs(dogImages)

    ## Descript local Maximums

def main():
    # image = Image.open("School Work\\Computer Vision\\images\\image0.jpg") # Car crash
    # image = Image.open("School Work\\Computer Vision\\images\\Valve_original_(1).png") # Valve
    image = Image.open("School Work\\Computer Vision\\images\\taj-rgb-noise.jpg")
    # image = Image.open("School Work\\Computer Vision\\images\\saltpepper.png")
    # image = Image.open("School Work\\Computer Vision\\images\\smallCross.png")
    # roomOne = Image.open("School Work\\Computer Vision\\images\\room1.jpeg")
    # roomTwo = Image.open("School Work\\Computer Vision\\images\\room2.jpeg")
    # image = Image.open(".\\School Work\\Computer Vision\\Processed Images\\Blured.png")
    
    # kernel = [
    #     [-1, -2, -1],
    #     [0, 0, 0],
    #     [1, 2, 1]
    # ]

    # Ixs = getEdgeXMapValues(roomOne)
    # Iys = getEdgeYMapValues(roomOne)
    # keyPoints = findLocalMaxs([Image.open("School Work\\Computer Vision\\Scaled-Blured Images\\DoG\\DoG-3-0.png"),Image.open("School Work\\Computer Vision\\Scaled-Blured Images\\DoG\\DoG-3-1.png")])
    # sizeOfWindow = 5
    # xSize = roomOne.size[0]
    # ySize = roomOne.size[1]

    # Ixx = 0
    # Iyy = 0
    # Ixy = 0

    # rValues = []

    # for keyPoint in keyPoints:
    #     location = keyPoint.location
    #     for x in range(location[0]-sizeOfWindow, location[0]+sizeOfWindow+1):
    #         for y in range(location[1]-sizeOfWindow, location[1]+sizeOfWindow+1):
    #             if(x >= 0 and x < xSize and y >= 0 and y < ySize):
    #                 Ixx += Ixs[x][y]**2
    #                 Iyy += Iys[x][y]**2
    #                 Ixy += Ixs[x][y] * Iys[x][y]
    #     w, v = np.linalg.eig([[Ixx, Ixy],[Ixy, Iyy]])
    #     rValues.append(w[0]*w[1] - .05 * ((w[0]+w[1])**2))

    # paintKeyPoints(decreaseSize(roomOne, 2), listOfKeyPoints)

    # print("test")

    # kernel = gaussianKernelGenerator(5, 1)
    # # image = image.convert('L')

    # bluredImage = convolve(image, kernel, 0)
    # bluredImage.save(".\\School Work\\Computer Vision\\Processed Images\\Blured.png")

    sharpen(image)

if __name__ == "__main__":
    main()

    