import os
import subprocess

def convert_notebooks_to_py(directory='.'):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.ipynb') and not file.startswith('.'):
                notebook_path = os.path.join(root, file)
                print(f"Converting {notebook_path} to .py...")
                subprocess.run([
                    'jupyter', 'nbconvert', '--to', 'script', notebook_path
                ])
                # (Opcjonalnie) Usuń oryginalny plik notebooka
                os.remove(notebook_path)
                print(f"Deleted {notebook_path}")

if __name__ == "__main__":
    convert_notebooks_to_py()