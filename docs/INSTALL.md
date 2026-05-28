# Installation Guide

Step-by-step instructions to install and use `weather-enquire` from scratch on a fresh machine. Works on Windows, macOS, and Linux.

> If you only want the short version: `pip install weather-enquire` → set `OPENWEATHER_API_KEY` env var → run `weather-enquire <city>`.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Get an OpenWeather API key](#step-1--get-an-openweather-api-key)
3. [Install the tool](#step-2--install-weather-enquire)
4. [Save your API key permanently](#step-3--save-your-api-key-permanently)
5. [Use it](#step-4--use-it)
6. [Update / uninstall](#updating-and-uninstalling)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

| Requirement | Check | How to install if missing |
|---|---|---|
| **Python 3.10 or newer** | `python --version` | Download from [python.org/downloads](https://www.python.org/downloads/). On Windows, tick **"Add Python to PATH"** during install. |
| **pip** (usually bundled with Python) | `pip --version` | If missing on Linux: `sudo apt install python3-pip` (Debian/Ubuntu) |
| **A free OpenWeather account** | [openweathermap.org](https://openweathermap.org) | See Step 1 below |
| **A modern terminal** | — | On Windows 11, **Windows Terminal** is the default and renders emojis/colours correctly. On macOS/Linux, the default Terminal works. |

---

## Step 1 — Get an OpenWeather API key

The CLI uses the OpenWeather API to fetch live weather data. The free tier gives you 60 calls/minute, 1 million calls/month — more than enough for personal use.

1. Go to **<https://openweathermap.org/users/sign_up>**
2. Sign up with your email, password, and a username
3. Verify your email (check inbox/spam)
4. Log in → click your username (top-right) → **My API keys**
5. Copy the **default key** that was auto-created for you (or click **Generate** to create a new one)

⚠️ **New keys can take up to 2 hours to activate.** Once you have it, you can test it directly in your browser by visiting:

```
https://api.openweathermap.org/data/2.5/weather?q=Bangalore&appid=YOUR_KEY
```

- If you see JSON with `"main":{"temp":...}` → key is active ✅
- If you see `{"cod":401, "message":"Invalid API key..."}` → still activating, wait 30 minutes and retry ⏳

---

## Step 2 — Install `weather-enquire`

You have two options. **`pipx` is recommended** for CLI tools because it installs each tool in its own isolated environment.

### Option A — Install with `pipx` (recommended)

```bash
# Install pipx itself (one-time)
python -m pip install --user pipx
python -m pipx ensurepath
```

**Close and reopen your terminal** so the new PATH is picked up. Then:

```bash
pipx install weather-enquire
```

### Option B — Install with plain `pip`

If you don't want to bother with pipx:

```bash
pip install --user weather-enquire
```

### Verify it's installed

```bash
weather-enquire --help
```

You should see the usage/help text. If you get `command not found` or `not recognized`, see the [Troubleshooting](#troubleshooting) section.

---

## Step 3 — Save your API key permanently

So you don't have to set it every time you open a new terminal.

### Windows (PowerShell)

```powershell
[System.Environment]::SetEnvironmentVariable("OPENWEATHER_API_KEY", "YOUR_KEY_HERE", "User")
```

**You must close all PowerShell windows and open a fresh one** for the change to take effect.

Verify:
```powershell
$env:OPENWEATHER_API_KEY
```

### macOS / Linux (bash)

Add to `~/.bashrc`:

```bash
echo 'export OPENWEATHER_API_KEY="YOUR_KEY_HERE"' >> ~/.bashrc
source ~/.bashrc
```

### macOS / Linux (zsh, default on modern macOS)

Add to `~/.zshrc`:

```bash
echo 'export OPENWEATHER_API_KEY="YOUR_KEY_HERE"' >> ~/.zshrc
source ~/.zshrc
```

Verify on any Unix:
```bash
echo $OPENWEATHER_API_KEY
```

You should see your key printed back.

---

## Step 4 — Use it

From **any folder**, in any terminal:

### Current weather
```bash
weather-enquire Bangalore
```

### With a 3-day forecast
```bash
weather-enquire Bangalore --days 3
```

### Multi-word city (must be quoted)
```bash
weather-enquire "New York"
```

### Short flag form
```bash
weather-enquire Mumbai -d 5
```

### See all options
```bash
weather-enquire --help
```

### Expected output

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

## Updating and uninstalling

### Update to the latest version

If you installed with `pipx`:
```bash
pipx upgrade weather-enquire
```

If you installed with `pip`:
```bash
pip install --upgrade weather-enquire
```

### Uninstall

If you installed with `pipx`:
```bash
pipx uninstall weather-enquire
```

If you installed with `pip`:
```bash
pip uninstall weather-enquire
```

Optionally remove the API key:

```powershell
# Windows PowerShell
[System.Environment]::SetEnvironmentVariable("OPENWEATHER_API_KEY", $null, "User")
```

```bash
# macOS/Linux — delete the export line from ~/.bashrc or ~/.zshrc
```

And the on-disk cache (safe to delete anytime):

```bash
# Windows
Remove-Item "$HOME\.weather_cache.json"

# macOS/Linux
rm ~/.weather_cache.json
```

---

## Troubleshooting

### `weather-enquire is not recognized` (Windows) / `command not found` (Mac/Linux)

The install put the executable in a folder that's not on your PATH.

**Quick fix on any OS:** close and reopen the terminal. PATH changes only take effect on shell startup.

**If still not found:** find where it landed:

```bash
# Try these one by one
where weather-enquire             # Windows
which weather-enquire             # macOS/Linux
python -m pip show -f weather-enquire | grep -i Location
```

The output will be a folder like:
- Windows: `C:\Users\<you>\.local\bin\` or `C:\Users\<you>\AppData\Roaming\Python\Python3xx\Scripts\`
- macOS/Linux: `~/.local/bin/` or `/usr/local/bin/`

Add that folder to your PATH (Step 3-style env var) and reopen your terminal.

---

### `OPENWEATHER_API_KEY is not set. Add it to your .env file.`

The CLI couldn't find your API key. Two possible causes:

1. You set the env var but didn't reopen the terminal → close and reopen, then verify with `echo $env:OPENWEATHER_API_KEY` (Windows) or `echo $OPENWEATHER_API_KEY` (Unix).
2. You set it in the wrong shell config file → on macOS the default shell is zsh, so use `~/.zshrc`. On Linux, usually `~/.bashrc`.

---

### `Invalid API key. New keys can take up to 2 hours to activate.`

OpenWeather hasn't enabled your new key yet. Test it directly in your browser:

```
https://api.openweathermap.org/data/2.5/weather?q=Bangalore&appid=YOUR_KEY
```

- If you see weather JSON → key is active; restart your terminal and retry the CLI.
- If you see `{"cod":401, ...}` → still activating; wait 30 minutes and try again.

---

### `City not found: <name>`

The OpenWeather API doesn't recognise that name. Try:
- The English name (`Bengaluru` and `Bangalore` both work)
- The full name without abbreviations (`Saint Petersburg`, not `St. Petersburg`)
- Add a country code with a comma: `weather-enquire "London,GB"` vs `weather-enquire "London,US"`

---

### Pretty colours / emojis don't render

You're using an old terminal that doesn't support UTF-8 or ANSI colour codes.

- **Windows:** install **Windows Terminal** from the Microsoft Store (it's the default in Windows 11)
- **macOS:** the default Terminal app supports both. If you're using something exotic, try iTerm2.
- **Linux:** any modern terminal emulator (GNOME Terminal, Konsole, Alacritty, kitty) works fine

---

## Reference links

| Resource | URL |
|---|---|
| 📦 PyPI package | <https://pypi.org/project/weather-enquire/> |
| 🐙 Source code | <https://github.com/narasimharao2743/weather-cli> |
| 🌦️ OpenWeather API docs | <https://openweathermap.org/api> |
| 🐍 pipx documentation | <https://pipx.pypa.io> |
| ❓ Report an issue | <https://github.com/narasimharao2743/weather-cli/issues> |
