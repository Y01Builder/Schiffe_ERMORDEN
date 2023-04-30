"""import Map and regex"""
import re
from DTO.map import Map


class Player:
    """the player class contains all actions from the player like shoot,place ships and print map"""
    #_ships = [["Schlachtschiff", 5, 1], ["Kreuzer", 4, 2], ["Zerstörer", 3, 3], ["Uboot", 2, 4]]
    _ships = [["Schlachtschiff", 5, 1]]

    def __init__(self, name, playerid):
        self.name = name
        self.playerid = playerid
        self.map = Map(playerid)

    def print_map(self, show_ships):
        """prints the user map"""
        try:
            print("\tA\tB\tC\tD\tE\tF\tG\tH\tI\tJ")
            print("")
            for row in range(0, 10):
                printable = [f"{row + 1}"]
                for columns in range(0, 10):
                    if self.map.fields[columns][row].shiponfield and show_ships:
                        printable.append("\tO")
                    elif self.map.fields[columns][row].fieldhit:
                        printable.append("\tX")
                    else:
                        printable.append("\t~")
                print(
                    f"{printable[0]}{printable[1]}{printable[2]}{printable[3]}{printable[4]}{printable[5]}{printable[6]}"
                    f"{printable[7]}{printable[8]}{printable[9]}{printable[10]}")
        except IndexError:
            print("Es ist ein Fehler 'player.print_map' bei der Verwendung des Indexes aufgetreten!")

    def shoot_field(self, opponent):
        """fire on the opponent field"""
        try:
            repeat = True
            while repeat:
                coordinate = input("Bitte geben Sie die Koordinate des Zieles (z.B.B4) an!")
                validated = opponent.validate_coordinate(coordinate)
                if not validated:
                    print("Bitte versuchen Sie es erneut")
                else:
                    if opponent.map.hit_field(validated):
                        repeat = False
                        if opponent.map.ship_tiles == 0:
                            return True
            return False
        except KeyboardInterrupt:
            print("Sie haben den Vorgang mit Ihrer Eingabe abgebrochen!")
            return False

    def place_ships(self):
        """iterate all ships to set their orientation and coordinates"""
        try:
            for name, length, count in self._ships:
                for _ in range(0, count):
                    repeat = True
                    while repeat:
                        self.print_map(show_ships=True)
                        coordinate = input(f"Bitte geben Sie die Startkoordinate für das Schiff {name} an! z.B. B4\n")
                        orientation = input(f"Bitte geben Sie die Orientierung für das Schiff {name} an! z.B. N, O, S, W\n")
                        splitted_coordinates = self.validate_coordinate(coordinate)
                        validated_orientation = self._validate_orientation(orientation)
                        if not splitted_coordinates or not validated_orientation:
                            print("Bitte versuchen Sie es erneut!")
                            repeat = True
                        else:
                            repeat = not self.map.place_ships(splitted_coordinates, validated_orientation, length)
            return True
        except KeyboardInterrupt:
            print("Sie haben den Vorgang mit Ihrer Eingabe abgebrochen!")
        return False

    def validate_coordinate(self, coordinate):
        """validate entered coordinate with regex"""
        try:
            pattern = re.compile("^([a-jA-J])([1-9]|[1][0])$")
            matches = pattern.match(coordinate)
            if matches:
                return matches.groups()

            print("Die Eingabe der Koordinaten war nicht korrekt!")
            return False
        except TypeError:
            print("Bei der Validierung der Koordinaten ist ein Typen Fehler aufgetreten! Bitte prüfen Sie die Werte!")
            return False

    def _validate_orientation(self, orientation):
        try:
            pattern = re.compile("^[N,W,O,S]$")
            matches = pattern.match(orientation)
            if matches:
                return matches.string

            print("Die Eingabe der Orientierung war nicht korrekt!")
            return False
        except TypeError:
            print("Bei der Validierung der Orientierung ist ein Typen Fehler aufgetreten! Bitte prüfen Sie die Werte!")
            return False
