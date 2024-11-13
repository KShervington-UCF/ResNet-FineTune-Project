import os
import time

class_mappings = {
    "smooth": "good",
    "slight": "intermediate",
    "severe": "bad"
}

# Create list of existing class names
og_class_names = class_mappings.keys()

# Parent folder of training dataset
parent_folder = '../../dataset/validation'

# list of folders in the parent folder
folders = [f for f in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, f))]

# iterate over each folder
for folder in folders:
    start = time.time()

    # get path and name of current image folder
    folder_path = os.path.join(parent_folder, folder)
    folder_name = os.path.basename(folder_path)

    # Get list of image names within current image folder
    image_names = os.listdir(folder_path)

    # Returns True or False if any word in og_class_names is found in the folder_name
    contains_mapped_class = any(word in folder_name for word in og_class_names)

    # Check if folder needs to be explored
    if contains_mapped_class:
        # Rename each image based on class_mappings
        for image_name in image_names:

            new_img_name = image_name

            # detect which class current image belongs to and replace it with new class
            for word in og_class_names:
                new_img_name = new_img_name.replace(word, class_mappings[word])

            # Rename the image 
            try:
                os.rename(os.path.join(folder_path, image_name), os.path.join(folder_path, new_img_name))
            except OSError as e:
                print(f"Error renaming file {image_name}: {e}")

        new_folder_name = folder

        for word in og_class_names:
            new_folder_name = new_folder_name.replace(word, class_mappings[word])

        # Rename the folder 
        try:
            # Handle naming collisions by ensuring the new folder name is unique
            if os.path.exists(os.path.join(parent_folder, new_folder_name)):
                counter = 1
                base_folder_name = new_folder_name
                while os.path.exists(os.path.join(parent_folder, new_folder_name)):
                    new_folder_name = f"{base_folder_name}_{counter}"
                    counter += 1

            os.rename(os.path.join(parent_folder, folder_name), os.path.join(parent_folder, new_folder_name))
        except OSError as e:
            print(f"Error renaming folder {folder_name}: {e}")

    end = time.time()

    print(f"Successfully mapped {folder_path} in {round(end - start)} seconds")