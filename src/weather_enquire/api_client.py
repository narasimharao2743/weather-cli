"""OpenWeather API client with on-disk caching."""

import json
import os
import time
from pathlib import Path

import requests

BASE_URL = "https://api.openweathermap.org/data/2.5"
GEO_URL = "https://api.openweathermap.org/geo/1.0/direct"
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


def _api_key() -> str:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise WeatherAPIError(
            "OPENWEATHER_API_KEY is not set. Add it to your .env file."
        )
    return api_key


def _request(url: str, params: dict) -> requests.Response:
    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.RequestException as exc:
        raise WeatherAPIError(f"Network error: {exc}") from exc

    if response.status_code == 401:
        raise WeatherAPIError(
            "Invalid API key. New keys can take up to 2 hours to activate."
        )
    return response


def _geocode(city: str) -> dict:
    """Resolve a city name to {lat, lon, name} via the Geocoding API.

    The geocoding database is far larger than the legacy /weather?q= city
    list, so smaller towns that 404 on the old endpoint resolve here. We also
    keep the geocoder's city name, which is cleaner than the weather station
    name the coordinate endpoint returns (e.g. "Bengaluru", not "Kanija Bhavan").
    """
    cache_key = f"geo:{city.lower()}"
    cached = _get_cached(cache_key)
    if cached is not None:
        return cached

    response = _request(GEO_URL, {"q": city, "limit": 1, "appid": _api_key()})
    if response.status_code != 200:
        raise WeatherAPIError(
            f"Geocoding API returned {response.status_code}: {response.text[:200]}"
        )

    results = response.json()
    if not results:
        raise CityNotFoundError(f"City not found: {city}")

    place = {
        "lat": results[0]["lat"],
        "lon": results[0]["lon"],
        "name": results[0]["name"],
    }
    _set_cached(cache_key, place)
    return place


def _call(endpoint: str, lat: float, lon: float) -> dict:
    params = {
        "lat": lat,
        "lon": lon,
        "appid": _api_key(),
        "units": "metric",
    }
    response = _request(f"{BASE_URL}/{endpoint}", params)
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

    place = _geocode(city)
    data = _call("weather", place["lat"], place["lon"])
    # Prefer the geocoder's city name over the weather station name.
    data["name"] = place["name"]
    _set_cached(cache_key, data)
    return data


def get_forecast(city: str) -> dict:
    cache_key = f"forecast:{city.lower()}"
    cached = _get_cached(cache_key)
    if cached is not None:
        return cached

    place = _geocode(city)
    data = _call("forecast", place["lat"], place["lon"])
    _set_cached(cache_key, data)
    return data
