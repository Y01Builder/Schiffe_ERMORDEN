import os

from DTO.Game import Game

if __name__ == '__main__':
    # get the path of the main directory to save and load gamedata
    path = f"{os.path.dirname(os.path.abspath(__file__))}"

    # create and start a new game
    game = Game(path)
    game.startGame()

    # repeat until no new game is wanted
    again = True
    while again == True:
        if input("Noch eine Runde? (J/N)") == "J":

            # create and start a new game
            game = Game(path)
            game.startGame()

        else:
            again = False
    exit(0)
