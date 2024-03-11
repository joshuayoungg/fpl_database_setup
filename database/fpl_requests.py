import pandas as pd
import mongodb_script
from pprint import pprint

from models.Teams import Teams, Team
from models.Player import Players, Player
from models.Fixture import PastFixture, UpcomingFixture, Fixtures
from models.Stats import Stats, PlayerStats
from constants.constants import POSITIONS, element_summary, bootstrap_static
from security import safe_requests


player_to_image = {}


def pretty_print(element):
    pprint(element, indent=2, depth=1, compact=True)


def get_player_position(element_type):
    return POSITIONS[element_type]


def get_upcoming_fixtures(upcoming, team_id, fixtures):
    for data in upcoming:
        if (not data['kickoff_time']):
            continue
        upcoming_fixture = UpcomingFixture(data, team_id)
        fixtures.add_upcoming_fixtures(upcoming_fixture)


def get_past_fixtures(history, team_id, fixtures):
    for data in history:
        past_fixture = PastFixture(data, team_id)
        fixtures.add_past_fixtures(past_fixture)


def get_player_stats(history, stats, player_id):
    for data in history:
        player_stats = PlayerStats(data, player_id)
        stats.add_player_stats(player_stats)
    return stats


def get_fixtures_and_stats(player_id, team_id, fixtures, stats):
    response = safe_requests.get(
        element_summary+str(player_id), timeout=60).json()
    history = response['history']
    get_upcoming_fixtures(response['fixtures'], team_id, fixtures)
    get_past_fixtures(history, team_id, fixtures)
    stats = get_player_stats(history, stats, player_id)
    return stats


def add_to_mongo_db(items):
    mongodb_script.mongo_db_operations('add', items)


def get_from_mongo_db():
    return mongodb_script.mongo_db_operations('get')


def get_player_data(response, players, fixtures, stats):
    players_data = response['elements']
    for data in players_data:
        if data['status'] != 'u':
            try:
                player_image = player_to_image[data['id']]
            except Exception:
                player_image = 'Photo-Missing'
            position = get_player_position(data['element_type'])
            player = Player(data, position, player_image)
            get_fixtures_and_stats(player.id, player.team_id, fixtures, stats)
            players.add_player(player)


def get_team_data(response, teams):
    fpl_teams_data = response['teams']
    for data in fpl_teams_data:
        team = Team(data)
        teams.teams.append(team)


def load_images():
    df = pd.read_excel('players.xlsx', sheet_name=0).values.tolist()
    for data in df:
        player_to_image[data[0]] = data[3]


def convert_to_dict_list(obj):
    obj_dict = []
    for item in obj:
        obj_dict.append({attr: getattr(item, attr)
                        for attr in dir(item) if not attr.startswith('__')})
    return obj_dict

def convert_team_to_dict_list(teams):
    obj_dict = []
    for item in teams:

        team_dict = ({attr: getattr(item, attr)
                        for attr in dir(item) if not attr.startswith('__')})
        team_dict['players'] = [player.__dict__ for player in item.players]
        obj_dict.append(team_dict)
    return obj_dict


if __name__ == '__main__':
    response = safe_requests.get(bootstrap_static, timeout=60).json()
    load_images()
    teams = Teams()
    players = Players()
    fixtures = Fixtures()
    stats = Stats()
    get_team_data(response, teams)
    get_player_data(response, players, fixtures, stats)
    add_to_mongo_db([('teams', convert_to_dict_list(teams.teams)), ('players', convert_to_dict_list(players.players)), ('past_fixtures', convert_to_dict_list(fixtures.past_fixtures)),
                    ('upcoming_fixtures', convert_to_dict_list(fixtures.upcoming_fixtures)), ('stats', convert_to_dict_list(stats.player_stats))])
