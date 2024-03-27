import pygame
from functions import scale_coords
import numpy as np
import cv2
import tensorflow as tf

# controllers only return 2 values: throttle (0->1) and steer (0->1)


class KeyboardController:
    def get_controls(self, delta_time):
        keys = pygame.key.get_pressed()

        # defaults
        throttle = 0  # lazy way to emulate friction
        steer = 0.5

        if keys[pygame.K_UP]:
            throttle = 1
        elif keys[pygame.K_DOWN]:
            throttle = 0  # breaks probably faster than accel

        if keys[pygame.K_LEFT]:
            steer = 0
        elif keys[pygame.K_RIGHT]:
            steer = 1

        return throttle, steer


class LaneController:
    def __init__(self, display, picar, display_view=True):
        self.display = display
        self.picar = picar
        self.display_view = display_view

        self.smoothing = 0.5  # 0-1, how much to factor in last outputs

        if display_view:
            cv2.namedWindow("AIController View")
            cv2.moveWindow("AIController View", 0, 100)
            cv2.resizeWindow("AIController View", 240, 240)

        self.last_outputs = 0, 1  # placeholder

    def get_controls(self, delta_time):
        steer = 1
        throttle = 1

        grid_size = 100
        picar_view = get_picar_view(self.display, self.picar)
        picar_view = cv2.resize(picar_view, (grid_size, grid_size))

        # filter out non-track stuff
        picar_view = cv2.cvtColor(picar_view, cv2.COLOR_RGB2GRAY)
        picar_view = cv2.erode(picar_view, kernel=np.ones((3, 3)), iterations=1)
        _, picar_view = cv2.threshold(picar_view, 30, 255, cv2.THRESH_BINARY)
        picar_view = cv2.bitwise_not(picar_view)

        bottom_half = picar_view[grid_size // 2 :, :]
        col_avgs = np.mean(bottom_half, axis=0)
        tracks = np.where(col_avgs > 0)[0]

        # if no tracks, use last outputs
        if len(tracks) == 0:
            return self.last_outputs

        if len(tracks) > 0:
            # reduce to left-most and right-most tracks
            tracks = (tracks[0], tracks[-1])

            track_center = np.mean(tracks)
            steer = track_center / grid_size - 0.5

            steer = np.clip(steer * 4, -1, 1)

            if self.display_view:
                self.display_view_cv2(picar_view, tracks, track_center, grid_size)

            a = self.smoothing ** (delta_time * 10)
            throttle, steer = (
                a * self.last_outputs[0] + (1 - a) * throttle,
                a * self.last_outputs[1] + (1 - a) * steer,
            )

            self.last_outputs = throttle, steer

        return throttle, steer  # placeholder

    def display_view_cv2(
        self, picar_view, tracks, track_center, grid_size, extras=True
    ):
        picar_view = cv2.cvtColor(picar_view, cv2.COLOR_GRAY2BGR)

        # draw tracks + center
        if extras and len(tracks) > 0:
            for track in tracks:
                cv2.line(picar_view, (track, 0), (track, grid_size), (0, 255, 0), 2)

            cv2.line(
                picar_view,
                (int(track_center), 0),
                (int(track_center), grid_size),
                (255, 0, 255),
                2,
            )

        picar_view = cv2.resize(picar_view, (240, 240))

        cv2.imshow("AIController View", picar_view)


class CNNController:
    def __init__(self, display, picar, steer_model_path, throttle_model_path, display_view=False):
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
        


def get_picar_view(display, picar):
    view_size = 32
    y_offset = -28  # to get picar out of view

    view_rect = (
        picar.display_x - view_size // 2,
        picar.display_y - view_size // 2 + y_offset,
        view_size,
        view_size,
    )
    view_rect = scale_coords(*view_rect)
    view_surface = display.subsurface(view_rect).copy()

    # convert to cv2 image
    view_img = pygame.surfarray.array3d(view_surface)
    view_img = np.rot90(view_img)
    view_img = cv2.flip(view_img, 0)
    view_img = cv2.cvtColor(view_img, cv2.COLOR_RGB2BGR)

    return view_img
