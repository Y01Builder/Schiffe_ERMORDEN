from DTO.Map import Map
import re

class Player:

    #__ships = [["Schlachtschiff", 5, 1], ["Kreuzer", 4, 2], ["Zerstörer", 3, 3], ["Uboot", 2, 4]]
    __ships = [["Schlachtschiff", 5, 1]]
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.__map = Map(id)


    def printMap(self, showShips):
        print(f"\tA\tB\tC\tD\tE\tF\tG\tH\tI\tJ")
        print("")
        for row in range(0, 10):
            printable = [f"{row+1}"]
            for columns in range(0,10):
                if self.__map.fields[columns][row].shipOnField and showShips:
                    printable.append(f"\tO")
                elif self.__map.fields[columns][row].fieldHit:
                    printable.append(f"\tX")
                else:
                    printable.append(f"\t~")
            print(f"{printable[0]}{printable[1]}{printable[2]}{printable[3]}{printable[4]}{printable[5]}{printable[6]}{printable[7]}{printable[8]}{printable[9]}{printable[10]}")


    def shootField(self, opponent):
        repeat = True
        while repeat:
            coordinate = input(f"Bitte geben Sie die Koordinate des Zieles (z.B.B4) an!")
            validated = opponent.__validateCoordinate(coordinate)
            if not validated:
                print("Bitte versuchen Sie es erneut")
            else:
                if opponent.__map.hitField(validated):
                    repeat = False
                    if opponent.__map.shipTiles == 0:
                        return True
        return False

    def placeShips(self):
        for name, length, count in self.__ships:
            for i in range(0, count):
                repeat = True
                while repeat:
                    self.printMap(showShips=True)
                    coordinate = input(f"Bitte geben Sie die Startkoordinate für das Schiff {name} an! z.B. B4\n")
                    orientation = input(f"Bitte geben Sie die Orientierung für das Schiff {name} an! z.B. N, O, S, W\n")
                    splittedCoordinates = self.__validateCoordinate(coordinate)
                    validatedOrientation = self.__validateOrientation(orientation)
                    if not splittedCoordinates or not validatedOrientation:
                        print("Bitte versuchen Sie es erneut!")
                        repeat = True
                    else:
                        repeat = not self.__map.placeShips(splittedCoordinates, validatedOrientation, length)
        return

    def __validateCoordinate(self, coordinate):
        pattern = re.compile("^([a-jA-J])([1-9]|[1][0])?$")
        matches = pattern.match(coordinate)
        if matches:
            return matches.groups()
        else:
            print("Die Eingabe der Koordinaten war nicht korrekt!")
            return False
            #todo Exception werfen

    def __validateOrientation(self, orientation):
        pattern = re.compile("^[N,W,O,S]?$")
        matches = pattern.match(orientation)
        if matches:
            return matches.string
        else:
            print("Die Eingabe der Orientierung war nicht korrekt!")
            return False
            #todo Exception werfen







