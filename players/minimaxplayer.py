from baseplayer import player, BasePlayer
import random


@player
class MinimaxPlayer(BasePlayer):
    def __init__(self, *args, **kwargs):
        super(MinimaxPlayer, self).__init__(*args, **kwargs)
        self.cache = dict()

    def get_move(self, ttt):
        _, action = self._minimax(ttt, ttt.state)
        return action

    def _minimax(self, ttt, state, maximizing=True, depth=0):
        if (state, maximizing, depth) not in self.cache:
            opponent = ['x', 'o'][self.name=='x']
            winner = ttt.winner(state)

            if winner == self.name:
                return 10 - depth, None  # try to win as soon as possible
            elif winner == opponent:
                return depth - 10, None  # try to lose as late as possible
            elif winner == 'draw':
                return 0, None

            choices = []
            if maximizing:
                value = float('-inf')
                for a, s in ttt.moves(self.name, state):
                    val, _ = self._minimax(ttt, s, not maximizing, depth + 1)
                    if val > value:
                        value, choices = val, [a]
                    elif val == value:
                        choices.append(a)
            else:
                value = float('inf')
                for a, s in ttt.moves(opponent, state):
                    val, _ = self._minimax(ttt, s, not maximizing, depth + 1)
                    if val < value:
                        value, choices = val, [a]
                    elif val == value:
                        choices.append(a)

            self.cache[(state, maximizing, depth)] = value, choices

        value, choices = self.cache[(state, maximizing, depth)]
        return value, random.choice(choices)
