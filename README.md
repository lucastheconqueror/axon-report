# Axon Report Fetcher

Fetch Axon (AppLovin) advertiser reports and display them in the terminal or export to CSV.

## Usage

```bash
# Print formatted table to terminal (default)
python3 axon_report.py --api-key YOUR_API_KEY

# Export to CSV file
python3 axon_report.py --api-key YOUR_API_KEY -o report.csv
```

### Options

| Argument | Description | Default |
|----------|-------------|---------|
| `--api-key` | Axon API key *(required)* | - |
| `--start` | Start date (YYYY-MM-DD) | `2025-12-24` |
| `--end` | End date (YYYY-MM-DD or `now`) | `now` |
| `--output`, `-o` | Output CSV file path (disables terminal table) | `None` |

### Examples

```bash
# Basic usage (terminal table)
python3 axon_report.py --api-key YOUR_API_KEY

# Custom date range
python3 axon_report.py --api-key YOUR_API_KEY --start 2025-12-24 --end 2025-12-27

# Export to custom CSV file
python3 axon_report.py --api-key YOUR_API_KEY -o my_report.csv
```

## Output Format

- **Terminal**: A clean, formatted table showing Date, Campaign Name, Campaign ID, Country, and Spend.
- **CSV**: A file with headers: `Date`, `campaign_name`, `campaign_id`, `country`, `spend`

## API Documentation

https://support.axon.ai/en/growth/promoting-your-apps/api/reporting-api/
