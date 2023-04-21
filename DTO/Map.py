from DTO.Field import Field
class Map:
    def __init__(self, ownerId, floatingShips = 0):
        self.floatingShips = floatingShips
        self.ownerId = ownerId
        self.fields = Field[10][10]

    def printThisMap(self, showShips):
        print(f'Hi')
        return

    def placeShips(coordinate, orientation, length):
        #todo validate coordinate length
        xValue = ord(coordinate[0].lower()) - 96
        yValue = coordinate[1] - 1
        for i in range(1, length):
            if orientation == "S":
                print("")
                #self.fields[yValue][xValue-i]
            elif orientation == "N":
                print("")
            elif orientation == "W":
                print("")
            elif orientation == "O":
                print("")
        return
    def __initMap(self):
        print("")

