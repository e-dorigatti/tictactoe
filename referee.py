from tictactoe import TicTacToe
import random


class Referee(object):
    def __init__(self):
        self.play_order = ['x', 'o']
        self._callbacks = {
            'on_match_start': set(),
            'on_match_end': set(),
        }
    
    def subscribe(self, event, handler):
        assert event in self._callbacks, 'Invalid event: %r' % event
        self._callbacks[event].add(handler)

    def unsubscribe(self, event, handler):
        assert event in self._callbacks and handler in self._callbacks[event]
        self._callbacks[event].remove(handler)

    def _invoke_handlers(self, event, *args, **kwargs ):
        assert event in self._callbacks, 'Invalid event: %r' % event
        for callback in self._callbacks[event]:
            callback(*args, **kwargs)

    def is_match_ended(self):
        return bool(self.ttt.winner())

    def start_game(self, player_x, player_o):
        self.ttt = TicTacToe()
        random.shuffle(self.play_order) # avoid facilitating the first moving player
        self.turn = 0

        self.players = {
            'x': player_x,
            'o': player_o,
        }

        self._invoke_handlers('on_match_start')

    def next_turn(self):
        assert not self.is_match_ended(), 'Match has ended, start a new one'
        self.turn += 1

        player_name = self.play_order[self.turn % 2]
        player = self.players[player_name]

        state = self.ttt.state
        move = player.get_move(self.ttt)
        assert self.ttt.state == state, 'Player %r is cheating! >:(' % player_name

        self.ttt.do_move(player_name, move)

        winner = self.ttt.winner()
        if winner:
            self._invoke_handlers('on_match_end', winner, self.ttt)

