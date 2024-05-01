import numpy as np
import cv2


def overhead_warp(img):
    w, h = img.shape[1], img.shape[0]

    top = int(0.33 * h)
    top_width = int(0.75 * w)
    bot_width = int(2.5 * w)
    offset_x = 0  # todo: measure this?

    src = np.float32(
        [
            [w // 2 - top_width // 2 + offset_x, top],
            [w // 2 + top_width // 2 + offset_x, top],
            [w // 2 + bot_width // 2 + offset_x, h],
            [w // 2 - bot_width // 2 + offset_x, h],
        ]
    )

    # draw on image
    # for i in range(4):
    #     cv2.line(
    #         img,
    #         tuple(src[i].astype(int)),
    #         tuple(src[(i + 1) % 4].astype(int)),
    #         (255, 0, 0),
    #         2,
    #     )

    mat = cv2.getPerspectiveTransform(
        src=src,
        dst=np.float32([[0, 0], [w, 0], [w, h], [0, h]]),
    )
    img = cv2.warpPerspective(
        img,
        mat,
        (w, h),
        borderMode=cv2.BORDER_REPLICATE,
    )

    return img


def extract_track(img, state_size=30):
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


