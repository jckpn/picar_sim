import cv2
import tensorflow as tf
import numpy as np
from utils import get_picar_view


class CNNController:
    def __init__(self, display, picar):
        self.display = display
        self.picar = picar

        # load model from file
        self.STEER_MODEL = tf.keras.models.load_model(
            "controllers/models/roadwarp-direction-32.h5"
        )

        self.last_outputs = 1, 0.5  # placeholder

        # pre-processing is built into the model -- no need to do it here

    def get_controls(self):
        throttle = 1

        # get picar view and erode to remove noise (+ make lines thicker)
        picar_view = get_picar_view(self.display, view_size=(50, 30))
        picar_view = cv2.erode(picar_view, kernel=np.ones((3, 3)), iterations=1)
        picar_view = cv2.resize(picar_view, (32, 32))

        # feed input into model
        batch = picar_view[None, :, :, :]
        steer = self.STEER_MODEL.predict(batch, verbose=0)[0, 0]
        throttle = 1

        # reduce steering sensitivity
        # sensitivity = 0.8
        # steer = (steer - 0.5) * sensitivity + 0.5

        self.last_outputs = throttle, steer

        return throttle, steer  # placeholder

    def display_view_cv2(self, picar_view):
        picar_view = cv2.resize(picar_view, (240, 240), interpolation=cv2.INTER_NEAREST)
        cv2.imshow("AIController View", picar_view)
