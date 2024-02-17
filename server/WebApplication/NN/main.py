import sys
import os
import modifyImage as mI
import datetime

from PIL import Image


if __name__ == "__main__":
    now = datetime.datetime.now().strftime("%Y.%m.%d_%H.%M.%S")
    filename = os.path.splitext(sys.argv[1])[0]
    originalImage = Image.open(sys.argv[1])
    mask = mI.getMask(originalImage)
    mask.save(f'{filename}1_{now}.png')
    newImage2 = mI.deleteBackground(originalImage, mask)
    newImage2.save(f'{filename}2_{now}.png')
    newImage3 = mI.highlights(originalImage, mask)
    newImage3.save(f'{filename}3_{now}.png')
    print(f'{sys.argv[1]}%{filename}1_{now}.png%{filename}2_{now}.png%{filename}3_{now}.png'.replace('images/', ''))
