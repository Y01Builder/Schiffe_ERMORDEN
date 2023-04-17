from DTO.Map import Map


class Player:

    __map = Map(id)
    __ships = [["Schlachtschiff", 5, 1], ["Kreuzer", 4, 2], ["Zerstörer", 3, 3], ["Uboot", 2, 4]]
    def __init__(self, name, id):
        self.name = name
        self.id = id


    def printMap(self, showShips):

        print("")

    def shootField(self):
        print(f'Hi')
        return True

    def placeShips(self, coordinate):
        for name, length, count in self.__ships:
            for i in range(1,count):
                coordinate = input(f"Bitte geben Sie die Startkoordinate für das Schiff {name} an! z.B. B4")
                orientation = input(f"Bitte geben Sie die Orientierung für das Schiff {name} an! z.B. N, O, S, W")
                self.__validateCoordinate(coordinate)
        input("Bitte geben Sie die Platzierung der Schiffe an:")
        self.__map.placeShips(coordinate)

    def __validateCoordinate(self,coordinate):
        print("Validiere Koordinate")





