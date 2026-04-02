import pandas as pd
import numpy as np

df = pd.read_csv("Crop_recommendation.csv")

df["yield"] = np.random.uniform(1, 10, size=len(df))

df.to_csv("Crop_recommendation_with_yield.csv", index=False)

print("Новий файл створено: Crop_recommendation_with_yield.csv")