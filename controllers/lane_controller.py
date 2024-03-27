import pygame
from utils import scale_coords
import numpy as np
import cv2


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
