"""Pretty-print weather data to the terminal using rich."""

from collections import defaultdict
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


def _weather_icon(main: str) -> str:
    icons = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Drizzle": "🌦️",
        "Thunderstorm": "⛈️",
        "Snow": "❄️",
        "Mist": "🌫️",
        "Fog": "🌫️",
        "Haze": "🌫️",
    }
    return icons.get(main, "🌡️")


def render_current(data: dict) -> None:
    city = data["name"]
    country = data["sys"]["country"]
    main = data["weather"][0]["main"]
    description = data["weather"][0]["description"].title()
    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    wind_kph = data["wind"]["speed"] * 3.6  # API returns m/s

    body = Text()
    body.append(f"{_weather_icon(main)}  {description}\n\n", style="bold")
    body.append(f"🌡️  Temperature   {temp:.1f}°C  (feels like {feels:.1f}°C)\n")
    body.append(f"💧 Humidity      {humidity}%\n")
    body.append(f"🌬️  Wind          {wind_kph:.1f} km/h\n")

    console.print(
        Panel(body, title=f"📍 {city}, {country}", border_style="cyan", expand=False)
    )


def render_forecast(data: dict, days: int) -> None:
    by_day: dict[str, list[dict]] = defaultdict(list)
    for entry in data["list"]:
        date = datetime.fromtimestamp(entry["dt"]).strftime("%Y-%m-%d")
        by_day[date].append(entry)

    table = Table(
        title=f"📅 Next {days}-day forecast",
        border_style="cyan",
        title_style="bold",
    )
    table.add_column("Date", style="bold")
    table.add_column("Day", style="dim")
    table.add_column("High", justify="right", style="red")
    table.add_column("Low", justify="right", style="blue")
    table.add_column("Conditions")

    for date in sorted(by_day.keys())[:days]:
        entries = by_day[date]
        temps = [e["main"]["temp"] for e in entries]
        midday = min(entries, key=lambda e: abs(datetime.fromtimestamp(e["dt"]).hour - 12))
        condition = midday["weather"][0]["description"].title()
        icon = _weather_icon(midday["weather"][0]["main"])
        day_name = datetime.strptime(date, "%Y-%m-%d").strftime("%a")
        table.add_row(
            date, day_name,
            f"{max(temps):.0f}°C", f"{min(temps):.0f}°C",
            f"{icon} {condition}",
        )

    console.print(table)


def render_error(message: str) -> None:
    console.print(f"[bold red]✗[/bold red] {message}")
