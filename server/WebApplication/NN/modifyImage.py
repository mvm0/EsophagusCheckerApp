import predict
from PIL import Image


def getMask(img):
    return predict.predictMask(img)


def deleteBackground(img, mask):
    img = img.convert("RGBA")
    mask = mask.convert("RGBA")
    pixImg = img.load()
    pixMask = mask.load()
    width, height = img.size
    for y in range(height):
        for x in range(width):
            if pixMask[x, y] == (0, 0, 0, 255):
                pixImg[x, y] = (0, 0, 0, 0)
    return img


def highlights(img, mask):
    img = img.convert("RGBA")
    mask = mask.convert("RGBA")
    newMask = mask
    pixMask = mask.load()
    pixNewImage = newMask.load()
    width, height = mask.size
    for y in range(height):
        for x in range(width):
            if pixMask[x, y] == (255, 0, 0, 255):
                pixNewImage[x, y] = (255, 0, 0, 64)
            if pixMask[x, y] == (0, 255, 0, 255):
                pixNewImage[x, y] = (0, 255, 0, 64)
            if pixMask[x, y] == (0, 0, 255, 255):
                pixNewImage[x, y] = (0, 0, 255, 64)
            if pixMask[x, y] == (0, 255, 255, 255):
                pixNewImage[x, y] = (0, 255, 255, 64)
            if pixMask[x, y] == (255, 0, 255, 255):
                pixNewImage[x, y] = (255, 0, 255, 64)
            if pixMask[x, y] == (0, 0, 0, 255):
                pixNewImage[x, y] = (0, 0, 0, 0)
    result = Image.alpha_composite(img, newMask)
    return result