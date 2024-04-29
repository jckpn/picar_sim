# convert the picar's camera view to the grid state

import cv2
import numpy as np
import pandas as pd
import time

now = time.time()


def view_to_state(img, grid_size=25):
    preview(img)

    img = overhead_warp(img)
    preview(img)

    # img = enhance_track(img)
    # preview(img)

    # Increase contrast
    mask = cv2.convertScaleAbs(img, alpha=1.5, beta=0)
    # preview(mask)

    # Convert to HSV
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2HSV)
    # preview(mask)

    # Construct mask first
    # Threshold for white pixels
    S_MAX = 0.25
    V_MIN = 0.75
    mask = cv2.inRange(mask, (0, 0, int(V_MIN * 255)), (180, int(S_MAX * 255), 255))
    # preview(mask)

    # Close the mask
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

    # Apply mask to original image, make unmasked areas red
    img[mask == 0] = [0, 0, 255]

    preview(img)
    cv2.imwrite("utils/track.jpg", img)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Threshold by HSV: S <= 0.3, V <= 0.5
    S_THRESHOLD = 0.5
    V_THRESHOLD = 0.25
    img = cv2.inRange(img, (0, 0, 0), (255, S_THRESHOLD * 255, V_THRESHOLD * 255))
    img = cv2.dilate(img, np.ones((5, 5), np.uint8), iterations=1)
    img = cv2.resize(img, (grid_size, grid_size), interpolation=cv2.INTER_NEAREST)

    preview(img)

    state = img / 255
    print(state.shape)
    return state


def preview(img):
    global now
    print(f"time: {(time.time() - now)*1000:.2f}ms")
    now = time.time()
    preview_img = cv2.resize(img, (320, 240), interpolation=cv2.INTER_NEAREST)
    cv2.imshow(str(now), preview_img)
    # cv2.waitKey(0)


def overhead_warp(img):
    # TODO: find the warp that puts ~60cm at the top of the image
    w, h = img.shape[1], img.shape[0]

    # close, probably ~30cm
    # top = 0.5 * h
    # bot = 1.0 * h
    # top_width = 0.6 * w
    # bot_width = 1.6 * w

    # further, like ~60cm
    # top = 0.4 * h
    # bot = 1.0 * h
    # top_width = 0.4 * w
    # bot_width = 1.7 * w

    top = 0.35 * h
    bot = 1.0 * h
    top_width = 0.5 * w
    bot_width = 1.8 * w

    mat = cv2.getPerspectiveTransform(
        # far
        src=np.float32(
            [
                [160 - top_width // 2, top],
                [160 + top_width // 2, top],
                [160 - bot_width // 2, bot],
                [160 + bot_width // 2, bot],
            ]
        ),
        dst=np.float32([[0, 0], [320, 0], [0, 240], [320, 240]]),
    )
    img = cv2.warpPerspective(
        img,
        mat,
        img.shape[:2][::-1],
        borderMode=cv2.BORDER_REPLICATE,
    )

    return img


def enhance_track(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = 255 - img
    _, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
    return img


def print_state(state):
    """Print the state as a 25x25 grid of characters. ' ' for < 0.5, '█' for >= 0.5"""
    for row in state:
        print("".join(["░" if cell < 0.75 else "█" for cell in row]))


if __name__ == "__main__":
    img = cv2.imread(
        f"C:/Users/Dino/OneDrive - The University of Nottingham/Year 4 MSc/MLiS P2/notts-mlis-picar/data/training_data/training_data/{np.random.randint(1, 10000)}.png"
    )
    # img = cv2.imread(
    #    r"C:\Users\Dino\Downloads\New folder1\Car1\downloads_images\1709571067912_90_35.png"
    # )
    # img = cv2.imread("utils/pic.jpg")
    state = view_to_state(img)
    print_state(state)

    cv2.waitKey(0)

    exit()

    # df = pd.read_csv("/Users/jckpn/dev/picar/data/training_norm.csv")

    # with open("state_data.csv", "a") as f:
    #     for entry in df.iterrows():
    #         print(entry[0])
    #         f.write(f"{entry[1]['speed']},{entry[1]['angle']}")
    #         img_path = f"/Users/jckpn/dev/picar/data/training_data/training_data/{int(entry[1]['image_id'])}.png"
    #         img = cv2.imread(img_path)
    #         state = view_to_state(img)
    #         state = state.flatten()
    #         for cell in state:
    #             f.write(f",{cell:.2f}")
    #         f.write("\n")
