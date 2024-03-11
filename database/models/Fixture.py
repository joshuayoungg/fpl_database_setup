class Fixtures:
    def __init__(self):
        self.past_fixtures = []
        self.upcoming_fixtures = []

    def get_past_fixture(self,key):
        for fixture in self.past_fixtures:
            if fixture.fixture_key == key:
                return True
        return False
    
    def get_upcoming_fixture(self,key):
        for fixture in self.upcoming_fixtures:
            if fixture.fixture_key == key:
                return True
        return False
    
    def add_past_fixtures(self,past_fixture):
        if is_added := self.get_past_fixture(past_fixture.fixture_key):
            return
        self.past_fixtures.append(past_fixture)
    
    def add_upcoming_fixtures(self,upcoming_fixture):
        if is_added := self.get_upcoming_fixture(upcoming_fixture.fixture_key):
            return
        self.upcoming_fixtures.append(upcoming_fixture)



class PastFixture():
    def __init__(self, params, team_id):
        self.team = team_id
        self.gameweek = params.get('round')
        self.kickoff_time = params.get('kickoff_time')
        self.was_home = params.get('was_home')
        self.opponent_team = params.get('opponent_team')
        self.home_team_score = params.get('team_h_score')
        self.away_team_score = params.get('team_a_score')
        self.fixture_key = str(self.team)+str(self.kickoff_time) if self.was_home else str(self.opponent_team)+str(self.kickoff_time)


class UpcomingFixture():
    def __init__(self, params, team_id):
        self.team = team_id
        self.gameweek = params.get('event')
        self.kickoff_time = params.get('kickoff_time')
        self.is_home = params.get('is_home')
        self.difficulty = params.get('difficulty')
        self.opponent_team = params.get('team_a') if self.is_home else params.get('team_h')
        self.fixture_key = str(self.team)+str(self.kickoff_time) if self.is_home else str(self.opponent_team)+str(self.kickoff_time)
