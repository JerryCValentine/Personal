import io
import math
from PIL import Image, ImageFilter
import numpy as np
import copy

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

def combineSobelXY(_imageOne, _imageTwo): # Assumes they are the same size.
    xSize = _imageOne.size[0]
    ySize = _imageOne.size[1]
    addedImage = Image.new('L', (xSize, ySize), color = 'white')
    addedImageFilter = addedImage.load()
    
    for x in range(xSize):
        for y in range(ySize):
            addedImageFilter[x, y] = int(round(math.sqrt(_imageOne.getpixel((x,y))**2 + _imageTwo.getpixel((x,y))**2)))

    return addedImage

def convolve(_image, _kernel, _isColor=True):
    posX = 0
    posY = 0
    pixelImage = _image.load()
    xSize = _image.size[0]
    ySize = _image.size[1]
    if(_isColor):
        newImage = Image.new('RGBA', (xSize, ySize), color = 'white')
    else:
        newImage = Image.new('L', (xSize, ySize), color = 'white')
    newPixelImage = newImage.load()
    
    while (posY < ySize):
        red = 0
        green = 0
        blue = 0
        intensity = 0
        pixelAverageScale = 0
        for x in range(int(len(_kernel)/-2), int((len(_kernel)/2) + 1)):
            for y in range(int(len(_kernel[0])/-2), int((len(_kernel[0])/2) + 1)):
                if((posX + x) >= 0 and (posX + x) < xSize and (posY + y) >= 0 and (posY + y) < ySize):
                    if(_isColor):
                        red += _kernel[x + int(len(_kernel)/2+.5)-1][y + int((len(_kernel[0])/2)+.5)-1] * pixelImage[posX + x, posY + y][0]
                        green += _kernel[x + int(len(_kernel)/2+.5)-1][y + int((len(_kernel[0])/2)+.5)-1] * pixelImage[posX + x, posY + y][1]
                        blue += _kernel[x + int(len(_kernel)/2+.5)-1][y + int((len(_kernel[0])/2)+.5)-1] * pixelImage[posX + x, posY + y][2]
                    else:
                        intensity += _kernel[x + int(len(_kernel)/2+.5)-1][y + int((len(_kernel[0])/2)+.5)-1] * pixelImage[posX + x, posY + y]
                    pixelAverageScale += abs(_kernel[x + int(len(_kernel)/2+.5)-1][y + int((len(_kernel[0])/2)+.5)-1])
        if(_isColor):
            newPixelImage[posX, posY] = (int(abs(red) / pixelAverageScale), int(abs(green) / pixelAverageScale), int(abs(blue) / pixelAverageScale))
        else:
            newPixelImage[posX, posY] = (int(abs(intensity) / pixelAverageScale))
        if(posX < xSize-1):
            posX += 1
        else:
            posX = 0
            posY += 1
    
    newImage.save(".\\School Work\\Computer Vision\\ConvoledImage.png") # For testing only
    return newImage

def getEdgeMap(_image):
    horizontalEdgeImage = getEdgeX(_image)
    verticalEdgeImage = getEdgeY(_image)
    return combineSobelXY(horizontalEdgeImage, verticalEdgeImage)

def getEdgeX(_image):
    horizontalSobelKernel = [
        [1, 0, -1],
        [2, 0, -2],
        [1, 0, -1]
    ]
    imageGreyScale = _image.convert('L')
    return convolve(imageGreyScale, horizontalSobelKernel, False)

def getEdgeY(_image):
    verticalSobelKernel = [
        [1, 2, 1],
        [0, 0, 0],
        [-1, -2, -1]
    ]
    imageGreyScale = _image.convert('L')
    return convolve(imageGreyScale, verticalSobelKernel, False)

def sharpen(_image):
    
    sharpenedImage = combineOriginalAndSobel(_image, getEdgeMap(_image), 1, 1)

    sharpenedImage.save(".\\School Work\\Computer Vision\\Sharpened.png")

def gaussianEquation(_x, _y, _sigma):
    # test = 1 / (2*np.pi*(_sigma**2)) * np.exp(-(_x**2 + _y**2)/(2* _sigma**2))
    # print(test)
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

def main():
    # image = Image.open("School Work\\Computer Vision\\images\\image0.jpg") # Car crash
    # image = Image.open("School Work\\Computer Vision\\images\\Valve_original_(1).png") # Valve
    # image = Image.open("School Work\\Computer Vision\\images\\taj-rgb-noise.jpg")
    image = Image.open("School Work\\Computer Vision\\images\\saltpepper.png")
    # image = Image.open("School Work\\Computer Vision\\images\\LinedImage.png")
    # kernel = [
    #     [1, 0, -1],
    #     [2, 0, -1],
    #     [1, 0, -1]
    # ]

    kernel = gaussianKernelGenerator(7, 1)

    image = convolve(image, kernel)
    image.save(".\\School Work\\Computer Vision\\Blured.png")

    # sharpen(image)

if __name__ == "__main__":
    main()

    