# TMDb Movie Data Report

## 1. Executive Summary

This report analyzes `tmdb_movies.csv`, a dataset of 18 English-language films released between 1997 and 2019. Every film in the file reported revenue above $1.24 billion, so this is a sample of very high-grossing films, not a representative cross-section of cinema.

Within that sample, *Avengers: Endgame* has the highest reported revenue ($2,927.4M), while *Avatar* has the highest reported profit ($2,686.7M) and the highest ROI (1,133.6%). Ratings fall in a narrow band (6.50 to 8.25) and every film has more than 10,000 votes. TMDb popularity is dominated by one outlier, *Avengers: Infinity War* (142.7), and popularity tracks vote count and rating more closely than it tracks revenue or ROI. The derived `profit` and `roi_percentage` columns are internally consistent with the budget and revenue columns, but they inherit the weaknesses of reported budgets and grosses.

All monetary values in this report are nominal millions of US dollars, as provided in the CSV.

## 2. Dataset Overview

The file contains **18 records and 15 columns**. There are no duplicate IDs or titles.

| Group | Columns |
|---|---|
| Identifiers | `id`, `title` |
| Descriptive | `release_date`, `original_language`, `genres`, `runtime`, `collection_name`, `director` |
| Financial | `budget (million usd)`, `revenue (million usd)`, `profit`, `roi_percentage` |
| Audience / platform | `popularity`, `vote_average`, `vote_count` |

**Missing values.** Only `collection_name` has missing values: 2 of 18 records (*Titanic* and *Beauty and the Beast*). The dataset does not say whether these films have no collection or whether the value failed to load, so they are treated as unknown rather than as "standalone." All financial and rating fields are fully populated, and no budget or revenue is zero.

**Data quality checks and issues.**

The derived columns validate correctly. `profit` equals revenue minus budget for every row, and `roi_percentage` equals profit divided by budget times 100, in both cases to within floating-point rounding (differences below 1e-12).

Budget and revenue have different precision. Budgets are whole numbers of millions, and 16 of 18 are multiples of 5, which suggests rounded estimates. Revenues carry six decimal places. Profit and ROI therefore look more precise than the budget input justifies. *Furious 7* revenue (1,515.400000) also appears rounded.

Units are stated in the budget and revenue headers but not in `profit`; profit is implicitly in million USD. `roi_percentage` is a percentage.

Multi-valued fields (`genres`, `director`) are pipe-delimited and need splitting before category analysis. Director order is inconsistent between related records: *Frozen* lists "Chris Buck|Jennifer Lee" and *Frozen II* lists "Jennifer Lee|Chris Buck". A naive group-by on the raw string would treat these as two different directors.

The rows are not sorted by any visible metric (for example, *Titanic* appears after *Avengers: Infinity War* despite higher revenue). The selection and ordering logic is not documented in the file.

There is no column recording when the data was retrieved, which matters for time-sensitive fields such as `popularity` and `vote_count`.

**Sample composition.** All 18 films are in English (`en`). Sixteen belong to a named collection, including four from *The Avengers Collection* and two each from the Star Wars, Jurassic Park and Frozen collections. Adventure appears in the genre list of 15 films, and Action and Science Fiction in 10 each.

## 3. Financial Performance

### Highest reported revenue

| Rank | Title | Revenue ($M) | Budget ($M) |
|---|---|---|---|
| 1 | Avengers: Endgame | 2,927.4 | 356 |
| 2 | Avatar | 2,923.7 | 237 |
| 3 | Titanic | 2,264.2 | 200 |
| 4 | Star Wars: The Force Awakens | 2,068.2 | 245 |
| 5 | Avengers: Infinity War | 2,052.4 | 300 |

The top two are separated by only $3.7M, about 0.1% of revenue, which is smaller than the plausible uncertainty in reported grosses.

### Highest reported profit (`profit` column)

| Rank | Title | Profit ($M) | Revenue rank |
|---|---|---|---|
| 1 | Avatar | 2,686.7 | 2 |
| 2 | Avengers: Endgame | 2,571.4 | 1 |
| 3 | Titanic | 2,064.2 | 3 |
| 4 | Star Wars: The Force Awakens | 1,823.2 | 4 |
| 5 | Avengers: Infinity War | 1,752.4 | 5 |

