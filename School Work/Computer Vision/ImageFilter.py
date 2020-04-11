import numpy as np
import io
import math
from PIL import Image, ImageFilter
import copy

def addImages(_imageOne, _imageTwo, _weightOne=1, _weightTwo=1): # Assumes they are the same size.
    xSize = _imageOne.size[0]
    ySize = _imageOne.size[1]
    addedImage = Image.new('RGBA', (xSize, ySize), color = 'white')
    addedImageFilter = addedImage.load()
    
    for x in range(xSize):
        for y in range(ySize):
            addedImageFilter[x, y] = (int(((_weightOne * _imageOne.getpixel((x, y))[0]) + (_weightTwo * _imageTwo.getpixel((x, y))[0]))), 
                                    int(((_weightOne * _imageOne.getpixel((x, y))[1]) + (_weightTwo * _imageTwo.getpixel((x, y))[1]))), 
                                    int(((_weightOne * _imageOne.getpixel((x, y))[2]) + (_weightTwo * _imageTwo.getpixel((x, y))[2])))
                                    )

    return addedImage

def convolve(_image, _kernel):
    posX = 0
    posY = 0
    pixelImage = _image.load()
    xSize = _image.size[0]
    ySize = _image.size[1]
    newImage = Image.new('RGBA', (xSize, ySize), color = 'white')
    newPixelImage = newImage.load()
    
    while (posY < ySize):
        red = 0
        green = 0
        blue = 0
        pixelCount = 0
        for x in range(int(len(_kernel)/-2), int((len(_kernel)/2) + 1)):
            for y in range(int(len(_kernel[0])/-2), int((len(_kernel[0])/2) + 1)):
                if((posX + x) >= 0 and (posX + x) < xSize and (posY + y) >= 0 and (posY + y) < ySize):
                    red += _kernel[x + int(len(_kernel)/2+.5)-1][y + int((len(_kernel[0])/2)+.5)-1] * pixelImage[posX + x, posY + y][0]
                    green += _kernel[x + int(len(_kernel)/2+.5)-1][y + int((len(_kernel[0])/2)+.5)-1] * pixelImage[posX + x, posY + y][1]
                    blue += _kernel[x + int(len(_kernel)/2+.5)-1][y + int((len(_kernel[0])/2)+.5)-1] * pixelImage[posX + x, posY + y][2]
                    pixelCount += 1
        
        newPixelImage[posX, posY] = (int(abs(red) / pixelCount), int(abs(green) / pixelCount), int(abs(blue) / pixelCount))

        if(posX < xSize-1):
            posX += 1
        else:
            posX = 0
            posY += 1
    
    newImage.save("potato3.png") # For testing only
    return newImage

def sharpen(_image):
    xSize = _image.size[0]
    ySize = _image.size[1]
    horizontalSobelKernel = [
        [1, 0, -1],
        [2, 0, -2],
        [1, 0, -1]
    ]
    verticalSobelKernel = [
        [1, 2, 1],
        [0, 0, 0],
        [-1, -2, -1]
    ]

    horizontalEdgeImage = convolve(_image, horizontalSobelKernel)
    verticalEdgeImage = convolve(_image, verticalSobelKernel)

    fullEdgeImage = addImages(horizontalEdgeImage, verticalEdgeImage, 1, 1)
    fullEdgeImage.save("potato.png")
    sharpenedImage = addImages(_image, fullEdgeImage, 1, 1)

    sharpenedImage.save("potato2.png")

    

def main():
    # image = Image.open("C:\\Users\\jvalen16\\Desktop\\image2.jpg") # Car crash
    # image = Image.open("D:\\School Work\\Computer Vision\\Valve_original_(1).png") # Valve
    # image = Image.open("D:\\School Work\\Computer Vision\\taj-rgb-noise.jpg")
    # image = Image.open("D:\\School Work\\Computer Vision\\cat.jpg")
    image = Image.open("D:\\School Work\\Computer Vision\\image0 (1).jpeg")
    # imageLow = Image.open("D:\\School Work\\potato.png")
    # imageHigh = Image.open("D:\\School Work\\potato2.png")
    kernel = [
        [1, 0, -1],
        [2, 0, -1],
        [1, 0, -1]
    ]

    # addImages(_imageOne=imageLow, _imageTwo=imageHigh).save("potatoFinale.png")

    # convolve(image, kernel)
    sharpen(image)

if __name__ == "__main__":
    main()

    