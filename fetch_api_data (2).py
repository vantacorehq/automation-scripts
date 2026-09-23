"""
fetch_api_data.py
------------------
Downloads data from a free public API (live currency exchange rates)
and saves the result to a JSON file with a timestamp.

How it works:
1. Send a GET request to a public exchange rate API
   (no signup or API key required).
2. Check that the API responded successfully.
3. Save the returned data to a JSON file, along with the request
   time and source - handy for logs/history.

Usage:
    python fetch_api_data.py
    python fetch_api_data.py --base EUR --output eur_rates.json

API: https://www.exchangerate-api.com/ (open endpoint, no key needed)
"""

import argparse
import json
import sys
from datetime import datetime, timezone

import requests

API_URL_TEMPLATE = "https://open.er-api.com/v6/latest/{base}"
REQUEST_TIMEOUT = 10  # seconds


def fetch_exchange_rates(base_currency: str) -> dict:
    """Requests current exchange rates relative to the base currency."""
    url = API_URL_TEMPLATE.format(base=base_currency.upper())
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    data = response.json()

    if data.get("result") != "success":
        raise ValueError(f"API returned an error: {data.get('error-type', 'unknown error')}")

    return data


def save_json(data: dict, output_path: str) -> None:
    """Saves the data to a JSON file, adding a timestamp and source."""
    payload = {
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "https://www.exchangerate-api.com/",
        "data": data,
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Downloads exchange rates from a public API and saves them to JSON.")
    parser.add_argument("--base", type=str, default="USD", help="Base currency, e.g. USD, EUR, UAH")
    parser.add_argument("--output", type=str, default="exchange_rates.json", help="Output JSON file name")
    args = parser.parse_args()

    print(f"Fetching exchange rates relative to {args.base.upper()}...")

    try:
        data = fetch_exchange_rates(args.base)
    except requests.RequestException as e:
        print(f"API request error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Data error: {e}", file=sys.stderr)
        sys.exit(1)

    save_json(data, args.output)

    rates_count = len(data.get("rates", {}))
    print(f"Done! Got {rates_count} exchange rates, saved to: {args.output}")


if __name__ == "__main__":
    main()
