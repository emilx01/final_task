from PIL import Image
import numpy as np

# image resizing
# img = Image.open("fish.png")
# img_resized = img.resize((1920, 1080))
# img_resized.save("resized_fish.png")

# image rotating
# img = Image.open("fish.png")
# theta = 90
# img_rotated = img.rotate(angle=theta)
# img_rotated.save("rotated_fish.png")

# rgb/bgr conversion
# img = Image.open("fish.png")
# rgb = np.array(img)
# bgr = rgb[:, :, ::-1]
# bgr_image = Image.fromarray(bgr)

# grayscale conversion
# img = Image.open("fish.png")
# img_grayscale = img.convert('L')
# img_grayscale.save("grayscale_fish.png")

# perspective transformation
# import sys

# def find_coeffs(pa, pb):
#     matrix = []
#     for p1, p2 in zip(pa, pb):
#         matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
#         matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

#     A = np.matrix(matrix, dtype=np.float)
#     B = np.array(pb).reshape(8)

#     res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
#     return np.array(res).reshape(8)

# img = Image.open(sys.argv[1])
# width, height = img.size
# m = -0.5
# xshift = abs(m) * width
# new_width = width + int(round(xshift))
# img = img.transform((new_width, height), Image.AFFINE,
#         (1, m, -xshift if m > 0 else 0, 0, 1, 0), Image.BICUBIC)
# img.save(sys.argv[2])

# png/jpeg conversion
# img = sys.argv[1].split(".")
# print(img)
# if img[1] == "png":
#     im = Image.open(sys.argv[1])
#     rgb_img = im.convert('RGB')
#     rgb_img.save('test2.JPEG')
# elif img[1] == "jpg":
#     im = Image.open(sys.argv[1])
#     rgb_img = im.convert('RGB')
#     rgb_img.save('test2.PNG')


image_path_list = ["/media/1_fish.png", "/media/2_fish.png", "/media/3_fish.png"]
image_list = [Image.open(file) for file in image_path_list]
image_list[0].save(
    'animation.gif',
    save_all=True,
    append_images=image_list[1:],
    duration=500,
    loop=0
)