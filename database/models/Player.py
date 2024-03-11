class Players:
    def __init__(self):
        self.players = []

    @property
    def get_player(self,id):
        for player in self.players:
            if player.id == id:
                return player

    @property
    def add_player(self,player):
        self.players.append(player)



class Player:
  def __init__(self, params, position,image):
    self.image = image
    self.position = position
    self.id = params.get('id')
    self.status = params.get('status')
    self.name = params.get('web_name')
    self.news = params.get('news')
    self.team_id = params.get('team')  # Connect to Team class using params
    self.points_per_game = params.get('points_per_game')
    self.total_points = params.get('total_points')
    self.clean_sheets = params.get('clean_sheets')
    self.assists = params.get('assists')
    self.goals_scored = params.get('goals_scored')
    self.yellow_cards = params.get('yellow_cards')
    self.red_cards = params.get('red_cards')
    self.expected_goals_total = float(params.get('expected_goals', 0))
    self.expected_assists_total = float(params.get('expected_assists', 0))
    self.expected_goals_conceded_total = float(params.get('expected_goals_conceded', 0))
    self.saves = int(params.get('saves', 0))
