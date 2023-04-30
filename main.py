import os

from DTO.Game import Game

if __name__ == '__main__':
    try:
        # get the path of the main directory to save and load gamedata
        path = f"{os.path.dirname(os.path.abspath(__file__))}"

        # create and start a new game
        game = Game(path)
        game.startGame()

        # repeat until no new game is wanted
        again = True
        while again:
            if input("Noch eine Runde? (J/N)") == "J":

                # create and start a new game
                game = Game(path)
                game.startGame()

            else:
                again = False
        exit(0)
    except KeyboardInterrupt:
        print("Sie haben das Spiel mit Ihrer Eingabe abgebrochen!")
    except Exception as e:
        print(f"Es ist ein Fehler in der Funktion 'main' aufgetreten! {e}")
