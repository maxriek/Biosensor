# Python script by Berke Santos and Max Riekeles (developed with the help of AI)

########################################################################################################################
########################################################################################################################

import cv2
import tifffile
import glob
import os

# Define the root directory
root_dir = ""
# Define the input folder directory (place all final files within the input folder)
input_dir = os.path.join(root_dir, "input")
# Define the input and output directories
output_dir = os.path.join(root_dir, "cropped")

# Ensure the final directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function for file output numbering
def numbers(value):
    if value < 10:
        return "000"+str(value)
    elif value < 100:
        return "00"+str(value)
    elif value < 1000:
        return "0"+str(value)
    else:
        return str(value)

# Size of the square crop
crop_size_width = 1250  # Adjust as needed
crop_size_height = 1250

# Iterate over subfolders in the input directory
for subfolder_name in os.listdir(input_dir):
    subfolder_path = os.path.join(input_dir, subfolder_name)
    output_folder_path = os.path.join(output_dir, f"{subfolder_name}_cropped")
    os.makedirs(output_folder_path, exist_ok=True)
    print(output_folder_path)

    # Calculate crop parameters for center cropping
    x = (2592 - crop_size_width) // 2
    y = (1944 - crop_size_height) // 2

    # Open each TIFF image, crop a square in the center, and save the cropped image
    for filename in glob.glob(os.path.join(subfolder_path, "*.tif")):
        # Open image
        img = tifffile.imread(filename)

        # Crop square in the center
        cropped_img = img[y:y+crop_size_height, x:x+crop_size_width]

        # Extract filename without extension
        img_name = os.path.splitext(os.path.basename(filename))[0]

        # Save cropped image
        output_file_path = os.path.join(output_folder_path, f"{img_name}_cropped.tif")
        tifffile.imwrite(output_file_path, cropped_img)

print("Images have been cropped and saved to output directory.")
