# IARAG-SynthData
Repository containing the synthetic dataset created for IARAG and helper classification script

# How to use
1. **Clone the repo and install dependencies:**

```bash
# Clone the repository
git clone https://github.com/alvarodelser/IARAG-SynthData.git
cd IARAG-SynthData

# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

2. **Add your dataset** to the root folder. It must be named `dataset-xxx` where xxx is the type of document to classify. Inside put the generated `.json` files to classify. Accepted types are:
  - NOTE
  - CALENDAR EVENT
  - EMAIL
  - FILE
  - TASK

3. **Add the classification categories** for that type to `classification_options.json`.

4. **Run `classify.py`** and begin classifying. Results are on `results.csv`. It will not ask you to classify something previously classified.

# Features
- Stores synthetic datasets in JSON format, organized by type (e.g. `dataset-note`, `dataset-task`, etc.)
- Provides a console-based checklist interface using `questionary` for easy classification
- Allows selecting the current validator and dataset type at runtime
- Automatically skips files already labeled by the current user
- Displays each document's contents in a readable format, with:
  - Pretty-printed JSON for structured fields
  - Detects and cleans up embedded HTML if present in any text fields
  - Long-form fields (like `"content"` or `"body"`) rendered as clean, line-broken panels
- "❌ Exit" at any classification point to stop the session
- Saves results incrementally to `results.csv`

