import os
import subprocess

files = [
    "top_200_global_daily.py",
    "top_100_global_daily.py",
    "top_50_global_daily.py"
]

def delete_py_files():
    src_folder = "src/top_global"
    for file_name in files:
        file_path = os.path.join(src_folder, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        else:
            print(f"File doesn't exist: {file_path}")

if __name__ == "__main__":
    delete_py_files()