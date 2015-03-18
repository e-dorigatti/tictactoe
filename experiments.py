from matches import play_matches, Referee, plot_plot
import matplotlib.pyplot as plt
import multiprocessing as mp
import players
import time
import sys


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
    player_x = players.QLearningPlayer('x', referee)
    player_o = players.QLearningPlayer('o', referee)

    player_o.Q = player_x.Q
    player_o.visited = player_x.visited

    print 'training the schizophrenic agent'
    print_results(referee, player_x, player_o, 10000, 5)

    print '\ncreating a fresh opponent and letting it play as \'x\''
    new_x = players.QLearningPlayer('x', referee)
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
    player_x = players.QLearningPlayer('x', referee)
    player_o = players.QLearningPlayer('o', referee)

    print 'training the agents'
    print_results(referee, player_x, player_o, 10000, 5)

    print '\ncreating a new \'x\' and letting the old \'x\' play as \'o\''
    new_x = players.QLearningPlayer('x', referee)
    player_x.name = 'o'
    player_x.match_count = 0
    new_o = player_x

    print_results(referee, new_x, new_o, 10000, 500)


@experiment
def learning_curves():
    """
    Shows how the match history of a QLearningPlayer vs a MinimaxPlayer
    varies as the learning rate coefficient of the former varies.
    """

    step = 250
    count = 100000
    for subplot, lrate_c in enumerate([0.0025, 0.001, 0.00025, 0.0001]):
        print '\nlearning rate', lrate_c
        referee = Referee()
        px = players.QLearningPlayer('x', referee, lrate_coeff=lrate_c)
        po = players.MinimaxPlayer('o', referee)

        prev = { 'i': 0, 'x': 0, 'draw': 0, 'o': 0 }
        partials = list()
        for i, results in enumerate(play_matches(referee, px, po, step, count)):
            partial = { k: v - prev[k] for k, v in results.iteritems() }
            partial['i'] = i * step
            partials.append(partial)
            prev = results
            sys.stderr.write('.')

        plt.subplot(2, 2, subplot + 1)
        plot_plot(partials, step, 'Learning Rate Coefficient %f' % lrate_c)

    plt.show()


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
