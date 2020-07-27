from PIL import Image
import os

inputdir = "D:/Word/DataSets/DS_1205/Migr/DS20180906120502_Full46786_2Conv_Migr_V0_60_R0_200_T0.5e6_Tc1"
outputdir = "D:/Word/DataSets/DS_1205/Migr/cropped"
img_names = os.listdir(inputdir)
for img_name in img_names:
    img_path = os.path.join(inputdir, img_name)
    img = Image.open(img_path)
    w, h = img.size
    left_top_box = (0, 0, w // 2, h // 2)
    right_top_box = (w // 2 + 1, 0, w, h // 2)
    left_bottom_box = (0, h // 2, w // 2, h)
    right_bottom_box = (w // 2 + 1, h // 2, w, h)

    name, ext = os.path.splitext(img_name)
    left_top_img = img.crop(left_top_box)
    left_top_img.save(os.path.join(outputdir, name + '_lt' + ext))
    right_top_img = img.crop(right_top_box)
    right_top_img.save(os.path.join(outputdir, name + '_rt' + ext))
    left_bottom_img = img.crop(left_bottom_box)
    left_bottom_img.save(os.path.join(outputdir, name + '_lb' + ext))
    right_bottom_img = img.crop(right_bottom_box)
    right_bottom_img.save(os.path.join(outputdir, name + '_rb' + ext))
