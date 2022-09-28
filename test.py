import os
import cv2
from tools.img_detect import img_detect
from tools.img_cut import img_cut,display_blocks
from tools.unites import show

img_path = '../imgs'

img_files = os.listdir(img_path)
for img_file in img_files:
    img_file_path = os.path.join(img_path, img_file)
    img = cv2.imread(img_file_path)
    detect_img = img_detect(img)
    out = show('detect',detect_img,5000)
    print(out)
    img_crops = img_cut(detect_img)
    display_blocks(img_crops)

