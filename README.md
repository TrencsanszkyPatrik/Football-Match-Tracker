# Football Match Tracker

A Flask-based web application for tracking football matches and league standings.

## Features

- View upcoming and live matches from top leagues
- Filter matches by status (Live, Today, Tomorrow)
- View detailed match statistics
- League standings table with key statistics
- Dark/Light theme support
- Responsive design for all devices

## Supported Leagues

- Premier League
- La Liga
- Bundesliga
- Serie A
- Ligue 1

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `config.py` file with your API key:
```python
FOOTBALL_DATA_API_KEY = 'your_api_key_here'
```
4. Run the application:
```bash
python api_example.py
```

## API

This application uses the Football-Data.org API. You'll need to:
1. Register at [Football-Data.org](https://www.football-data.org/)
2. Get your API key
3. Add it to the `config.py` file

## Contributing

Feel free to submit issues and enhancement requests!