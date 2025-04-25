import papermill as pm

workflow_notebooks = [
    "top_200_global_daily.ipynb",
    "top_100_global_daily.ipynb",
    "top_50_global_daily.ipynb"
]

for nb in workflow_notebooks:
    print(f'Running {nb}...')
    pm.execute_notebook(
        nb
    )