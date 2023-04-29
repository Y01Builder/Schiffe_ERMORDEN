import os
import sys
import json

from DTO.Player import Player

class Game:


    def __init__(self):
        self.player1 = self.__createPlayer(0)
        self.player2 = self.__createPlayer(1)

    def startGame(self):
        print("Spiel Beginn!")


        while True:

            if self.player1.shootField(self.player2):
                self.endGame(self.player1)
                break
            self.__saveGame(self.player1)
            self.__saveGame(self.player2)
            self.player1.printMap(showShips=True)
            self.player2.printMap(showShips=False)
            # Speichern
            if self.player2.shootField(self.player1):
                self.endGame(self.player2)
                break
            self.__saveGame(self.player1)
            self.__saveGame(self.player2)
            self.player2.printMap(showShips=True)
            self.player1.printMap(showShips=False)
            # Speichern
        return

    def __createPlayer(self, id):
        namePlayer = input(f"Bitte benennen Sie Spieler {id+1}!\n")

        player = Player(namePlayer, id)
        print("")
        self.__setShips(player)
        return player

    def __setShips(self, player):
        print(f"{player.name}! Setze deine Schiffe!")
        player.placeShips()
        return

    def __loadGame(self):

        # TODO: Speicher laden lassen.

        print()
        return

    def endGame(self, winner):
        print(f'{winner.name} Hat alle Schiffe seines Gegners ERMORDET!')

    def clear(self):
        if sys.platform == "win32":
            clear = "cls"
        else:
            clear = "clear"
        os.system(clear)
