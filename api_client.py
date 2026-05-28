"""OpenWeather API client with on-disk caching."""

import json
import os
import time
from pathlib import Path

import requests

BASE_URL = "https://api.openweathermap.org/data/2.5"
CACHE_PATH = Path.home() / ".weather_cache.json"
CACHE_TTL_SECONDS = 600  # 10 minutes


class WeatherAPIError(Exception):
    """Raised for any error talking to the OpenWeather API."""


class CityNotFoundError(WeatherAPIError):
    """Raised when the API returns 404 for an unknown city."""


def _load_cache() -> dict:
    if not CACHE_PATH.exists():
        return {}
    try:
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _save_cache(cache: dict) -> None:
    try:
        CACHE_PATH.write_text(json.dumps(cache), encoding="utf-8")
    except OSError:
        pass


def _get_cached(key: str) -> dict | None:
    cache = _load_cache()
    entry = cache.get(key)
    if not entry:
        return None
    if time.time() - entry["fetched_at"] > CACHE_TTL_SECONDS:
        return None
    return entry["data"]


def _set_cached(key: str, data: dict) -> None:
    cache = _load_cache()
    cache[key] = {"fetched_at": time.time(), "data": data}
    _save_cache(cache)


def _call(endpoint: str, params: dict) -> dict:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise WeatherAPIError(
            "OPENWEATHER_API_KEY is not set. Add it to your .env file."
        )

    params = {**params, "appid": api_key, "units": "metric"}

    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=10)
    except requests.RequestException as exc:
        raise WeatherAPIError(f"Network error: {exc}") from exc

    if response.status_code == 404:
        raise CityNotFoundError(f"City not found: {params.get('q')}")
    if response.status_code == 401:
        raise WeatherAPIError(
            "Invalid API key. New keys can take up to 2 hours to activate."
        )
    if response.status_code != 200:
        raise WeatherAPIError(
            f"API returned {response.status_code}: {response.text[:200]}"
        )

    return response.json()


def get_current_weather(city: str) -> dict:
    cache_key = f"current:{city.lower()}"
    cached = _get_cached(cache_key)
    if cached is not None:
        return cached

    data = _call("weather", {"q": city})
    _set_cached(cache_key, data)
    return data


def get_forecast(city: str) -> dict:
    cache_key = f"forecast:{city.lower()}"
    cached = _get_cached(cache_key)
    if cached is not None:
        return cached

    data = _call("forecast", {"q": city})
    _set_cached(cache_key, data)
    return data
