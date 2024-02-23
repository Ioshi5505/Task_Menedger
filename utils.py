import json
from collections import defaultdict

def save_tasks_to_file(tasks_by_date, filename="tasks.json"):
    with open(filename, "w") as file:
        json.dump(tasks_by_date, file)

def load_tasks_from_file(filename="tasks.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file, object_hook=lambda d: defaultdict(list, d))
    except FileNotFoundError:
        return defaultdict(list)

def load_stylesheet(filename="style.css"):
    try:
        with open(filename, "r") as file:
            return file.read()
    except FileNotFoundError:
        print("Stylesheet file not found.")
        return None
