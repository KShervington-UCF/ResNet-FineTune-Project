import os
import shutil
import time

# Code by ChatGPT o1-preview
# Organizes images into folders based on their class labels

def get_dataset_dir():
    """Get the absolute path to the dataset directory"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '..', '..', 'dataset'))

def extract_class_label(filename):
    """
    Extract the class label from the filename.
    Assumes the filename format is: <ID>-<CLASS>.jpg
    """
    # Split the filename at the first dash
    parts = filename.split('-', 1)
    if len(parts) > 1:
        # The class label is everything after the first dash, without the file extension
        class_label_with_ext = parts[1]
        class_label = os.path.splitext(class_label_with_ext)[0]
        return class_label
    else:
        # If no dash is found, use the entire filename without extension
        class_label = os.path.splitext(filename)[0]
        return class_label

# Paths to your datasets
dataset_dir = get_dataset_dir()
data_dirs = [os.path.join(dataset_dir, split) for split in ['validation', 'test']]

for data_dir in data_dirs:
    print(f"Processing directory: {data_dir}")

    start = time.time()

    # List all files in the directory
    try:
        file_list = os.listdir(data_dir)
    except FileNotFoundError:
        print(f"Error: Directory not found: {data_dir}")
        continue
    
    for filename in file_list:
        # Full path to the file
        file_path = os.path.join(data_dir, filename)
        if os.path.isfile(file_path):
            # Skip hidden files or system files
            if filename.startswith('.'):
                continue
            # Extract the class label from the filename
            class_label = extract_class_label(filename)
            # Directory for the class
            class_dir = os.path.join(data_dir, class_label)
            # Create the class directory if it doesn't exist
            os.makedirs(class_dir, exist_ok=True)
            # Destination path for the file
            dest_path = os.path.join(class_dir, filename)
            # Move the file to the class directory
            shutil.move(file_path, dest_path)
        else:
            print(f"Skipping {file_path}, not a file")
    
    end = time.time()

    print(f"Successfully processed directory: {data_dir} in {round(end - start)} seconds")
