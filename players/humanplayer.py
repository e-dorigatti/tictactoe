from baseplayer import player, BasePlayer

@player
class HumanPlayer(BasePlayer):
    def __init__(self, name, referee, *args, **kwargs):
        super(HumanPlayer, self).__init__(name, referee, *args, **kwargs)
        if referee:
            self.referee = referee
            referee.subscribe('on_match_end', self.match_ended)

    def get_move(self, ttt):
        state = [ str(i) if x == '-' else x for i, x in enumerate(ttt.state) ]
        print ' '.join(state[0:3])
        print ' '.join(state[3:6])
        print ' '.join(state[6:9])

        valid = [str(x) for x, _ in ttt.moves(self.name)]
        move = -1

        while not move in valid:
            print '\nPlayer %s, pick a move, valid moves are %s' % (self.name, 
                ', '.join(str(x) for x in valid))

            move = raw_input('? ')
            if not move in valid:
                print 'Ivalid move'

        return int(move)

    def match_ended(self, winner, ttt, *args, **kwargs):
        if winner == self.name:
            print 'You won!\n'
        elif winner == 'draw':
            print 'Tie...\n'
        else:
            print 'You lost :(\n'
        raw_input('Press enter to continue...')
