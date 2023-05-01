"""import Map and regex"""
import re
from DTO.map import Map


class Player:
    """the player class contains all actions from the player like shoot,place ships and print map"""
    # create array of all ships that a player has to have: [name, length, number]
    #_ships = [["Schlachtschiff", 5, 1], ["Kreuzer", 4, 2], ["Zerstörer", 3, 3], ["Uboot", 2, 4]]
    _ships = [["Schlachtschiff", 5, 1]]

    def __init__(self, name, playerid):
        # set name and ID of player
        self.name = name
        self.playerid = playerid
        # link map object to the player ID
        self.map = Map(playerid)
        # bool to save whose turn it is after loading a savefile.
        self.turn = False

    def print_map(self, show_ships):
        """prints the user map. If show_ships == True, all ships will be shown"""
        try:
            print("")
            print(f"Karte von {self.name}:")
            print("\tA\tB\tC\tD\tE\tF\tG\tH\tI\tJ")

            # iterating through rows
            for row in range(0, 10):

                # create array of current row and add row number to begin with
                printable = [f"{row + 1}"]

                # iterate through columns of the map
                for columns in range(0, 10):

                    if self.__map.fields[columns][row].shipOnField:
                        if self.__map.fields[columns][row].fieldHit:
                            # add Ø when there is a ship and it is hit
                            printable.append(f"\tØ")

                        elif show_ships:
                            # add O when there is a ship and user has permission to see it
                            printable.append(f"\tO")

                        else:
                            # add ~ when there is a ship that has not been hit and the user has no permission to see it
                            printable.append(f"\t~")

                    elif self.__map.fields[columns][row].fieldHit:
                        # add X when there is no ship and the field is hit
                        printable.append(f"\tX")

                    else:
                        # add ~ in all other cases
                        printable.append(f"\t~")

                # print the array of the current row and move to the next one
                print(
                    f"{printable[0]}{printable[1]}{printable[2]}{printable[3]}{printable[4]}{printable[5]}{printable[6]}"
                    f"{printable[7]}{printable[8]}{printable[9]}{printable[10]}")

                # spacing between map and following text
                print("")
                print("")

        except IndexError:
            print("Es ist ein Fehler 'player.print_map' bei der Verwendung des Indexes aufgetreten!")

    def shoot_field(self, opponent):
        """fire on the opponent field"""
        try:
            # repeat while the shot has not been successful
            repeat = True
            while repeat:

                # input of target coordinates
                coordinate = input("Bitte geben Sie die Koordinate des Zieles (z.B.B4) an!\n")

                # validate given coordinates
                validated = opponent.validate_coordinate(coordinate)
                if not validated:
                    print("Bitte versuchen Sie es erneut")
                else:

                    # try to hit the validated coordinates
                    if opponent.map.hit_field(validated):
                        # when the hit was successful: stop the loop, end your turn and set turn of next player
                        repeat = False
                        self.turn = False
                        opponent.turn = True

                        # check before going to the next player, as to stop the opponent from seeing your map
                        input("Nächster Spieler bereit?")

                        # return end of game, when the last ship tile of the opponent has been sunk.
                        if opponent.map.ship_tiles == 0:
                            return True

            # return ongoing game, when the opponent has floating ship tiles left
            return False
        except KeyboardInterrupt:
            print("Sie haben den Vorgang mit Ihrer Eingabe abgebrochen!")
            return False

    def place_ships(self):
        """iterate all ships to set their orientation and coordinates"""
        try:
            # iterate through each ship type
            for name, length, count in self._ships:

                # iterate through the number of ships of current ship type
                for _ in range(0, count):

                    # repeat until ship has been successfully placed
                    repeat = True
                    while repeat:

                        # print map of current player
                        self.print_map(show_ships=True)

                        # input coordinate and orientation
                        coordinate = input(f"Bitte geben Sie die Startkoordinate für das Schiff {name} an! z.B. B4\n")
                        orientation = input(f"Bitte geben Sie die Orientierung für das Schiff {name} an! z.B. N, O, S, W\n")

                        # split and validate coordinates and orientation
                        splitted_coordinates = self.validate_coordinate(coordinate)
                        validated_orientation = self._validate_orientation(orientation)

                        # if any check failed, repeat the coordinate selection.
                        if not splitted_coordinates or not validated_orientation:
                            print("Bitte versuchen Sie es erneut!")
                            repeat = True
                        else:
                            # if ship placement returns success, the loop will stop, because repeat == False
                            repeat = not self.map.place_ships(splitted_coordinates, validated_orientation, length)

            # return successful ship placement
            return True
        except KeyboardInterrupt:
            print("Sie haben den Vorgang mit Ihrer Eingabe abgebrochen!")
        return False

    def validate_coordinate(self, coordinate):
        """validate entered coordinate with regex"""
        try:
            # check input via regular expression. It needs to contain one letter between A & J + a number between 1 & 10
            pattern = re.compile("^([a-jA-J])([1-9]|[1][0])$")

            # load matches into variable
            matches = pattern.match(coordinate)
            if matches:

                # if a match has been found it will be returned
                return matches.groups()

            # if no match has been found, the validation  will return a failure.
            print("Die Eingabe der Koordinaten war nicht korrekt!")
            return False
        except TypeError:
            print("Bei der Validierung der Koordinaten ist ein Typen Fehler aufgetreten! Bitte prüfen Sie die Werte!")
            return False

    def _validate_orientation(self, orientation):
        """validate entered orientation with regex"""
        try:
            # check input via regular expression. It needs to contain either N, W, O or S
            pattern = re.compile("^[N,W,O,S]?$")

            # load matches into variable
            matches = pattern.match(orientation)
            if matches:

                # if a match has been found it will be returned
                return matches.string

            # if no match has been found, the validation  will return a failure.
            print("Die Eingabe der Orientierung war nicht korrekt!")
            return False
        except TypeError:
            print("Bei der Validierung der Orientierung ist ein Typen Fehler aufgetreten! Bitte prüfen Sie die Werte!")
            return False