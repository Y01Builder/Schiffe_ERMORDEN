from DTO.map import Map
import re


class Player:
    _ships = [["Schlachtschiff", 5, 1], ["Kreuzer", 4, 2], ["Zerstörer", 3, 3], ["Uboot", 2, 4]]
    # _ships = [["Schlachtschiff", 5, 1]]

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.map = Map(id)

    def printMap(self, showShips):
        try:
            print(f"\tA\tB\tC\tD\tE\tF\tG\tH\tI\tJ")
            print("")
            for row in range(0, 10):
                printable = [f"{row + 1}"]
                for columns in range(0, 10):
                    if self.map.fields[columns][row].shiponfield and showShips:
                        printable.append(f"\tO")
                    elif self.map.fields[columns][row].fieldhit:
                        printable.append(f"\tX")
                    else:
                        printable.append(f"\t~")
                print(
                    f"{printable[0]}{printable[1]}{printable[2]}{printable[3]}{printable[4]}{printable[5]}{printable[6]}{printable[7]}{printable[8]}{printable[9]}{printable[10]}")
        except Exception as e:
            print(f"Es ist ein Fehler in der Funktion 'printMap' aufgetreten! {e}")

    def shootField(self, opponent):
        try:
            repeat = True
            while repeat:
                coordinate = input(f"Bitte geben Sie die Koordinate des Zieles (z.B.B4) an!")
                validated = opponent._validateCoordinate(coordinate)
                if not validated:
                    print("Bitte versuchen Sie es erneut")
                else:
                    if opponent.map.hitField(validated):
                        repeat = False
                        if opponent.map.shipTiles == 0:
                            return True
            return False
        except KeyboardInterrupt:
            print("Sie haben den Vorgang mit Ihrer Eingabe abgebrochen!")
        except Exception as e:
            print(f"Es ist ein Fehler in der Funktion 'shootField' aufgetreten! {e}")

    def placeShips(self):
        try:
            for name, length, count in self.__ships:
                for i in range(0, count):
                    repeat = True
                    while repeat:
                        self.printMap(showShips=True)
                        coordinate = input(f"Bitte geben Sie die Startkoordinate für das Schiff {name} an! z.B. B4\n")
                        orientation = input(f"Bitte geben Sie die Orientierung für das Schiff {name} an! z.B. N, O, S, W\n")
                        splittedCoordinates = self._validateCoordinate(coordinate)
                        validatedOrientation = self._validateOrientation(orientation)
                        if not splittedCoordinates or not validatedOrientation:
                            print("Bitte versuchen Sie es erneut!")
                            repeat = True
                        else:
                            repeat = not self.map.placeShips(splittedCoordinates, validatedOrientation, length)
            return True
        except KeyboardInterrupt:
            print("Sie haben den Vorgang mit Ihrer Eingabe abgebrochen!")
        except Exception as e:
            print(f"Es ist ein Fehler in der Funktion 'placeShips' aufgetreten! {e}")
        return False

    def _validateCoordinate(self, coordinate):
        try:
            pattern = re.compile("^([a-jA-J])([1-9]|[1][0])$")
            matches = pattern.match(coordinate)
            if matches:
                return matches.groups()
            else:
                print("Die Eingabe der Koordinaten war nicht korrekt!")
                return False
        except Exception as e:
            print(f"Bei der Validierung der Koordinaten ist ein Fehler aufgetreten! Bitte prüfen Sie die Werte! {e}")

    def _validateOrientation(self, orientation):
        try:
            pattern = re.compile("^[N,W,O,S]?$")
            matches = pattern.match(orientation)
            if matches:
                return matches.string
            else:
                print("Die Eingabe der Orientierung war nicht korrekt!")
                return False
        except Exception as e:
            print(f"Bei der Validierung der Orientierung ist ein Fehler aufgetreten! Bitte prüfen Sie die Werte! {e}")
