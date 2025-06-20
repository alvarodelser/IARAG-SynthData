import os
import json
import csv
from pathlib import Path
import questionary

# CONFIG
FOLDER_PREFIX = "dataset-"
OPTIONS_PATH = "classification_options.json"
RESULTS_CSV = "results.csv"

VALIDATORS = ["ALVARO", "VIRGINIA", "PAUL", "CARLOS"]

def load_classification_options():
    with open(OPTIONS_PATH, "r") as f:
        return json.load(f)

def load_existing_results():
    if not os.path.exists(RESULTS_CSV):
        return {}
    with open(RESULTS_CSV, newline='') as f:
        reader = csv.DictReader(f)
        return {(row['file'], row['validator']): row['label'] for row in reader}

def save_result(file, validator, label):
    file_exists = os.path.exists(RESULTS_CSV)
    with open(RESULTS_CSV, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['file', 'validator', 'label'])
        if not file_exists:
            writer.writeheader()
        writer.writerow({'file': file, 'validator': validator, 'label': label})

def display_json(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
    print(f"\n--- {filepath.name} ---")
    print(json.dumps(data, indent=2))

def classify_files():
    classification_options = load_classification_options()

    # --- Select validator
    validator = questionary.select(
        "Who is doing the classification?",
        choices=VALIDATORS
    ).ask()

    # --- Select dataset type
    dataset_type = questionary.select(
        "What dataset are you classifying?",
        choices=list(classification_options.keys())
    ).ask()

    options = classification_options[dataset_type]
    folder_name = f"{FOLDER_PREFIX}{dataset_type.lower()}"
    dataset_path = Path(folder_name)

    if not dataset_path.exists():
        print(f"Folder '{folder_name}' does not exist.")
        return

    existing = load_existing_results()
    files = list(dataset_path.glob("*.json"))

    for file in files:
        if (file.name, validator) in existing:
            continue

        display_json(file)

        label = questionary.select(
            f"How would you classify '{file.name}'?",
            choices=options
        ).ask()

        save_result(file.name, validator, label)

if __name__ == "__main__":
    classify_files()
