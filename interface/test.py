from PIL import Image
im = Image.open("/interface/IQA/default1.bmp")
print('original:', im.size)
box = (100, 100, 700, 700)
region = im.crop(box)
region.save('IQA/crop1.bmp')
