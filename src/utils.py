import os

def ensure_project_folders():
    folders = ["data", "database", "outputs", "notebooks", "src", "powerbi"]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)