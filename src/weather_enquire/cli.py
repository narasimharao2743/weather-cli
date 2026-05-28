"""Command-line weather tool — current conditions + multi-day forecast."""

import argparse
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from dotenv import load_dotenv

from .api_client import (
    CityNotFoundError,
    WeatherAPIError,
    get_current_weather,
    get_forecast,
)
from .formatter import render_current, render_error, render_forecast


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="weather-enquire",
        description="Get current weather and forecast for any city.",
    )
    parser.add_argument(
        "city",
        nargs="+",
        help='City name (e.g. "Bangalore" or "New York")',
    )
    parser.add_argument(
        "-d", "--days",
        type=int,
        default=0,
        choices=range(0, 6),
        help="Show an N-day forecast in addition to current weather (0-5, default: 0)",
    )
    return parser.parse_args()


def main() -> int:
    load_dotenv()
    args = parse_args()
    city = " ".join(args.city)

    try:
        current = get_current_weather(city)
        render_current(current)

        if args.days > 0:
            forecast = get_forecast(city)
            render_forecast(forecast, args.days)

    except CityNotFoundError as exc:
        render_error(str(exc))
        return 1
    except WeatherAPIError as exc:
        render_error(str(exc))
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
