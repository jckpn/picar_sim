import numpy as np
import cv2
import tensorflow as tf
import os
import sys

# import tflite_runtime.interpreter as tflite
# from pprint import pprint

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from overhead_warp import overhead_warp_point

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    import tflite_runtime.interpreter as tflite

    interpreter = tflite.Interpreter(
        model_path=os.path.join(CURRENT_DIR, "od_model", "model_edgetpu.tflite"),
        experimental_delegates=[tf.lite.experimental.load_delegate("libedgetpu.so.1")],
    )
    print("Using EdgeTPU for object detection")
except Exception as e:
    print(f"Error loading EdgeTPU: {e}")
    interpreter = tf.lite.Interpreter(
        model_path=os.path.join(CURRENT_DIR, "od_model", "model.tflite")
    )
    print("Using CPU for object detection")

interpreter.allocate_tensors()

SCORE_THRESHOLD = 0.3
IOU_THRESHOLD = 0.5

class_map = {
    0: "obstacle",
    1: "obstacle",
    2: "left_sign",
    3: "obstacle",
    4: "obstacle",
    5: "red_light",
    6: "right_sign",
    7: "obstacle",
    8: "obstacle",
}

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

_, input_height, input_width, _ = input_details[0]["shape"]

output_map = {"output_0": 2, "output_1": 0, "output_2": 3, "output_3": 1}


def _preprocess_image(image, input_size):
    original_h, original_w, _ = image.shape
    image = tf.image.convert_image_dtype(image, tf.uint8)
    image = tf.image.resize(image, input_size)
    image = image[tf.newaxis, :]
    image = tf.cast(image, dtype=tf.uint8)
    return image, (original_h, original_w)


def extract_obstacles(img, state_size=30):
    processed_img, original_size = _preprocess_image(img, (input_height, input_width))

    # output = signature_fn(images=processed_img) # Removed by edgetpu_compiler...

    interpreter.set_tensor(input_details[0]["index"], processed_img)
    interpreter.invoke()

    output = {}
    for key, i in output_map.items():
        output[key] = interpreter.get_tensor(output_details[i]["index"])

    # pprint(output)

    if output_details[0]["dtype"] == np.uint8:
        for key, i in output_map.items():
            output_scale, output_zero_point = output_details[i]["quantization"]
            output[key] = output[key].astype(np.float32)
            output[key] = (output[key] - output_zero_point) * output_scale

        output["output_0"] = np.round(output["output_0"]).astype(np.uint8)
        output["output_2"] = np.round(output["output_2"]).astype(np.uint8)

    count = int(np.squeeze(output["output_0"]))
    scores = np.squeeze(output["output_1"])
    classes = np.squeeze(output["output_2"])
    boxes = np.squeeze(output["output_3"])

    results = []
    for i in range(count):
        if scores[i] >= SCORE_THRESHOLD:
            result = {
                "bounding_box": boxes[i],
                "class_id": classes[i],
                "score": scores[i],
            }
            results.append(result)

    # pprint(results)

    obstacles = []
    for i in range(count):
        if scores[i] < SCORE_THRESHOLD:
            # print("Score too low")
            continue

        y_min, x_min, y_max, x_max = boxes[i]

        # Scale to original image size
        x_min = int(x_min * original_size[1])
        x_max = int(x_max * original_size[1])
        # y_min = int(y_min * original_size[0]) # Unused
        y_max = int(y_max * original_size[0])

        # Bottom-center of object for position
        # TODO: Either go up a bit; or change to bounding box IOU outside of state
        x = x_min + (x_max - x_min) // 2
        y = y_max
        # print(f"Original x: {x}, y: {y}")
        x, y = overhead_warp_point(x, y)
        # print(f"Warped x: {x}, y: {y}")

        # Scale to state grid
        x = x / original_size[1] * state_size
        y = y / original_size[0] * state_size

        # pprint(f"Grid Position: {position}")

        # Ignore if out of range
        # if position.max() >= state_size or position.min() < 0:
        #     # print("Out of range")
        #     continue
        
        # if beyond distance, add to top of state anyway
        if y < 0:
            y = 0
        
        if y >= state_size or x < 0 or x >= state_size:
            # print("Out of range")
            continue
        
        position = np.array([x, y], dtype=int)

        obstacles.append((class_map[classes[i]], position))

    return obstacles


if __name__ == "__main__":
    import time

    times = []
    for i in range(50):
        t1 = time.time()
        obstacles = extract_obstacles(cv2.imread("test-imgs/5.png"))
        t2 = time.time()
        time_taken = t2 - t1
        print(f"Time taken: {time_taken*1000}ms")
        times.append(time_taken)

    print(f"Average time taken: {np.mean(times)*1000}ms")

    print(obstacles)
