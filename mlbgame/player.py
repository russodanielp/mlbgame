import mlbgame.data
import mlbgame.object

import mlbgame

import lxml.etree as etree

from collections import Counter
from functools import reduce



def get_player_data():
    """Returns a list current players and their attributes in a dictionary"""
    data = mlbgame.data.get_current_rosters()
    headers = data.readline().decode('ISO-8859-1').split(',')
    output = []
    for d in data.readlines():
        player_data = d.decode('ISO-8859-1').split(',')
        output.append(dict(zip(headers, player_data)))
    return output


def single_game_batting_data(response):
    """Should be an HTTPResponse object of player batting data"""
    parsed = etree.parse(response)
    root = parsed.getroot()
    abs = root.find('atbats')
    results = Counter()
    for ab in abs:
        results[ab.attrib['event']] =+ 1
    return results

def most_recent_game(team):
    """Returns the most recent game_id for a team"""
    import datetime
    return str(datetime.date.today()).split('-')


class PlayerBatting(mlbgame.object.Object):

    def __init__(self, data):
        mlbgame.object.Object.__init__(self, data)

class Player(mlbgame.object.Object):

    def __init__(self, data):
        if data['mlb_team_long'] == 'Anaheim Angels':
            self.team_ob = mlbgame.TEAMS['Los Angeles Angels']
        else:
            self.team_ob = mlbgame.TEAMS[data['mlb_team_long']]
        mlbgame.object.Object.__init__(self, data)

    def __str__(self):
        return self.mlb_name

    def get_batting_stats(self, year, month=None, day=None):
        games = mlbgame.games(year, month, day, home=self.team_ob.club_common_name, away=self.team_ob.club_common_name)
        game_ids = [game.game_id for game in mlbgame.combine_games(games)]
        responses = [mlbgame.data.get_player_from_game(game_id, self.mlb_id) for game_id in game_ids]
        data = [single_game_batting_data(response)for response in responses if response is not None]
        results = Counter()
        for d in data:
            results += d
        return results

