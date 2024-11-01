# Python script by Berke Santos and Max Riekeles (developed with the help of AI)

########################################################################################################################
########################################################################################################################

import cv2 as cv
import os
import glob
import numpy as np
import shutil
import csv
import re

# Helper function to sort alphanumerically
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def process_blob_detection(shortened_path, min_distance=30, clipLimit=0.6, tileGridSize=(16, 16), dark_minThreshold=30,
                           dark_maxThreshold=150, dark_minArea=80, dark_maxArea=250, bright_minThreshold=80,
                           bright_maxThreshold=255, bright_minArea=80, bright_maxArea=250):
    destination_directory = os.path.join(shortened_path, "blobdetection")

    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    clahe = cv.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGridSize)

    params_dark = cv.SimpleBlobDetector_Params()
    params_dark.minThreshold = dark_minThreshold
    params_dark.maxThreshold = dark_maxThreshold
    params_dark.filterByArea = True
    params_dark.minArea = dark_minArea
    params_dark.maxArea = dark_maxArea
    params_dark.filterByCircularity = False
    params_dark.filterByConvexity = False
    params_dark.filterByInertia = False

    params_bright = cv.SimpleBlobDetector_Params()
    params_bright.minThreshold = bright_minThreshold
    params_bright.maxThreshold = bright_maxThreshold
    params_bright.filterByArea = True
    params_bright.minArea = bright_minArea
    params_bright.maxArea = bright_maxArea
    params_bright.filterByCircularity = False
    params_bright.filterByConvexity = False
    params_bright.filterByInertia = False

    detector_dark = cv.SimpleBlobDetector_create(params_dark)
    detector_bright = cv.SimpleBlobDetector_create(params_bright)

    overall_results = []

    def process_images_in_directory(directory):
        output_path = os.path.join(directory, "processed_images_CLAHE")

        # Check if CLAHE folder already exists, if so, skip processing
        if os.path.exists(output_path):
            print(f"Skipping CLAHE processing for {directory} (already exists).")
            return

        os.makedirs(output_path)
        results = []
        previous_total_blobs = None

        # Sorting files in natural order
        for file_path in sorted(glob.glob(os.path.join(directory, "*_image.*")), key=natural_sort_key):
            img = cv.imread(file_path, 0)

            shutil.copy(file_path, output_path)
            img_resized = cv.resize(img, (2048, 2048), interpolation=cv.INTER_LINEAR)
            img_clahe = clahe.apply(img_resized)

            img_color = cv.cvtColor(img_clahe, cv.COLOR_GRAY2BGR)
            keypoints_dark = detector_dark.detect(img_clahe)
            img_inverted = cv.bitwise_not(img_clahe)
            keypoints_bright = detector_bright.detect(img_inverted)

            keypoints = keypoints_dark + keypoints_bright
            filtered_keypoints = []
            for kp in keypoints:
                if all(np.linalg.norm(np.array(kp.pt) - np.array(k.pt)) >= min_distance for k in filtered_keypoints):
                    filtered_keypoints.append(kp)

            for k in filtered_keypoints:
                color = (0, 255, 0) if k in keypoints_dark else (0, 0, 255)
                cv.circle(img_color, (int(k.pt[0]), int(k.pt[1])), int(k.size / 2), color, -1)

            base_filename = os.path.basename(file_path)
            output_file_path = os.path.join(output_path, os.path.splitext(base_filename)[0] + "_blobs.tiff")
            cv.imwrite(output_file_path, img_color)

            shutil.copy(output_file_path, destination_directory)

            dark_count = len(keypoints_dark)
            bright_count = len(keypoints_bright)
            total_blobs = len(filtered_keypoints)

            # Check if total_blobs is not zero before calculating fraction
            if total_blobs > 0:
                fraction = previous_total_blobs / total_blobs if previous_total_blobs else 0
            else:
                fraction = 0  # Handle case where total_blobs is zero

            results.append(f"{base_filename}: {dark_count} dark, {bright_count} bright, {total_blobs} total")
            previous_total_blobs = total_blobs

            print(f"Processed {base_filename}: {dark_count} dark, {bright_count} bright, {total_blobs} total blobs")

        # Save results to the CLAHE folder
        results_file_path = os.path.join(output_path, "results.txt")
        with open(results_file_path, "w") as f:
            for result in results:
                f.write(result + "\n")

        overall_results.append("\n".join(results) + "\n\n")

    for dataset_dir in sorted(os.listdir(shortened_path), key=natural_sort_key):
        validate_dir = os.path.join(shortened_path, dataset_dir, "validate")
        if os.path.isdir(validate_dir):
            print(f"Processing images in directory: {validate_dir}")
            process_images_in_directory(validate_dir)

    # Save overall results in the blobdetection folder
    overall_results_file_path = os.path.join(destination_directory, "blobdetection_allds.txt")
    with open(overall_results_file_path, "w") as f:
        for result in overall_results:
            f.write(result)


