# weather-enquire

> A terminal weather tool — give it a city, get current conditions + a multi-day forecast in pretty colours.

[![PyPI](https://img.shields.io/pypi/v/weather-enquire?logo=pypi&logoColor=white&color=3775A9)](https://pypi.org/project/weather-enquire/)
[![Python](https://img.shields.io/pypi/pyversions/weather-enquire?logo=python&logoColor=white)](https://pypi.org/project/weather-enquire/)
[![Downloads](https://static.pepy.tech/badge/weather-enquire)](https://pepy.tech/project/weather-enquire)
[![License](https://img.shields.io/pypi/l/weather-enquire)](LICENSE)

A small but polished command-line tool built in Python that fetches live weather data from the OpenWeather API and renders it in the terminal with [rich](https://github.com/Textualize/rich). Includes on-disk response caching so repeated calls don't hit the API.

---

## Demo

> _Record a 10-second GIF of running the command and replace the line below._

![demo](docs/demo.gif)

---

## Install

```bash
pip install weather-enquire
```

Then set your OpenWeather API key as an environment variable:

```bash
# Linux / Mac
export OPENWEATHER_API_KEY=your_api_key_here

# Windows PowerShell
$env:OPENWEATHER_API_KEY = "your_api_key_here"
```

Get a free API key at [openweathermap.org/users/sign_up](https://openweathermap.org/users/sign_up). New keys can take up to 2 hours to activate.

---

## Usage

```bash
# Current weather
weather-enquire Bangalore

# Multi-word city (quote it)
weather-enquire "New York"

# Add a 3-day forecast
weather-enquire Bangalore --days 3

# Up to 5-day forecast
weather-enquire Mumbai -d 5

# Help
weather-enquire --help
```

### Example output

```
┌────────────── 📍 Bengaluru, IN ───────────────┐
│ ☁️  Scattered Clouds                          │
│                                               │
│ 🌡️  Temperature   23.4°C  (feels like 24.0°C) │
│ 💧 Humidity      84%                          │
│ 🌬️  Wind          9.3 km/h                    │
└───────────────────────────────────────────────┘
                📅 Next 3-day forecast
┌────────────┬─────┬──────┬──────┬────────────────────┐
│ Date       │ Day │ High │  Low │ Conditions         │
├────────────┼─────┼──────┼──────┼────────────────────┤
│ 2026-05-28 │ Thu │ 23°C │ 23°C │ 🌧️ Light Rain      │
│ 2026-05-29 │ Fri │ 33°C │ 22°C │ ☁️ Overcast Clouds │
│ 2026-05-30 │ Sat │ 31°C │ 22°C │ ☁️ Overcast Clouds │
└────────────┴─────┴──────┴──────┴────────────────────┘
```

---

## Features

- 🌡️ **Current weather** — temperature, feels-like, humidity, wind for any city worldwide
- 📅 **Multi-day forecast** — up to 5 days of highs/lows + conditions
- 💾 **On-disk caching** — responses cached for 10 minutes in `~/.weather_cache.json` to avoid hammering the API
- ❌ **Graceful errors** — clean messages for unknown cities, bad API keys, and network failures (with proper exit codes)
- 🎨 **Pretty output** — colour-coded panels and tables via `rich`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| HTTP | `requests` |
| Pretty terminal output | `rich` |
| Environment | `python-dotenv` |
| Weather data | [OpenWeather API](https://openweathermap.org/api) (free tier) |
| Packaging | `pyproject.toml` + `setuptools` |

---

## How It Works

1. **CLI parsing** — `argparse` turns terminal arguments into a city + days value
2. **API client** (`api_client.py`) — wraps the OpenWeather REST endpoints (`/weather` and `/forecast`), reads the API key from the environment, handles HTTP errors with custom exceptions
3. **Caching** — every successful response is written to `~/.weather_cache.json` with a timestamp. Repeat queries within 10 minutes return the cached copy instead of calling the API again
4. **Formatter** (`formatter.py`) — uses `rich.Panel` for the current-weather card and `rich.Table` for the forecast grid

---

## Engineering Decisions

| Decision | Choice | Why |
|---|---|---|
| **Cache TTL** | 10 minutes | Weather doesn't change minute-to-minute, but a stale forecast > 10 min old feels wrong |
| **Cache location** | `~/.weather_cache.json` (home dir, not repo) | Same machine, multiple project checkouts share the cache; doesn't leak into git |
| **Custom exceptions** | `CityNotFoundError`, `WeatherAPIError` | Lets the CLI distinguish "user typo" (exit 1) from "API down" (exit 2) for shell scripts |
| **`units=metric` hardcoded** | Yes | Simpler. Adding `--units` later is a one-line tweak |
| **Forecast aggregation** | Group 3-hourly entries by date, show min/max + mid-day conditions | OpenWeather free tier doesn't provide a daily summary endpoint, so we synthesise it from the 5-day/3-hour data |
| **Package layout** | `src/weather_enquire/` | Standard PyPI src-layout — prevents accidentally importing from the working directory during development |

---

## Development (install from source)

```bash
git clone https://github.com/narasimharao2743/weather-cli.git
cd weather-cli

python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -e ".[dev]" || pip install -e .

# Set up your API key (.env file works for local dev)
cp .env.example .env
# then edit .env and paste your key

# Run
weather-enquire Bangalore --days 3
```

---

## Project Structure

```
weather-cli/
├── src/
│   └── weather_enquire/
│       ├── __init__.py       # package version
│       ├── cli.py            # argparse + main entry point
│       ├── api_client.py     # OpenWeather wrapper + caching
│       └── formatter.py      # rich rendering
├── pyproject.toml            # package metadata + dependencies
├── LICENSE                   # MIT
├── requirements.txt          # development dependencies
├── .env.example              # template for OPENWEATHER_API_KEY
├── .gitignore
└── README.md
```

---

## Roadmap

- [ ] `--units imperial|metric` flag
- [ ] Bulk mode: `weather-enquire Bangalore Mumbai Delhi` in one table
- [ ] Config file at `~/.weather.yaml` with a default city
- [ ] `--alert "rain"` flag with exit code 1 if rain in forecast (useful in cron jobs)
- [ ] Streaming output for `--watch` mode

---

## Author

**Narasimharao Bhavirisetty** — Python backend & GenAI engineer.

- 🌐 Portfolio: [narasimharao2743.github.io](https://narasimharao2743.github.io)
- 💼 LinkedIn: [linkedin.com/in/narasimharao-bhavirisetty-0526891b0](https://linkedin.com/in/narasimharao-bhavirisetty-0526891b0)
- 📦 PyPI: [pypi.org/project/weather-enquire](https://pypi.org/project/weather-enquire/)

If this project helped you, a ⭐ on the repo is appreciated.
