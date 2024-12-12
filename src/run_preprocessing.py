import subprocess
import os
import sys
import shlex

def check_dataset_structure():
    base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'dataset')
    required_dirs = ['train', 'validation', 'test']
    
    if not os.path.exists(base_dir):
        print(f"Error: Dataset directory not found at {base_dir}")
        return False
        
    for dir_name in required_dirs:
        dir_path = os.path.join(base_dir, dir_name)
        if not os.path.exists(dir_path):
            print(f"Error: Required directory {dir_name} not found at {dir_path}")
            return False
            
    return True

def run_script(script_name):
    # Split the script_name into the actual script and any arguments
    parts = shlex.split(script_name)
    script_file = parts[0]
    script_args = parts[1:] if len(parts) > 1 else []
    
    # Construct the full path to the script
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'preprocessing', script_file)
    print(f"\nRunning {script_path} {' '.join(script_args)}...")
    
    try:
        env = os.environ.copy()
        env['PYTHONPATH'] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Combine the script path with any additional arguments
        command = [sys.executable, script_path] + script_args
        
        result = subprocess.run(command, check=True, env=env)
        print(f"Successfully completed {script_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_file}: {e}")
        return False

def main(downsize_num=0):
    if not check_dataset_structure():
        print("\nPreprocessing stopped due to missing dataset structure.")
        sys.exit(1)

    # Base scripts list
    scripts = ['reorganize_data.py']
    
    # Add delete_to_n.py if downsizing is requested
    if downsize_num > 0:
        scripts.append(f'delete_to_n.py {downsize_num}')
    
    # Add remaining scripts
    scripts.extend([
        'map_class_names.py',
        'underscore_to_dash.py',
        'reduce_classes.py',
    ])
    
    success = True
    for script in scripts:
        if not run_script(script):
            success = False
            break
    
    if success:
        print("\nAll preprocessing steps completed successfully!")
    else:
        print("\nPreprocessing stopped due to an error.")
        sys.exit(1)

if __name__ == "__main__":
    will_delete_to_n = input("Would you like to downsize the dataset? ([y]/n): ")

    if will_delete_to_n.lower() in ['y', '']:
        while True:
            downsize_num = input('What is the maximum number of examples you want in each class? (default: 5000): ') or '5000'
            
            try:
                downsize_num = abs(int(downsize_num))
                if downsize_num <= 0:
                    print("Error: Please enter a positive integer.")
                    continue
                break
            except ValueError:
                print("Error: Please enter a valid integer.")
        main(downsize_num)
    else:
        main(0)
