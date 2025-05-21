import subprocess

workflow_scripts = [
    "src/target/top_200_global_daily.py",
    "src/target/top_100_global_daily.py",
    "src/target/top_50_global_daily.py",
    "src/target/followers_reporting.py"
]

for script in workflow_scripts:
    print(f'Running {script}...')
    subprocess.run(["python", script], check=True)
