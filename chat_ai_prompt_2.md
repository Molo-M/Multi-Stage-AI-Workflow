# Task: Analyze TMDb Movie Data and Generate a Report

You are the second stage of a multi-stage AI workflow. The previous stage used GitHub Copilot in VS Code to transform saved TMDb API responses into a structured CSV file. Your input is `tmdb_movies.csv`.

Analyze the attached CSV and produce a concise, evidence-based report titled **TMDb Movie Data Report**.

## Requirements

### 1. Understand and validate the dataset
- Identify the number of movie records and columns.
- Summarize the available fields and any important missing values.
- Identify data quality issues that may affect the analysis.
- Do not assume missing values are zero.

### 2. Analyze financial performance
- Identify the movies with the highest reported revenue.
- Identify the movies with the highest reported profit, using the `profit` column when available.
- Calculate descriptive statistics for budget, revenue, and profit where valid data exists.
- Explain the limitations of using revenue minus budget as a profit measure.
- Analyze ROI only where `roi_percentage` is valid and the budget is positive.

### 3. Analyze ratings and popularity
- Identify highly rated movies, considering `vote_count` when interpreting ratings.
- Compare TMDb popularity with ratings and financial performance where the data supports meaningful observations.
- Avoid assuming that popularity, audience rating, and revenue measure the same thing.

### 4. Present key findings
- Provide five concise findings supported by the dataset.
- Include specific movie titles and numerical values where useful.
- Distinguish factual observations from possible explanations.
- Do not claim causation or invent context that is absent from the dataset.

### 5. State limitations
Discuss relevant limitations, including the small and deliberately selected sample of movies, missing data, the limitations of reported budgets and revenues, and the fact that TMDb popularity is a platform-specific metric.

## Output format

Produce a Markdown report suitable for saving as `movie_report.md`, with these sections:

1. Executive Summary
2. Dataset Overview
3. Financial Performance
4. Ratings and Popularity
5. Key Findings
6. Limitations
7. Conclusion

Use readable headings, concise paragraphs, and tables where useful. Check calculations against the provided data. If a requested statistic cannot be calculated reliably, explain why rather than guessing.

Base all findings on the attached CSV. Do not browse the web or introduce external movie information. Do not write Python code unless necessary to explain a data quality issue.