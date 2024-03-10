import requests
import pandas as pd
import database.mongodb_script as mongodb_script
from pprint import pprint

from .models.Teams import Teams, Team
from .models.Player import Players, Player
from .models.Fixture import PastFixture, UpcomingFixture, Fixtures
from .models.Stats import Stats, PlayerStats
from .constants.constants import BASE_URL,POSITIONS,TEAMS_ABB, element_summary, bootstrap_static


player_to_image = {}


def pretty_print(element):
    pprint(element, indent=2, depth=1, compact=True)


def get_player_position(element_type):
    return POSITIONS[element_type]


def get_upcoming_fixtures(upcoming, team_id, fixtures):
    for data in upcoming:
        if(not data['kickoff_time']):
            continue
        upcoming_fixture = UpcomingFixture(data, team_id)
        fixtures.add_upcoming_fixtures(upcoming_fixture)


def get_past_fixtures(history, team_id, fixtures):
    for data in history:
        past_fixture = PastFixture(data,team_id)
        fixtures.add_past_fixtures(past_fixture)


def get_player_stats(history, stats):
    for data in history:
        player_stats = PlayerStats(data)
        stats.add_player_stats(player_stats)
    return stats


def get_fixtures_data(player_id, team_id, fixtures, stats):
    response = requests.get(element_summary+str(player_id)).json()
    history = response['history']
    get_upcoming_fixtures(response['fixtures'], team_id, fixtures)
    get_past_fixtures(history, team_id, fixtures)
    stats = get_player_stats(history, stats)
    return stats

        
def add_to_mongo_db(items):
    mongodb_script.mongo_db_operations('add', items)

def get_from_mongo_db():
    return mongodb_script.mongo_db_operations('get')


def get_player_data(response,players,fixtures,stats):
    players_data = response['elements']
    for data in players_data:
        status = data['status']
        if status != 'u':
            player_image = player_to_image[data['id']]
            position = get_player_position(data['element_type'])
            player = Player(data,position,player_image)
            get_fixtures_data(player.id,player.team_id,fixtures, stats)
            players.add_player(player)

def get_team_data(response, teams):
    fpl_teams_data = response['teams']
    for data in fpl_teams_data:
        name_abb = TEAMS_ABB[data['id']]
        team = Team(data, name_abb)
        teams.teams.append(team)

def load_images():
    df = pd.read_excel('players.xlsx', sheet_name=0).values.tolist()
    for data in df:
        player_to_image[data[0]] = data[3]


if __name__ == '__main__':
    response = requests.get(bootstrap_static).json()
    load_images()
    teams = Teams()
    players = Players()
    fixtures = Fixtures()
    stats = Stats()
    get_team_data(response, teams)
    get_player_data(response,players,fixtures,stats)
    add_to_mongo_db([teams.teams, players.players, fixtures.past_fixtures, fixtures.upcoming_fixtures,stats.player_stats])
    # items = get_from_mongo_db()
    # get_gameweek_stats(items)
    # add_to_mongo_db([gameweek_stats])
