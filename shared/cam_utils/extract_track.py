import cv2
import numpy as np
import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from overhead_warp import overhead_warp_img


def extract_track(img, state_size=30):
    img = overhead_warp_img(img)

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

    cv2.imwrite("utils/track.jpg", img)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Threshold track by HSV: S <= 0.3, V <= 0.5
    S_THRESHOLD = 0.3
    V_THRESHOLD = 0.4
    img = cv2.inRange(img, (0, 0, 0), (255, S_THRESHOLD * 255, V_THRESHOLD * 255))
    img = cv2.dilate(img, np.ones((6, 6), np.uint8), iterations=1)
    img = cv2.resize(img, (state_size, state_size), interpolation=cv2.INTER_NEAREST)

    track_layer = img / 255

    return track_layer


if __name__ == "__main__":
    # img = cv2.imread("/Users/jckpn/dev/picar/data/training_data/training_data/9.png")

    # track_layer = extract_track(
    #     cv2.imread("/Users/jckpn/dev/picar/data/training_data/training_data/9.png")
    # )

    # track_layer = cv2.resize(track_layer, (240, 240), interpolation=cv2.INTER_NEAREST)
    # cv2.imshow("Track", track_layer)
    # cv2.waitKey(0)

    df = pd.read_csv("/Users/jckpn/dev/picar/data/training_norm.csv")

    with open("state_data.csv", "a") as f:
        for entry in df.iterrows():
            print(entry[0])
            f.write(f"{entry[1]['speed']},{entry[1]['angle']}")
            img_path = f"/Users/jckpn/dev/picar/data/training_data/training_data/{int(entry[1]['image_id'])}.png"
            img = cv2.imread(img_path)
            state = extract_track(img)
            state = state.flatten()
            for cell in state:
                f.write(f",{cell:.2f}")
            f.write("\n")