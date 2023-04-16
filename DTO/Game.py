from typing import Any
from DTO.Player import Player

class Game:


    def __init__(self, size):
        self.size = size

    def startGame(self):

        print("Spiel Beginn!")
        player1 = self.__createPlayer(0)
        player2 = self.__createPlayer(1)

        # TODO: Würfeln wer anfängt.

        player1.shootField()

        while True:

            if player1.shootField() == True:
                self.endGame(player1)
                break
                # Speichern
            if player2.shootField() == True:
                self.endGame(player2)
                break
                # Speichern
        return

    def __createPlayer(self, id):
        namePlayer = input(f"Bitte benennen Sie Spieler {id+1}!")

        player = Player(namePlayer, id)

        self.__setShips(player)
        return player

    def __setShips(self, player):
        print(f"{player.name}! Setze deine Schiffe!")
        player.placeShips()

    def __loadGame(self):

        # TODO: Speicher laden lassen.

        print()


    def endGame(self, winner):
        print(f'{winner.name} Hat alle Schiffe seines Gegners ERMORDET!')

    def clear(self):
        print(f'Hi')




