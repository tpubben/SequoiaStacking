''' This script is prepared by Tyler Pubben and is licensed under the MIT license framework.
It is free to use and distribute however please reference http://www.tjscientific.com or my 
GIT repository at https://github.com/tpubben/SequoiaStacking/'''

import numpy as np
import cv2
import os

def align_images(in_fldr, out_fldr, moving, fixed):
    MIN_MATCH_COUNT = 10

    moving_im = cv2.imread(moving, 0)  # image to be distorted
    fixed_im = cv2.imread(fixed, 0)  # image to be matched

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(moving_im, None)
    kp2, des2 = sift.detectAndCompute(fixed_im, None)

    # use FLANN method to match keypoints. Brute force matches not appreciably better
    # and added processing time is significant.
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1, des2, k=2)

    # store all the good matches following Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        h, w = moving_im.shape  # shape of input images, needs to remain the same for output

        outimg = cv2.warpPerspective(moving_im, M, (w, h))

        return outimg


    else:
        print("Not enough matches are found for moving image")
        matchesMask = None

ch1 = int(input('Which band do you want for channel 1 on output image? Green(1), Red(2), Red Edge(3) or NIR(4)'))
ch2 = int(input('Which band do you want for channel 2 on output image? Green(1), Red(2), Red Edge(3) or NIR(4)'))
ch3 = int(input('Which band do you want for channel 3 on output image? Green(1), Red(2), Red Edge(3) or NIR(4)'))
channel_order = [ch1,ch2,ch3]


output_folder = str(input('Enter path to output folder: '))
input_folder = str(input('Enter path to input folder: '))

image_list = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder,f))]
image_tups = zip(*[image_list[i::4] for i in range(4)])

# set the fixed image to minimize amount of translation that needs to occur
if 1 in channel_order and 2 in channel_order and 3 in channel_order:
    fixed_image = 1
    moving_im1 = 0
    moving_im2 = 2
elif 2 in channel_order and 3 in channel_order and 4 in channel_order:
    fixed_image = 2
    moving_im1 = 1
    moving_im2 = 3
elif 1 in channel_order and 3 in channel_order and 4 in channel_order:
    fixed_image = 2
    moving_im1 = 0
    moving_im2 = 3
elif 1 in channel_order and 2 in channel_order and 4 in channel_order:
    fixed_image = 1
    moving_im1 = 0
    moving_im2 = 3

# iterate through each set of 4 images
for tup in image_tups:
    band1 = align_images(input_folder, output_folder, os.path.join(input_folder, tup[moving_im1]),
                         os.path.join(input_folder, tup[fixed_image]))
    band2 = align_images(input_folder, output_folder, os.path.join(input_folder, tup[moving_im2]),
                         os.path.join(input_folder, tup[fixed_image]))
    band3 = cv2.imread(os.path.join(input_folder, tup[fixed_image]), 0)

    merged = cv2.merge((band1, band2, band3))

    cv2.imwrite(os.path.join(output_folder, tup[fixed_image][-30:-4]) + '_merged.jpg', merged)
