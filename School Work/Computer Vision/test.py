from PIL import Image
img = Image.open("C:\\Users\\jvalen16\\Documents\\Personal\\School Work\\Computer Vision\\saltpepper.png")

img_w = img.size[0]
img_h = img.size[1]

# The bigger the kernel size, the more intense the blur
kernel = [[1]*10]*10

outputIm = Image.new("RGB", (img_w, img_h))
d = []
for y in range(0, int(img_h)):
    for x in range(0, int(img_w)):
        r, g, b, count = 0, 0, 0, 0
        index_y = int((len(kernel[0]) - 1) / 2.0) * -1

        for kernel_offset_y in kernel:
            index_x = int((len(kernel_offset_y) - 1) / 2.0) * -1

            for kernel_val in kernel_offset_y:

                if img_w > x + index_x+1 > 0 and img_h > y + index_y+1 > 0:
                    temp_r, temp_g, temp_b = img.getpixel((int(x + index_x), int(y + index_y)))
                    r += temp_r * kernel_val
                    g += temp_g * kernel_val
                    b += temp_b * kernel_val
                    count += 1
                    index_x += 1
            index_y += 1

        if (r > 0):
            r = r / count
        if (g > 0):
            g = g / count
        if (b > 0):
            b = b / count

        d.append((r,g,b))

outputIm.putdata(d)
outputIm.save('blurred.png')