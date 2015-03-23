from matches import play_matches, Referee, plot_plot
import matplotlib.pyplot as plt
import multiprocessing as mp
import pandas as pd
import players
import time
import sys
import math


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
def learning_curves(*args):
    """
    Shows how the match history of a QLearningPlayer vs a MinimaxPlayer
    varies as the learning rate coefficient of the former varies.

    Specify learning rates coefficients as parameters
    """

    lrates = [float(x) for x in args]
    assert lrates, 'Specity learning rates as parameters'
    subplots_y = math.ceil(math.sqrt(len(lrates)))
    subplots_x = (subplots_y - 1 if subplots_y * (subplots_y - 1) > len(lrates) 
                                 else subplots_y)

    step, count = 250, 100000

    pool = mp.Pool()
    results = pool.imap(_learning_curves_parallel,
                       ((i + 1, lrate_c, step, count) for i, lrate_c in enumerate(lrates)))
    for subplot, lrate_c, partials in results:
        plt.subplot(subplots_x, subplots_y, subplot)
        df = pd.DataFrame(data=(x.values() for x in partials), columns=partials[0].keys())
        plt.title('Learning rate coeff.: %f' % lrate_c)
        df['draw'].plot(x=df['i'])
        df['o'].plot(x=df['i'])
        df['states_visited'].plot(x=df['i'], secondary_y=True)

    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95)
    plt.show()


def _learning_curves_parallel(args):
    subplot, lrate_c, step, count = args

    referee = Referee()
    px = players.QLearningPlayer('x', referee, lrate_coeff=lrate_c)
    po = players.MinimaxPlayer('o', referee)

    prev = { 'i': 0, 'x': 0, 'draw': 0, 'o': 0, 'lr': 0.0 }
    partials = list()
    for i, results in enumerate(play_matches(referee, px, po, step, count)):
        partial = { k: v - prev[k] for k, v in results.iteritems() }
        partial['i'] = i * step
        partial.update(px.debug_info())

        partials.append(partial)
        prev = results
        sys.stderr.write(str(subplot))

    return subplot, lrate_c, partials


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
