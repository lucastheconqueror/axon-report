#!/usr/bin/env python3
"""
Axon (AppLovin) Advertiser Report Fetcher

Fetches advertiser reports from Axon's Reporting API and exports to CSV.
Documentation: https://support.axon.ai/en/growth/promoting-your-apps/api/reporting-api/

Usage:
    python axon_report.py --api-key YOUR_API_KEY
    python axon_report.py --api-key YOUR_API_KEY --start 2025-12-24 --end now --output report.csv
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError


# Base URL for Axon Reporting API
BASE_URL = "https://r.applovin.com/report"

# Column mapping: API column name -> CSV header name
COLUMN_MAPPING = {
    "day": "Date",
    "campaign": "campaign_name",
    "campaign_id_external": "campaign_id",
    "country": "country",
    "cost": "spend",
}


def fetch_report(api_key: str, start_date: str, end_date: str) -> list[dict]:
    """
    Fetch advertiser report from Axon API.
    
    Args:
        api_key: Axon API key
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format or 'now'
    
    Returns:
        List of report data dictionaries
    """
    # Build query parameters
    params = {
        "api_key": api_key,
        "start": start_date,
        "end": end_date,
        "columns": ",".join(COLUMN_MAPPING.keys()),
        "format": "json",
        "report_type": "advertiser",
    }
    
    url = f"{BASE_URL}?{urlencode(params)}"
    
    print(f"Fetching report from {start_date} to {end_date}...")
    
    try:
        request = Request(url, headers={"User-Agent": "AxonReportFetcher/1.0"})
        with urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
            
            if isinstance(data, dict) and "error" in data:
                raise ValueError(f"API Error: {data['error']}")
            
            if isinstance(data, dict) and "results" in data:
                return data["results"]
            
            if isinstance(data, list):
                return data
            
            raise ValueError(f"Unexpected response format: {type(data)}")
            
    except HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        raise RuntimeError(f"HTTP Error {e.code}: {e.reason}\n{error_body}")
    except URLError as e:
        raise RuntimeError(f"URL Error: {e.reason}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse JSON response: {e}")


def export_to_csv(data: list[dict], output_path: str) -> None:
    """
    Export report data to CSV file.
    
    Args:
        data: List of report data dictionaries
        output_path: Path to output CSV file
    """
    if not data:
        print("Warning: No data to export.")
        return
    
    # CSV headers in desired order
    csv_headers = list(COLUMN_MAPPING.values())
    
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)
        
        for row in data:
            csv_row = [
                row.get("day", ""),
                row.get("campaign", ""),
                row.get("campaign_id_external", ""),
                row.get("country", ""),
                row.get("cost", ""),
            ]
            writer.writerow(csv_row)
    
    print(f"Exported {len(data)} rows to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch Axon (AppLovin) advertiser reports and export to CSV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python axon_report.py --api-key YOUR_API_KEY
    python axon_report.py --api-key YOUR_API_KEY --start 2025-12-24 --end now
    python axon_report.py --api-key YOUR_API_KEY --output my_report.csv
        """,
    )
    
    parser.add_argument(
        "--api-key",
        required=True,
        help="Axon API key (get from https://ads.axon.ai/account/api-keys)",
    )
    parser.add_argument(
        "--start",
        default="2025-12-24",
        help="Start date in YYYY-MM-DD format (default: 2025-12-24)",
    )
    parser.add_argument(
        "--end",
        default="now",
        help="End date in YYYY-MM-DD format or 'now' (default: now)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="axon_report.csv",
        help="Output CSV file path (default: axon_report.csv)",
    )
    
    args = parser.parse_args()
    
    # Validate dates
    if args.start != "now":
        try:
            datetime.strptime(args.start, "%Y-%m-%d")
        except ValueError:
            print(f"Error: Invalid start date format: {args.start}. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
    
    if args.end != "now":
        try:
            datetime.strptime(args.end, "%Y-%m-%d")
        except ValueError:
            print(f"Error: Invalid end date format: {args.end}. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
    
    try:
        # Fetch report data
        data = fetch_report(args.api_key, args.start, args.end)
        
        # Export to CSV
        export_to_csv(data, args.output)
        
        print("Done!")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
