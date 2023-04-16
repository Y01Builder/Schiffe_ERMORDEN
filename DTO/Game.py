from typing import Any
import DTO.Player


class Game:

    __player1 = None
    __player2 = None

    def __init__(self, size):
        self.size = size

    def startGame(self):
        exitGame = False
        while True:
            print("Spiel Beginn!")
            test = DTO.Player("Name", 2)



            return

    def __createPlayers__(self):
        namePlayer1 = input("Bitte benennen Sie Spieler 1:")

        namePlayer2 = input("Bitte benennen Sie Spieler 2:")

        __player1 = Player(namePlayer1, 0)
        __player2 = Player(namePlayer2, 1)


    def endGame(self):
        print(f'Hi')

    def clear(self):
        print(f'Hi')




