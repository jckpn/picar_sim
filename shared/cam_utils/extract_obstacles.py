import numpy as np
import cv2
import tensorflow as tf
import keras_cv
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from overhead_warp import overhead_warp_point

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


interpreter = tf.lite.Interpreter(model_path=CURRENT_DIR + "/od_model.tflite")

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
interpreter.resize_tensor_input(input_details[0]["index"], (1, 256, 384, 3))
interpreter.allocate_tensors()

yolomodel = keras_cv.models.YOLOV8Detector(
    num_classes=9,
    bounding_box_format="xywh",
    fpn_depth=2,
    backbone=keras_cv.models.YOLOV8Backbone.from_preset("yolo_v8_s_backbone"),
)
yolomodel.prediction_decoder = keras_cv.layers.NonMaxSuppression(
    bounding_box_format="xywh",
    from_logits=True,
    iou_threshold=0.5,  # Minimum IOU for two boxes to be considered the same
    confidence_threshold=0.501,  # Minimum confidence for a box to be considered a detection
    max_detections=8,  # Maximum number of detections to keep
)

image_size = 384, 256
validation_resizing = keras_cv.layers.Resizing(
    width=image_size[0],
    height=image_size[1],
    bounding_box_format="xywh",
    pad_to_aspect_ratio=True,
)

class_map = {
    0: "obstacle",
    1: "obstacle",
    2: "left_arrow",
    3: "obstacle",
    4: "obstacle",
    5: "red_light",
    6: "right_arrow",
    7: "obstacle",
    8: "obstacle",
}


def extract_obstacles(img, state_size=30):
    img = validation_resizing([img])

    interpreter.set_tensor(input_details[0]["index"], img)
    interpreter.invoke()

    y_pred = {
        "classes": interpreter.get_tensor(output_details[0]["index"]),
        "boxes": interpreter.get_tensor(output_details[1]["index"]),
    }
    y_pred = yolomodel.decode_predictions(y_pred, img)  # decode pred tensor
    
    # print(y_pred)

    boxes = y_pred["boxes"][0].numpy()
    classes = y_pred["classes"][0].numpy()

    obstacles = []
    for class_, box in zip(classes, boxes):
        if class_ < 0:
            break  # model returns -1 when no more detections

        x, y, w, h = np.array(box, dtype=int)
        class_name = class_map[class_]
        
        # print(class_name, x, y, w, h)

        # got the object from view, now add to state
        # use bottom-center of object for position
        x, y = overhead_warp_point(x + w // 2, y + h)  # invert y

        # quantise to state grid
        x = x / image_size[0] * state_size
        y = y / image_size[1] * state_size
        position = np.array([x, y], dtype=int)

        # ignore if out of range
        if position.max() >= state_size or position.min() < 0:
            continue

        obstacles.append((class_name, position))

    return obstacles


if __name__ == "__main__":
    extract_obstacles(
        cv2.imread("/Users/jckpn/dev/picar/data/training_data/training_data/9.png")
    )
