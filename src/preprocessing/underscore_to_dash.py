import os

def get_dataset_dir():
    """Get the absolute path to the dataset directory"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '..', '..', 'dataset'))

exceptions = ['fresh_snow', 'melted_snow']

# Get dataset directory and create paths for all splits
dataset_dir = get_dataset_dir()
data_dirs = [os.path.join(dataset_dir, split) for split in ['train', 'validation', 'test']]

for parent_folder in data_dirs:
    if not os.path.exists(parent_folder):
        print(f"Warning: Directory not found: {parent_folder}")
        continue

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
            new_folder_name = folder_name.replace('_', '-')

            # Rename the folder 
            try:
                # Handle naming collisions by ensuring the new folder name is unique
                if os.path.exists(os.path.join(parent_folder, new_folder_name)):
                    counter = 1
                    base_folder_name = new_folder_name
                    while os.path.exists(os.path.join(parent_folder, new_folder_name)):
                        new_folder_name = f"{base_folder_name}_{counter}"
                        counter += 1

                os.rename(folder_path, os.path.join(parent_folder, new_folder_name))
                print(f"Successfully changed {folder_path}")
                
            except OSError as e:
                print(f"Error renaming folder {folder_name}: {e}")