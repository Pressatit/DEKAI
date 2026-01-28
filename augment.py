import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img

# Paths
input_dir = "/Users/marion/Desktop/Dedan_Dataset/Dedan_Img_dataset"        # folder with your .jpg images
output_dir = "augmented"    # folder where augmented images will be saved

os.makedirs(output_dir, exist_ok=True)

# Image augmentation settings
datagen = ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    brightness_range=[0.8, 1.2],
    zoom_range=0.2,
    horizontal_flip=True
)

num_augmented=5

# Loop through all images in the folder
for filename in os.listdir(input_dir):
    if filename.lower().endswith(".jpg"):   # only process .jpg
        filepath = os.path.join(input_dir, filename)

        # Load and preprocess image
        img = load_img(filepath, target_size=(128, 128))  # resize for consistency
        x = img_to_array(img)
        x = x.reshape((1,) + x.shape)

        aug_iter = datagen.flow(
            x,
            batch_size=1,
            save_to_dir=output_dir,
            save_prefix=os.path.splitext(filename)[0],
            save_format="jpg",
            shuffle=False  # prevents extra duplicates
        )

        for i in range(num_augmented):
            next(aug_iter)

print("✅ Augmentation complete! Check the 'augmented' folder.")
