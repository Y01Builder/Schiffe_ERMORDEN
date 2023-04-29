import json

from DTO.Field import Field
class Map:
    def __init__(self, ownerId, floatingShips = 0):
        self.floatingShips = floatingShips
        self.ownerId = ownerId
        self.fields: list[list[Field]] = []
        self.rows = 10
        self.columns = 10
        self.shipTiles = 30
        self.__initMap()
        #Anzahl an Feldern mit Schiffen zu Beginn des Spiels


    def placeShips(self, coordinate, orientation, length):
        #todo validate coordinate length
        xValue = ord(coordinate[0].lower()) - 97
        yValue = int(coordinate[1]) - 1
        if self.__validateShipPlacement(xValue, yValue, orientation, length):
            for i in range(0, length):
                self.fields[xValue][yValue].shipOnField = True
                if orientation == "S":
                    yValue += 1
                elif orientation == "N":
                    yValue -= 1
                elif orientation == "W":
                    xValue -= 1
                elif orientation == "O":
                    xValue += 1
        else:
            print("Das Schiff kann so nicht platziert werden! Probieren Sie es erneut!")
            return False
        return True

    def hitField(self, coordinate):
        xValue = ord(coordinate[0].lower()) - 97
        yValue = int(coordinate[1]) - 1
        actualField = self.fields[xValue][yValue]
        if actualField.fieldHit:
            print("Dieses Feld wurde bereits getroffen!")
            return False
        elif actualField.shipOnField:
            print("Schiff wurde getroffen!")
            self.shipTiles -= 1
            #Spiel Ende, wenn Tiles = 0
        else:
            print("Daneben!")
        actualField.fieldHit = True
        self.__saveMap(self.fields[0][0])
        return True

    def __saveMap(self, field):
        with open(f"mapPlayer{self.ownerId}.json", "w") as f:
            f.write(json.dumps(field, indent=2))
            #json.dumps(field, default=lambda o: o.dict, sort_keys=True, indent=4)

    def __initMap(self):
        print("")

        # Befüllen des 2D Arrays
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                row.append(Field(False, False))
            self.fields.append(row)


    def __validateShipPlacement(self, xValue, yValue, orientation, length):
        for i in range(0, length):
            # Iteriert durch Schiffe
            for j in range(-1,2):
                for k in range(-1,2):
                    # Iteriert durch die umliegenden Felder eines Schiffpunktes
                    if xValue+j < 0 or xValue+j >= 10 or yValue+k < 0 or yValue+k >= 10:
                        continue
                    else:
                        if self.fields[xValue+j][yValue+k].shipOnField:
                            return False

            # Checkt ob das Schiff außerhalb des Spielfelds liegen würde
            if xValue < 0 or xValue >= 10:
                return False
            elif yValue < 0 or yValue >= 10:
                return False

            # erweitert Schiff nach Orientierung
            if orientation == "S":
                yValue += 1
            elif orientation == "N":
                yValue -= 1
            elif orientation == "W":
                xValue -= 1
            elif orientation == "O":
                xValue += 1

        return True
