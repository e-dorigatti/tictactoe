from players.qlearningplayer import QLearningPlayer
from matches import play_matches, Referee
import multiprocessing as mp
import time


experiments = dict()
def experiment(function):
    experiments[function.__name__] = function
    return function


def print_results(referee, player_x, player_o, step, epochs):
    count, prev = 0, None

    for victories in play_matches(referee, player_x, player_o, step, step * epochs):
        difference = (dict((k, victories[k] - prev[k]) for k in victories) if prev 
                      else victories)
        prev = dict(victories)
        count += step

        descr = ', '.join('%s: %.2f%%' % (k, 100. * v / step)
                                          for k, v in difference.iteritems())
        seen_x = sum(len(x) for x in player_x.Q)
        seen_o = sum(len(x) for x in player_o.Q)
        print 'i: %d, %s, seen_x: %d, seen_o: %d' % (count, descr, seen_x, seen_o)


@experiment
def schizophrenia():
    """
    Create a schizophrenic agent who plays both as 'x' and as 'o' at the same time
    during the training phase, then let it play versus a new agent.

    Intuitively, the schizophrenic agent should wreck the new one as he has already
    played a lot of matches both as 'x' and as 'o'.
    """
    referee = Referee()
    player_x = QLearningPlayer('x', referee)
    player_o = QLearningPlayer('o', referee)

    player_o.Q = player_x.Q
    player_o.visited = player_x.visited

    print 'training the schizophrenic agent'
    print_results(referee, player_x, player_o, 10000, 5)

    print '\ncreating a fresh opponent and letting it play as \'x\''
    new_x = QLearningPlayer('x', referee)
    new_o = player_o
    new_o.match_count = 0
    print_results(referee, new_x, new_o, 10000, 10)


@experiment
def side_invert():
    """
    Train an agent to play as 'x', then force it to play as 'o'.

    Intuitively, this should cause a disaster and make it as good (bad)
    as a completely new agent.
    """
    referee = Referee()
    player_x = QLearningPlayer('x', referee)
    player_o = QLearningPlayer('o', referee)

    print 'training the agents'
    print_results(referee, player_x, player_o, 10000, 5)

    print '\ncreating a new \'x\' and letting the old \'x\' play as \'o\''
    new_x = QLearningPlayer('x', referee)
    player_x.name = 'o'
    player_x.match_count = 0
    new_o = player_x

    print_results(referee, new_x, new_o, 10000, 500)


if __name__ == '__main__':
    from sys import argv
    choice = argv[1] if len(argv) > 1 else ''

    contains = [(function, choice in name) for name, function in experiments.iteritems()]
    matching = [f for f, c in contains if c]
    if len(matching) != 1:
        print 'Usage: %s <experiment>\n' % argv[0]
        print 'Available experiments are %s' % ', '.join(experiments.keys())
        print 'Abbreviations are accepted iff unambiguous'
    else:
        print matching[0].__doc__
        matching[0](*argv[2:])
