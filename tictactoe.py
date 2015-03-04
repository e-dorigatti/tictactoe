class TicTacToe:
    def __init__(self):
        self.state = '---------'

    def valid_move(self, move, state=None):
        state = state or self.state
        return 0 <= move < len(state) and state[move] == '-'

    def try_move(self, move, player, state=None):
        """
        Returns the resulting state after the player has performed the given move
        (does not alter game state).
        """
        state = state or self.state
        assert self.valid_move(move, state)
        return state[0:move] + player + state[move + 1:]
        
    def do_move(self, player, move):
        """
        Actually perform the given move by the player.
        """
        assert self.valid_move(move)
        self.state = self.try_move(move, player)

    def at(self, x, y):
        return self.state[3 * y + x]

    def moves(self, player, state=None):
        """
        Returns a list containing all the valid moves in the given or current state.
        Each element is a tuple (move, resulting state).
        """
        state = state or self.state
        blanks = [i for i, c in enumerate(state) if c == '-']
        return [(b, self.try_move(b, player, state)) for b in blanks]

    def winner(self, state=None):
        """
        Returns the winner in the given or current state, draw if the game has ended
        with a draw and None if there is no winner (game still in progress).
        """
        state = state or self.state 
        if self.would_win('x', state):
            return 'x'
        elif self.would_win('o', state):
            return 'o'
        elif not '-' in state:
            return 'draw'
        else:
            return None

    def would_lose(self, player, state=None):
        """
        Returns wheter the given state is a losing state for the specified player.
        """
        state = state or self.state
        player = ['x', 'o'][player == 'x']
        return self.would_win(player, state)

    def would_win(self, player, state=None):
        """
        Returns wheter the given state is a winning state for the specified player.
        """
        state = state or self.state

        # check for horizontal win: 'xxx------', '---xxx---' and '------xxx'
        if (state[0] == state[1] == state[2] == player or
            state[3] == state[4] == state[5] == player or
            state[6] == state[7] == state[8] == player):
            return True

        # check for vertical win: 'x--x--x--', '-x--x--x-' and '--x--x--x'
        if (state[0] == state[3] == state[6] == player or
            state[1] == state[4] == state[7] == player or
            state[2] == state[5] == state[8] == player):
            return True

        # check for diagonal win: 'x---x---x' and '--x-x-x--'
        if (state[0] == state[4] == state[8] == player or
            state[2] == state[4] == state[6] == player):
            return True

if __name__ == '__main__':
    t = TicTacToe()

    player = 'x'
    while t.winner() == '':
        print t.state[0:3]
        print t.state[3:6]
        print t.state[6:9]
        print
        print player, 'is moving'
        i = input('Enter position:')
        t.do_move(player, i)

        player = ['x', 'o'][player == 'x']

    print t.winner(), ' won'
    print t.state
