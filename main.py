"""import os and sys"""
import os
import sys

from DTO.game import Game

if __name__ == '__main__':
    try:
        # get the path of the main directory to save and load gamedata
        path = f"{os.path.dirname(os.path.abspath(__file__))}"

        # create and start a new game
        game = Game(path)
        game.start_game()

        # repeat until no new game is wanted
        again = True
        while again:
            if input("Noch eine Runde? (J/N)") == "J":

                # create and start a new game
                game = Game(path)
                game.start_game()

            else:
                again = False
        sys.exit(0)
    except KeyboardInterrupt:
        print("Sie haben das Spiel mit Ihrer Eingabe abgebrochen!")
        sys.exit(0)
