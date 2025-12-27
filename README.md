# Axon Report Fetcher

Fetch Axon (AppLovin) advertiser reports and export to CSV.

## Usage

```bash
python3 axon_report.py --api-key YOUR_API_KEY
```

### Options

| Argument | Description | Default |
|----------|-------------|---------|
| `--api-key` | Axon API key *(required)* | - |
| `--start` | Start date (YYYY-MM-DD) | `2025-12-24` |
| `--end` | End date (YYYY-MM-DD or `now`) | `now` |
| `--output`, `-o` | Output CSV file path | `axon_report.csv` |

### Examples

```bash
# Basic usage
python3 axon_report.py --api-key YOUR_API_KEY

# Custom date range
python3 axon_report.py --api-key YOUR_API_KEY --start 2025-12-24 --end 2025-12-27

# Custom output file
python3 axon_report.py --api-key YOUR_API_KEY -o my_report.csv
```

## Output Format

CSV with columns: `Date`, `campaign_name`, `campaign_id`, `country`, `spend`

## API Documentation

https://support.axon.ai/en/growth/promoting-your-apps/api/reporting-api/
