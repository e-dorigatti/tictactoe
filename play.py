from referee import Referee
import matplotlib.pyplot as plt
from matches import play_matches, plot_plot
import click
import players


@click.command(help='Let two players of the given classes play together. '
                    'Print match results in csv format')
@click.argument('player_x', type=click.Choice(players.available_players))
@click.argument('player_o', type=click.Choice(players.available_players))
@click.option('--step', '-s', default=1000,
              help='Interval at which a summary about victories and ties is printed')
@click.option('--count', '-c', default=100000,
              help='How many matches to play')
@click.option('--plot/--no-plot', '-p',
              help='Draw a plot with victories and ties at the end')
def cli(player_x, player_o, step, count, plot):
    print 'i,victories_x,draw,victories_o'

    referee = Referee()
    px = players.available_players[player_x]('x', referee)
    po = players.available_players[player_o]('o', referee)

    prev = { 'i': 0, 'x': 0, 'draw': 0, 'o': 0 }
    partials = list()
    for i, results in enumerate(play_matches(referee, px, po, step, count)):
        partial = { k: v - prev[k] for k, v in results.iteritems() }
        partial['i'] = i * step
        partials.append(partial)
        prev = results

        print ','.join(str(x) for x in partial.values())

    if plot:
        title = '%s as X vs. %s as O' % (player_x, player_o)
        plot_plot(partials, step, title)
        plt.show()

if __name__ == '__main__':
    cli()

