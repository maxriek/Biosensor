# Python script by Berke Santos and Max Riekeles (developed with the help of AI)

########################################################################################################################
########################################################################################################################

from PIL import Image
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from dateutil import parser
import re
import math
import shutil
import glob

def resize_and_convert_tif_images(parent_folder_path):
    try:
        print(f"Starting resize_and_convert_tif_images for {parent_folder_path}")
        for folder in os.listdir(parent_folder_path):
            folder_path = os.path.join(parent_folder_path, folder)
            if os.path.isdir(folder_path):
                print(f"Processing folder: {folder_path}")
                change_folder_path = os.path.join(folder_path, "change")
                if not os.path.exists(change_folder_path):
                    os.makedirs(change_folder_path)

                for subdir in os.listdir(folder_path):
                    subdir_path = os.path.join(folder_path, subdir)
                    if os.path.isdir(subdir_path) and subdir not in ["change", "shortened"]:
                        print(f"Processing subdir: {subdir_path}")
                        changed_subdir_path = os.path.join(change_folder_path, f"{subdir}_changed", "raw")
                        if not os.path.exists(changed_subdir_path):
                            os.makedirs(changed_subdir_path)
                        tif_files = [f for f in os.listdir(subdir_path) if f.lower().endswith('.tif')]
                        timepoint_file_pairs = []
                        for file_name in tif_files:
                            match = re.search(r"b0t(\d+)", file_name)
                            if match:
                                timepoint = int(match.group(1))
                                timepoint_file_pairs.append((timepoint, file_name))
                        timepoint_file_pairs.sort(key=lambda x: x[0])
                        for counter, (timepoint, file_name) in enumerate(timepoint_file_pairs, start=0):
                            file_path = os.path.join(subdir_path, file_name)
                            with Image.open(file_path) as img:
                                img = img.resize((2048, 2048), Image.LANCZOS)
                                img = img.convert('L')
                                new_file_name = f"{os.path.splitext(file_name)[0]}_{counter:05d}.tif"
                                new_file_path = os.path.join(changed_subdir_path, new_file_name)
                                img.save(new_file_path, compression='none')
                                print(
                                    f"Processed {counter + 1}/{len(timepoint_file_pairs)} in {changed_subdir_path}: {new_file_name}")
    except Exception as e:
        print(f"Error in resize_and_convert_tif_images: {e}")

def sort_key(filename):
    match = re.search(r'_b0t(\d+)c0x', filename)
    if match:
        return int(match.group(1))
    return 0

