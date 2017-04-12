import mlbgame.data
import mlbgame.object


def get_player_data():
    data = mlbgame.data.get_current_rosters()
    headers = data.readline().decode('ISO-8859-1').split(',')
    output = []
    for d in data.readlines():
        player_data = d.decode('ISO-8859-1').split(',')
        output.append(dict(zip(headers, player_data)))
    return output


class Player(mlbgame.object.Object):

    def __init__(self, data):
        mlbgame.object.Object.__init__(self, data)