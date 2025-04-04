# Football Match Tracker

A web application that displays football matches from major European leagues using the football-data.org API.


## Features
- Python API handle
- Live match tracking
- Multiple league support - TOP 5 (Premier League, La Liga, Bundesliga, Serie A, Ligue 1)
- Filter matches by:
  - Live matches
  - Upcoming matches
    - Today's matches
    - Tomorrow's matches
- Dark/Light mode toggle
- Responsive design - Made with AI!!
- Modern UI with league icons and team crests

## Setup
1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `config.py` file with your API key:
```python
FOOTBALL_DATA_API_KEY = "your_api_key_here"
```
4. Run the application:
```bash
python api_example.py
```

## API Key
Get your API key from [football-data.org](https://www.football-data.org/) 
10 request per min