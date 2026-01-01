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


# image_path_list = ["media/chick1.png", "media/chick2.png", "media/chick3.png"]
# raw_images = [Image.open(file) for file in image_path_list]
# target_size = raw_images[0].size
# resized_images = [
#     img.resize(target_size, Image.Resampling.LANCZOS) 
#     for img in raw_images
# ]

# resized_images[0].save(
#     'animation.gif',
#     save_all=True,
#     append_images=resized_images[1:],
#     duration=500,
#     loop=0
# )

# import base64

# base64_string = "data:media/chick1.png;base64, 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"
# png_str = base64_string.split(",")[1]
# png_bytes = base64.b64decode(png_str)
# with open('output_image.png', 'wb') as fid:
#     fid.write(png_bytes)