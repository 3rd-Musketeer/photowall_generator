import os
import random
import shutil
from PIL import Image
import time
import cv2 as cv

### PARAMETERS

mask_img_path = # dir of the front photo

save_filename = "export" # name of file to save the output photo

random.seed(219) # choose your own seed

output_side = 100 # number of photos on each side of the output photo (default rectangular)

photo_side = 300 # number of pixels on each side of the component photos

###

path = os.getcwd()

save_path = os.path.join(path, save_filename)

if not os.path.exists(save_path):
    os.mkdir(save_path)

photo_path = []

for i in os.listdir():
    if ('.png' in i) or ('.jpg' in i):
        photo_path.append(os.path.join(path, i))

num_photos = output_side ** 2

lst_time = time.time()

total_time = 0

'''
target = Image.new('RGB', (photo_side * output_side, photo_side * output_side))

for i in range(output_side):
    for j in range(output_side):
        processed_photos = i * output_side + j + 1
        rate = processed_photos / num_photos
        num1 = int(50 * rate)
        num2 = 50 - num1
        img = Image.open(photo_path[random.randint(0, 63)])
        img = img.resize((photo_side, photo_side), Image.ANTIALIAS)
        target.paste(img, (0 + i * photo_side, 0 + j * photo_side))
        cur_time = time.time()
        total_time += cur_time - lst_time
        remtime = total_time / processed_photos * (num_photos - processed_photos)
        print('\rcreating photo [{}][{:-6.2f}%] {} remaining'.format('*' * num1 + '.' * num2, rate * 100, time.strftime(" %H h %M m %S s", time.gmtime(remtime))), end = '')
        lst_time = cur_time

target.save(os.path.join(save_path, time.strftime("%Y%m%d_%H%M%S_", time.localtime()) + 'output.jpg'), quality = 100)
'''

col_img = []

processed_photos = 0

read_ind = [[-1 for _ in range(output_side)] for _ in range(output_side)]

for i in range(output_side):
    for j in range(output_side):
        tmp = random.randint(0, 63)
        while (i > 0 and read_ind[i-1][j] == tmp) or (j > 0 and read_ind[i][j-1] == tmp):
            tmp = random.randint(0, 63)
        read_ind[i][j] = tmp

for i in range(output_side):
    row_img = []
    for j in range(output_side):
        img = cv.imread(photo_path[read_ind[i][j]])
        img = cv.resize(img, (photo_side, photo_side), interpolation = cv.INTER_AREA)
        row_img.append(img)

        processed_photos += 1
        rate = processed_photos / num_photos
        num1 = int(rate * 100)
        num2 = 100 - num1

        cur_time = time.time()
        total_time += cur_time - lst_time
        lst_time = cur_time
        remtime = total_time / processed_photos * (num_photos - processed_photos)

        print('\rcreating photo [{}][{:-6.2f}%] {} remaining'.format(
            '*' * num1 + '.' * num2,
            rate * 100,
            time.strftime(" %H h %M m %S s",time.gmtime(remtime))), end='')

    row_img = cv.hconcat(row_img)
    col_img.append(row_img)

output_img = cv.vconcat(col_img)

mask_img = cv.imread(mask_img_path)

cv.imwrite(os.path.join(save_path, time.strftime("%Y%m%d_%H%M%S_", time.localtime()) + 'mask.jpg'), output_img)

output_img = cv.resize(output_img, mask_img.shape[:-1])

output_img = cv.addWeighted(mask_img, 0.75, output_img, 0.25, 0)

cv.imwrite(os.path.join(save_path, time.strftime("%Y%m%d_%H%M%S_", time.localtime()) + 'output.jpg'), output_img)

cv.namedWindow('img', 0)

cv.resizeWindow('img', 1000, 1000)

cv.imshow('img', output_img)

k = cv.waitKey(0)

if k == 27: # detect ESC
    cv.destroyAllWindows()



