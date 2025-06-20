# IARAG-SynthData
Repository containing the synthetic dataset created for IARAG and helper classification script

# How to use
0. Clone the repo and install dependencies:

```bash
git clone https://github.com/alvarodelser/IARAG-SynthData.git
cd IARAG-SynthData
pip install -r requirements.txt
```

1. Add your dataset to the root folder. It must be named dataset-xxx where xxx is the type of document to classify. Inside put the generated .json files to classify. Accepted types are:
  - NOTE
  - CALENDAR EVENT
  - EMAIL
  - FILE
  - TASK

3. Add the classification categories for that type to classification_options.json.

4. Run classify.py and begin classifying. Results are on results.csv. It will not ask you to classify something previously classified.
