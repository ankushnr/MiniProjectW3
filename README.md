# ETL Pipeline + Tests

A simple Python mini-project that extracts user data from a REST API, transforms it using Pandas, and saves the cleaned data to a CSV file. The project also includes automated unit tests using Pytest.

## Features

- Fetches user records from a REST API.
- Converts the JSON response into a Pandas DataFrame.
- Selects the required columns: `id`, `name`, `username`, and `email`.
- Cleans whitespace from text fields.
- Converts email addresses to lowercase.
- Removes duplicate records based on `id`.
- Sorts records by `id`.
- Saves the processed data as a CSV file.
- Includes Pytest unit tests for the transformation logic.

## Tech Stack

- **Python**
- **Requests** — API requests
- **Pandas** — data transformation
- **Pytest** — automated testing

## Project Structure

```text
WEEK3/
├── etl_pipeline.py
├── data/
│   └── users.csv        # Generated when the pipeline runs
└── README.md
```

## Requirements

- Python 3.10 or later
- An internet connection to access the API

## Installation

Install the required packages:

```bash
pip install requests pandas pytest
```

## Run the Pipeline

Run the Python file:

```bash
python etl_pipeline.py
```

The pipeline will:

1. Extract user data from the API.
2. Transform and clean the records using Pandas.
3. Save the output to `data/users.csv`.
4. Display a preview of the processed records in the terminal.

### Data Source

The project uses the JSONPlaceholder sample users endpoint:

`https://jsonplaceholder.typicode.com/users`

## Run the Tests

Execute the unit tests with:

```bash
python -m pytest etl_pipeline.py -v
```

The tests check that:

- Text fields are trimmed and email addresses are converted to lowercase.
- Duplicate IDs are removed.
- Empty input returns an empty DataFrame with the expected columns.

## Sample Output

```text
Starting ETL pipeline...
Extracted 10 records.
Transformed 10 records.
Saved CSV file to: data/users.csv

Preview:
 id             name  username                     email
  1    Leanne Graham      Bret         sincere@april.biz
  2     Ervin Howell Antonette         shanna@melissa.tv
  3 Clementine Bauch  Samantha        nathan@yesenia.net
  4 Patricia Lebsack  Karianne julianne.oconner@kory.org
  5 Chelsey Dietrich    Kamren  lucio_hettinger@annie.ca

ETL pipeline completed successfully.
```

## Future Improvements

- Add logging instead of relying only on printed messages.
- Add retry handling for temporary API failures.
- Add data validation for malformed or incomplete API records.
- Support command-line arguments for choosing the API endpoint and output path.

## License

This project is intended for learning and educational purposes.
