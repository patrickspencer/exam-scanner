from PIL import Image

img = Image.open("exam_small_spacing_blank_right_rotated.png")
# dimensions = (start_x, start_y, end_x, end_y)
dimensions = (180, 450, 700, 890)
img2 = img.crop(dimensions)
img2.save("cropped_to_be_graded.png")


