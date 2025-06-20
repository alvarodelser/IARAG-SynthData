import os
import json
import csv
from pathlib import Path
import questionary
from rich import print_json
from rich.panel import Panel
from rich.console import Console
from bs4 import BeautifulSoup


# CONFIG
FOLDER_PREFIX = "dataset-"
OPTIONS_PATH = "classification_options.json"
RESULTS_CSV = "results.csv"
VALIDATORS = ["ALVARO", "VIRGINIA", "PAUL", "CARLOS"]

FIELDNAMES = ['file', 'dataset'] + VALIDATORS

console = Console()

def load_classification_options():
    with open(OPTIONS_PATH, "r") as f:
        return json.load(f)

def initialize_results_csv(files, dataset_type):
    """Ensure results.csv exists and includes all files for this dataset."""
    existing_rows = {}
    if os.path.exists(RESULTS_CSV):
        with open(RESULTS_CSV, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_rows[row['file']] = row

    # Add missing files for this dataset
    for file in files:
        if file.name not in existing_rows:
            existing_rows[file.name] = {
                'file': file.name,
                'dataset': dataset_type,
                **{v: '' for v in VALIDATORS}
            }

    # Write full results table
    with open(RESULTS_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in existing_rows.values():
            writer.writerow(row)

def load_results():
    results = {}
    with open(RESULTS_CSV, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results[row['file']] = row
    return results

def save_results(results):
    with open(RESULTS_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in results.values():
            writer.writerow(row)




def is_long_text(key, value):
    return (
        isinstance(value, str)
        and key.lower() in {"content", "body", "description"}
        and len(value) > 80
    )

def clean_text(text):
    if "\\n" in text:
        text = text.encode().decode("unicode_escape")
    return text.strip()

def html_to_text(html_string):
    soup = BeautifulSoup(html_string, "html.parser")
    return soup.get_text(separator="\n").strip()

def display_json(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)

    print(f"\n[bold yellow]--- {filepath.name} ---[/bold yellow]")

    cleaned = {}
    extracted_long_texts = {}

    for key, value in data.items():
        if isinstance(value, str) and is_long_text(key, value):
            if any(tag in value for tag in ("<p", "<div", "<br", "</")):
                extracted_long_texts[key] = clean_text(html_to_text(value))
            else:
                extracted_long_texts[key] = clean_text(value)
        else:
            cleaned[key] = value

    print_json(data=cleaned)

    for key, content in extracted_long_texts.items():
        console.print(Panel(content, title=f"[cyan]{key}", border_style="magenta"))

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
    initialize_results_csv(files, dataset_type)
    results = load_results()

    for file in files:
        row = results.get(file.name)
        if not row:
            continue  # should not happen if initialization was correct

        # Validate it's the correct dataset
        if row['dataset'] != dataset_type:
            continue

        # Skip if already labeled by this validator
        if row.get(validator):
            continue

        display_json(file)

        choices_with_exit = options + ["❌ Exit"]
        label = questionary.select(
            f"How would you classify '{file.name}'?",
            choices=choices_with_exit
        ).ask()
        
        if label == "❌ Exit":
            print("Exiting classification session.")
            break

        row[validator] = label
        results[file.name] = row
        save_results(results)

if __name__ == "__main__":
    classify_files()
