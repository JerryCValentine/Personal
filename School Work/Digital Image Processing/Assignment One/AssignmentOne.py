from PIL import Image, ImageFilter
import math

def readVoltages(_path):
    fileObject = open(_path,"r")
    fileString = fileObject.readlines()[0][1:-1].split(", ")
    voltageList = [float(i) for i in fileString]
    return voltageList

def convertVoltageToIntensity(_voltageList):
    intensities = [int((i - .2) / 1.3 * 255) for i in _voltageList]
    fileObject = open("School Work\\Digital Image Processing\\Assignment One\\test.txt","w")
    x = 0
    for i in range(len(intensities)):
        if(x == 256):
            x = 0
            fileObject.write("\n")
        fileObject.write(str(intensities[i]) + ", ")
    fileObject.close()
    return intensities

def convertIntensityToImage(_intensityList):
    size = int(math.sqrt(len(_intensityList)))
    newImage = Image.new('L', (size, size), color = 'white')
    newPixelImage = newImage.load()
    y = 0

    for y in range(size):
        for x in range(size):
            newPixelImage[x,y] = newPixelImage[x,y] - _intensityList[x + (y * 255)]
        newImage.save("School Work\\Digital Image Processing\\Assignment One\\easy.png")
    
    return newImage
    

def main():
    voltageListEasy = readVoltages("School Work\\Digital Image Processing\\Assignment One\\jvalen16_easy.txt")
    # voltageListMedium = readVoltages("School Work\\Digital Image Processing\\Assignment One\\jvalen16_medium.txt")
    # voltageListHard = readVoltages("School Work\\Digital Image Processing\\Assignment One\\jvalen16_hard.txt")

    intensityListEasy = convertVoltageToIntensity(voltageListEasy)
    # intensityListMedium = convertVoltageToIntensity(voltageListMedium)
    # intensityListHard = convertVoltageToIntensity(voltageListHard)

    convertIntensityToImage(intensityListEasy).save("School Work\\Digital Image Processing\\Assignment One\\easy.png")
    # convertIntensityToImage(intensityListMedium).save("School Work\\Digital Image Processing\\Assignment One\\medium.png")
    # convertIntensityToImage(intensityListHard).save("School Work\\Digital Image Processing\\Assignment One\\hard.png")

if __name__ == "__main__":
    main()