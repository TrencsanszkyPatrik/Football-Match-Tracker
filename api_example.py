import requests
from config import FOOTBALL_DATA_API_KEY
from datetime import datetime, timedelta
from flask import Flask, render_template, request

app = Flask(__name__)

class FootballDataAPI:
    def __init__(self):
        self.base_url = "http://api.football-data.org/v4"
        self.headers = {
            'X-Auth-Token': FOOTBALL_DATA_API_KEY
        }
        self.leagues = {
            '2021': 'Premier League',
            '2014': 'La Liga',
            '2002': 'Bundesliga',
            '2019': 'Serie A',
            '2015': 'Ligue 1'
        }
        self.league_icons = {
            '2021': "https://media.api-sports.io/football/leagues/39.png",
            '2014': "https://media.api-sports.io/football/leagues/140.png",
            '2002': "https://media.api-sports.io/football/leagues/78.png",
            '2019': "https://media.api-sports.io/football/leagues/135.png",
            '2015': "https://media.api-sports.io/football/leagues/61.png"
        }

    def get_matches(self, competition_id, date_from, date_to):
        endpoint = f"{self.base_url}/competitions/{competition_id}/matches"
        params = {
            'dateFrom': date_from,
            'dateTo': date_to
        }
        response = requests.get(endpoint, headers=self.headers, params=params)
        return response.json()

    def get_match_details(self, match_id):
        endpoint = f"{self.base_url}/matches/{match_id}"
        response = requests.get(endpoint, headers=self.headers)
        return response.json()

def format_match(match):
    home_team = match['homeTeam']['name']
    away_team = match['awayTeam']['name']
    home_team_crest = match['homeTeam'].get('crest', '')
    away_team_crest = match['awayTeam'].get('crest', '')
    
    utc_date = datetime.strptime(match['utcDate'], "%Y-%m-%dT%H:%M:%SZ")
    local_date = utc_date + timedelta(hours=2)
    formatted_date = local_date.strftime("%Y-%m-%d %H:%M")
    
    match_data = {
        'id': match['id'],
        'date': formatted_date,
        'home_team': home_team,
        'away_team': away_team,
        'home_team_crest': home_team_crest,
        'away_team_crest': away_team_crest,
        'status': match['status'],
        'stage': match.get('stage', ''),
        'competition': match.get('competition', {}).get('name', ''),
        'venue': match.get('venue', ''),
        'referee': match.get('referees', [{}])[0].get('name', '') if match.get('referees') else '',
        'season': match.get('season', {}).get('currentMatchday', '')
    }
    
    if match['status'] == 'LIVE' or match['status'] == 'FINISHED':
        score = f"{match['score']['fullTime']['home']} - {match['score']['fullTime']['away']}"
        minute = match.get('minute', '')
        
        match_data.update({
            'score': score,
            'minute': minute,
            'home_score': match['score']['fullTime']['home'],
            'away_score': match['score']['fullTime']['away'],
            'half_time_score': f"{match['score']['halfTime']['home']} - {match['score']['halfTime']['away']}",
            'possession_home': match.get('statistics', []).get('ball_possession', {}).get('home', 0),
            'possession_away': match.get('statistics', []).get('ball_possession', {}).get('away', 0),
            'shots_home': match.get('statistics', []).get('shots', {}).get('home', 0),
            'shots_away': match.get('statistics', []).get('shots', {}).get('away', 0),
            'shots_on_target_home': match.get('statistics', []).get('shots_on_goal', {}).get('home', 0),
            'shots_on_target_away': match.get('statistics', []).get('shots_on_goal', {}).get('away', 0),
            'corners_home': match.get('statistics', []).get('corner_kicks', {}).get('home', 0),
            'corners_away': match.get('statistics', []).get('corner_kicks', {}).get('away', 0),
            'fouls_home': match.get('statistics', []).get('fouls', {}).get('home', 0),
            'fouls_away': match.get('statistics', []).get('fouls', {}).get('away', 0),
            'yellow_cards_home': match.get('statistics', []).get('yellow_cards', {}).get('home', 0),
            'yellow_cards_away': match.get('statistics', []).get('yellow_cards', {}).get('away', 0),
            'red_cards_home': match.get('statistics', []).get('red_cards', {}).get('home', 0),
            'red_cards_away': match.get('statistics', []).get('red_cards', {}).get('away', 0),
            'offsides_home': match.get('statistics', []).get('offsides', {}).get('home', 0),
            'offsides_away': match.get('statistics', []).get('offsides', {}).get('away', 0)
        })
        
    return match_data

@app.route('/')
def index():
    api = FootballDataAPI()
    selected_league = request.args.get('league', '2021')
    show_live = request.args.get('live', 'false') == 'true'
    show_today = request.args.get('today', 'false') == 'true'
    show_tomorrow = request.args.get('tomorrow', 'false') == 'true'
    dark_mode = request.args.get('dark_mode', 'false') == 'true'
    
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    
    matches = api.get_matches(selected_league, today, next_week)
    match_list = matches.get('matches', [])
    
    filtered_matches = []
    if match_list:
        for match in match_list:
            match_date = datetime.strptime(match['utcDate'], "%Y-%m-%dT%H:%M:%SZ")
            match_date = match_date.strftime("%Y-%m-%d")
            
            if show_live and match['status'] != 'LIVE':
                continue
            if show_today and match_date != today:
                continue
            if show_tomorrow and match_date != tomorrow:
                continue
                
            filtered_matches.append(format_match(match))
    
    return render_template('index.html', 
                         matches=filtered_matches,
                         leagues=api.leagues,
                         league_icons=api.league_icons,
                         selected_league=selected_league,
                         show_live=show_live,
                         show_today=show_today,
                         show_tomorrow=show_tomorrow,
                         dark_mode=dark_mode)

@app.route('/match/<int:match_id>')
def match_details(match_id):
    api = FootballDataAPI()
    dark_mode = request.args.get('dark_mode', 'false') == 'true'
    match_data = api.get_match_details(match_id)
    
    if match_data:
        match = format_match(match_data)
        return render_template('match_details.html',
                             match=match,
                             dark_mode=dark_mode)
    
    return "Match not found", 404

if __name__ == "__main__":
    app.run(debug=True)
