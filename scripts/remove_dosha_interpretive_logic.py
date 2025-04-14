#!/usr/bin/env python3
"""
Script to remove interpretive logic from Dosha modules
"""

import os
import re
import glob

def remove_description_function(file_path):
    """
    Remove the generate_*_description function from a file
    
    Args:
        file_path (str): Path to the file
    """
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find and remove the generate_*_description function
    pattern = r'def generate_\w+_dosha_description\([^)]*\):\s*"""[^"]*""".*?(?=\n\n|$)'
    new_content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Remove the description parameter from the return statement
    pattern = r"'description': [^}]*"
    new_content = re.sub(pattern, '', new_content)
    
    # Fix any double commas in dictionaries
    new_content = new_content.replace(',\n    }', '\n    }')
    new_content = new_content.replace(',}', '}')
    
    # Remove the description generation line
    pattern = r"# Generate the description\s*description = generate_\w+_dosha_description\([^)]*\)"
    new_content = re.sub(pattern, '', new_content, flags=re.DOTALL)
    
    with open(file_path, 'w') as f:
        f.write(new_content)
    
    print(f"Removed interpretive logic from {file_path}")

def main():
    """
    Main function
    """
    # Get all Dosha module files
    dosha_dir = 'astrovedic/vedic/compatibility/dosha'
    dosha_files = glob.glob(f"{dosha_dir}/*.py")
    
    # Process each file
    for file_path in dosha_files:
        if os.path.basename(file_path) not in ['__init__.py']:
            remove_description_function(file_path)
    
    print("Done!")

if __name__ == '__main__':
    main()
