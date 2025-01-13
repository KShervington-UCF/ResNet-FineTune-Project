import os
import sys

def find_min_class(parent_dir):
    list_of_folders = os.listdir(parent_dir)
    min = float('inf')

    for class_folder in list_of_folders:
        folder_path = os.path.join(parent_dir, class_folder)
        num_images = len(os.listdir(folder_path)) 
        min = min if min < num_images else num_images

    return min


def get_dataset_dir():
    """Get the absolute path to the dataset directory"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, 'dataset'))

def main():
    dataset_dir = get_dataset_dir()
    splits = ['train', 'validation', 'test']
    
    for split in splits:
        split_dir = os.path.join(dataset_dir, split)
        print(f"Processing {split} directory...")
        split_min = find_min_class(split_dir)
        print(f"{split} directory min is {split_min}")

if __name__ == "__main__":
    main()
