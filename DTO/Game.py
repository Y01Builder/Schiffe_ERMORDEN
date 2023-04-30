import os
import pickle
import sys

from DTO.Player import Player


class Game:

    def __init__(self, path):

        # set players as a standard player object in case of an error
        self.player1 = Player("User1", 0)
        self.player2 = Player("User2", 1)

        # get path of main.py to load and save the player objects
        self.path = path

    def startGame(self):
        try:
            print("Spiel Beginn!")
            print("")

            # if save files exist: try to load them.
            if os.path.exists(f"{self.path}\mapPlayer{self.player1.id + 1}.pickle") and os.path.exists(
                    f"{self.path}\mapPlayer{self.player2.id + 1}.pickle"):
                try:
                    self.player1 = self.__loadGame(self.player1)
                    self.player2 = self.__loadGame(self.player2)
                except:
                    # create new players, when the save file can not be loaded
                    print("Ein Fehler ist beim Laden aufgetreten! Erstelle neue Spieler.")
                    self.player1 = self.__createPlayer(0)
                    self.player2 = self.__createPlayer(1)
            else:

                # create new players, when there is no save file
                self.player1 = self.__createPlayer(0)
                self.player2 = self.__createPlayer(1)

            # loop attacks while no player has won
            while True:

                # clear the screen
                self.clear()

                # check if it is player 1's turn
                if self.player1.turn and not self.player2.turn:

                    # break the loop, if the Turn returns end of game
                    if self.__playerTurn(player=self.player1, opponent=self.player2):
                        break

                # check if it is player 2's turn
                elif self.player2.turn and not self.player1.turn:

                    # break the loop, if the Turn returns end of game
                    if self.__playerTurn(player=self.player2, opponent=self.player1):
                        break

                else:
                    # player 1 will start, if no save file can be found
                    self.player1.turn = True
                    self.player2.turn = False

            # return to main, once the game has ended
            return
        except KeyboardInterrupt:
            print("Sie haben den Vorgang mit Ihrer Eingabe abgebrochen!")
        except Exception as e:
            print(f"Es ist ein Fehler in der Funktion 'startGame' aufgetreten! {e}")


    def __createPlayer(self, id):
        try:
            print("")

            # get Name of player and create the object
            namePlayer = input(f"Bitte benennen Sie Spieler {id + 1}!\n")
            player = Player(namePlayer, id)
            print("")

            # let the player place his ships
            self.__setShips(player)

            # clear the screen
            self.clear()

            # return the player object
            return player
        except KeyboardInterrupt:
            print("Sie haben den Vorgang mit Ihrer Eingabe abgebrochen!")
        except Exception as e:
            print(f"Es ist ein Fehler in der Funktion 'Game.__createPlayer' aufgetreten! {e}")

    def __setShips(self, player):
        try:
            # call the placeShips function on the new player
            print(f"{player.name}! Setze deine Schiffe!")
            player.placeShips()
            return True
        except Exception as e:
            print(f"Es ist ein Fehler in der Funktion 'Game.__setShips' aufgetreten! {e}")

    def __playerTurn(self, player, opponent):
        try:
            # prints ASCII art of the player
            self.__printPlayer(player.id)

            # show maps of opponent (top) and player (bottom)
            opponent.printMap(showShips=False)
            player.printMap(showShips=True)

            # the loop will break, if the shootField method returns end of game
            if player.shootField(opponent):
                self.endGame(player)
                return True

            # save after each hit, as to prevent data loss
            self.__saveMap(self.player1)
            self.__saveMap(self.player2)

            return False
        except Exception as e:
            print(f"Es ist ein Fehler in der Funktion 'Game.__playerTurn' aufgetreten! {e}")

    def __saveMap(self, player):
        try:
            # save the player object into the mapPlayerX.pickle file
            with open(f"mapPlayer{player.id + 1}.pickle", "wb") as f:
                pickle.dump(player, f)
        except Exception as e:
            print(f"Es ist ein Fehler in der Funktion 'Game.__saveMap' aufgetreten! {e}")


    def __loadGame(self, player):
        try:
            # load the player object from the mapPlayerX.pickle file
            with open(f"mapPlayer{player.id + 1}.pickle", "rb") as f:
                player = pickle.load(f)

            # return the player object
            return player
        except PermissionError:
            print(f"Sie haben keine Berechtigung auf die Datei oder Ordner zuzugreifen!")
        except FileNotFoundError:
            print(f"Die Datei mapPlayer{player.id + 1}.pickle war nicht vorhanden!")
        except Exception as e:
            print(f"Es ist ein Fehler in der Funktion 'Game.__loadGame' aufgetreten! {e}")

    def endGame(self, winner):
        try:
            # print the winner and delete current save files
            print(f'{winner.name} Hat alle Schiffe seines Gegners ERMORDET!')
            os.remove(f"{self.path}\mapPlayer1.pickle")
            os.remove(f"{self.path}\mapPlayer2.pickle")
        except Exception as e:
            print(f"Es ist ein Fehler in der Funktion 'Game.endGame' aufgetreten! {e}")

    def clear(self):
        try:
            # check for OS and set the according "clear screen" command
            if sys.platform == "win32":
                clear = "cls"
            else:
                clear = "clear"

            # execute the "clear screen" command
            os.system(clear)
        except Exception as e:
            print(f"Es ist ein Fehler in der Funktion 'Game.clear' aufgetreten! {e}")

    def __printPlayer(self, id):
        if id == 0:

            # print "Spieler 1" in ASCII art
            print("  ____        _      _             _ ")
            print(" / ___| _ __ (_) ___| | ___ _ __  / |")
            print(" \___ \| '_ \| |/ _ \ |/ _ \ '__| | |")
            print("  ___) | |_) | |  __/ |  __/ |    | |")
            print(" |____/| .__/|_|\___|_|\___|_|    |_|")
            print("       |_|")
            print("")

        elif id == 1:

            # print "Spieler 2" in ASCII art
            print("  ____        _      _             ____  ")
            print(" / ___| _ __ (_) ___| | ___ _ __  |___ \ ")
            print(" \___ \| '_ \| |/ _ \ |/ _ \ '__|   __) |")
            print("  ___) | |_) | |  __/ |  __/ |     / __/ ")
            print(" |____/| .__/|_|\___|_|\___|_|    |_____|")
            print("       |_|")
            print("")
