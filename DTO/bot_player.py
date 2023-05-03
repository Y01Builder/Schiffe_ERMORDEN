#pylint: disable=E0401
#pylint is unable to import 'DTO.*' because it`s not in the same folder
"""import randint and Player"""
from random import randint
from DTO.player import Player

class BotPlayer(Player):
    """
    A class representing a bot player in the game.

    Attributes:
    -----------
        difficulty : int
            The difficulty level of the bot player.
        __statistic_matrix : List[List[int]]
            The matrix representing the probability of having a ship in each position of the map


    Methods:
    --------
        __init__(name: String, playerid: int, difficulty: int, optional)
            Initializes a new instance of the class BotPlayer.
        
        set_difficulty(difficulty: int) -> bool:
            Sets the difficulty level of the bot player.

        reset_statistic_table():
            Resets the __statistic_matrix attribute to its initial values.

        shoot_field(opponent: Player) -> bool:
            Shoots at a field on the opponent player's map.

        __shoot_cords(opponent: Player) -> Union[List[str, int], bool]:
            Generates coordinates to shoot at on the opponent player's map.

        place_ships():
            Places the ships randomly on the bot player's map.

        __get_placement(length: int, ship_fields: List[List[int]]) -> Tuple[List[str], List[str]]:
            Generates placement coordinates for a ship on the bot player's map.

        __statistical_analysis(opponent: Player) -> List[str]:
            Analyzes the probabilities of randomly placed ships and each shot fired
            to determine the most likely target to shoot at.




    Initializes a new instance of the class BotPlayer,
    with the specified name, player ID, and optional difficulty level.
    It also set the __statistic_matrix to its initial values.

    Parameters:
    -----------
        name : str
            The name of the player.
        playerid : int
            The ID of the player.
        difficulty : int, optional
            The difficulty level of the game, default is 1.
    """
    def __init__(self, name, playerid, difficulty=1):
        super().__init__(name, playerid)
        self.is_bot = True
        self.turn = False
        self.difficulty = difficulty
        self._ships = [
        ["Schlachtschiff", 5, 1], ["Kreuzer", 4, 2], ["Zerstörer", 3, 3], ["Uboot", 2, 4]]
        self.__statistic_matrix = [
        [20, 30, 36, 39, 40, 40, 39, 36, 30, 20],
        [30, 40, 46, 49, 50, 50, 49, 46, 40, 30],
        [36, 46, 52, 55, 56, 56, 55, 52, 46, 36],
        [39, 49, 55, 58, 59, 59, 58, 55, 49, 39],
        [40, 50, 56, 59, 60, 60, 59, 56, 50, 40],
        [40, 50, 56, 59, 60, 60, 59, 56, 50, 40],
        [39, 49, 55, 58, 59, 59, 58, 55, 49, 39],
        [36, 46, 52, 55, 56, 56, 55, 52, 46, 36],
        [30, 40, 46, 49, 50, 50, 49, 46, 40, 30],
        [20, 30, 36, 39, 40, 40, 39, 36, 30, 20]]


    def set_difficulty(self, difficulty):
        """
        Sets the difficulty level of the bot.

        Parameters:
        -----------
            difficulty : int
                The difficulty level of the bot, ranging from 0 (easiest) to 2 (hardest).

        Returns:
        --------
            bool
                True if the difficulty is set successfully, False otherwise.
        """
        if 0 <= difficulty <= 2:
            self.difficulty = difficulty
            self.reset_statistic_table()
            return True
        return False

    def reset_statistic_table(self):
        """
        Resets the __statistic_matrix attribute to its initial values.
        """
        self.__statistic_matrix = [
        [20, 30, 36, 39, 40, 40, 39, 36, 30, 20],
        [30, 40, 46, 49, 50, 50, 49, 46, 40, 30],
        [36, 46, 52, 55, 56, 56, 55, 52, 46, 36],
        [39, 49, 55, 58, 59, 59, 58, 55, 49, 39],
        [40, 50, 56, 59, 60, 60, 59, 56, 50, 40],
        [40, 50, 56, 59, 60, 60, 59, 56, 50, 40],
        [39, 49, 55, 58, 59, 59, 58, 55, 49, 39],
        [36, 46, 52, 55, 56, 56, 55, 52, 46, 36],
        [30, 40, 46, 49, 50, 50, 49, 46, 40, 30],
        [20, 30, 36, 39, 40, 40, 39, 36, 30, 20]]

    def shoot_field(self, opponent):
        """
        Shoots at a field on the opponent player's map.

        Parameters:
        -----------
            opponent : Player
                The opponent player.

        Returns:
        --------
            bool
                True if the opponent's ships have been completely destroyed, False otherwise.
        """
        coordinate = self.__shoot_cords(opponent)
        if opponent.map.hit_field(coordinate):
            # when the hit was successful:
            # stop the loop, end your turn and set turn of next player
            self.turn = False
            opponent.turn = True

            # return end of game, when the last ship tile of the opponent has been sunk.
            if opponent.map.ship_tiles == 0:
                return True
        return False

    def __shoot_cords(self, opponent):
        """
        Generates coordinates to shoot at on the opponent player's map.

        Parameters:
        -----------
            opponent : Player
                The opponent player.

        Returns:
        --------
            Union[List[str, int], bool]
                A list containing the coordinates to shoot at,
                or False if there are no valid coordinates.
        """
        match self.difficulty:
            case 0:
                valid_hit = False
                while not valid_hit:
                    trgt_x = randint(0, 9)
                    trgt_y = randint(0, 9)
                    if not opponent.map.fields[trgt_x][trgt_y].get_field_hit():
                        valid_hit = True
                        return [chr(trgt_x+97),trgt_y+1]
                    continue
            case 1:
                target = self.__statistical_analysis(opponent)
                return target
            case 2:
                for trgt_y in range(0, 10):
                    for trgt_x in range(0, 10):
                        slctd_field = opponent.map.fields[trgt_x][trgt_y]
                        if slctd_field.get_ship_on_field() and not slctd_field.get_field_hit():
                            return [chr(trgt_x+97),trgt_y+1]
        return False


    def place_ships(self):
        """
        Randomly places the bot's ships on the map.
        """
        ship_fields = []
        for name, length, count in self._ships:
            for i in range(0, count):
                orientation, coordinate = self.__get_placement(length, ship_fields)
                if not self.map.place_ships(coordinate, orientation, length):
                    print(f"Fehler placeShips: {i}. {name}")

    def __get_placement(self, length, ship_fields):
        """
        Helper method for the `place_ships` method.
        Returns the orientation and coordinates for placing a ship of the given length on the map.

        Parameters:
        -----------
            length : int
                The length of the ship, which should be place on the map.
            ship_fields : List[List[int]]
                A list of significant ship fields that have already been placed on the map.

        Returns:
        --------
            Tuple[List[str], List[str]]
                A tuple containing the orientation and coordinates for placing the ship on the map.
        """
        not_good = True
        while not_good:

            orientation = randint(0, 3) # 0 = north, 1 = east, 2 = south, 3 = west

            match orientation:
                case 0: # north
                    ori = 'N'
                    strt_y = randint(length-1, 9)
                    strt_x = randint(0, 9)
                    end_y = strt_y-(length-1)
                    end_x = strt_x

                case 1: # east
                    ori = 'O'
                    strt_y = randint(0, 9)
                    strt_x = randint(0, 10-length)
                    end_y = strt_y
                    end_x = strt_x+(length-1)

                case 2: # south
                    ori = 'S'
                    strt_y = randint(0, 10-length)
                    strt_x = randint(0, 9)
                    end_y = strt_y+(length-1)
                    end_x = strt_x

                case 3: # west
                    ori = 'W'
                    strt_y = randint(0, 9)
                    strt_x = randint(length-1, 9)
                    end_y = strt_y
                    end_x = strt_x-(length-1)

            not_good = False
            for shp_x,shp_y in ship_fields:
                # Check if start coordinate isn´t on a occupied field
                if strt_x-1 <= shp_x <= strt_x+1 and strt_y-1 <= shp_y <= strt_y+1:
                    not_good = True

                # Check if end coordinate isn´t on a occupied field
                if end_x-1 <= shp_x <= end_x+1 and end_y-1 <= shp_y <= end_y+1:
                    not_good = True

        # Add significant ship field to ship_fields
        ship_fields.append([strt_x,strt_y])
        if length==5:
            # If the ship is a carrier the middle is also a significant ship field
            btwn_x = strt_x if strt_x == end_x else (end_x+strt_x)/2
            btwn_y = strt_y if strt_y == end_y else (end_y+strt_y)/2
            ship_fields.append([btwn_x,btwn_y])
        ship_fields.append([end_x,end_y])

        coords = [chr(strt_x+97), str(strt_y+1)]
        return ori, coords

    # pylint Removing any of these statements would negatively impact the bot's performance.
    #pylint: disable=too-many-branches
    def __statistical_analysis(self, opponent):
        """
        Update the probability matrix that the bot uses to decide where to shoot
        based on the current state of the game and the behavior of the opponent. 

        Parameters:
        -----------
            opponent : Player
                An instance of the Player class representing the opponent player.

        Returns:
        --------
            List[str, int]
                A list containing the coordinates to shoot at
        """
        tmp, tmp_x, tmp_y =  -1, -1, -1
        matrix = self.__statistic_matrix

        # Find the highest score in the probability matrix and saves its coordinates
        for trgt_y, row in enumerate(matrix):
            for trgt_x, score in enumerate(row):
                if score > tmp:
                    tmp = score
                    tmp_y, tmp_x = trgt_y, trgt_x

        # Check whether there is a ship on that coordinate or not
        if opponent.map.fields[tmp_x][tmp_y].get_ship_on_field():

            # If no ship is on that field, the probability of it to obtain a hidden ship is zero
            matrix[tmp_y][tmp_x] = 0

            # Also the probability on all fields diagonally to it is zero and
            # the probability of all other fields to have a hidden ship field increases by 20
            for mod_y in range(-1, 2):
                for mod_x in range(-1, 2):
                    if mod_y == 0 and mod_x == 0:
                        continue

                    # mtrx are the actual coordinates of the field to be processed
                    mtrx_y, mtrx_x = tmp_y + mod_y, tmp_x + mod_x
                    if (0 <= mtrx_y <= 9 and 0 <= mtrx_x <= 9) and matrix[mtrx_y][mtrx_x] != 0:
                        if mod_y == 0 or mod_x == 0:
                            matrix[mtrx_y][mtrx_x] += 20
                        else:
                            matrix[mtrx_y][mtrx_x] = 0

        else:
            # If no ship is on that field, the probability of it to obtain a hidden ship is zero
            matrix[tmp_y][tmp_x] = 0

            # If no ship is found on the selected cell, the method subtracts points
            # from cells in the vertical and horizontal lines, that pass through the selected cell.
            # The number of points subtracted is determined by the number of reduced opportunities.
            for mod_y in range(-4, 5):
                for mod_x in range(-4, 5): #These if-statements allow to query the required fields
                    if mod_y == 0 and mod_x == 0:
                        continue
                    if mod_y != 0 and mod_x != 0:
                        continue

                    # mtrx are the actual coordinates of the field to be processed
                    mtrx_y, mtrx_x = tmp_y + mod_y, tmp_x + mod_x
                    if (0 <= mtrx_y <= 9 and 0 <= mtrx_x <= 9) and matrix[mtrx_y][mtrx_x] != 0:
                        dstnc = abs(mod_y+mod_x) # Determine the distance
                        match dstnc: # Function explained in docu
                            case 1:
                                matrix[mtrx_y][mtrx_x] -= 20
                            case 2:
                                matrix[mtrx_y][mtrx_x] -= 10
                            case 3:
                                matrix[mtrx_y][mtrx_x] -= 4
                            case 4:
                                matrix[mtrx_y][mtrx_x] -= 1

        # Returns the choosen coordinates
        return [chr(tmp_x+97),tmp_y+1]
