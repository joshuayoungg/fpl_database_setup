class Stats:
    def __init__(self):
        self.player_stats = []
    
    def add_player_stats(self, player_stats):
        self.player_stats.append(player_stats)


class PlayerStats:
    def __init__(self, params, team_id):
        self.team = team_id
        self.player_id = params.get('element')
        self.gameweek = params.get('round')
        self.opponent = params.get('opponent_team')
        self.total_points = params.get('total_points', 0)
        self.was_home = params.get('was_home') == 'true'
        self.kickoff_time = params.get('kickoff_time')
        self.minutes = params.get('minutes')
        self.goals_scored = params.get('goals_scored')
        self.assists = params.get('assists')
        self.clean_sheets = params.get('clean_sheets')
        self.goals_conceded = params.get('goals_conceded')
        self.own_goals = params.get('own_goals')
        self.penalties_saved = params.get('penalties_saved')
        self.penalties_missed = params.get('penalties_missed')
        self.yellow_cards = params.get('yellow_cards')
        self.red_cards = params.get('red_cards')
        self.saves = params.get('saves')
        self.bonus = params.get('bonus')
        self.expected_goals = float(params.get('expected_goals', 0.0))  # Default to 0.0
        self.expected_assists = float(params.get('expected_assists', 0.0))
        self.goals_conceded = params.get('goals_conceded',0)
        