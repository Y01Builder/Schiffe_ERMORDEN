from DTO.Field import Field


class Map:
    def __init__(self, ownerId, floatingShips = 0):
        self.floatingShips = floatingShips
        self.ownerId = ownerId
        self.fields = Field[10][10]
        self.__initMap()

    def printThisMap(self, showShips):
        print("/tA/tB/tC/TD/TE/tF/tG/tH/TI/TJ")
        for i in range(1, 10):
            print(f"{i}")
        return

    def placeShips(self, coordinate, orientation, length):
        #todo validate coordinate length
        #todo ggf Rollback falls Schiffe nicht vollständig gesetzt werden können oder vorher abfragen
        xValue = ord(coordinate[0].lower()) - 96
        yValue = coordinate[1] - 1
        for i in range(1, length):
            if orientation == "S":
                yValue += 1
            elif orientation == "N":
                yValue -= 1
            elif orientation == "W":
                xValue -= 1
            elif orientation == "O":
                xValue += 1
            self.fields[xValue][yValue].shipOnField = True
        return True

    def hitField(self, coordinate):
        #todo validate coordinate
        xValue = ord(coordinate[0].lower()) - 96
        yValue = coordinate[1] - 1
        actualField = self.fields[xValue][yValue]
        if actualField.shipOnField:
            print("Schiff wurde getroffen!")
            #todo Prüfen ob Schiff versunken / Spiel Ende?
        actualField.fieldHit = True

        return True

    def __validateShipPlacement(self, xValue, yValue):
        if xValue < 0 or xValue >= 10:
            #Exception werfen
            print("Koordinaten dürfen nicht außerhalb des Spielfelds liegen!")
            return False
        elif yValue < 0 or yValue >= 10:
            #Exception werfen
            print("Koordinaten dürfen nicht außerhalb des Spielfelds liegen!")
            return False
        elif self.fields[xValue][yValue].shipOnField == 1:
            #Exception werfen
            print("Schiffe dürfen nicht aufeinander platziert werden!")
            return False
        return True

    def __initMap(self):
        for column in self.fields:
            for row in self.fields[column]:
                self.fields[column][row] = Field(0, 0)

