import numpy as np
import tensorflow as tf
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class ExpertController:
    def __init__(self, model_name, track_only=True, steer_only=True, crop_track=False):
        self.model_name = model_name
        self.track_only = track_only
        self.steer_only = steer_only
        self.crop_track = crop_track

        model_path = os.path.join(CURRENT_DIR, "models", f"{model_name}.tflite")

        try:
            # raise Exception("EdgeTPU not available")
            delegate = tf.lite.experimental.load_delegate("libedgetpu.so.1")
            self.interpreter = tf.lite.Interpreter(
                model_path=model_path,
                experimental_delegates=[delegate],
            )
            print(f"Using EdgeTPU for {model_name}")
        except Exception as e:
            print(f"Error loading EdgeTPU: {e}")
            self.interpreter = tf.lite.Interpreter(model_path=model_path)
            print(f"Using CPU for {model_name}")

        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def __str__(self):
        return self.model_name

    def predict_from_state(self, state):
        if self.track_only:
            x = state.get_layer("track")
            x = np.expand_dims(x, axis=-1)  # reshape track from (30, 30) -> (30, 30, 1)
            if self.crop_track:
                x = x[20:]  # crop to bottom 1/3 for faster inference
        else:
            x = state.get_state_img()

        x = np.expand_dims(x, axis=0)  # model expects batch dimension

        x = np.float32(x)

        self.interpreter.set_tensor(self.input_details[0]["index"], x)
        self.interpreter.invoke()
        y_hat = self.interpreter.get_tensor(self.output_details[0]["index"])[0]

        angle, speed = y_hat if not self.steer_only else [y_hat[0], 1.0]

        # predictions are normalised -- convert to car angle/speed
        angle = angle * 80 + 50
        speed = speed * 35  # TODO: see if max speed needs to be changed in controller

        # angle = 60 if angle < 70 else 90 if angle < 110 else 120

        return angle, speed
