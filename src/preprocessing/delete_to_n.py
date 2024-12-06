import os
import random
import argparse

def get_dataset_dir():
    """Get the absolute path to the dataset directory"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '..', '..', 'dataset'))

def get_reduction_ratio(folder_path, target_num):
    """Calculate the reduction ratio based on the largest class in the folder"""
    folders = os.listdir(folder_path)
    max_images = 0
    
    for folder in folders:
        folder_path_full = os.path.join(folder_path, folder)
        if os.path.isdir(folder_path_full):
            image_files = [f for f in os.listdir(folder_path_full) if f.lower().endswith('.jpg')]
            max_images = max(max_images, len(image_files))
    
    if max_images <= target_num:
        return 1.0  # No reduction needed
    return target_num / max_images

def delete_to_n(folder_path, target_num, reduction_ratio=None):
    """
    Delete images from each class in the folder to reach the target number
    If reduction_ratio is provided, use that instead of target_num
    """
    if not os.path.exists(folder_path):
        print(f"Warning: Directory not found: {folder_path}")
        return

    # List of subdirectories in the parent folder
    folders = os.listdir(folder_path)

    # Iterate through each folder that contains images
    for folder in folders:
        folder_path_full = os.path.join(folder_path, folder)
        if not os.path.isdir(folder_path_full):
            continue

        # List all files within the current folder
        files = os.listdir(folder_path_full)
        image_files = [file for file in files if file.lower().endswith('.jpg')]
        num_images = len(image_files)

        if reduction_ratio is not None:
            # Calculate target based on reduction ratio
            current_target = int(num_images * reduction_ratio)
            current_target = max(1, current_target)  # Ensure at least one image remains
        else:
            current_target = target_num

        # If the number of images is greater than the target number, proceed to randomly delete files
        if num_images > current_target:
            # Calculate how many images need to be deleted
            images_to_delete = num_images - current_target
            
            # Randomly select images to delete
            images_to_delete_list = random.sample(image_files, images_to_delete)
            
            # Delete the selected images
            for image in images_to_delete_list:
                os.remove(os.path.join(folder_path_full, image))

            print(f"{images_to_delete} images deleted from {folder}. Now there are {current_target} images left.")
        else:
            print(f"No need to delete images from {folder}. The folder contains {num_images} images, which is less than or equal to {current_target}.")

def main(target_num):
    # Base directory containing all dataset splits
    dataset_dir = get_dataset_dir()
    splits = ['train', 'validation', 'test']
    
    # Calculate reduction ratio from training set
    train_dir = os.path.join(dataset_dir, 'train')
    if not os.path.exists(train_dir):
        print(f"Error: Training directory not found: {train_dir}")
        return
        
    reduction_ratio = get_reduction_ratio(train_dir, target_num)
    
    print(f"\nReduction ratio calculated from training set: {reduction_ratio:.2%}")
    
    # Process each split
    for split in splits:
        split_dir = os.path.join(dataset_dir, split)
        print(f"\nProcessing {split} dataset...")
        if split == 'train':
            delete_to_n(split_dir, target_num)  # Use absolute target for training
        else:
            delete_to_n(split_dir, target_num, reduction_ratio)  # Use ratio for val/test

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Delete images to reach a target number per class')
    parser.add_argument('target_num', type=int, help='Target number of images to keep in each class')
    args = parser.parse_args()

    if args.target_num <= 0:
        print("Target number must be a positive integer.")
        exit(1)
    
    main(args.target_num)
