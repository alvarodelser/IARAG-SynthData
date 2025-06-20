# IARAG-SynthData
Repository containing the synthetic dataset created for IARAG and helper classification script

# How to use
1. Upload your dataset to the root folder. It must be named dataset-xxx where xxx is the type of document to classify. Accepted types are NOTE, CALENDAR EVENT, EMAIL, FILE and TASK. Inside the generated .json files to classify.

2. Add the classification categories for that type to classification_options.json.

3. Run classify.py and begin classifying. Results are on results.csv. It will not ask you to classify something previously classified.
