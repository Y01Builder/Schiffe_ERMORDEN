#pylint: disable=E0401
"""import modules"""
import os
import pickle
import sys
from DTO.player import Player
from DTO.bot_player import BotPlayer


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

        self.clear()

        try:
            print("Spiel Beginn!")
            print("")

            # if save files exist: try to load them.
            if os.path.exists(rf"{self.path}\mapPlayer{self.player1.playerid + 1}.pickle") and os.path.exists(
            rf"{self.path}\mapPlayer{self.player2.playerid + 1}.pickle"):

                self.player1 = self.__load_game(self.player1)
                self.player2 = self.__load_game(self.player2)

                if not self.player1 or not self.player2:

                    bot = self.__startscreen()

                    # create new players, when the save file can not be loaded
                    print("Vorhin ist ein Fehler beim Laden aufgetreten! Erstelle neue Spieler.")
                    self.player1 = self.__create_player(0)
                    self.player2 = self.__create_player(1, bot)
            else:

                bot = self.__startscreen()

                # create new players, when there is no save file
                self.player1 = self.__create_player(0)
                self.player2 = self.__create_player(1, bot)

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

                # check before going to the next player (except bot), as to stop the opponent from seeing your map
                self.clear()
                if not self.player1.turn and self.player2.turn and self.player2.is_bot:
                    pass
                else:
                    input("Spieler bereit?")
                    print("")

            # return to main, once the game has ended
            return
        except KeyboardInterrupt:
            print("Sie haben den Vorgang mit Ihrer Eingabe abgebrochen!")
            sys.exit(0)

    def __startscreen(self):
        self.__print_kill_ship()
        repeat = True
        while repeat:
            print("Welche Option soll es sein? (1 oder 2)")
            print("1. 1 Spieler: Player vs. Computer")
            print("2. 2 Spieler: Player vs. Player")
            mode = input("")
            print("")

            match mode:
                case "1":
                    init_bot = True
                    repeat = False
                case "2":
                    init_bot = False
                    difficulty = 1
                    repeat = False
                case _:
                    print("Fehler bei der Eingabe!")
                    repeat = True

        if init_bot:
            repeat = True
            while repeat:
                print("Welche Schwierigkeitsstufe soll es sein?")
                print("1. Rekrut  (Einfach)")
                print("2. Marine  (Medium)")
                print("3. Veteran (Schwer)")
                difficulty = input("")
                print("")

                match difficulty:
                    case "1":
                        repeat = False
                        difficulty = 0
                    case "2":
                        repeat = False
                        difficulty = 1
                    case "3":
                        repeat = False
                        difficulty = 2
                    case _:
                        print("Fehler bei der Eingabe!")
                        print("")
                        repeat = True

        repeat = True
        while repeat:
            rules = input("Möchten sie die Regeln erneut sehen? (J/N)\n")
            match rules:
                case "J":
                    self.clear()
                    self.__print_kill_ship_rules()
                    input("Zum Fortfahren Enter druecken...")
                    repeat = False
                case "N":
                    repeat = False
                case _:
                    print("Fehler bei der Eingabe!")
                    print("")
                    repeat = True
        self.clear()
        return init_bot, difficulty

    def __print_kill_ship_rules(self):
        print("Regeln für Schiffe ermorden:")
        print("")
        print("1. Jeder Spieler hat 1 Schlachtschiff (5 Felder), 2 Kreuzer (4 Felder), 3 Zerstörer ",
              "(3 Felder) und 4 U-Boote (2 Felder)")
        print("2. deine Schiffe dürfen sich nicht berühren")
        print("3. Die Spieler schießen nacheinander auf die Karte des Gegners")
        print("4. Der Spieler, der zuerst alle gegnerischen Schiffe komplett ermordet hat, hat gewonnen.")
        print("")

    def __print_kill_ship(self):
        self.clear()

        print("")
        print("Willkommen! Zu...")
        print("")
        print("")
        print("   _____      _     _  __  __           ______ _____  __  __  ____  _____  ______ _   _   _ ")
        print("  / ____|    | |   (_)/ _|/ _|         |  ____|  __ \|  \/  |/ __ \|  __ \|  ____| \ | | | |")# pylint: disable=anomalous-backslash-in-string
        print(" | (___   ___| |__  _| |_| |_ ___      | |__  | |__) | \  / | |  | | |  | | |__  |  \| | | |")# pylint: disable=anomalous-backslash-in-string
        print("  \___ \ / __| '_ \| |  _|  _/ _ \     |  __| |  _  /| |\/| | |  | | |  | |  __| | . ` | | |")# pylint: disable=anomalous-backslash-in-string
        print("  ____) | (__| | | | | | | ||  __/     | |____| | \ \| |  | | |__| | |__| | |____| |\  | |_|")# pylint: disable=anomalous-backslash-in-string
        print(" |_____/ \___|_| |_|_|_| |_| \___|     |______|_|  \_\_|  |_|\____/|_____/|______|_| \_| (_)")# pylint: disable=anomalous-backslash-in-string
        print("")

    def __create_player(self, playerid, bot=None):
        """creates the player object and set the ships"""
        if bot is None:
            bot = [False, 1]
        try:
            print("")

            if not bot[0]:
                # get Name of player and create the object if the mode chosen is PvP
                name_player = input(f"Bitte benennen Sie Spieler {playerid + 1}!\n")
                player = Player(name_player, playerid)
                print("")

                # let the player place his ships
                self.__set_ships(player)
            else:
                # create a Bot, if the mode chosen is PvC
                name_player = "Jack Sparrow"
                player = BotPlayer(name_player, playerid, difficulty=bot[1])

                # let the bot place its ships
                player.place_ships()
            # clear the screen
            self.clear()

            # return the player object
            return player
        except KeyboardInterrupt:
            print("Sie haben den Vorgang mit Ihrer Eingabe abgebrochen!")
            sys.exit(0)

    def __set_ships(self, player):
        # call the place_ships function on the new player
        self.clear()
        print(f"{player.name}! Setze deine Schiffe!")
        return player.place_ships()

    def __player_turn(self, player, opponent):
        # prints ASCII art of the player
        if not player.is_bot:
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
        except MemoryError:
            print(f"Die Datei mapPlayer{player.playerid + 1}.pickle ist beschädigt und konnte nicht geladen werden!")
        except pickle.UnpicklingError:
            print(f"Die Datei mapPlayer{player.playerid + 1}.pickle war defekt!")
        return False

    def end_game(self, winner):
        """ends the game with a print and deleting game files"""
        try:
            # print "Winner!" ASCII art
            self.clear()
            print(" __          ___                       _ ")
            print(" \ \        / (_)                     | |")# pylint: disable=anomalous-backslash-in-string
            print("  \ \  /\  / / _ _ __  _ __   ___ _ __| |")# pylint: disable=anomalous-backslash-in-string
            print("   \ \/  \/ / | | '_ \| '_ \ / _ \ '__| |")# pylint: disable=anomalous-backslash-in-string
            print("    \  /\  /  | | | | | | | |  __/ |  |_|")# pylint: disable=anomalous-backslash-in-string
            print("     \/  \/   |_|_| |_|_| |_|\___|_|  (_)")# pylint: disable=anomalous-backslash-in-string
            print("")

            # print the winner and delete current save files
            print(f'{winner.name} Hat alle Schiffe seines Gegners ERMORDET!')

            # check for OS and use the according path seperator
            if sys.platform == "win32":
                os.remove(f"{self.path}\mapPlayer1.pickle")
                os.remove(f"{self.path}\mapPlayer2.pickle")
            else:
                os.remove(f"{self.path}/mapPlayer1.pickle")
                os.remove(f"{self.path}/mapPlayer2.pickle")

            input("Drücke Enter um fortzufahren...")
        except FileNotFoundError:
            print(f"Beim löschen der Datei ist ein Fehler aufgetreten {self.path}!")

    def clear(self):
        """clear the console window"""
        try:
            # check for OS and set the according "clear screen" command
            if sys.platform == "win32":
                clearcommand = "cls"
            else:
                clearcommand = "clear"

            # execute the "clear screen" command
            os.system(clearcommand)
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
