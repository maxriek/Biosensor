# Python script by Berke Santos and Max Riekeles (developed with the help of AI)

########################################################################################################################
########################################################################################################################

import os
from PIL import Image
import re

def resize_and_convert_tif_images(parent_folder_path):
    # Define the path for the new 'shortened' folder
    shortened_folder_path = os.path.join(parent_folder_path, "shortened")

    # Create the shortened folder if it doesn't exist
    if not os.path.exists(shortened_folder_path):
        os.makedirs(shortened_folder_path)

    # Iterate through each folder in the parent directory
    for folder in os.listdir(parent_folder_path):
        folder_path = os.path.join(parent_folder_path, folder)

        # Skip the 'shortened' folder itself to avoid processing it
        if folder == "shortened" or not os.path.isdir(folder_path):
            continue

        print(f"Processing folder: {folder_path}")

        # Create the output path inside the shortened folder, with the same folder name as the original
        output_folder_path = os.path.join(shortened_folder_path, folder, "raw")

        # Create the output 'raw' folder if it doesn't exist
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)

        # Find and process all .tif files in the folder
        tif_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.tif')]
        print(f"Found {len(tif_files)} TIFF files in {folder_path}")

        # Extract the last part of the filenames (after the last underscore) which is assumed to be a counter
        def extract_counter(file_name):
            match = re.search(r'_(\d+)\.tif$', file_name)
            return int(match.group(1)) if match else 0

        # Sort files based on the extracted counter
        tif_files.sort(key=extract_counter)
        print(tif_files)

        for counter, file_name in enumerate(tif_files, start=1):
            file_path = os.path.join(folder_path, file_name)
            print(file_path)
            try:
                # Open the image, resize it, and convert it to grayscale ('L' mode)
                with Image.open(file_path) as img:
                    img = img.resize((2048, 2048), Image.LANCZOS)
                    img = img.convert('L')

                    # Remove the last part of the original filename (after the last underscore)
                    base_name = file_name.rsplit('_', 1)[0]
                    new_file_name = f"{base_name}_{counter:05d}.tif"
                    new_file_path = os.path.join(output_folder_path, new_file_name)

                    # Save the processed image
                    img.save(new_file_path, compression='none')
                    print(f"Processed and saved: {new_file_name}")

            except Exception as e:
                print(f"Error processing {file_path}: {e}")

# Example usage
parent_folder_path = ""
resize_and_convert_tif_images(parent_folder_path)
