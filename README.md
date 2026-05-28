# Weather CLI

> A terminal weather tool — give it a city, get current conditions + a multi-day forecast in pretty colours.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Requests](https://img.shields.io/badge/HTTP-requests-blue)
![Rich](https://img.shields.io/badge/UI-rich-purple)
![OpenWeather](https://img.shields.io/badge/API-OpenWeather-orange)

A small but polished command-line tool built in Python that fetches live weather data from the OpenWeather API and renders it in the terminal with [rich](https://github.com/Textualize/rich). Includes on-disk response caching so repeated calls don't hit the API.

---

## Demo

> _Record a 10-second GIF of running the command and replace the line below._

![demo](docs/demo.gif)

---

## Features

- 🌡️ **Current weather** — temperature, feels-like, humidity, wind for any city worldwide
- 📅 **Multi-day forecast** — up to 5 days of highs/lows + conditions
- 💾 **On-disk caching** — responses cached for 10 minutes in `~/.weather_cache.json` to avoid hammering the API
- ❌ **Graceful errors** — clean messages for unknown cities, bad API keys, and network failures
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

---

## Setup

### 1. Clone

```bash
git clone https://github.com/narasimharao2743/weather-cli.git
cd weather-cli
```

### 2. Virtual environment + dependencies

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Get a free OpenWeather API key

1. Sign up at [openweathermap.org/users/sign_up](https://openweathermap.org/users/sign_up)
2. Copy your API key from the **API keys** tab
3. _New keys can take up to 2 hours to activate._

### 4. Create a `.env` file

```bash
cp .env.example .env
# then edit .env and paste your key
```

```
OPENWEATHER_API_KEY=your_api_key_here
```

---

## Usage

```bash
# Current weather
python weather.py Bangalore

# Multi-word city
python weather.py "New York"

# Add a 3-day forecast
python weather.py Bangalore --days 3

# Up to 5-day forecast
python weather.py Mumbai -d 5
```

### `--help`

```
usage: weather [-h] [-d {0,1,2,3,4,5}] city [city ...]

Get current weather and forecast for any city.

positional arguments:
  city                  City name (e.g. "Bangalore" or "New York")

options:
  -h, --help            show this help message and exit
  -d {0,1,2,3,4,5}, --days {0,1,2,3,4,5}
                        Show an N-day forecast in addition to current weather (0-5, default: 0)
```

---

## How It Works

1. **CLI parsing** — `argparse` turns terminal arguments into a city + days value
2. **API client** (`api_client.py`) — wraps the OpenWeather REST endpoints (`/weather` and `/forecast`), reads the API key from `.env`, handles HTTP errors with custom exceptions
3. **Caching** — every successful response is written to `~/.weather_cache.json` with a timestamp. Repeat queries within 10 minutes return the cached copy instead of calling the API again
4. **Formatter** (`formatter.py`) — uses `rich.Panel` for the current-weather card and `rich.Table` for the forecast grid

---

## Project Structure

```
weather-cli/
├── weather.py          # CLI entry point (argparse + orchestration)
├── api_client.py       # OpenWeather API wrapper + caching
├── formatter.py        # Pretty terminal output via rich
├── requirements.txt    # Python dependencies
├── .env.example        # Template for your API key
├── .env                # Your real key (gitignored)
├── .gitignore
└── README.md
```

---

## Engineering Decisions

| Decision | Choice | Why |
|---|---|---|
| **Cache TTL** | 10 minutes | Weather doesn't change minute-to-minute, but a stale forecast > 10 min old feels wrong |
| **Cache location** | `~/.weather_cache.json` (home dir, not repo) | Same machine, multiple project checkouts share the cache; doesn't leak into git |
| **Custom exceptions** | `CityNotFoundError`, `WeatherAPIError` | Lets `weather.py` distinguish "user typo" (exit 1) from "API down" (exit 2) for shell scripts |
| **`units=metric` hardcoded** | Yes | Simpler. Adding `--units` later is a one-line tweak |
| **Forecast aggregation** | Group 3-hourly entries by date, show min/max + mid-day conditions | OpenWeather free tier doesn't provide a daily summary endpoint, so we synthesise it from the 5-day/3-hour data |

---

## Roadmap

- [ ] `--units imperial|metric` flag
- [ ] Bulk mode: `weather Bangalore Mumbai Delhi` in one table
- [ ] Config file at `~/.weather.yaml` with a default city
- [ ] Package and publish to PyPI as `pip install rao-weather`
- [ ] `--alert "rain"` flag with exit code 1 if rain in forecast (useful in cron jobs)

---

## Author

**Narasimharao Bhavirisetty** — Python backend & GenAI engineer.

- 🌐 Portfolio: [narasimharao2743.github.io](https://narasimharao2743.github.io)
- 💼 LinkedIn: [linkedin.com/in/narasimharao-bhavirisetty-0526891b0](https://linkedin.com/in/narasimharao-bhavirisetty-0526891b0)
