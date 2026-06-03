# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the script

```bash
python main.py
```

Requires a `.env` file with the following variables:

```
STOCK_API_KEY=     # Alpha Vantage API key
NEWS_API_KEY=      # NewsAPI.org API key
MY_EMAIL=          # Gmail address used to send emails
PASSWORD=          # Gmail app password
```

## Architecture

Single-file script (`main.py`) with three sequential stages:

1. **Stock price fetch** — calls Alpha Vantage `TIME_SERIES_DAILY` for `TSLA`, extracts the two most recent closing prices, and computes the percentage difference.
2. **News fetch** — if any price difference exists, queries NewsAPI for articles with `TESLA Inc` in the title and takes the top 3.
3. **Email dispatch** — sends each article (headline + brief) as a separate Gmail email via `smtplib` with STARTTLS to `jkayabas@gmail.com`.

There is commented-out Twilio SMS code as an alternative delivery mechanism — the intent was to support SMS but Gmail was used instead.

## Dependencies

Managed via pip. Key packages: `requests`, `python-dotenv`. Install with:

```bash
pip install requests python-dotenv
```
