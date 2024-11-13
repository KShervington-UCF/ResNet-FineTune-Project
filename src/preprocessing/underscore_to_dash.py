import os

exceptions = ['fresh_snow', 'melted_snow']

# Parent folder of training dataset
parent_folder = '../../dataset/train'

# list of folders in the parent folder
folders = [f for f in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, f))]

# iterate over each folder
for folder in folders:
    # get path and name of current image folder
    folder_path = os.path.join(parent_folder, folder)
    folder_name = os.path.basename(folder_path)

    # Returns True or False if any word in og_class_names is found in the folder_name
    contains_underscore = '_' in folder_name

    # Returns True if the folder name matches any name from the list of exceptions
    is_exception = any(True for name in exceptions if name in folder_name)

    # Check if folder needs to be explored
    if contains_underscore and not is_exception:

        new_folder_name = folder

        new_folder_name = new_folder_name.replace('_', '-')

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

    print(f"Successfully changed {folder_path}")