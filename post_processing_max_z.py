# Python script by Berke Santos and Max Riekeles (developed with the help of AI)

########################################################################################################################
########################################################################################################################

import os
import shutil

def copy_mhi_files(main_folder):
    # Walk through the main directory to find each subfolder
    for subdir, dirs, files in os.walk(main_folder):
        # Check if the current directory is the 'shortened' folder
        if os.path.basename(subdir) == "shortened":
            # Extract the parent folder name that contains the 'shortened' folder
            parent_folder = os.path.basename(os.path.dirname(subdir))
            print(parent_folder)

            # Define the new folder path in the main directory with the "_MHIs" suffix
            mhis_dir = os.path.join(main_folder, parent_folder + "_MHIs")
            print(mhis_dir)

            # Create the MHIs folder if it doesn't exist
            if not os.path.exists(mhis_dir):
                os.makedirs(mhis_dir)

            # Now, look for the 'validate' folder inside the 'shortened' folder
            for validate_subdir, validate_dirs, validate_files in os.walk(subdir):
                if os.path.basename(validate_subdir) == "validate":
                    # Loop through the files in the 'validate' folder
                    print(validate_subdir)
                    for file in validate_files:
                        # Check if the file ends with '_mhi.png'
                        if file.endswith("_mhi.png"):
                            # Construct the full file path
                            file_path = os.path.join(validate_subdir, file)
                            # Copy the file to the new MHIs folder in the main directory
                            shutil.copy(file_path, mhis_dir)

            print(f"Files from {parent_folder} copied to {mhis_dir}")

if __name__ == "__main__":
    # Prompt the user to enter the main folder path
    main_folder_path = ""

    # Call the function with the provided main folder path
    copy_mhi_files(main_folder_path)
