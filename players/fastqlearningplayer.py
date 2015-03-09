from qlearningplayer import QLearningPlayer
from baseplayer import player


@player
class FastQLearningPlayer(QLearningPlayer):
    def _update_q(self, ttt, state, action, value):
        for s, a in self._equivalent_states(state, action):
            super(FastQLearningPlayer, self)._update_q(ttt, s, a, value)

         # this has disastrous consequences!!!
         #for s, a in self._equivalent_states(state, action):
         #   s = state.replace('x', 'a').replace('o', 'x').replace('a', 'o')
         #   super(FastQLearningPlayer, self)._update_q(ttt, s, a, -value)

    def _equivalent_states(self, state, action):
        for i in range(4):
            yield state, action
            # interestingly, this is also bad
            # yield self._mirror(state, action)

            state, action = self._rotate_90_clockwise(state, action)
            
    def _rotate_90_clockwise(self, state, action):
        """
        Rotates 90 degrees clockwise the give state-action pair.

        012       630
        345  -->  741
        678       852
        """
        state = (state[6] + state[3] + state[0] + 
                 state[7] + state[4] + state[1] + 
                 state[8] + state[5] + state[2])
        action = [2, 5, 8, 1, 4, 7, 0, 3, 6][action]

        return state, action

    def _mirror(self, state, action):
        """
        Horizontally mirrors the given state-action pair.

        012       210
        345  -->  543
        678       876
        """
        state = (state[2] + state[1] + state[0] +
                 state[5] + state[4] + state[3] +
                 state[8] + state[7] + state[6])
        action = [2, 1, 0, 5, 4, 3, 8, 7, 6][action]

        return state, action

