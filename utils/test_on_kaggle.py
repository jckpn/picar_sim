import numpy as np
import cv2
import pandas as pd
from shared.model import Model


samples = 13000
model = Model()

csv_path = "/Users/jckpn/dev/picar/data/training_norm.csv"
df = pd.read_csv(csv_path)

total_square_error = 0
angle_square_error = 0
speed_square_error = 0

for i in range(samples):
    id = int(df.iloc[i]["image_id"])
    path = f"/Users/jckpn/dev/picar/data/training_data/training_data/{id}.png"
    img = cv2.imread(path)
    
    y = df.iloc[i]["angle"], df.iloc[i]["speed"]

    pred = model.predict(img)
    y_hat = ((pred[0] - 50) / 80, pred[1] / 35)
    
    angle_square_error += (y[0] - y_hat[0]) ** 2
    speed_square_error += (y[1] - y_hat[1]) ** 2
    total_square_error += (y[0] - y_hat[0]) ** 2 + (y[1] - y_hat[1]) ** 2

mse = total_square_error / samples / 2
angle_mse = angle_square_error / samples
speed_mse = speed_square_error / samples

print(f"MSE: {mse}, Angle MSE: {angle_mse}, Speed MSE: {speed_mse}")