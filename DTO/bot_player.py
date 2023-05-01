"""import randint, Player and Map"""
from random import randint
from player import Player
#from map import Map

class BotPlayer(Player):
    """
    A class representing a bot player in the game.

    Attributes:
    -----------
        __difficulty : int
            The difficulty level of the bot player.
        __statistic_matrix : List[List[int]]
            The matrix representing the probability of having a ship in each position of the map


    Methods:
    --------
        set_difficulty(difficulty: int) -> bool:
            Sets the difficulty level of the bot player.

        shoot_field(opponent: Player) -> bool:
            Shoots at a field on the opponent player's map.

        __shoot_cords(opponent: Player) -> Union[List[str, int], bool]:
            Generates coordinates to shoot at on the opponent player's map.

        place_ships():
            Places the ships randomly on the bot player's map.

        __get_placement(length: int, ship_fields: List[List[int]]) -> Tuple[List[str], List[str]]:
            Generates placement coordinates for a ship on the bot player's map.

        reset_statistic_table():
            Resets the __statistic_matrix attribute to its initial values.

        __statistics_bitch(opponent: Player) -> List[str]:
            Analyzes the probabilities of randomly placed ships and each shot fired
            to determine the most likely target to shoot at.
    """
    __difficulty = 1

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
        if difficulty >= 0:
            if difficulty <= 2:
                self.__difficulty = difficulty
                self.reset_statistic_table()
                return True
        return False

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
        repeat = True
        while repeat:
            coordinate = self.__shoot_cords(opponent)
            if opponent.map.hit_field(coordinate):
                repeat = False
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
        valid_hit = False
        while not valid_hit:
            match self.__difficulty:
                case 0:
                    trgt_x = randint(0, 9)
                    trgt_y = randint(0, 9)
                    if opponent.map.fields[trgt_y][trgt_x].get_field_hit():
                        valid_hit = True
                        return [chr(trgt_x+97),trgt_y+1]
                    continue
                case 1:
                    valid_hit = True
                    target = self.__statistics_bitch(opponent)
                    return target
                case 2:
                    for trgt_y, row in enumerate(opponent.map):
                        for trgt_x, field in enumerate(row):
                            if field.get_ship_on_field():
                                if not field.get_field_hit():
                                    valid_hit = True
                                    return [chr(trgt_x+97),trgt_y+1]
                    continue
        return False


    def place_ships(self):
        """
        Randomly places the bot's ships on the map.
        """
        ship_fields = [[]]
        for name, length, count in super()._ships:
            for i in range(0, count):
                orientation, coordinate = self.__get_placement(length, ship_fields)
                if not self.map.place_ships(coordinate, orientation, length):   # FOR DEBUG
                    print(f"Fehler placeShips: {i}. {name}")                    # FOR DEBUG

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
                    ori = ['N']
                    strt_y = randint(length-1, 9)
                    strt_x = randint(0, 9)
                    end_y = strt_y-(length-1)
                    end_x = strt_x
                case 1: # east
                    ori = ['O']
                    strt_y = randint(0, 9)
                    strt_x = randint(0, 10-length)
                    end_y = strt_y
                    end_x = strt_x+(length-1)
                case 2: # south
                    ori = ['S']
                    strt_y = randint(0, 10-length)
                    strt_x = randint(0, 9)
                    end_y = strt_y+(length-1)
                    end_x = strt_x
                case 3: # west
                    ori = ['W']
                    strt_y = randint(0, 9)
                    strt_x = randint(length-1, 9)
                    end_y = strt_y
                    end_x = strt_x-(length-1)

            not_good = False
            for shp_x,shp_y in ship_fields:
                if strt_x-1 <= shp_x:
                    if shp_x <= strt_x+1:
                        if strt_y-1 <= shp_y:
                            if shp_y <= strt_y+1:
                                not_good = True

                if end_x-1 <= shp_x:
                    if shp_x <= end_x+1:
                        if end_y-1 <= shp_y:
                            if shp_y <= end_y+1:
                                not_good = True


        ship_fields.append([strt_x,strt_y])
        if length==5:
            btwn_x = strt_x if strt_x == end_x else (end_x+strt_x)/2
            btwn_y = strt_y if strt_y == end_y else (end_y+strt_y)/2
            ship_fields.append([btwn_x,btwn_y])
        ship_fields.append([end_x,end_y])

        coords = [chr(strt_x+97), str(strt_y+1)]
        return ori, coords

    __statistic_matrix = [
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


    def __statistics_bitch(self, opponent):
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
        tmp, tmp_x, tmp_y = -1
        for trgt_y, row in enumerate(self.__statistic_matrix):
            for trgt_x, score in enumerate(row):
                if score > tmp:
                    tmp = score
                    tmp_y = trgt_y
                    tmp_x = trgt_x

        if opponent.map.fields[tmp_y][tmp_x].get_ship_on_field():
            self.__statistic_matrix[tmp_y][tmp_x] = 0
            """
            if (tmp_y-1)>=0:
                self.__statistic_matrix[(tmp_y-1)][(tmp_x)] += 5

                if (tmp_x-1)>=0:
                    self.__statistic_matrix[(tmp_y)][(tmp_x-1)] += 5
                    self.__statistic_matrix[(tmp_y-1)][(tmp_x-1)] = 0

                if (tmp_x+1)<=9:
                    self.__statistic_matrix[(tmp_y)][(tmp_x+1)] += 5
                    self.__statistic_matrix[(tmp_y-1)][(tmp_x+1)] = 0

            else:
                if (tmp_x-1)>=0:
                    self.__statistic_matrix[(tmp_y)][(tmp_x-1)] += 5

                if (tmp_x+1)<=9:
                    self.__statistic_matrix[(tmp_y)][(tmp_x+1)] += 5

            if (tmp_y+1)<=9:
                self.__statistic_matrix[(tmp_y+1)][(tmp_x)] += 5

                if (tmp_x-1)>=0:
                    self.__statistic_matrix[(tmp_y+1)][(tmp_x-1)] = 0

                if (tmp_x+1)<=9:
                    self.__statistic_matrix[(tmp_y+1)][(tmp_x+1)] = 0
            """
        else:
            self.__statistic_matrix[tmp_y][tmp_x] = 0

            if (tmp_y-4) >= 0:
                self.__statistic_matrix[(tmp_y-1)][(tmp_x)] -= 20
                self.__statistic_matrix[(tmp_y-2)][(tmp_x)] -= 10
                self.__statistic_matrix[(tmp_y-3)][(tmp_x)] -= 4
                self.__statistic_matrix[(tmp_y-4)][(tmp_x)] -= 1

                if (tmp_y+4) <= 9:
                    self.__statistic_matrix[(tmp_y+1)][(tmp_x)] -= 20
                    self.__statistic_matrix[(tmp_y+2)][(tmp_x)] -= 10
                    self.__statistic_matrix[(tmp_y+3)][(tmp_x)] -= 4
                    self.__statistic_matrix[(tmp_y+4)][(tmp_x)] -= 1

                elif (tmp_y+3) <= 9:
                    self.__statistic_matrix[(tmp_y+1)][(tmp_x)] -= 20
                    self.__statistic_matrix[(tmp_y+2)][(tmp_x)] -= 10
                    self.__statistic_matrix[(tmp_y+3)][(tmp_x)] -= 4

                elif (tmp_y+2) <= 9:
                    self.__statistic_matrix[(tmp_y+1)][(tmp_x)] -= 20
                    self.__statistic_matrix[(tmp_y+2)][(tmp_x)] -= 10

                elif (tmp_y+1) <= 9:
                    self.__statistic_matrix[(tmp_y+1)][(tmp_x)] -= 20

            elif (tmp_y-3) >= 0:
                self.__statistic_matrix[(tmp_y-1)][(tmp_x)] -= 20
                self.__statistic_matrix[(tmp_y-2)][(tmp_x)] -= 10
                self.__statistic_matrix[(tmp_y-3)][(tmp_x)] -= 4

                self.__statistic_matrix[(tmp_y+1)][(tmp_x)] -= 20
                self.__statistic_matrix[(tmp_y+2)][(tmp_x)] -= 10
                self.__statistic_matrix[(tmp_y+3)][(tmp_x)] -= 4
                self.__statistic_matrix[(tmp_y+4)][(tmp_x)] -= 1

            elif (tmp_y-2) >= 0:
                self.__statistic_matrix[(tmp_y-1)][(tmp_x)] -= 20
                self.__statistic_matrix[(tmp_y-2)][(tmp_x)] -= 10

                self.__statistic_matrix[(tmp_y+1)][(tmp_x)] -= 20
                self.__statistic_matrix[(tmp_y+2)][(tmp_x)] -= 10
                self.__statistic_matrix[(tmp_y+3)][(tmp_x)] -= 4
                self.__statistic_matrix[(tmp_y+4)][(tmp_x)] -= 1

            elif (tmp_y-1) >= 0:
                self.__statistic_matrix[(tmp_y-1)][(tmp_x)] -= 20

                self.__statistic_matrix[(tmp_y+1)][(tmp_x)] -= 20
                self.__statistic_matrix[(tmp_y+2)][(tmp_x)] -= 10
                self.__statistic_matrix[(tmp_y+3)][(tmp_x)] -= 4
                self.__statistic_matrix[(tmp_y+4)][(tmp_x)] -= 1


            if (tmp_x-4) >= 0:
                self.__statistic_matrix[(tmp_y)][(tmp_x-1)] -= 20
                self.__statistic_matrix[(tmp_y)][(tmp_x-2)] -= 10
                self.__statistic_matrix[(tmp_y)][(tmp_x-3)] -= 4
                self.__statistic_matrix[(tmp_y)][(tmp_x-4)] -= 1

                if (tmp_x+4) <= 9:
                    self.__statistic_matrix[(tmp_y)][(tmp_x+1)] -= 20
                    self.__statistic_matrix[(tmp_y)][(tmp_x+2)] -= 10
                    self.__statistic_matrix[(tmp_y)][(tmp_x+3)] -= 4
                    self.__statistic_matrix[(tmp_y)][(tmp_x+4)] -= 1

                elif (tmp_x+3) <= 9:
                    self.__statistic_matrix[(tmp_y)][(tmp_x+1)] -= 20
                    self.__statistic_matrix[(tmp_y)][(tmp_x+2)] -= 10
                    self.__statistic_matrix[(tmp_y)][(tmp_x+3)] -= 4

                elif (tmp_x+2) <= 9:
                    self.__statistic_matrix[(tmp_y)][(tmp_x+1)] -= 20
                    self.__statistic_matrix[(tmp_y)][(tmp_x+2)] -= 10

                elif (tmp_x+1) <= 9:
                    self.__statistic_matrix[(tmp_y)][(tmp_x+1)] -= 20


            elif (tmp_x-3) >= 0:
                self.__statistic_matrix[(tmp_y)][(tmp_x-1)] -= 20
                self.__statistic_matrix[(tmp_y)][(tmp_x-2)] -= 10
                self.__statistic_matrix[(tmp_y)][(tmp_x-3)] -= 4

                self.__statistic_matrix[(tmp_y)][(tmp_x+1)] -= 20
                self.__statistic_matrix[(tmp_y)][(tmp_x+2)] -= 10
                self.__statistic_matrix[(tmp_y)][(tmp_x+3)] -= 4
                self.__statistic_matrix[(tmp_y)][(tmp_x+4)] -= 1

            elif (tmp_x-2) >= 0:
                self.__statistic_matrix[(tmp_y)][(tmp_x-1)] -= 20
                self.__statistic_matrix[(tmp_y)][(tmp_x-2)] -= 10

                self.__statistic_matrix[(tmp_y)][(tmp_x+1)] -= 20
                self.__statistic_matrix[(tmp_y)][(tmp_x+2)] -= 10
                self.__statistic_matrix[(tmp_y)][(tmp_x+3)] -= 4
                self.__statistic_matrix[(tmp_y)][(tmp_x+4)] -= 1

            elif (tmp_x-1) >= 0:
                self.__statistic_matrix[(tmp_y)][(tmp_x-1)] -= 20

                self.__statistic_matrix[(tmp_y)][(tmp_x+1)] -= 20
                self.__statistic_matrix[(tmp_y)][(tmp_x+2)] -= 10
                self.__statistic_matrix[(tmp_y)][(tmp_x+3)] -= 4
                self.__statistic_matrix[(tmp_y)][(tmp_x+4)] -= 1

        return [chr(tmp_x+97),tmp_y+1]
