import os
import argparse

# Define project type-specific ignore configurations
ignore_configs = {
    "frontend-web": {
        "ignore_folders": {"node_modules", ".firebase", "dist", "build", "coverage", ".idea", "Include", "Lib", "Scripts", ".git"},
        "ignore_files": {"package-lock.json", "yarn.lock", ".env"},
    },
    "backend": {
        "ignore_folders": {"node_modules", "__pycache__", "migrations", ".idea", "Include", "Lib", "Scripts", ".git"},
        "ignore_files": {"requirements.txt", "package-lock.json", "yarn.lock", ".env"},
    },
    "ml": {
        "ignore_folders": {"__pycache__", ".ipynb_checkpoints", "venv", "experiments", "logs", ".idea", "Include", "Lib", "Scripts", ".git"},
        "ignore_files": {"requirements.txt", "env.yaml"},
    },
}

# Default ignore patterns if no project type is specified
default_ignore_folders = {"node_modules", "__pycache__", ".idea", "Include", "Lib", "Scripts", ".git"}
default_ignore_files = {"package-lock.json", "yarn.lock", ".env"}


def get_ignore_config(project_type, custom_folders, custom_files):
    """Get the ignore configuration based on the project type and custom settings."""
    if project_type in ignore_configs:
        ignore_folders = ignore_configs[project_type]["ignore_folders"]
        ignore_files = ignore_configs[project_type]["ignore_files"]
    else:
        ignore_folders = default_ignore_folders
        ignore_files = default_ignore_files

    # Add custom ignore patterns
    ignore_folders.update(custom_folders)
    ignore_files.update(custom_files)

    return ignore_folders, ignore_files


def generate_directory_tree(root_dir, ignore_folders, ignore_files, level=0):
    """Recursively generates a directory tree, ignoring specified files and folders."""
    if level == 0:
        print(f"📂 {os.path.basename(root_dir)}")
    for item in sorted(os.listdir(root_dir)):
        item_path = os.path.join(root_dir, item)

        # Check if the current item is in the ignore list
        if item in ignore_folders or item in ignore_files:
            continue

        if os.path.isdir(item_path):
            print("  " * (level + 1) + f"📂 {item}")
            generate_directory_tree(item_path, ignore_folders, ignore_files, level + 1)
        else:
            print("  " * (level + 1) + f"📄 {item}")


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate a directory tree while ignoring specified files and folders.')
    parser.add_argument('--project-type', type=str, choices=['frontend-web', 'backend', 'ml'], help='Specify the project type to apply default ignore settings.')
    parser.add_argument('--ignore-folders', type=str, help='Additional folders to ignore, comma-separated.')
    parser.add_argument('--ignore-files', type=str, help='Additional files to ignore, comma-separated.')
    parser.add_argument('--root-dir', type=str, default='.', help='Root directory path (default is current directory).')
    
    args = parser.parse_args()

    # Process custom ignore patterns
    custom_folders = set(args.ignore_folders.split(',')) if args.ignore_folders else set()
    custom_files = set(args.ignore_files.split(',')) if args.ignore_files else set()

    # Determine the ignore configuration
    ignore_folders, ignore_files = get_ignore_config(args.project_type, custom_folders, custom_files)

    # Generate the directory tree
    print("\nGenerated Directory Tree:\n")
    generate_directory_tree(args.root_dir, ignore_folders, ignore_files)

if __name__ == "__main__":
    main()