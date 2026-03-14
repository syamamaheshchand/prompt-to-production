# skills.md

skills:
  - name: load_dataset
    description: Reads the budget CSV, validates columns, and reports the null count and specific rows before returning the dataset.
    input: File path to the budget CSV.
    output: A validated dataset collection containing the rows, and a report on null values.
    error_handling: If the schema doesn't match or the file is missing, refuse processing and raise an error.

  - name: compute_growth
    description: Takes the validated dataset, filters by the specific ward and category, and computes the specified growth type per period.
    input: Dataset, specific ward name, specific category name, and growth_type (e.g. 'MoM').
    output: A per-period table (list of dicts) with the computed growth, actual spend, and the explicit formula shown for each row.
    error_handling: If actual_spend is null for a period, it must flag the row in the output instead of computing a value. If growth_type is unknown, it must refuse. If the user requests to skip the ward or category filter to aggregate, it must refuse.
