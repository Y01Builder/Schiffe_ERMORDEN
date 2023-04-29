from DTO.Map import Map
import re

class Player:

    #_ships = [["Schlachtschiff", 5, 1], ["Kreuzer", 4, 2], ["Zerstörer", 3, 3], ["Uboot", 2, 4]]
    _ships = [["Schlachtschiff", 5, 1]]
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self._map = Map(id)


    def printMap(self, showShips):
        print(f"\tA\tB\tC\tD\tE\tF\tG\tH\tI\tJ")
        print("")
        for row in range(0, 10):
            printable = [f"{row+1}"]
            for columns in range(0,10):
                if self._map.fields[columns][row].shipOnField and showShips:
                    printable.append(f"\tO")
                elif self._map.fields[columns][row].fieldHit:
                    printable.append(f"\tX")
                else:
                    printable.append(f"\t~")
            print(f"{printable[0]}{printable[1]}{printable[2]}{printable[3]}{printable[4]}{printable[5]}{printable[6]}{printable[7]}{printable[8]}{printable[9]}{printable[10]}")


    def shootField(self, opponent):
        repeat = True
        while repeat:
            coordinate = input(f"Bitte geben Sie die Koordinate des Zieles (z.B.B4) an!")
            validated = opponent._validateCoordinate(coordinate)
            if not validated:
                print("Bitte versuchen Sie es erneut")
            else:
                if opponent._map.hitField(validated):
                    repeat = False
                    if opponent._map.shipTiles == 0:
                        return True
        return False

    def placeShips(self):
        for name, length, count in self._ships:
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
                        repeat = not self._map.placeShips(splittedCoordinates, validatedOrientation, length)
        return

    def _validateCoordinate(self, coordinate):
        pattern = re.compile("^([a-jA-J])([1-9]|[1][0])?$")
        matches = pattern.match(coordinate)
        if matches:
            return matches.groups()
        else:
            print("Die Eingabe der Koordinaten war nicht korrekt!")
            return False
            #todo Exception werfen

    def _validateOrientation(self, orientation):
        pattern = re.compile("^[N,W,O,S]?$")
        matches = pattern.match(orientation)
        if matches:
            return matches.string
        else:
            print("Die Eingabe der Orientierung war nicht korrekt!")
            return False
            #todo Exception werfen







