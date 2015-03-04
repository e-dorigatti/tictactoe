available_players = dict()
def player(cls):
    assert issubclass(cls, BasePlayer)
    available_players[cls.__name__] = cls
    return cls


class BasePlayer(object):
    def __init__(self, name, referee):
        self.name = name
        self.referee = referee

    def get_move(self, ttt):
        raise NotImplemented
