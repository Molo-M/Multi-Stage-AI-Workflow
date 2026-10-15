# Task: Build a TMDb JSON to CSV data transformation script

Create a Python script in `process_tmdb_data.py` that reads the existing `tmdb_movies_raw.json` file in the project root and transforms the saved TMDb movie API responses into a clean CSV file named `tmdb_movies.csv`.

## Requirements

1. Read the JSON file from the project root using Python's `json` module. Do not make any API requests. The script must work offline once the JSON file exists.

2. Validate the input. Handle a missing file, invalid JSON, an unexpected top-level data structure, and records that are API error responses rather than valid movie records. Print clear error messages or skip invalid records appropriately.

3. Extract these fields when available:
   - `id`
   - `title`
   - `release_date`
   - `original_language`
   - `genres`
   - `budget`
   - `revenue`
   - `runtime`
   - `popularity`
   - `vote_average`
   - `vote_count`
   - `belongs_to_collection`
   - `credits`

4. Flatten nested fields:
   - Convert `genres` into a pipe-separated string of genre names.
   - Extract `belongs_to_collection.name` as `collection_name`.
   - Extract the names of people whose `job` is `Director` from `credits.crew` into a pipe-separated `director` column.
   - Handle missing or malformed nested data without crashing.

5. Clean the data:
   - Parse `release_date` as a date in ISO format (`YYYY-MM-DD`), leaving invalid or missing dates blank.
   - Treat zero or negative budgets, revenues, and runtimes as missing for analysis, represented by blank CSV cells.
   - Preserve valid numeric values for popularity and vote metrics.
   - Do not invent or impute missing values.
   - Keep financial values in their original TMDb units, which are nominally US dollars. Do not convert them to millions in this script.
   - Convert the `revenue` and `budget` columns to convert to (million usd) by dividing them by 1,000,000. Make sure to rename the columns by adding (million usd) to the column name.

6. Add two derived columns:
   - `profit`: revenue minus budget, only when both values are positive and valid.
   - `roi_percentage`: `(revenue - budget) / budget * 100`, only when both values are positive and valid.

   Leave both derived values blank when the required inputs are missing or invalid. Explain in a code comment that these are simple reported revenue-minus-budget metrics and do not represent net profit after marketing, distribution, or other costs.

7. Export the result to `tmdb_movies.csv` using UTF-8 encoding, with one row per valid movie and consistent column names.

8. Print a short validation summary showing:
   - Number of valid movies exported
   - Number of invalid records skipped
   - Number of duplicate movie IDs, if any
   - Number of missing values in important columns such as budget, revenue, and vote_average

9. Write readable, modular Python code with functions where appropriate, a main entry point, and comments explaining non-obvious logic. Avoid unnecessary classes or complicated architecture.

10. Do not overwrite `api_call.py` or modify `tmdb_movies_raw.json`. Do not install packages or create unrelated files.

Before implementing, briefly explain the proposed approach. Then create `process_tmdb_data.py` and show me how to run it and verify its output.