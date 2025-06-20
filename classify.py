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

def initialize_results_csv(files):
    """Create results.csv with empty entries if not present."""
    if not os.path.exists(RESULTS_CSV):
        with open(RESULTS_CSV, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['file'] + VALIDATORS)
            writer.writeheader()
            for file in files:
                writer.writerow({'file': file.name, **{v: '' for v in VALIDATORS}})

def load_results():
    """Load the full table of results as a dict keyed by filename."""
    results = {}
    if not os.path.exists(RESULTS_CSV):
        return results
    with open(RESULTS_CSV, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results[row['file']] = row
    return results

def save_results(all_rows):
    """Write the full table back to the CSV file."""
    with open(RESULTS_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['file'] + VALIDATORS)
        writer.writeheader()
        for row in all_rows.values():
            writer.writerow(row)

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

    files = list(dataset_path.glob("*.json"))
    initialize_results_csv(files)
    results = load_results()

    for file in files:
        row = results.get(file.name)
        if not row:
            row = {'file': file.name, **{v: '' for v in VALIDATORS}}
            results[file.name] = row
        if row[validator]:
            continue

        display_json(file)

        label = questionary.select(
            f"How would you classify '{file.name}'?",
            choices=options
        ).ask()

        row[validator] = label
        results[file.name] = row
        save_results(results)  # Save after each classification

if __name__ == "__main__":
    classify_files()
