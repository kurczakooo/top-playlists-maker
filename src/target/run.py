import subprocess

workflow_scripts = [
    "spotify_auth.py",
    "top_200_global_daily.py",
    "top_100_global_daily.py",
    "top_50_global_daily.py"
]

for script in workflow_scripts:
    print(f'Running {script}...')
    subprocess.run(["python", script], check=True)
