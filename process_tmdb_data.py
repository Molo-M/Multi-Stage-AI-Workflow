"""Transform saved TMDb movie responses into a clean CSV file."""

import csv
import json
import sys
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any


INPUT_FILE = Path(__file__).resolve().with_name("tmdb_movies_raw.json")
OUTPUT_FILE = Path(__file__).resolve().with_name("tmdb_movies.csv")

CSV_COLUMNS = [
    "id",
    "title",
    "release_date",
    "original_language",
    "genres",
    "budget (million usd)",
    "revenue (million usd)",
    "runtime",
    "popularity",
    "vote_average",
    "vote_count",
    "collection_name",
    "director",
    "profit",
    "roi_percentage",
]


def load_records(path: Path) -> list[Any]:
    """Load the saved API responses, reporting file and JSON errors clearly."""
    try:
        with path.open("r", encoding="utf-8") as input_file:
            data = json.load(input_file)
    except FileNotFoundError as error:
        raise ValueError(f"Input file not found: {path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in {path} at line {error.lineno}, column {error.colno}"
        ) from error
    except OSError as error:
        raise ValueError(f"Could not read input file {path}: {error}") from error

    if not isinstance(data, list):
        raise ValueError(
            f"Unexpected top-level JSON structure in {path}: expected a list of records"
        )
    return data


def is_movie_record(record: Any) -> bool:
    """Reject API errors and objects without the identifying movie fields."""
    if not isinstance(record, dict):
        return False
    if record.get("success") is False or (
        "status_code" in record and "status_message" in record
    ):
        return False

    movie_id = record.get("id")
    title = record.get("title")
    return (
        movie_id is not None
        and str(movie_id).strip() != ""
        and isinstance(title, str)
        and bool(title.strip())
    )


def parse_number(value: Any) -> Decimal | None:
    """Return a finite decimal number, or None for absent or malformed values."""
    if isinstance(value, bool) or value is None:
        return None
    try:
        number = Decimal(str(value).strip())
    except (InvalidOperation, ValueError):
        return None
    return number if number.is_finite() else None


def format_number(value: Decimal | None) -> str:
    """Format decimals without unnecessary trailing zeroes."""
    if value is None:
        return ""
    formatted = format(value, "f")
    if "." in formatted:
        formatted = formatted.rstrip("0").rstrip(".")
    return formatted


def positive_number(value: Any) -> Decimal | None:
    number = parse_number(value)
    return number if number is not None and number > 0 else None


def clean_release_date(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    try:
        parsed_date = date.fromisoformat(value)
    except ValueError:
        return ""
    return parsed_date.isoformat() if value == parsed_date.isoformat() else ""


def clean_names(value: Any) -> str:
    """Join names from a TMDb list, tolerating missing or malformed entries."""
    if not isinstance(value, list):
        return ""
    names = [
        item["name"].strip()
        for item in value
        if isinstance(item, dict)
        and isinstance(item.get("name"), str)
        and item["name"].strip()
    ]
    return "|".join(names)


def extract_collection_name(value: Any) -> str:
    if not isinstance(value, dict):
        return ""
    name = value.get("name")
    return name.strip() if isinstance(name, str) else ""


def extract_directors(value: Any) -> str:
    if not isinstance(value, dict):
        return ""
    crew = value.get("crew")
    if not isinstance(crew, list):
        return ""

    directors = [
        person["name"].strip()
        for person in crew
        if isinstance(person, dict)
        and person.get("job") == "Director"
        and isinstance(person.get("name"), str)
        and person["name"].strip()
    ]
    return "|".join(directors)


def clean_text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def transform_record(record: dict[str, Any]) -> dict[str, str]:
    budget = positive_number(record.get("budget"))
    revenue = positive_number(record.get("revenue"))
    budget_millions = budget / Decimal(1_000_000) if budget is not None else None
    revenue_millions = revenue / Decimal(1_000_000) if revenue is not None else None

    # These are simple reported revenue-minus-budget metrics, not net profit
    # after marketing, distribution, or other costs.
    profit = (
        revenue_millions - budget_millions
        if revenue_millions is not None and budget_millions is not None
        else None
    )
    roi_percentage = (
        (revenue - budget) / budget * Decimal(100)
        if revenue is not None and budget is not None
        else None
    )

    credits = record.get("credits")
    genres = clean_names(record.get("genres"))
    return {
        "id": str(record.get("id", "")).strip(),
        "title": clean_text(record.get("title")),
        "release_date": clean_release_date(record.get("release_date")),
        "original_language": clean_text(record.get("original_language")),
        "genres": genres,
        "budget (million usd)": format_number(budget_millions),
        "revenue (million usd)": format_number(revenue_millions),
        "runtime": format_number(positive_number(record.get("runtime"))),
        "popularity": format_number(parse_number(record.get("popularity"))),
        "vote_average": format_number(parse_number(record.get("vote_average"))),
        "vote_count": format_number(parse_number(record.get("vote_count"))),
        "collection_name": extract_collection_name(
            record.get("belongs_to_collection")
        ),
        "director": extract_directors(credits),
        "profit": format_number(profit),
        "roi_percentage": format_number(roi_percentage),
    }


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def print_summary(rows: list[dict[str, str]], invalid_count: int) -> None:
    duplicate_count = len(rows) - len({row["id"] for row in rows})
    missing_columns = (
        "budget (million usd)",
        "revenue (million usd)",
        "vote_average",
    )

    print(f"Valid movies exported: {len(rows)}")
    print(f"Invalid records skipped: {invalid_count}")
    print(f"Duplicate movie IDs: {duplicate_count}")
    print("Missing values:")
    for column in missing_columns:
        missing_count = sum(not row[column] for row in rows)
        print(f"  {column}: {missing_count}")


def main() -> int:
    try:
        records = load_records(INPUT_FILE)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    rows = []
    invalid_count = 0
    for record in records:
        if not is_movie_record(record):
            invalid_count += 1
            continue
        rows.append(transform_record(record))

    try:
        write_csv(rows, OUTPUT_FILE)
    except OSError as error:
        print(f"Error: could not write CSV file {OUTPUT_FILE}: {error}", file=sys.stderr)
        return 1

    print(f"CSV written to: {OUTPUT_FILE}")
    print_summary(rows, invalid_count)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())