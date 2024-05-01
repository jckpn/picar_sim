import cv2
import numpy as np


# define overhead transform
w, h = 320, 240
top = int(0.33 * h)
top_width = int(0.75 * w)
bot_width = int(2.5 * w)
overhead_transform = cv2.getPerspectiveTransform(
    src=np.float32(
        [
            [w // 2 - top_width // 2, top],
            [w // 2 + top_width // 2, top],
            [w // 2 + bot_width // 2, h],
            [w // 2 - bot_width // 2, h],
        ]
    ),
    dst=np.float32([[0, 0], [w, 0], [w, h], [0, h]]),
)


def overhead_warp_point(x, y):
    pt = cv2.perspectiveTransform(
        np.array([[[x, y]]], dtype=np.float32), overhead_transform
    )[0][0]

    return pt.astype(int)


def overhead_warp_img(img):
    img = cv2.warpPerspective(
        img,
        overhead_transform,
        (w, h),
        borderMode=cv2.BORDER_REPLICATE,
    )

    return img


if __name__ == "__main__":
    pt = overhead_warp_point(120, 100)
    print(pt)

    img = cv2.imread("/Users/jckpn/dev/picar/data/training_data/training_data/9.png")
    img = overhead_warp_img(img)
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
