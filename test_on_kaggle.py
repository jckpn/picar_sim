import numpy as np
import cv2
import pandas as pd
from shared.model import Model


samples = 13000
model = Model()

csv_path = "data/training_norm.csv"
df = pd.read_csv(csv_path)

angles = [
    0.0,
    0.0625,
    0.125,
    0.1875,
    0.25,
    0.3125,
    0.375,
    0.4375,
    0.5,
    0.5625,
    0.625,
    0.6875,
    0.75,
    0.8125,
    0.875,
    0.9375,
    1.0,
]

# Filter df to only include angle = 0.01
# df = df[df["angle"] == angles[0]]


total_square_error = 0
angle_square_error = 0
speed_square_error = 0

for i in range(samples):
    id = int(df.iloc[i]["image_id"])
    path = f"data/training_data/training_data/{id}.png"
    img = cv2.imread(path)

    y = df.iloc[i]["angle"], df.iloc[i]["speed"]

    pred = model.predict(img)
    y_hat = ((pred[0] - 50) / 80, pred[1] / 35)

    angle_square_error += (y[0] - y_hat[0]) ** 2
    speed_square_error += (y[1] - y_hat[1]) ** 2
    total_square_error += (y[0] - y_hat[0]) ** 2 + (y[1] - y_hat[1]) ** 2

    print(f"{i}/{samples}")
    # cv2.imshow("Image", img)
    # cv2.waitKey(0)
cv2.destroyAllWindows()

mse = total_square_error / samples / 2
angle_mse = angle_square_error / samples
speed_mse = speed_square_error / samples

print(f"MSE: {mse}, Angle MSE: {angle_mse}, Speed MSE: {speed_mse}")
