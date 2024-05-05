import cv2
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from overhead_warp import overhead_warp_img


def preview(img):
    return  # comment this line for previews at each step
    img = cv2.resize(img, (320, 320), interpolation=cv2.INTER_NEAREST_EXACT)
    if len(img.shape) < 3 or img.shape[2] != 3:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.imshow("", img)
    cv2.waitKey(0)
    

def extract_track(img, state_size=30):
    preview(img)
    
    img = overhead_warp_img(img)
    preview(img)
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    


def extract_track_(img, state_size=30):
    img = overhead_warp_img(img)

    preview(img)

    # Increase contrast
    mask = cv2.convertScaleAbs(img, alpha=1.5, beta=0)

    # Convert to HSV
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2HSV)

    # Construct mask first
    # Threshold for white pixels
    S_MAX = 0.25
    V_MIN = 0.75
    mask = cv2.inRange(mask, (0, 0, int(V_MIN * 255)), (180, int(S_MAX * 255), 255))

    # Close the mask
    kernel = np.ones((9, 9), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Select largest connected component
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(mask)
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(mask, [max_contour], -1, (255), -1)

    # Apply mask to original image, make unmasked areas red
    img[mask == 0] = [0, 0, 255]

    # cv2.imwrite("utils/track.jpg", img)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Threshold track by HSV: S <= 0.3, V <= 0.5
    S_THRESHOLD = 0.3
    V_THRESHOLD = 0.4
    img = cv2.inRange(img, (0, 0, 0), (255, S_THRESHOLD * 255, V_THRESHOLD * 255))
    img = cv2.dilate(img, np.ones((6, 6), np.uint8), iterations=1)
    img = cv2.resize(img, (state_size, state_size), interpolation=cv2.INTER_NEAREST)

    preview(img)

    track_layer = img / 255

    return track_layer


if __name__ == "__main__":
    demo = np.zeros((240*2, 240*8, 3), dtype=np.uint8)
    for i in range(8):
        example = np.zeros((240*2, 240, 3), dtype=np.uint8)
        
        id = np.random.randint(1, 13000)
        # path = f"/Users/jckpn/dev/picar/data/training_data/training_data/{id}.png"
        path = "/Users/jckpn/Desktop/Screenshot 2024-05-05 at 13.36.32.png"
        img = cv2.imread(path)
        track = extract_track(img.copy()) * 255
        img = cv2.resize(img, (240, 240), interpolation=cv2.INTER_NEAREST_EXACT)
        track = cv2.resize(track, (240, 240), interpolation=cv2.INTER_NEAREST_EXACT)
        track = np.stack((track, track, track), axis=-1)
        
        demo[:240, i*240:(i+1)*240] = img
        demo[240:, i*240:(i+1)*240] = track
    
    cv2.imshow("demo", demo)
    cv2.waitKey(0)