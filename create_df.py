import os
import pandas as pd

# Paths
image_dir = "/Users/marion/Desktop/Dedan_Dataset/augmented"  
output_csv = "aug_captions.csv"

# Collect all image filenames
files = [f for f in os.listdir(image_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

# Create DataFrame with empty captions
df = pd.DataFrame({"filename": files, "caption": [""] * len(files)})

# Save to CSV
df.to_csv(output_csv, index=False)

print(f"✅ Created {output_csv}. You can now open it and fill in captions manually.")