def get_acquisition_time(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        acquisition_time_element = root.find('.//AcquisitionTime')
        if acquisition_time_element is not None:
            acquisition_time = acquisition_time_element.text
            return parser.parse(acquisition_time)
        else:
            print(f"AcquisitionTime not found in {file_path}")
            return None
    except Exception as e:
        print(f"Error parsing file {file_path}: {e}")
        return None

def write_results(results, results_file_path):
    with open(results_file_path, 'a') as results_file:
        for result in results:
            results_file.write(result)

def analyze_subfolders(parent_folder_path, timestamps):
    print(f"Starting analyze_subfolders for {parent_folder_path} with timestamps {timestamps}")
    for folder in os.listdir(parent_folder_path):
        folder_path = os.path.join(parent_folder_path, folder)
        if os.path.isdir(folder_path):
            print(f"Analyzing folder: {folder_path}")
            results_file_path = os.path.join(folder_path, "analysis_results.txt")
            results = []

            for subfolder in os.listdir(folder_path):
                subfolder_path = os.path.join(folder_path, subfolder)

                if subfolder in ["change"] or "shortened" in subfolder:
                    continue

                if os.path.isdir(subfolder_path):
                    print(f"Processing subfolder: {subfolder_path}")
                    xml_files = [f for f in os.listdir(subfolder_path) if f.endswith('.tif_metadata.xml')]
                    xml_files.sort(key=sort_key)

                    if xml_files:
                        first_xml_file = xml_files[0]
                        last_xml_file = xml_files[-1]

                        first_time = get_acquisition_time(os.path.join(subfolder_path, first_xml_file))
                        last_time = get_acquisition_time(os.path.join(subfolder_path, last_xml_file))

                        if first_time and last_time:
                            time_diff = (last_time - first_time).total_seconds()
                            frame_count = len(xml_files)
                            frame_rate = (frame_count - 1) / time_diff

                            max_available_time = frame_count / frame_rate

                            for timestamp in timestamps:
                                if timestamp > max_available_time:
                                    print(
                                        f"Timestamp {timestamp} seconds exceeds the maximum available time {max_available_time:.2f} seconds. Skipping this timestamp.")
                                    continue

                                frame_rate_hz = frame_rate
                                images_for_timestamp = timestamp * frame_rate

                                result = (
                                    f"Subfolder: {subfolder}\n"
                                    f"Timestamp: {timestamp}\n"
                                    f"Frame rate: {frame_rate_hz:.2f} Hz\n"
                                    f"Number of images for at least {timestamp} seconds: {images_for_timestamp:.2f}\n"
                                    f"Total time: {time_diff:.2f} seconds\n"
                                    f"First acquisition time: {first_time}\n"
                                    f"Last acquisition time: {last_time}\n\n"
                                )
                                results.append(result)
                        else:
                            print(f"Skipping subfolder {subfolder} due to parsing issues.")
                    else:
                        print(f"No XML files found in subfolder {subfolder}")

            write_results(results, results_file_path)

def sort_key_custom(filename):
    base_name = os.path.basename(filename)
    num_part = base_name.split('_')[-1].split('.')[0]
    return int(num_part)

def copy_and_rename_images(src_dir, dst_dir, n_images, base_name):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    images = glob.glob(os.path.join(src_dir, "*.tif"))
    images_sorted = sorted(images, key=sort_key_custom)

    for index, img in enumerate(images_sorted[:n_images]):
        src_file_path = img
        extension = os.path.splitext(img)[1]
        new_filename = f"{base_name}_{index:05d}{extension}"
        dest_file_path = os.path.join(dst_dir, new_filename)
        shutil.copy2(src_file_path, dest_file_path)
        print(f"Copied and renamed {os.path.basename(img)} to {dest_file_path}")

def process_image_copying_and_renaming(parent_folder_path, timestamps):
    print(f"Starting process_image_copying_and_renaming for {parent_folder_path} with timestamps {timestamps}")
    for folder in os.listdir(parent_folder_path):
        folder_path = os.path.join(parent_folder_path, folder)
        if os.path.isdir(folder_path):
            print(f"Processing folder: {folder_path}")
            change_dir = os.path.join(folder_path, "change")

            results_file_path = os.path.join(folder_path, "analysis_results.txt")
            if not os.path.exists(results_file_path):
                print(f"No analysis results file found for {folder_path}. Skipping.")
                continue

            with open(results_file_path, "r") as file:
                content = file.read()
                sections = content.split("Subfolder:")[1:]

                for section in sections:
                    lines = section.strip().split("\n")
                    subfolder_name = lines[0].strip()
                    timestamp = float(lines[1].split(":")[1].strip())
                    n_images = math.ceil(float(lines[3].split(":")[1].strip()))

                    subfolder_changed_name = subfolder_name + "_changed"
                    src_dir = os.path.join(change_dir, subfolder_changed_name, "raw")
                    dst_dir = os.path.join(folder_path, f"shortened_{int(timestamp)}seconds", subfolder_changed_name,
                                           "raw")

                    if os.path.exists(src_dir):
                        base_name = subfolder_changed_name.replace('.tif_files_changed', '')
                        copy_and_rename_images(src_dir, dst_dir, n_images, base_name)
                    else:
                        print(f"Source directory does not exist: {src_dir}")

def pre_processing(parent_folder_path, timestamps):
    print(f"Starting pre_processing for {parent_folder_path} with timestamps {timestamps}")
    resize_and_convert_tif_images(parent_folder_path)
    analyze_subfolders(parent_folder_path, timestamps)
    process_image_copying_and_renaming(parent_folder_path, timestamps)

parent_folder_path = ""
timestamps = [2, 5, 10]
pre_processing(parent_folder_path, timestamps)
