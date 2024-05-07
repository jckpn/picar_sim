import cv2
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from overhead_warp import overhead_warp_img


def preview(img):
    return  # comment out this line for previews

    img = cv2.resize(img, (320, 320), interpolation=cv2.INTER_NEAREST_EXACT)
    if len(img.shape) < 3 or img.shape[2] != 3:  # some bw images don't have 3rd axis
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.imshow("", img)
    cv2.waitKey(0)


def extract_track(img, state_size=30):
    img = overhead_warp_img(img)
    # preview(img)

    grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Blur
    grey_img = cv2.GaussianBlur(grey_img, (5, 5), 0)
    # preview(grey_img)
    # Apply threshold of 180 to make a mask
    _, mask = cv2.threshold(grey_img, 175, 255, cv2.THRESH_BINARY)
    # preview(mask)
    mask_preclosing = mask.copy()
    # Apply closing to the mask
    kernel = np.ones((7, 7), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # preview(mask)
    # Select largest connected component
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(mask)
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(mask, [max_contour], -1, (255), -1)
    # preview(mask)

    mask_diff = cv2.bitwise_and(cv2.bitwise_not(mask_preclosing), mask)

    # preview(mask_diff)

    # Apply mask_diff to the original image, replace unmasked pixels with red
    mask_diff = cv2.bitwise_not(mask_diff)
    img[mask_diff == 255] = [0, 0, 255]

    # Convert to HSV
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Apply HSV Threshold
    S_THRESH = 0.8
    V_THRESH = 0.7

    mask = cv2.inRange(hsv_img, (0, 0, 0), (255, S_THRESH * 255, V_THRESH * 255))

    # preview(mask)

    # Apply closing to the mask
    kernel = np.ones((7, 7), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # preview(mask)

    # Apply dilation to the mask
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.resize(mask, (state_size, state_size), interpolation=cv2.INTER_NEAREST)

    mask = mask // 255

    return mask


if __name__ == "__main__":
    # folder = "New folder2/downloads_images"
    # paths_in_folder = os.listdir(folder)
    # # Shuffle the paths
    # import random

    # random.shuffle(paths_in_folder)
    # for path in paths_in_folder:
    #     print(path)
    #     img = cv2.imread(os.path.join(folder, path))
    #     track = extract_track(img)
    # preview(track)
    # Img size: 320x240
    # Create an empty canvas to hold the combined image
    canvas = np.zeros((300, 300), dtype=np.uint8)

    # Loop through the images and place them on the canvas
    for i in range(1, 101):
        print(i)
        row = (i - 1) // 10
        col = (i - 1) % 10

        img = cv2.imread(f"test-imgs/{i}.png")
        track = extract_track_(img)

        # Set border to white
        track[0, :] = 1
        track[-1, :] = 1
        track[:, 0] = 1
        track[:, -1] = 1

        # Calculate the coordinates to place the image on the canvas
        x = col * 30
        y = row * 30

        # Place the image on the canvas
        canvas[y : y + 30, x : x + 30] = track * 255

    # Save the combined image
    cv2.imwrite("combined_image_thresh.jpg", canvas)
