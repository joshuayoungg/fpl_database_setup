class Teams:
    def __init__(self):
        self.teams = []

    def get_team(self,id):
        for team in self.teams:
            if team.id == id:
                return team

    def add_team(self,team):
        self.teams.append(team)
    
    def add_player_to_team(self,player,team_id):
        team = self.get_team(team_id)
        team.players.append(player)

    def get_teams(self):
        return self.teams

class Team:
    def __init__(self,params):
        self.name_abb = params.get('short_name')
        self.id = params.get('id')
        self.name = params.get('name')
        self.strength = params.get('strength')
        self.strength_overall_home = params.get('strength_overall_home')
        self.strength_overall_away = params.get('strength_overall_away')
        self.players = []
        self.past_fixtures = []
        self.goals = 0
        self.saves = 0
        self.expected_goals = 0
        self.expected_goals_conceded = 0
        self.expected_assists = 0
        self.median_expected_goals = 0
        self.total_expected_goals = 0
        self.median_expected_assists = 0
        self.total_expected_assists = 0
    
    
    # @property
    # def add_team_stats(self, params):
    #     self.goals = params.get('goals',0)
    #     self.saves = params.get('saves',0)
    #     self.expected_goals = params.get('expected_goals',0)
    #     self.expected_goals_conceded = params.get('expected_goals_conceded',0)
    #     self.expected_assists = params.get('expected_assists',0)
        
    #     self.median_expected_goals = params.get('median_expected_goals',0)
    #     self.total_expected_goals = params.get('total_expected_goals',0)
    #     self.median_expected_assists = params.get('median_expected_assists',0)
    #     self.total_expected_assists = params.get('total_expected_assists',0)