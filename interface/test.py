from PIL import Image
import os


def scale_image(input_image_path,
                output_image_path,
                width=None,
                height=None
                ):
    original_image = Image.open(input_image_path)
    w, h = original_image.size
    print('The original image size is {wide} wide x {height} '
          'high'.format(wide=w, height=h))

    if width and height:
        max_size = (width, height)
    elif width:
        max_size = (width, h)
    elif height:
        max_size = (w, height)
    else:
        # No width or height specified
        raise RuntimeError('Width or height required!')

    original_image.thumbnail(max_size, Image.ANTIALIAS)
    original_image.save(output_image_path)

    scaled_image = Image.open(output_image_path)
    width, height = scaled_image.size
    print('The scaled image size is {wide} wide x {height} '
          'high'.format(wide=width, height=height))


inputdir = "D:/Word/big_img/DS20180906120502_Full46786_2Conv_V0_60_R0_200_T0.5e6_Tc1"
outputdir = "D:/Word/big_img/scaled"
img_names = os.listdir(inputdir)
w, h = 3449, 7866
for name in img_names:
    input_path = os.path.join(inputdir, name)
    output_path = os.path.join(outputdir, name)
    scale_image(input_path, output_path, w//2, h//2)
