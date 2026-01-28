import pandas as pd
import re

# Load original CSV
df = pd.read_csv("captions.csv", encoding="latin1")


# --- Clean image paths ---
df["image_path"] = (
    df["image_path"]
    .astype(str)
    .str.strip()
)

# Add prefix ONLY if not already present
df["image_path"] = df["image_path"].apply(
    lambda x: x if x.startswith("Dedan_Img_dataset/") else f"Dedan_Img_dataset/{x}"
)

# --- Clean captions ---
def clean_caption(text):
    text = str(text)

    # Remove ellipsis characters
    text = text.replace("…", "")

    # Remove surrounding quotes
    text = text.strip('"\'')

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Final trim
    return text.strip()

df["captions"] = df["captions"].apply(clean_caption)

# Save cleaned dataset
df.to_csv("captions_cleaned.csv", index=False)

print("✅ captions_cleaned.csv created successfully")
