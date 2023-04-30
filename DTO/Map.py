from DTO.Field import Field


class Map:
    # Number of rows and columns
    ROWS = 10
    COLUMNS = 10

    def __init__(self, ownerId):
        # Player ID
        self.ownerId = ownerId
        # 2D-Array containing Field Objects
        self.fields: list[list[Field]] = []
        ''' 
        total Number of Tiles with ships on them 
        (gets subtracted by one for each hit) 
        Player wins, when opponent is 0
        '''
        self.shipTiles = 30
        # initializing Map
        self.__initMap()

    def placeShips(self, coordinate, orientation, length):
        try:
            # translating Input (i.e. A8) to X & Y coordinates
            xValue = ord(coordinate[0].lower()) - 97
            yValue = int(coordinate[1]) - 1

            # validating X & Y values + checking spacing around ship
            if self.__validateShipPlacement(xValue, yValue, orientation, length):

                # iteration through tiles of current ship
                for i in range(0, length):
                    # setting Ship on current field
                    self.fields[xValue][yValue].shipOnField = True

                    # moving to next ship tile, depending on chosen orientation
                    values = self.__nextTile(xValue, yValue, orientation)
                    xValue = values[0]
                    yValue = values[1]

            else:
                # return info, that placement has failed. Function will be called again.
                print("Das Schiff kann so nicht platziert werden! Probieren Sie es erneut!")
                return False

            # return info, that placement has been successful.
            return True
        except Exception as e:
            print(f"Es ist ein Fehler in der Funktion 'Map.placeShips' aufgetreten! {e}")

    def hitField(self, coordinate):
        try:
            # translating Input (i.e. A8) to X & Y coordinates
            xValue = ord(coordinate[0].lower()) - 97
            yValue = int(coordinate[1]) - 1

            # setting actualField to X & Y values
            actualField = self.fields[xValue][yValue]

            # check if field has already been hit and report failure
            if actualField.fieldHit:
                print("Dieses Feld wurde bereits getroffen!")
                return False

            # check if field has ship on it
            elif actualField.shipOnField:
                print("Schiff wurde getroffen!")

                # subtracting floating shipTiles. When it reaches 0, the game is lost.
                self.shipTiles -= 1
            else:
                print("Daneben!")

            # set field to "already hit" and report successful hit
            actualField.fieldHit = True
            return True
        except Exception as e:
            print(f"Es ist ein Fehler in der Funktion 'Map.hitField' aufgetreten! {e}")

    def __initMap(self):
        try:
            # filling the 2D Array with field objects
            for i in range(self.ROWS):
                currentRow = []
                for j in range(self.COLUMNS):
                    # new field objects are not hit and have no ship on it
                    currentRow.append(Field(False, False))
                self.fields.append(currentRow)
        except Exception as e:
            print(f"Es ist ein Fehler in der Funktion 'Map.__initMap' aufgetreten! {e}")

    def __validateShipPlacement(self, xValue, yValue, orientation, length):
        try:
            # iterating through the number of ship tiles
            for i in range(0, length):
                # iterating through the 9 surrounding fields of each ship tile
                for j in range(-1, 2):
                    for k in range(-1, 2):

                        # check if fields are out of map, if so: skip ship check
                        if xValue + j < 0 or xValue + j >= 10 or yValue + k < 0 or yValue + k >= 10:
                            continue
                        else:

                            # if there is already a ship on the field return fail
                            if self.fields[xValue + j][yValue + k].shipOnField:
                                return False

                # check if the ship tile would be out of map, if so: return fail.
                if xValue < 0 or xValue >= 10:
                    return False
                elif yValue < 0 or yValue >= 10:
                    return False

                # moving to next ship tile, depending on chosen orientation
                values = self.__nextTile(xValue, yValue, orientation)
                # empty returned tuple into the corresponding value
                xValue = values[0]
                yValue = values[1]

            # after iterating through the entire ship: return successful validation
            return True
        except Exception as e:
            print(f"Es ist ein Fehler in der Funktion 'Map.__validateShipPlacement' aufgetreten! {e}")

    def __nextTile(self, xValue, yValue, orientation):
        try:
            # move current Tile coordinates to the following tile in given orientation
            if orientation == "S":
                yValue += 1
            elif orientation == "N":
                yValue -= 1
            elif orientation == "W":
                xValue -= 1
            elif orientation == "O":
                xValue += 1

            # return coordinates as a tuple
            return xValue, yValue
        except Exception as e:
            print(f"Es ist ein Fehler in der Funktion 'Map.__nextTile' aufgetreten! {e}")
