from PIL import Image


def extract_fragment(path_to_img, output_file, relative_pos, frag_size = (200, 200)):
    img = Image.open(path_to_img)
    width, heigth = img.size
    x, y = relative_pos
    frame = (int(width * x) - frag_size[0]//2,
             int(heigth * (1 - y)) - frag_size[1]//2,
             int(width * x) + frag_size[0]//2,
             int(heigth * (1 - y)) + frag_size[1]//2)
    fragment = img.crop(frame)
    fragment.save(output_file)


def count_relative_pos(rect, point):
    return ((point.x() - rect.x()) / rect.width(), 1 - (point.y() - rect.y()) / rect.height())