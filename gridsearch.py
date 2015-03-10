from matches import play_tournament
from players import QLearningPlayer
import players
import sys

#http://stackoverflow.com/questions/23916413/celery-parallel-distributed-task-with-multiprocessing

def _grid_generator(grid_spec):
    """
    Explicitly generate all the points belonging to the grid.
    grid_spec is a list of values to use for each axis.
    """
    if not grid_spec:
        yield ()
    else:
        for x in grid_spec[0]:
            for g in _grid_generator(grid_spec[1:]):
                yield (x,) + g

def main(count, grid_spec):
    """
    Compares the learning performances of certain agents using the given parameters
    in a head-to-head game composed of a certain number of matches. Agents do not
    preserve memory between games, this means that a fresh agent is created for
    every opponent.
    Score is computed as follows: 3 * number of won matches + number of ties
    """
 
    num_players = reduce(lambda x, y: x*y, (len(x) for x in grid_spec))
    expected = count * num_players * (num_players - 1)
    sys.stderr.write('Expected number of matches: %d (ca. %d minutes at 10000m/s)\n' % (
        expected, int(expected / (10000. * 60))))

    grid = [(QLearningPlayer, x) for x in _grid_generator(grid_spec)]
    ranking = play_tournament(count, grid)

    max_score = float(max(ranking.values()) or 1)
    print '\n\n*** Final Normalized Ranking (%d matches per game) ***' % count
    print '\n'.join('%d) %.2f (%d points) -- %s, %s' % (i + 1, v/max_score, v, c.__name__, k)
        for i, ((c, k), v) in enumerate(sorted(ranking.items(), key=lambda x: -x[1])))


if __name__ == '__main__':
    from sys import argv

    if len(argv) >= 4:
        count = int(argv[1])
        grid_spec = [[float(x) for x in a.split(',')] for a in argv[2:]]

        main(count, grid_spec)
    else:
        print 'Arguments: <match count per game> <grid axis specification>'
        print 'Grid axis specification: comma-separated list of floating point values'
        print 'One for each axis'

