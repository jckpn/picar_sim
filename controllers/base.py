import pygame
from utils import scale_coords
import numpy as np
import cv2


class CNNController:
    def __init__(
        self, display, picar, steer_model_path, throttle_model_path, display_view=False
    ):
        self.display = display
        self.picar = picar
        self.display_view = display_view

        if display_view:
            cv2.namedWindow("AIController View")
            cv2.moveWindow("AIController View", 0, 100)
            cv2.resizeWindow("AIController View", 240, 240)

        # load model from file
        self.STEER_MODEL = tf.keras.models.load_model(steer_model_path)
        self.THROTTLE_MODEL = tf.keras.models.load_model(throttle_model_path)

        self.MODEL_TIME_INTERVAL = 0  # min s wait between model predictions
        self.SMOOTHING = 0.5  # 0->1, how much to factor in last outputs

        self.time_counter = 0
        self.last_outputs = 1, 0.5  # placeholder

        # pre-processing is built into the model -- no need to do it here

    def get_controls(self, delta_time):
        # check enough time has elapsed
        self.time_counter += delta_time
        if self.time_counter < self.MODEL_TIME_INTERVAL:
            return self.last_outputs
        else:
            self.time_counter = 0

        throttle = 1

        # get picar view and erode to remove noise (+ make lines thicker)
        picar_view = get_picar_view(self.display, self.picar)
        picar_view = cv2.erode(picar_view, kernel=np.ones((5, 5)), iterations=1)
        picar_view = cv2.resize(picar_view, (32, 32))

        # minmax normalisation
        # picar_view = picar_view - np.min(picar_view)
        # picar_view = picar_view / np.max(picar_view)
        # picar_view = (picar_view * 255).astype(np.uint8)

        if self.display_view:
            self.display_view_cv2(picar_view)

        # feed input into model
        batch = picar_view[None, :, :, :]
        steer = self.STEER_MODEL.predict(batch, verbose=0)[0, 0]
        throttle = self.THROTTLE_MODEL.predict(batch, verbose=0)[0, 0]
        print(steer, throttle)

        a = self.SMOOTHING ** (delta_time * 10)
        throttle, steer = (
            a * self.last_outputs[0] + (1 - a) * throttle,
            a * self.last_outputs[1] + (1 - a) * steer,
        )

        # reduce steering sensitivity
        # sensitivity = 0.8
        # steer = (steer - 0.5) * sensitivity + 0.5

        self.last_outputs = throttle, steer

        return throttle, steer  # placeholder

    def display_view_cv2(self, picar_view):
        picar_view = cv2.resize(picar_view, (240, 240), interpolation=cv2.INTER_NEAREST)
        cv2.imshow("AIController View", picar_view)