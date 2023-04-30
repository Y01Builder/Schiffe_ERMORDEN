"""import modules"""
import os
import pickle
import sys
from DTO.player import Player


class Game:
    """the game class manages the game functions"""
    def __init__(self, path):

        # set players as a standard player object in case of an error
        self.player1 = Player("User1", 0)
        self.player2 = Player("User2", 1)

        # get path of main.py to load and save the player objects
        self.path = path

    def start_game(self):
        """starts the game and check if old game exists (then load the old game)"""
        try:
            print("Spiel Beginn!")
            print("")

            # if save files exist: try to load them.
            if os.path.exists(rf"{self.path}\mapPlayer{self.player1.playerid + 1}.pickle") and os.path.exists(
                    rf"{self.path}\mapPlayer{self.player2.playerid + 1}.pickle"):
                self.player1 = self.__load_game(self.player1)
                self.player2 = self.__load_game(self.player2)

                if not self.player1 or not self.player2:
                    # create new players, when the save file can not be loaded
                    print("Ein Fehler ist beim Laden aufgetreten! Erstelle neue Spieler.")
                    self.player1 = self.__create_player(0)
                    self.player2 = self.__create_player(1)
            else:

                # create new players, when there is no save file
                self.player1 = self.__create_player(0)
                self.player2 = self.__create_player(1)

            # loop attacks while no player has won
            while True:

                # clear the screen
                self.clear()

                # check if it is player 1's turn
                if self.player1.turn and not self.player2.turn:

                    # break the loop, if the Turn returns end of game
                    if self.__player_turn(player=self.player1, opponent=self.player2):
                        break

                # check if it is player 2's turn
                elif self.player2.turn and not self.player1.turn:

                    # break the loop, if the Turn returns end of game
                    if self.__player_turn(player=self.player2, opponent=self.player1):
                        break

                else:
                    # player 1 will start, if no save file can be found
                    self.player1.turn = True
                    self.player2.turn = False

            # return to main, once the game has ended
            return
        except KeyboardInterrupt:
            print("Sie haben den Vorgang mit Ihrer Eingabe abgebrochen!")

    def __create_player(self, playerid):
        """creates the player object and set the ships"""
        try:
            print("")

            # get Name of player and create the object
            name_player = input(f"Bitte benennen Sie Spieler {playerid + 1}!\n")
            player = Player(name_player, playerid)
            print("")

            # let the player place his ships
            self.__set_ships(player)

            # clear the screen
            self.clear()

            # return the player object
            return player
        except KeyboardInterrupt:
            print("Sie haben den Vorgang mit Ihrer Eingabe abgebrochen!")
            return False

    def __set_ships(self, player):
        # call the place_ships function on the new player
        print(f"{player.name}! Setze deine Schiffe!")
        return player.place_ships()

    def __player_turn(self, player, opponent):
        # prints ASCII art of the player
        self.__print_player(player.playerid)

        # show maps of opponent (top) and player (bottom)
        opponent.print_map(show_ships=False)
        player.print_map(show_ships=True)

        # the loop will break, if the shoot_field method returns end of game
        if player.shoot_field(opponent):
            self.end_game(player)
            return True

        # save after each hit, as to prevent data loss
        self.__save_map(self.player1)
        self.__save_map(self.player2)

        return False

    def __save_map(self, player):
        try:
            # save the player object into the mapPlayerX.pickle file
            with open(f"mapPlayer{player.playerid + 1}.pickle", "wb") as file:
                pickle.dump(player, file)
        except IOError:
            print("Fehler beim schreiben/lesen der Datei in __save_map")
        except pickle.PickleError:
            print("Es ist ein Fehler in der Pickle Komponente aufgetreten!")

    def __load_game(self, player):
        try:
            # load the player object from the mapPlayerX.pickle file
            with open(f"mapPlayer{player.playerid + 1}.pickle", "rb") as file:
                player = pickle.load(file)
            # return the player object
            return player
        except PermissionError:
            print("Sie haben keine Berechtigung auf die Datei oder Ordner zuzugreifen!")
        except FileNotFoundError:
            print(f"Die Datei mapPlayer{player.playerid + 1}.pickle war nicht vorhanden!")
        return False

    def end_game(self, winner):
        """ends the game with a print and deleting game files"""
        try:
            # print the winner and delete current save files
            print(f'{winner.name} Hat alle Schiffe seines Gegners ERMORDET!')
            os.remove(rf"{self.path}\mapPlayer1.pickle")
            os.remove(rf"{self.path}\mapPlayer2.pickle")
        except FileNotFoundError:
            print(f"Beim löschen der Datei ist ein Fehler aufgetreten {self.path}!")

    def clear(self):
        """clear the console window"""
        try:
            # check for OS and set the according "clear screen" command
            if sys.platform == "win32":
                clear = "cls"
            else:
                clear = "clear"

            # execute the "clear screen" command
            os.system(clear)
        except NameError:
            print("Ein Problem beim importieren der Bibliotheken ist aufgetreten!")

    def __print_player(self, playerid):
        if playerid == 0:

            # print "Spieler 1" in ASCII art
            print("  ____        _      _             _ ")
            print(" / ___| _ __ (_) ___| | ___ _ __  / |")
            print(" \___ \| '_ \| |/ _ \ |/ _ \ '__| | |")  # pylint: disable=anomalous-backslash-in-string
            print("  ___) | |_) | |  __/ |  __/ |    | |")
            print(" |____/| .__/|_|\___|_|\___|_|    |_|")  # pylint: disable=anomalous-backslash-in-string
            print("       |_|")
            print("")

        elif playerid == 1:

            # print "Spieler 2" in ASCII art
            print("  ____        _      _             ____  ")
            print(" / ___| _ __ (_) ___| | ___ _ __  |___ \ ")  # pylint: disable=anomalous-backslash-in-string
            print(" \___ \| '_ \| |/ _ \ |/ _ \ '__|   __) |")  # pylint: disable=anomalous-backslash-in-string
            print("  ___) | |_) | |  __/ |  __/ |     / __/ ")
            print(" |____/| .__/|_|\___|_|\___|_|    |_____|")  # pylint: disable=anomalous-backslash-in-string
            print("       |_|")
            print("")
