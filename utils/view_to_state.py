# convert the picar's camera view to the grid state

import cv2
import numpy as np
import pandas as pd
import time

now = time.time()


def view_to_state(img, grid_size=25):
    # preview(img)

    img = overhead_warp(img)
    # preview(img)

    # img = enhance_track(img)
    # preview(img)
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = 255 - img
    img = cv2.dilate(img, np.ones((5, 5)), iterations=1)
    img = cv2.resize(img, (grid_size, grid_size), interpolation=cv2.INTER_NEAREST)
    # preview(img)

    state = img / 255
    print(state.shape)
    return state


def preview(img):
    global now
    print(f"time: {(time.time() - now)*1000:.2f}ms")
    preview_img = cv2.resize(img, (320, 240), interpolation=cv2.INTER_NEAREST)
    cv2.imshow("", preview_img)
    cv2.waitKey(0)
    now = time.time()


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

    top = 0.4 * h
    bot = 1.0 * h
    top_width = 0.6 * w
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


if __name__ == "__main__":
    # img = cv2.imread(
    #     f"/Users/jckpn/dev/picar/data/training_data/training_data/{np.random.randint(1, 10000)}.png"
    # )
    # state = view_to_state(img)
    # exit()

    df = pd.read_csv("/Users/jckpn/dev/picar/data/training_norm.csv")

    with open("state_data.csv", "a") as f:
        for entry in df.iterrows():
            print(entry[0])
            f.write(f"{entry[1]['speed']},{entry[1]['angle']}")
            img_path = f"/Users/jckpn/dev/picar/data/training_data/training_data/{int(entry[1]['image_id'])}.png"
            img = cv2.imread(img_path)
            state = view_to_state(img)
            state = state.flatten()
            for cell in state:
                f.write(f",{cell:.2f}")
            f.write("\n")
