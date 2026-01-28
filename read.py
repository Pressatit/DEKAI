from PIL import Image
import pandas as pd

df = pd.read_csv("captions_cleaned.csv")

Image.open(df.iloc[0]["image_path"]).show()
print(df.iloc[0]["captions"])