def copy_mhi_files(shortened_path):
    mhis_dir = os.path.join(shortened_path, "MHIs")
    if not os.path.exists(mhis_dir):
        os.makedirs(mhis_dir)

    for subdir, _, files in os.walk(shortened_path):
        if os.path.basename(subdir) == "validate":
            for file in sorted(files, key=natural_sort_key):
                if file.endswith("_mhi.png"):
                    file_path = os.path.join(subdir, file)
                    shutil.copy(file_path, mhis_dir)


def organize_analysis(root_directory, subfolder, folder_name):
    def is_image_file(filename):
        return filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tif', '.tiff'))

    analysis_folder_path = os.path.join(root_directory, f"{subfolder}_{folder_name}_analysis")
    if not os.path.exists(analysis_folder_path):
        os.makedirs(analysis_folder_path)

    shortened_path = os.path.join(root_directory, subfolder, folder_name)
    if os.path.isdir(shortened_path):
        blobdetection_file = os.path.join(shortened_path, "blobdetection", "blobdetection_allds.txt")

        if os.path.isfile(blobdetection_file):  # Ensure blobdetection file exists
            csv_file = os.path.join(analysis_folder_path,
                                    "blobdetection_results.csv")  # Save directly in analysis folder

            with open(blobdetection_file, "r") as txt_file, open(csv_file, "w", newline="") as csv_out:
                csv_writer = csv.writer(csv_out)
                csv_writer.writerow(["Filename", "Total Blobs OG"])  # Header

                current_filename = None
                for line in txt_file:
                    line = line.strip()
                    if "Results for dataset:" in line:  # Skip dataset header lines
                        continue

                    # Extract the first image's filename and total blobs count
                    if "first_image" in line:
                        parts = line.split(":")
                        if len(parts) >= 2:
                            filename = parts[0].strip()
                            total_blobs = parts[1].split(",")[-1].split()[0]  # Extract total blobs
                            csv_writer.writerow([filename, total_blobs])
            print(f"CSV saved at {csv_file}")

        for item in sorted(os.listdir(shortened_path), key=natural_sort_key):
            item_path = os.path.join(shortened_path, item)
            if os.path.isdir(item_path) and item.startswith("MHI"):
                shutil.copytree(item_path, os.path.join(analysis_folder_path, item))

        for subsubfolder in sorted(os.listdir(shortened_path), key=natural_sort_key):
            subsubfolder_path = os.path.join(shortened_path, subsubfolder)
            if os.path.isdir(subsubfolder_path):
                validate_path = os.path.join(subsubfolder_path, "validate")
                if os.path.isdir(validate_path):
                    processed_images_path = os.path.join(validate_path, "processed_images_CLAHE")
                    if os.path.isdir(processed_images_path):
                        for item in sorted(os.listdir(processed_images_path), key=natural_sort_key):
                            item_path = os.path.join(processed_images_path, item)
                            if os.path.isfile(item_path) and is_image_file(item):
                                shutil.copy(item_path, analysis_folder_path)
                        print(f"Copied processed images to {analysis_folder_path}")


def run_all_functions(root_directory, folders):
    for subfolder in sorted(os.listdir(root_directory), key=natural_sort_key):
        subfolder_path = os.path.join(root_directory, subfolder)
        if os.path.isdir(subfolder_path):
            for folder in sorted(folders, key=natural_sort_key):
                shortened_path = os.path.join(subfolder_path, folder)
                if os.path.isdir(shortened_path):
                    print(f"Starting process for: {shortened_path}")
                    process_blob_detection(shortened_path)
                    copy_mhi_files(shortened_path)
                    organize_analysis(root_directory, subfolder, folder)
                    print(f"Completed processing for: {shortened_path}")


root_directory = ""
folders = ["shortened_2seconds", "shortened_5seconds", "shortened_10seconds"]
run_all_functions(root_directory, folders)