The top five by profit are the same films as by revenue. *Avatar* overtakes *Endgame* because its reported budget is $119M lower. The lowest profit belongs to *Star Wars: The Last Jedi* ($1,034.4M), which ranks 14th of 18 by revenue but has the joint-second-largest budget ($300M).

### Descriptive statistics (n = 18 for every measure)

| Measure | Mean | Median | Std. dev. | Min | Max | Total |
|---|---|---|---|---|---|---|
| Budget ($M) | 213.8 | 200.0 | 62.0 | 125 | 356 | 3,848 |
| Revenue ($M) | 1,699.0 | 1,484.5 | 537.6 | 1,243.2 | 2,927.4 | 30,582.7 |
| Profit ($M) | 1,485.3 | 1,301.3 | 504.2 | 1,034.4 | 2,686.7 | 26,734.7 |
| ROI (%) | 719.5 | 694.5 | 212.1 | 344.8 | 1,133.6 | n/a |

Revenue and profit are right-skewed: the mean exceeds the median by more than $180M in both cases, pulled up by *Endgame*, *Avatar* and *Titanic*.

### Limitations of revenue minus budget as profit

The `profit` column is a simple gross margin, not a profit figure in an accounting sense. Reported budgets typically refer to production cost and may exclude marketing, distribution and financing costs. Reported revenue is gross receipts, of which only a share reaches the producer or studio. The calculation also ignores timing and inflation: figures span 1997 to 2019 and are nominal, so *Titanic*'s numbers are not directly comparable to *Endgame*'s. Finally, the budgets here look rounded, so small profit differences between films should not be over-interpreted. The column is best read as "reported gross minus reported production budget."

### ROI

All 18 films have a positive budget and a valid `roi_percentage`, so ROI is analyzed for the full sample.

| Highest ROI | ROI (%) | Budget ($M) | | Lowest ROI | ROI (%) | Budget ($M) |
|---|---|---|---|---|---|---|
| Avatar | 1,133.6 | 237 | | Star Wars: The Last Jedi | 344.8 | 300 |
| Titanic | 1,032.1 | 200 | | Avengers: Age of Ultron | 498.0 | 235 |
| Jurassic World | 1,014.4 | 150 | | Incredibles 2 | 521.6 | 200 |
| Harry Potter and the Deathly Hallows: Part 2 | 973.2 | 125 | | The Lion King | 539.2 | 260 |
| Frozen II | 869.1 | 150 | | Black Panther | 575.0 | 200 |

ROI rankings differ noticeably from revenue rankings. *Jurassic World* is 6th by revenue but 3rd by ROI; *Avengers: Endgame* is 1st by revenue but 8th by ROI. Across the sample, ROI moves weakly in the opposite direction to budget (Spearman ρ = −0.45). Part of this is mechanical, because budget is the ROI denominator, and part may reflect how the sample was chosen: since every film cleared roughly $1.24B in revenue, a smaller budget almost guarantees a higher ratio.

## 4. Ratings and Popularity

### Highly rated films, with vote counts

| Title | Vote average | Vote count |
|---|---|---|
| Avengers: Endgame | 8.246 | 29,005 |
| Avengers: Infinity War | 8.245 | 33,148 |
| Harry Potter and the Deathly Hallows: Part 2 | 8.081 | 22,569 |
| The Avengers | 8.080 | 40,030 |
| Titanic | 7.901 | 27,901 |

Vote counts range from 10,511 (*Frozen II*) to 40,030 (*The Avengers*). Because every film has more than 10,000 votes, none of these averages rests on a thin base, and vote count does not need to be used to discount any film here. The more important caveat is that the rating range is narrow (6.50 to 8.25; standard deviation 0.54). The top two differ by 0.001 and the next two by 0.001, so these should be treated as ties. The lowest-rated films are *Jurassic World: Fallen Kingdom* (6.50), *Star Wars: The Last Jedi* (6.70) and *Jurassic World* (6.70).

### Popularity

TMDb popularity ranges from 31.3 (*Jurassic World*) to 142.7 (*Avengers: Infinity War*), with a median of 46.1. *Infinity War* is a clear outlier at 1.6 times the next-highest value (*Endgame*, 87.2). Excluding it lowers the mean from 54.5 to 49.3.

### How the measures relate

Rank correlations (Spearman ρ, n = 18) are used because of the small sample and the popularity outlier.

