import cv2
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from overhead_warp import overhead_warp_img


def preview(img):
    # return  # comment out this line for previews

    img = cv2.resize(img, (320, 320), interpolation=cv2.INTER_NEAREST_EXACT)
    if len(img.shape) < 3 or img.shape[2] != 3:  # some bw images don't have 3rd axis
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.imshow("", img)
    cv2.waitKey(0)


def extract_track(img, state_size=30):
    img = cv2.erode(img, np.ones((3, 3), np.uint8), iterations=1)
    preview(img)

    img = overhead_warp_img(img)
    preview(img)

    grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Blur
    # grey_img = cv2.GaussianBlur(grey_img, (5, 5), 0)
    # preview(grey_img)
    # Apply threshold of 180 to make a mask
    _, mask = cv2.threshold(grey_img, 160, 255, cv2.THRESH_BINARY)
    preview(mask)
    mask_preclosing = mask.copy()
    # Apply closing to the mask
    kernel = np.ones((9, 9), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    preview(mask)
    # Select largest connected component
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(mask)
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(mask, [max_contour], -1, (255), -1)
    preview(mask)

    mask_diff = cv2.bitwise_and(cv2.bitwise_not(mask_preclosing), mask)

    # Erode
    kernel = np.ones((3, 3), np.uint8)
    mask_diff = cv2.erode(mask_diff, kernel, iterations=1)
    kernel = np.ones((5, 5), np.uint8)
    mask_diff = cv2.dilate(mask_diff, kernel, iterations=1)

    preview(mask_diff)

    # Apply mask_diff to the original image, replace unmasked pixels with red
    mask_diff = cv2.bitwise_not(mask_diff)
    img[mask_diff == 255] = [0, 0, 255]

    preview(img)

    cv2.imwrite("output.png", img)

    # Convert to HSV
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Apply HSV Threshold
    S_THRESH = 0.3
    V_THRESH = 0.75

    mask = cv2.inRange(hsv_img, (0, 0, 0), (255, S_THRESH * 255, V_THRESH * 255))

    preview(mask)

    # Apply closing to the mask
    kernel = np.ones((7, 7), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    preview(mask)

    # Apply dilation to the mask
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.resize(mask, (state_size, state_size), interpolation=cv2.INTER_NEAREST)

    preview(mask)
    mask = mask // 255

    return mask


if __name__ == "__main__":
    demo = np.zeros((240 * 2, 240 * 8, 3), dtype=np.uint8)
    for i in range(8):
        example = np.zeros((240 * 2, 240, 3), dtype=np.uint8)

        id = np.random.randint(1, 13000)
        path = f"data/training_data/training_data/{id}.png"
        print(path)
        img = cv2.imread(path)
        track = extract_track(img.copy()) * 255
        img = cv2.resize(img, (240, 240), interpolation=cv2.INTER_NEAREST_EXACT)
        track = cv2.resize(track, (240, 240), interpolation=cv2.INTER_NEAREST_EXACT)
        track = np.stack((track, track, track), axis=-1)

        demo[:240, i * 240 : (i + 1) * 240] = img
        demo[240:, i * 240 : (i + 1) * 240] = track

    cv2.imshow("demo", demo)
    cv2.waitKey(0)
