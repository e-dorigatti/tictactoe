TicTacToe
===
A couple of AI algorithms to play the tic tac toe game. You can play as well!

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

 - `python play.py -p -c 75000 -s 500 QLearningPlayer QLearningPlayer`
 ![](https://cloud.githubusercontent.com/assets/5585926/6541288/eecacb1c-c4c7-11e4-977c-ab5bf2f324f2.png)
 
 Learning works! Eventually the opponents cannot win anymore and they always tie (blue line). Moreover, the
 win rate decreases in almost the same way for both players because they have the same learning parameters,
 thus they behave in the same way.
 
 - `python play.py -p -c 30000 -s 250 QLearningPlayer FastQLearningPlayer`
 ![](https://cloud.githubusercontent.com/assets/5585926/6541286/eec02d60-c4c7-11e4-934d-065463c20981.png)
 
 As you can see, the fast learning player (red line) is indeed learning faster and is able to outplay the normal
 player (green line) in the inital games. As time goes on, though, they both converge to the optimal strategy
 and tie every game.
 
 - `python play.py -p -c 15000 -s 100 QLearningPlayer MinimaxPlayer`
 ![](https://cloud.githubusercontent.com/assets/5585926/6541287/eec3f79c-c4c7-11e4-93d5-0f8f743a7e0c.png)
 
 This is what I meant when I said that the `MinimaxPlayer` is the perfect opponent. As you can see, it has never
 lost a match! On the other hand, the `QLearningPlayer` was able to learn the optimal strategy much faster than
 when it was playing against another learning player; this happened becase it had a better teacher.
 
 - `python play.py -p -c 15000 -s 100 FastQLearningPlayer MinimaxPlayer`
 ![](https://cloud.githubusercontent.com/assets/5585926/6541284/eeb522f8-c4c7-11e4-80fc-f8f2b073be32.png)
 
 Again, the fast Q-learning is indeed faster to learn the optimal strategy because it reacts faster to new 
 strategies found by its opponent. You can see this by looking at the red victory spikes during the late
 games: with the `FastQLearningPlayer` they are fewer and of shorter duration.
 
 - `python play.py -p -c 15000 -s 100 MinimaxPlayer MinimaxPlayer`
 ![](https://cloud.githubusercontent.com/assets/5585926/6541285/eeb9bde0-c4c7-11e4-872f-cc030b8dd4dd.png)
 
 What happens when a perfect player plays versus another perfect player? Thi is the least exciting plot which
 confirms once again the perfection of the `MinimaxPlayer`.
