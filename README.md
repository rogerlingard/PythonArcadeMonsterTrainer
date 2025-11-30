# Overview
The game I wrote is a simple tile pusher game; instead of a crate, we use a cake. We push the cake to the other side of the grid to win. You also have to dodge the spikes with the guy you control and the cake to avoid a game over. The movement is contained within a grid, making it easy to push the cake through the spikes without destroying it.

You start the game on the beginning menu, which tells you the game name, how to start the game, and how to move the character. Upon pressing enter, you will start the game with your player character and a cake in front of you. You use the arrow keys to move the player character, and when you try to move onto the cake, it will push it in the direction that you moved it from. The goal is to push the cake to the other end of the grid. If you do so, you win. If the player hits a spike or the cake does, then you lose. On both the Game Over and win menu, you can press ENTER to restart, or Backspace to quit out.

The purpose of writing this software was to get a better idea of a game framework, because I have often wanted to learn how to make a game. For me, learning how to make a game is very helpful with learning functions and also organizing your work so that it doesn't become a mess. Plus, learning how to use a game framework will make me better at problem-solving and also how my code is connected. 

[Demonstration of a Monster Trainer Code](https://youtu.be/EeYBEd8lCOk)

# Development Environment
* Visual Studio Code - 1.106.2
* Pyhton - 3.9.13
    - Arcade - 3.0.2
    - Random Library
* GitHub

# Useful Websites

{Make a list of websites that you found helpful in this project}
* [Grid layout for game](https://api.arcade.academy/en/3.3.1/example_code/array_backed_grid_sprites_2.html#array-backed-grid-sprites-2)
* [Documentation for Python arcade 3.3.1](https://api.arcade.academy/en/3.3.1/index.html)
* [Youtube serires for Python arcade library](https://youtube.com/playlist?list=PL1P11yPQAo7qgk8uk_A5UxiTrMt6obCc5&si=kbRsVTgWLB6-D4aa)

# Future Work
* Add a timer to make the player sensitive to beat it quicker.
* Add a scoring system for each grid square the cake has traveled forward, plus extra points for beating the maze quicker, so there can be multiple playthroughs.
* Adding a checker pattern to the end of the maze so people know that it is the end of the grid.
* Put the different views into different Python files to keep code organized better.

