import os
import shutil

# Purpose of this script:
# Reduces the number of classes in the dataset by mapping classes to a new set of classes

def get_dataset_dir():
    """Get the absolute path to the dataset directory"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '..', '..', 'dataset'))

# Define the class mapping for reduction
class_mapping = {
    # Asphalt classes (dry)
    'dry-asphalt-good': 'asphalt-good',
    'dry-asphalt-intermediate': 'asphalt-intermediate',
    'dry-asphalt-bad': 'asphalt-bad',
    
    # Asphalt classes (wet)
    'wet-asphalt-good': 'asphalt-good',
    'wet-asphalt-intermediate': 'asphalt-intermediate',
    'wet-asphalt-bad': 'asphalt-bad',
    
    # Water-covered asphalt
    'water-asphalt-smooth': 'water-asphalt',
    'water-asphalt-intermediate': 'water-asphalt',
    'water-asphalt-bad': 'water-asphalt',
    
    # Concrete classes (dry)
    'dry-concrete-good': 'paved-good',
    'dry-concrete-intermediate': 'paved-intermediate',
    'dry-concrete-bad': 'paved-bad',
    
    # Concrete classes (wet)
    'wet-concrete-good': 'paved-good',
    'wet-concrete-intermediate': 'paved-intermediate',
    'wet-concrete-bad': 'paved-bad',
    
    # Water-covered concrete
    'water-concrete-good': 'water-paved',
    'water-concrete-intermediate': 'water-paved',
    'water-concrete-bad': 'water-paved',
    
    # Unpaved classes (dry)
    'dry-gravel': 'unpaved',
    'dry-mud': 'unpaved',
    
    # Unpaved classes (wet)
    'wet-gravel': 'unpaved',
    'wet-mud': 'unpaved',
    
    # Water-covered unpaved
    'water-gravel': 'water-unpaved',
    'water-mud': 'water-unpaved',
    
    # Snow and ice (map to unpaved)
    'fresh_snow': 'unpaved',
    'melted_snow': 'unpaved',
    'ice': 'unpaved'
}

def process_directory(directory):
    """Process a single directory to reduce classes"""
    if not os.path.exists(directory):
        print(f"Warning: Directory not found: {directory}")
        return

    # Create temporary directory for new class structure
    temp_dir = directory + '_temp'
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    # Create directories for new classes
    new_classes = set(class_mapping.values())
    for new_class in new_classes:
        os.makedirs(os.path.join(temp_dir, new_class))

    # Process each class directory
    for class_dir in os.listdir(directory):
        class_path = os.path.join(directory, class_dir)
        if not os.path.isdir(class_path):
            continue

        # Get the new class name
        new_class = None
        for old_class, mapped_class in class_mapping.items():
            if old_class in class_dir:
                new_class = mapped_class
                break

        if new_class is None:
            print(f"Warning: No mapping found for class {class_dir}")
            continue

        # Process images in the class directory
        for image in os.listdir(class_path):
            if not image.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue

            # Create new image name with new class
            image_parts = image.split('-')
            new_image_name = f"{image_parts[0]}-{new_class}.{image.split('.')[-1]}"
            
            # Copy image to new location
            src_path = os.path.join(class_path, image)
            dst_path = os.path.join(temp_dir, new_class, new_image_name)
            shutil.copy2(src_path, dst_path)

    # Replace original directory with new structure
    shutil.rmtree(directory)
    shutil.move(temp_dir, directory)

def main():
    dataset_dir = get_dataset_dir()
    splits = ['train', 'validation', 'test']
    
    for split in splits:
        split_dir = os.path.join(dataset_dir, split)
        print(f"Processing {split} directory...")
        process_directory(split_dir)
        print(f"Finished processing {split} directory")

if __name__ == "__main__":
    main()
