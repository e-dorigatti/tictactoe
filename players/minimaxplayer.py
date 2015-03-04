from baseplayer import player, BasePlayer


@player
class MinimaxPlayer(BasePlayer):
    def __init__(self, *args, **kwargs):
        super(MinimaxPlayer, self).__init__(*args, **kwargs)
        self.cache = dict()

    def get_move(self, ttt):
        _, action = self._minimax(ttt, ttt.state)
        return action

    def _minimax(self, ttt, state, maximizing=True, depth=0):
        if (state, maximizing, depth) in self.cache:
            return self.cache[(state, maximizing, depth)]

        opponent = ['x', 'o'][self.name=='x']
        winner = ttt.winner(state)

        if winner == self.name:
            return 10 - depth, None
        elif winner == opponent:
            return depth - 10, None
        elif winner == 'draw':
            return 0, None

        best_action = None
        if maximizing:
            value = float('-inf')
            for a, s in ttt.moves(self.name, state):
                val, _ = self._minimax(ttt, s, not maximizing, depth + 1)
                if val > value:
                    value, best_action = val, a
        else:
            value = float('inf')
            for a, s in ttt.moves(opponent, state):
                val, _ = self._minimax(ttt, s, not maximizing, depth + 1)
                if val < value:
                    value, best_action = val, a

        self.cache[(state, maximizing, depth)] = value, best_action
        return value, best_action
