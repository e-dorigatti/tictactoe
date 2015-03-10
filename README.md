TicTacToe
===
A couple of AI algorithms to play the tic tac toe game. You can play as well!

## Content of repo
The algorithms are implemented in the players folder, here you will find:
 - **MinimaxPlayer**: Implementation of the popular [minimax algorithm](http://en.wikipedia.org/wiki/Minimax),
 which is basically a sistematic exploration of the tree whose nodes are game states and the children of a node
 are all the states which can be reached from there by performing a valid move. This is basically the perfect
 opponent as it never loses a game.
 - **QLearningPlayer**: This player is able to learn with experience, initially it performs random moves but as
 it plays more and more games it will learn and become a very strong opponent. The algorithm used is called 
 [Q-learning](http://en.wikipedia.org/wiki/Q-learning) because it is based on a function which tells the Quality
 of a move in a certain game state.
 - **FastQLearningPlayer**: By leveraging simmetries in the game states this player is able to learn how to play
 the tic tac toe game faster than the "vanilla" Q-learning implementation.
 - **HumanPlayer**: This is you! This player implements one of the most successful learning algorithms ever devised
 by mankind, or does it? Prove your skills and challenge the other players :)
 
Additionally, you will find these scripts:
 - **play.py**: Play a number of head to head matches between two players. You can use this to see how players
 behave and to play yourself. Can draw a plot with victores/ties.
 - **experiments.py**: I was wondering how learning players reacted in particular situations. Q-learning is 
  based on a table mapping state-action pairs to (expected) utilities, so what happens when an agent is suddenly
  forced to play in states it has never visited?
 - **gridsearch.py**: Q-learning agents have distinct characters controlled by three parameters, namely the
  *discount factor* (how far in time the agent thiks, does it prefer short term rewards or is it keen on pursuing
  a bad short term strategy to eventually reach a better reward), the *exploration coefficient* (once the agend
  finds a fairly decent stragegy, does it stick with that one or does it try new ones, thus exploring new states)
  and the *learning rate*. This script explores the parameters space to find the combinations which work better.
 - **tictactoe.py**: Contains the `TicTacToe` class implementing the mechanics of the game. Most methods allow for
  an optional parameter specifying a state of the game different from the current one; this is to allow players
  to try and experiment "mentally" with the game.
 - **referee.py**: The referee manages matches alternating turns between players. It generates an event when the
  a match starts and when it ends.
 - **matches.py**: Utilities for playing high number of matches and even tournaments.
 
## Player Comparison
Let's see how players play!

 - `python play.py -p --count 75000 --step 500 QLearningPlayer QLearningPlayer`
 ![](https://cloud.githubusercontent.com/assets/5585926/6541288/eecacb1c-c4c7-11e4-977c-ab5bf2f324f2.png)
 
 Learning works! Eventually the opponents cannot win anymore and they always tie (blue line). Moreover, the
 win rate decreases in almost the same way for both players because they have the same learning parameters,
 thus they behave in the same way.
 
 - `python play.py -p --count 30000 --step 250 QLearningPlayer FastQLearningPlayer`
 ![](https://cloud.githubusercontent.com/assets/5585926/6541286/eec02d60-c4c7-11e4-934d-065463c20981.png)
 
 As you can see, the fast learning player (red line) is indeed learning faster and is able to outplay the normal
 player (green line) in the inital games. As time goes on, though, they both converge to the optimal strategy
 and tie every game.
 
 - `python play.py -p --count 15000 --step 100 QLearningPlayer MinimaxPlayer`
 ![](https://cloud.githubusercontent.com/assets/5585926/6541287/eec3f79c-c4c7-11e4-93d5-0f8f743a7e0c.png)
 
 This is what I meant when I said that the `MinimaxPlayer` is the perfect opponent. As you can see, it has never
 lost a match! On the other hand, the `QLearningPlayer` was able to learn the optimal strategy much faster than
 when it was playing against another learning player; this happened becase it had a better teacher.
 
 - `python play.py -p --count 15000 --step 100 FastQLearningPlayer MinimaxPlayer`
 ![](https://cloud.githubusercontent.com/assets/5585926/6541284/eeb522f8-c4c7-11e4-80fc-f8f2b073be32.png)
 
 Again, the fast Q-learning is indeed faster to learn the optimal strategy because it reacts faster to new 
 strategies found by its opponent. You can see this by looking at the red victory spikes during the late
 games: with the `FastQLearningPlayer` they are fewer and of shorter duration.
 
 - `python play.py -p --count 15000 --step 100 MinimaxPlayer MinimaxPlayer`
 ![](https://cloud.githubusercontent.com/assets/5585926/6541285/eeb9bde0-c4c7-11e4-872f-cc030b8dd4dd.png)
 
 What happens when a perfect player plays versus another perfect player? Thi is the least exciting plot which
 confirms once again the perfection of the `MinimaxPlayer`.


## Parameter selection
As previously mentioned, Q-learning needs two parameters which determine how learning actually happens and the
`QLearningPlayer` needs another parameter to determine how keen the player is about exploring new states and
strategies. Together, these parameters determine the agent's character but then one question arises: which are
the best values for these parameters?

To determine this, I made a function which plays a tournament in which partecipate players with different parameter
combinations. Every player plays a certain number of matches versus all the other players and a score is computed
over all matches played according to the formula `3*matches won + matches tied`. The player is reinitialized for
every new opponent.


The script `gridsearch.py` generates a grid according to its arguments and plays a tournament, then aggregates the
results and shows the final ranking. For example `python gridsearch.py 50000 1.0,0.5,0.0 0.01,0.0001,0.0 0.01,0.0001,0.0`
uses the points `1.0,0.5,0.0` on the discount factor axis and `0.01,0.0001,0.0` on both the exploration coefficient axis
and the learning rate axis, thus the grid generated will have the points  `1.0,0.01,0.01`, `1.0,0.01,0.0001`, `1.0,0.01,0.0`,
`1.0,0.0001,0.01`, ..., `0.5,0.01,0.01` etc. These points will be used as initialization parameters for the players, and
every player will play `50000` matches versus every other player.

Why try these parameters first? Because they span over all the range of reasonable parameters. In fact, the discount factor
lies in the closed interval `[0,1]`, and note that `exp(50000 * -0.01) = 7.12e-218`, `exp(50000 * -0.0001) = 0.0067` and
obviously `exp(50000 * -0.0) = 1.0` (this is how these coefficient are used) thus we have a very fast decreasing factor,
a slowly decreasing factor and a constant one. Here are the results:

```
$  python gridsearch.py 50000 1.0,0.5,0.0 0.01,0.0001,0.0 0.01,0.0001,0.0
Expected number of matches: 35100000 (ca. 58 minutes at 10000m/s)
INFO: played 35100000 matches in 2770.92 seconds (12667.26 m/s)

*** Final Normalized Ranking (50000 matches per game) ***
1) 1.00 (5386717 points) -- QLearningPlayer, (1.0, 0.0001, 0.0001)
2) 0.97 (5228251 points) -- QLearningPlayer, (1.0, 0.0001, 0.0)
3) 0.97 (5228251 points) -- QLearningPlayer, (1.0, 0.01, 0.0)
4) 0.97 (5210564 points) -- QLearningPlayer, (1.0, 0.01, 0.0001)
5) 0.95 (5099464 points) -- QLearningPlayer, (0.5, 0.0001, 0.0001)
6) 0.94 (5065203 points) -- QLearningPlayer, (0.5, 0.0001, 0.0)
7) 0.90 (4837323 points) -- QLearningPlayer, (0.5, 0.01, 0.0)
8) 0.88 (4745205 points) -- QLearningPlayer, (0.5, 0.01, 0.0001)
9) 0.77 (4163845 points) -- QLearningPlayer, (1.0, 0.0, 0.0001)
10) 0.77 (4124522 points) -- QLearningPlayer, (0.5, 0.0, 0.0001)
11) 0.75 (4031219 points) -- QLearningPlayer, (1.0, 0.0, 0.0)
12) 0.75 (4031199 points) -- QLearningPlayer, (0.5, 0.0, 0.0)
13) 0.57 (3078038 points) -- QLearningPlayer, (0.0, 0.0001, 0.0001)
14) 0.57 (3068884 points) -- QLearningPlayer, (0.0, 0.0001, 0.0)
15) 0.57 (3068884 points) -- QLearningPlayer, (0.0, 0.01, 0.0)
16) 0.55 (2976843 points) -- QLearningPlayer, (0.0, 0.01, 0.0001)
17) 0.55 (2974507 points) -- QLearningPlayer, (0.5, 0.0, 0.01)
18) 0.54 (2927445 points) -- QLearningPlayer, (1.0, 0.0, 0.01)
19) 0.47 (2506538 points) -- QLearningPlayer, (1.0, 0.0001, 0.01)
20) 0.46 (2451970 points) -- QLearningPlayer, (0.5, 0.01, 0.01)
21) 0.38 (2061437 points) -- QLearningPlayer, (1.0, 0.01, 0.01)
22) 0.36 (1961624 points) -- QLearningPlayer, (0.0, 0.0, 0.0001)
23) 0.36 (1945913 points) -- QLearningPlayer, (0.0, 0.0, 0.0)
24) 0.35 (1897693 points) -- QLearningPlayer, (0.0, 0.0, 0.01)
25) 0.33 (1780285 points) -- QLearningPlayer, (0.0, 0.0001, 0.01)
26) 0.33 (1764722 points) -- QLearningPlayer, (0.5, 0.0001, 0.01)
27) 0.30 (1614861 points) -- QLearningPlayer, (0.0, 0.01, 0.01)
```

What can be seen from this ranking? First of all, note that the first positions are all occupied by a `1.0` discount factor,
and that a `0.0` exploration coefficient does not appear until the 9th position. (Interestingly enough, a constant exploration
coefficient corresponds to no exploration at all, see `get_move()` and `exploration_function()` in the `QLearningPlayer`).
In general, a fast decreasing parameter (`0.01` coefficient) appears to be bad for both the exploration coefficient and the
learning rate coefficient.

```
$ python gridsearch.py 50000 1.0,0.75,0.5 0.01,0.001,0.0001 0.001,0.0001,0.0
Expected number of matches: 35100000 (ca. 58 minutes at 10000m/s)
INFO: played 35100000 matches in 2747.31 seconds (12776.15 m/s)

*** Final Normalized Ranking (50000 matches per game) ***
1) 1.00 (4657625 points) -- QLearningPlayer, (1.0, 0.0001, 0.0001)
2) 0.98 (4548085 points) -- QLearningPlayer, (0.75, 0.0001, 0.0001)
3) 0.97 (4527811 points) -- QLearningPlayer, (1.0, 0.001, 0.0001)
4) 0.93 (4310985 points) -- QLearningPlayer, (0.5, 0.0001, 0.0001)
5) 0.92 (4285526 points) -- QLearningPlayer, (0.75, 0.0001, 0.0)
6) 0.91 (4253457 points) -- QLearningPlayer, (1.0, 0.001, 0.0)
7) 0.91 (4253457 points) -- QLearningPlayer, (1.0, 0.0001, 0.0)
8) 0.91 (4253457 points) -- QLearningPlayer, (1.0, 0.01, 0.0)
9) 0.90 (4203483 points) -- QLearningPlayer, (0.75, 0.001, 0.0001)
10) 0.90 (4194513 points) -- QLearningPlayer, (1.0, 0.01, 0.0001)
11) 0.89 (4167204 points) -- QLearningPlayer, (0.5, 0.0001, 0.0)
12) 0.87 (4041855 points) -- QLearningPlayer, (0.75, 0.01, 0.0)
13) 0.86 (3985915 points) -- QLearningPlayer, (0.75, 0.001, 0.0)
14) 0.84 (3892518 points) -- QLearningPlayer, (0.75, 0.01, 0.0001)
15) 0.82 (3828701 points) -- QLearningPlayer, (0.5, 0.001, 0.0001)
16) 0.79 (3696240 points) -- QLearningPlayer, (0.5, 0.001, 0.0)
17) 0.77 (3607995 points) -- QLearningPlayer, (0.5, 0.01, 0.0)
18) 0.75 (3512317 points) -- QLearningPlayer, (0.5, 0.01, 0.0001)
19) 0.48 (2253998 points) -- QLearningPlayer, (0.5, 0.0001, 0.001)
20) 0.45 (2101198 points) -- QLearningPlayer, (0.75, 0.0001, 0.001)
21) 0.44 (2065873 points) -- QLearningPlayer, (1.0, 0.0001, 0.001)
22) 0.42 (1975385 points) -- QLearningPlayer, (1.0, 0.001, 0.001)
23) 0.42 (1972458 points) -- QLearningPlayer, (0.75, 0.001, 0.001)
24) 0.40 (1881625 points) -- QLearningPlayer, (0.5, 0.01, 0.001)
25) 0.40 (1876707 points) -- QLearningPlayer, (1.0, 0.01, 0.001)
26) 0.40 (1875698 points) -- QLearningPlayer, (0.5, 0.001, 0.001)
27) 0.39 (1830711 points) -- QLearningPlayer, (0.75, 0.01, 0.001)
```

Note that the last positions are all occuped by players which have used a learning rate coefficient of `0.001`. This happened because
`exp(50000 * -0.001) = 1.93e-22` and `exp(5000 * -0.001) = 0.0067`, basically those agents have all stopped learning by the 5000th match
and spent the remaining 45000 matches playing whatever strategy they found; they have been outplayed because they could not adapt to
their opponents' evolving strategies. The first four positions are occupied by the learning rate coefficient `0.0001`, followed by
four `0.0`. Which is the best learning rate then? I believe that this strongly depend on the number of matches two agents
play one versus the other; there will be a point after which an agent stops learning whereas the other is still able to find a
better strategy and outplay its opponent (unless the game lasts enough and both agents find the optimal strategy for the game).
Why, then, `0.0001` performs significantly better than `0.0` (there is an 8% difference in the scores)? Generally, a decreasing learning
rate is required for a learning algorithm to converge to the optimal solution (I do not know specifically about Q-learning, but 
this is especially important for gradient descent-based learning algorithms).
