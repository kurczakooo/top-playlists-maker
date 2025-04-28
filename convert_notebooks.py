import os
import subprocess

target_path = 'src/target'

def convert_notebooks_to_py(directory='.'):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.ipynb') and not file.startswith('.'):
                notebook_path = os.path.join(root, file)
                print(f"Converting {notebook_path} to .py...")
                
                subprocess.run([
                    'jupyter', 'nbconvert', 
                    '--to', 'script',
                    '--output-dir', target_path, 
                    notebook_path
                ])
                
                print(f'Success in converting {notebook_path}.')

if __name__ == "__main__":
    convert_notebooks_to_py()