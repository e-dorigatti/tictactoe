import multiprocessing as mp
from referee import Referee
import matplotlib.pyplot as plt
import players
import time
import sys


def play_matches(referee, player_x, player_o, step, count):
    victories, i = { 'x': 0, 'o': 0, 'draw': 0 }, 0
    while i <= count:
        referee.start_game(player_x, player_o)
        while not referee.is_match_ended():
            referee.next_turn()

        victories[referee.ttt.winner()] += 1
        i += 1

        if i % step == 0:
            yield dict(victories)   # we give a copy of this dict, otherwise
                                    # obscure things could happen...


def play_tournament(count_per_game, players, worker_count=None):
    """
    Play a tournament in which every player plays count_per_game matches versus
    every other player. Score is given as 3 * victories + ties

    players: list of tuples (player class, player initialization parameters)
    """
    assert (not worker_count or worker_count > 0) and count_per_game > 0

    pool = mp.Pool(processes=worker_count)
    args = ((count_per_game, x, y) for x in players for y in players if x != y)

    results = pool.imap(_compare_players, args)

    match_count, start_time = 0, time.time()
    ranking = dict((p, 0) for p in players)
    for (param_x, score_x), (param_o, score_o) in results:
        duration = time.time() - start_time
        match_count += count_per_game

        ranking[param_x] += score_x
        ranking[param_o] += score_o

        sys.stderr.write('INFO: played %d matches in %.2f seconds (%.2f m/s)\r'  % (
            match_count, duration, match_count / duration))

    return ranking

def _compare_players(args):
    count, (class_x, param_x), (class_o, param_o)= args

    referee = Referee()
    px = class_x('x', referee, *param_x)
    po = class_o('o', referee, *param_o)

    victories = play_matches(referee, px, po, count, count).next()

    score_x = 3 * victories['x'] + victories['draw']
    score_o = 3 * victories['o'] + victories['draw']
    
    return ((class_x, param_x), score_x), ((class_o, param_o), score_o)


def plot_plot(victories, step, title):
    plt.title(title)
    plt.plot([x['i'] for x in victories], [x['draw'] for x in victories], label='Ties')
    plt.plot([x['i'] for x in victories], [x['x'] for x in victories], label='X')
    plt.plot([x['i'] for x in victories], [x['o'] for x in victories], label='O')
    plt.ylim(ymax=step+10); plt.grid(True); plt.legend(loc='lower right') 

