from DTO.Player import Player

class Game:


    def __init__(self):
        return
    def startGame(self):
        print("Spiel Beginn!")
        player1 = self.__createPlayer(0)
        player2 = self.__createPlayer(1)


        while True:

            if player1.shootField(player2):
                self.endGame(player1)
                break
            player1.printMap(showShips=True)
            player2.printMap(showShips=False)
            # Speichern
            if player2.shootField(player1):
                self.endGame(player2)
                break
            player2.printMap(showShips=True)
            player1.printMap(showShips=False)
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
        print(f'Hi')