| Pair | ρ |
|---|---|
| Vote average vs vote count | 0.70 |
| Popularity vs vote count | 0.68 |
| Popularity vs vote average | 0.56 |
| Popularity vs revenue | 0.40 |
| Vote average vs revenue | 0.40 |
| Popularity vs ROI | −0.05 |

With only 18 films, coefficients below roughly 0.47 are not distinguishable from zero at conventional significance levels, so only the first three relationships are reasonably clear. Popularity aligns more with audience engagement on TMDb (vote count, rating) than with financial outcomes, and has essentially no relationship with ROI.

Individual cases illustrate that these metrics measure different things. *Jurassic World* is 6th by revenue and 3rd by ROI, but has the lowest popularity in the dataset and the second-lowest rating. *Jurassic World: Fallen Kingdom* has the lowest rating (6.50) but the 6th-highest popularity (54.5). *Frozen II* is 10th by revenue yet has the fewest votes.

## 5. Key Findings

1. **Revenue leadership and profit leadership differ at the top.** *Avengers: Endgame* has the highest reported revenue ($2,927.4M) but *Avatar* has the highest reported profit ($2,686.7M) and ROI (1,133.6%), because its reported budget is $119M lower. The revenue gap between them is only $3.7M.

2. **Large budgets do not translate into higher returns in this sample.** *Star Wars: The Last Jedi* ($300M budget) has both the lowest profit ($1,034.4M) and the lowest ROI (344.8%), while *Harry Potter and the Deathly Hallows: Part 2*, with the smallest budget ($125M), has the 4th-highest ROI (973.2%). This is an observed pattern, not evidence that smaller budgets cause better returns; the selection of only $1.2B+ films and the use of budget as the ROI denominator both contribute.

3. **Ratings are uniformly well-supported but tightly clustered.** All films exceed 10,000 votes and score between 6.50 and 8.25. The top four (*Endgame*, *Infinity War*, *Deathly Hallows: Part 2*, *The Avengers*) all score above 8.0 and are separated by less than 0.17 points.

4. **The four Avengers Collection films lead on TMDb popularity.** They occupy the top four popularity positions (142.7, 87.2, 83.1, 65.5) and include the two highest-rated films. A possible explanation is ongoing franchise-level attention on the platform, but the dataset contains nothing that would confirm this.

5. **Popularity is a poor proxy for financial success here.** Popularity correlates with vote count (ρ = 0.68) and rating (ρ = 0.56) but only weakly with revenue (ρ = 0.40) and not at all with ROI (ρ = −0.05). *Jurassic World* (high revenue and ROI, lowest popularity) is the clearest counter-example.

## 6. Limitations

**Small, deliberately selected sample.** Eighteen films, all English-language and all above roughly $1.24B in reported revenue, cannot support conclusions about films in general. There are no flops, mid-budget films or non-English titles, so the analysis describes variation among blockbusters only. Correlations computed on 18 points are unstable and could change substantially with a few added or removed films.

**Missing and undocumented data.** `collection_name` is missing for two films, and the file gives no reason. The selection criteria, row order and data retrieval date are not documented.

**Reported budgets and revenues.** Budgets appear rounded, likely cover production only, and come from public reporting rather than audited accounts. Revenues are gross figures, not producer income. All values are nominal across a 22-year span, so older films are understated relative to newer ones in real terms. The `profit` and `roi_percentage` columns inherit all of these issues.

**TMDb-specific metrics.** `popularity` is a platform-internal score that reflects activity on TMDb at the time of retrieval; it is not a measure of box-office demand or general audience size, and it changes over time. `vote_average` and `vote_count` reflect TMDb users, who may not represent cinema audiences as a whole.

## 7. Conclusion

The dataset is clean and internally consistent: no duplicate records, only two missing values (both in `collection_name`), and derived profit and ROI columns that match their inputs exactly. Within this blockbuster-only sample, revenue and profit rankings are broadly similar at the top, but ROI reorders films substantially and favors lower-budget titles such as *Avatar*, *Titanic*, *Jurassic World* and *Harry Potter and the Deathly Hallows: Part 2*. Ratings are well-supported but narrowly spread, and TMDb popularity relates more to on-platform engagement than to financial performance. Given the small, selective sample and the nature of reported budgets and grosses, these results are best treated as descriptive observations about these 18 films rather than general conclusions about what drives film success.
