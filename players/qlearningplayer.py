from random import random
from baseplayer import player, BasePlayer
import itertools
from math import exp


@player
class QLearningPlayer(BasePlayer):
    def __init__(self, name, referee=None, discount=1.0,
                 exploration_coeff=0.0001, lrate_coeff=0.00001):
        super(QLearningPlayer, self).__init__(name, referee)

        if referee:
            self.referee = referee
            referee.subscribe('on_match_start', self.on_match_start)
            referee.subscribe('on_match_end', self.learn_from_match)

        self.Q, self.visited = dict(), dict()
        self.discount = discount
        self.lrate_coeff = abs(lrate_coeff)
        self.exploration_coeff = abs(exploration_coeff)
        self.match_count = 0

    def _update_q(self, ttt, state, action, value):
        self._init_q(ttt, state)
        self.visited[state][action] += 1
        self.Q[state][action] += value

    def _init_q(self, ttt, state):
        """
        Lazy initialization of the tables needed to learning.
        """
        if state not in self.Q:
            initial = dict((action, 0.0) for action, _ in ttt.moves(self.name, state))

            self.Q[state] = initial
            self.visited[state] = dict(initial)

    def on_match_start(self, *args, **kwargs):
        """
        Reset the current episode.
        """
        self._match = list()

    def learn_from_match(self, winner, ttt, *args, **kwargs):
        """
        Learn, this is where all the magic happens.
        Technically speaking this is an episodic-based, temporal-difference Q learning.
        """
        if winner == self.name:
            reward = 1
        elif winner == 'draw':
            reward = 0
        else:
            reward = -1

        states_list = zip(self._match, self._match[1:] + [(None, None)])
        for (action, state), (_, result) in reversed(states_list):
            lrate = exp(-self.lrate_coeff * self.match_count)
            estimated_optimal_future = max(self.Q[result].values()) if result else 0.0
            learned = reward + self.discount * estimated_optimal_future
            self._update_q(ttt, state, action, lrate * (learned - self.Q[state][action]))

            reward = 0  # reward is given only when winning or losing

        self.match_count += 1

    def get_move(self, ttt):
        """
        Choose the move to do in the state the game is currently in.
        """
        self._init_q(ttt, ttt.state)

        best_action, _ = max(self.Q[ttt.state].iteritems(),
                             key=lambda x: self.exploration_function(ttt, *x))
        self._match.append((best_action, ttt.state))

        return best_action

    def exploration_function(self, ttt, action, quality):
        """
        Alter the quality of a state-action pair to promote exploration of rarely
        visited state-action pairs.
        """
        return (quality + exp(-self.exploration_coeff * self.visited[ttt.state][action]))

    def debug_info(self):
        """
        Returns some (hopefully useful) metrics as a dict
        """

        state_action_pairs_num = sum(len(x) for x in self.visited)
        visited_sum = sum(sum(v.values()) for k, v in self.visited.iteritems())

        return {
            'avg_visited':  float(visited_sum) / state_action_pairs_num,
            'states_visited': len(self.visited),
        }
