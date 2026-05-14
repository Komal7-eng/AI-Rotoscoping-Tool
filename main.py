from rembg import remove
from PIL import Image
import os

input_folder = "input"
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        print(f"Processing: {filename}")
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename.rsplit('.', 1)[0] + "_nobg.png")
        with open(input_path, 'rb') as f:
            input_data = f.read()
        output_data = remove(input_data)
        with open(output_path, 'wb') as f:
            f.write(output_data)
        print(f"Done! Saved to: {output_path}")

print("All images processed!")