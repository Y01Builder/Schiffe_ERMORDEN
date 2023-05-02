"""import the field class"""
from DTO.field import Field


class Map:
    """the map class manages the activities on the map with validation"""
    # Number of rows and columns
    ROWS = 10
    COLUMNS = 10

    def __init__(self, ownerid):
        # Player ID
        self.ownerid = ownerid
        # 2D-Array containing Field Objects
        self.fields: list[list[Field]] = []
        ''' 
        total Number of Tiles with ships on them 
        (gets subtracted by one for each hit) 
        Player wins, when opponent is 0
        '''
        self.ship_tiles = 0
        # initializing Map
        self.__init_map()

    def place_ships(self, coordinate, orientation, length):
        """place the ship with coordinate, orientation and length"""
        try:
            # translating Input (i.e. A8) to X & Y coordinates
            x_value = ord(coordinate[0].lower()) - 97
            y_value = int(coordinate[1]) - 1

            # validating X & Y values + checking spacing around ship
            if self.__validate_ship_placement(x_value, y_value, orientation, length):

                # iteration through tiles of current ship
                for _ in range(0, length):
                    # setting Ship on current field and adding to number of floating ship tiles
                    self.fields[x_value][y_value].shiponfield = True
                    self.ship_tiles += 1

                    # moving to next ship tile, depending on chosen orientation
                    values = self.__next_tile(x_value, y_value, orientation)
                    x_value = values[0]
                    y_value = values[1]

            else:
                # return info, that placement has failed. Function will be called again.
                print("Das Schiff kann so nicht platziert werden! Probieren Sie es erneut!")
                return False

            # return info, that placement has been successful.
            return True
        except IndexError:
            print("Es ist ein Fehler 'Map.place_ships' bei der Index Verwendung aufgetreten!")
            return False

    def hit_field(self, coordinate):
        """hit the field with the given coordinate"""
        try:
            # translating Input (i.e. A8) to X & Y coordinates
            x_value = ord(coordinate[0].lower()) - 97
            y_value = int(coordinate[1]) - 1

            # setting actual_field to X & Y values
            actual_field = self.fields[x_value][y_value]

            # check if field has already been hit and report failure
            if actual_field.fieldhit:
                print(f"Dieses Feld wurde bereits getroffen! Koordinate: {coordinate}")
                return False

            # check if field has ship on it
            if actual_field.shiponfield:
                print("Schiff wurde getroffen!")

                # subtracting floating ship_tiles. When it reaches 0, the game is lost.
                self.ship_tiles -= 1
            else:
                print("Daneben!")

            # set field to "already hit" and report successful hit
            actual_field.fieldhit = True
            return True
        except IndexError:
            print("Es ist ein Fehler in der Funktion 'Map.hit_field' bei der Index Verwendung aufgetreten!")
            return False

    def __init_map(self):
        # filling the 2D Array with field objects
        for _ in range(self.ROWS):
            current_row = []
            for _ in range(self.COLUMNS):
                # new field objects are not hit and have no ship on it
                current_row.append(Field(False, False))
            self.fields.append(current_row)

    def __validate_surrounding_fields(self, x_value, y_value):
        # iterating through the 9 surrounding fields of each ship tile
        for j in range(-1, 2):
            for k in range(-1, 2):

                # check if fields are out of map, if so: skip ship check
                if x_value + j < 0 or x_value + j >= 10 or y_value + k < 0 or y_value + k >= 10:
                    continue
                # if there is already a ship on the field return fail
                if self.fields[x_value + j][y_value + k].shiponfield:
                    return False
        return True

    def __validate_ship_placement(self, x_value, y_value, orientation, length):
        try:
            # iterating through the number of ship tiles
            for _ in range(0, length):
                # check surrounding fields for shiponfield or out of map
                if not self.__validate_surrounding_fields(x_value, y_value):
                    return False

                # check if the ship tile would be out of map, if so: return fail.
                if x_value < 0 or x_value >= 10:
                    return False
                if y_value < 0 or y_value >= 10:
                    return False

                # moving to next ship tile, depending on chosen orientation
                values = self.__next_tile(x_value, y_value, orientation)
                # empty returned tuple into the corresponding value
                x_value = values[0]
                y_value = values[1]

            # after iterating through the entire ship: return successful validation
            return True
        except IndexError:
            print("Es ist ein Fehler 'Map.__validate_ship_placement' bei der Verwendung des Indexes aufgetreten!")
            return False

    def __next_tile(self, x_value, y_value, orientation):
        # move current Tile coordinates to the following tile in given orientation
        if orientation == "S":
            y_value += 1
        elif orientation == "N":
            y_value -= 1
        elif orientation == "W":
            x_value -= 1
        elif orientation == "O":
            x_value += 1

        # return coordinates as a tuple
        return x_value, y_value
