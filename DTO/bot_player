from random import randint
from DTO.map import Map

class BotPlayer(Player):

    __difficulty = 1

    def set_difficulty(self, difficulty):
        if difficulty>=0 and difficulty<=2:
            __difficulty = difficulty
            reset_statistic_table
            return True
        else:
            return False

    def shoot_field(self, opponent): 
        ship_fields = [[]]
        repeat = True
        while repeat:
            coordinate = __shoot_cords(opponent, ship_fields)            
            if opponent.map.hit_field(coordinate):
                repeat = False
                if opponent.map.ship_tiles == 0:
                    return True
        return False

    def __shoot_cords(self, opponent, ship_fields):
        valid_hit = False
        while not valid_hit:
            match __difficulty:
                case 0:
                    tx = randint(0, 9)
                    ty = randint(0, 9)
                    if opponent.map.fields[ty][tx].get_field_hit():
                        valid_hit = True
                        return [chr(tx+97),ty+1]                        
                case 1:               
                    valid_hit = True
                    return __statistics_bitch(opponent)
                case 2:
                    for ty, row in enumerate(opponent.map):
                        for tx, field in enumerate(row):
                            if field.get_ship_on_field():
                                if not field.get_field_hit():
                                    valid_hit = True
                                    return [chr(tx+97),ty+1]
                    

    def place_ships(self):    
        ship_fields = [[]]
        for name, length, count in super()._ships:
            for i in range(0, count):
                orientation, coordinate = __get_placement(length, ship_fields)
                if not super().map.place_ships(coordinate, orientation, length):    # FOR DEBUG
                    print("Fehler placeShips")                                      # FOR DEBUG
        return
           
    def __get_placement(self, length, ship_fields):
        not_good = True
        while not_good:
            orientation = randint(0, 3) # 0 = north, 1 = east, 2 = south, 3 = west
            match orientation:
                case 0: # north
                    ori = ['N']
                    sy = randint(length-1, 9)
                    sx = randint(0, 9)
                    ey = sy-(length-1)
                    ex = sx
                    
                case 1: # east
                    ori = ['O']
                    sy = randint(0, 9)
                    sx = randint(0, 10-length)
                    ey = sy
                    ex = sx+(length-1)
                
                case 2: # south
                    ori = ['S']
                    sy = randint(0, 10-length)
                    sx = randint(0, 9)
                    ey = sy+(length-1)
                    ex = sx
                
                case 3: # west
                    ori = ['W']
                    sy = randint(0, 9)
                    sx = randint(length-1, 9)
                    ey = sy
                    ex = sx-(length-1)
                    
            not_good = False
            for px,py in ship_fields:
                if sx-1 <= px and px <= sx+1 and sy-1 <= py and py <= sy+1:
                    not_good = True
                    
                if ex-1 <= px and px <= ex+1 and ey-1 <= py and py <= ey+1:
                    not_good = True
            
            
        ship_fields.append([sx,sy])
        if length==5:        
            bx = sx if sx == ex else (ex+sx)/2
            by = sy if sy == ey else (ey+sy)/2
            ship_fields.append([ex,ey])
        ship_fields.append([ex,ey])
        
        coords = [chr(sx+97), str(sy+1)]
        return ori, coords
    
    __statistic_matrix = [[20, 30, 36, 39, 40, 40, 39, 36, 30, 20], [30, 40, 46, 49, 50, 50, 49, 46, 40, 30], [36, 46, 52, 55, 56, 56, 55, 52, 46, 36], [39, 49, 55, 58, 59, 59, 58, 55, 49, 39], [40, 50, 56, 59, 60, 60, 59, 56, 50, 40], [40, 50, 56, 59, 60, 60, 59, 56, 50, 40], [39, 49, 55, 58, 59, 59, 58, 55, 49, 39], [36, 46, 52, 55, 56, 56, 55, 52, 46, 36], [30, 40, 46, 49, 50, 50, 49, 46, 40, 30], [20, 30, 36, 39, 40, 40, 39, 36, 30, 20]]
    
    def reset_statistic_table(self):
        self.__statistic_matrix = [[20, 30, 36, 39, 40, 40, 39, 36, 30, 20], [30, 40, 46, 49, 50, 50, 49, 46, 40, 30], [36, 46, 52, 55, 56, 56, 55, 52, 46, 36], [39, 49, 55, 58, 59, 59, 58, 55, 49, 39], [40, 50, 56, 59, 60, 60, 59, 56, 50, 40], [40, 50, 56, 59, 60, 60, 59, 56, 50, 40], [39, 49, 55, 58, 59, 59, 58, 55, 49, 39], [36, 46, 52, 55, 56, 56, 55, 52, 46, 36], [30, 40, 46, 49, 50, 50, 49, 46, 40, 30], [20, 30, 36, 39, 40, 40, 39, 36, 30, 20]]
    
    def __statistics_bitch(self, opponent):  
        
        tmp, tmp_x, tmp_y = -1
        for ty, row in enumerate(self.__statistic_matrix):
            for tx, score in enumerate(row):
                if score > tmp:
                    tmp = score
                    tmp_y = ty
                    tmp_x = tx
                        
        if opponent.map.fields[tmp_y][tmp_x].get_ship_on_field():
        
            __statistic_matrix[tmp_y][tmp_x] = 0
            
            if (tmp_y-1)>=0 and (tmp_x-1)>=0:
                __statistic_matrix[(tmp_y-1)][(tmp_x-1)] = 0
                
            if (tmp_y-1)>=0 and (tmp_x+1)<=9:
                __statistic_matrix[(tmp_y-1)][(tmp_x+1)] = 0
                
            if (tmp_y+1)<=9 and (tmp_x-1)>=0:
                __statistic_matrix[(tmp_y+1)][(tmp_x-1)] = 0
                
            if (tmp_y+1)<=9 and (tmp_x+1)<=9:
                __statistic_matrix[(tmp_y+1)][(tmp_x+1)] = 0
            
        else:            
            __statistic_matrix[tmp_y][tmp_x] = 0
            
            if (tmp_y-4) >= 0:
                __statistic_matrix[(tmp_y-1)][(tmp_x)] -= 20
                __statistic_matrix[(tmp_y-2)][(tmp_x)] -= 10
                __statistic_matrix[(tmp_y-3)][(tmp_x)] -= 4
                __statistic_matrix[(tmp_y-4)][(tmp_x)] -= 1
                   
                if (tmp_y+4) <= 9:
                    __statistic_matrix[(tmp_y+1)][(tmp_x)] -= 20
                    __statistic_matrix[(tmp_y+2)][(tmp_x)] -= 10
                    __statistic_matrix[(tmp_y+3)][(tmp_x)] -= 4
                    __statistic_matrix[(tmp_y+4)][(tmp_x)] -= 1
                
                elif (tmp_y+3) <= 9:
                    __statistic_matrix[(tmp_y+1)][(tmp_x)] -= 20
                    __statistic_matrix[(tmp_y+2)][(tmp_x)] -= 10
                    __statistic_matrix[(tmp_y+3)][(tmp_x)] -= 4
                
                elif (tmp_y+2) <= 9:
                    __statistic_matrix[(tmp_y+1)][(tmp_x)] -= 20
                    __statistic_matrix[(tmp_y+2)][(tmp_x)] -= 10
                
                elif (tmp_y+1) <= 9:
                    __statistic_matrix[(tmp_y+1)][(tmp_x)] -= 20
                
            elif (tmp_y-3) >= 0:
                __statistic_matrix[(tmp_y-1)][(tmp_x)] -= 20
                __statistic_matrix[(tmp_y-2)][(tmp_x)] -= 10
                __statistic_matrix[(tmp_y-3)][(tmp_x)] -= 4
                
                __statistic_matrix[(tmp_y+1)][(tmp_x)] -= 20
                __statistic_matrix[(tmp_y+2)][(tmp_x)] -= 10
                __statistic_matrix[(tmp_y+3)][(tmp_x)] -= 4
                __statistic_matrix[(tmp_y+4)][(tmp_x)] -= 1
            
            elif (tmp_y-2) >= 0:
                __statistic_matrix[(tmp_y-1)][(tmp_x)] -= 20
                __statistic_matrix[(tmp_y-2)][(tmp_x)] -= 10
                
                __statistic_matrix[(tmp_y+1)][(tmp_x)] -= 20
                __statistic_matrix[(tmp_y+2)][(tmp_x)] -= 10
                __statistic_matrix[(tmp_y+3)][(tmp_x)] -= 4
                __statistic_matrix[(tmp_y+4)][(tmp_x)] -= 1
            
            elif (tmp_y-1) >= 0:
                __statistic_matrix[(tmp_y-1)][(tmp_x)] -= 20
                
                __statistic_matrix[(tmp_y+1)][(tmp_x)] -= 20
                __statistic_matrix[(tmp_y+2)][(tmp_x)] -= 10
                __statistic_matrix[(tmp_y+3)][(tmp_x)] -= 4
                __statistic_matrix[(tmp_y+4)][(tmp_x)] -= 1
            
            
            if (tmp_x-4) >= 0:
                __statistic_matrix[(tmp_y)][(tmp_x-1)] -= 20
                __statistic_matrix[(tmp_y)][(tmp_x-2)] -= 10
                __statistic_matrix[(tmp_y)][(tmp_x-3)] -= 4
                __statistic_matrix[(tmp_y)][(tmp_x-4)] -= 1
                   
                if (tmp_x+4) <= 9:
                    __statistic_matrix[(tmp_y)][(tmp_x+1)] -= 20
                    __statistic_matrix[(tmp_y)][(tmp_x+2)] -= 10
                    __statistic_matrix[(tmp_y)][(tmp_x+3)] -= 4
                    __statistic_matrix[(tmp_y)][(tmp_x+4)] -= 1
                
                elif (tmp_x+3) <= 9:
                    __statistic_matrix[(tmp_y)][(tmp_x+1)] -= 20
                    __statistic_matrix[(tmp_y)][(tmp_x+2)] -= 10
                    __statistic_matrix[(tmp_y)][(tmp_x+3)] -= 4
                
                elif (tmp_x+2) <= 9:
                    __statistic_matrix[(tmp_y)][(tmp_x+1)] -= 20
                    __statistic_matrix[(tmp_y)][(tmp_x+2)] -= 10
                
                elif (tmp_x+1) <= 9:
                    __statistic_matrix[(tmp_y)][(tmp_x+1)] -= 20
                
            
            elif (tmp_x-3) >= 0:
                __statistic_matrix[(tmp_y)][(tmp_x-1)] -= 20
                __statistic_matrix[(tmp_y)][(tmp_x-2)] -= 10
                __statistic_matrix[(tmp_y)][(tmp_x-3)] -= 4
            
                __statistic_matrix[(tmp_y)][(tmp_x+1)] -= 20
                __statistic_matrix[(tmp_y)][(tmp_x+2)] -= 10
                __statistic_matrix[(tmp_y)][(tmp_x+3)] -= 4
                __statistic_matrix[(tmp_y)][(tmp_x+4)] -= 1
            
            elif (tmp_x-2) >= 0:
                __statistic_matrix[(tmp_y)][(tmp_x-1)] -= 20
                __statistic_matrix[(tmp_y)][(tmp_x-2)] -= 10
            
                __statistic_matrix[(tmp_y)][(tmp_x+1)] -= 20
                __statistic_matrix[(tmp_y)][(tmp_x+2)] -= 10
                __statistic_matrix[(tmp_y)][(tmp_x+3)] -= 4
                __statistic_matrix[(tmp_y)][(tmp_x+4)] -= 1
            
            elif (tmp_x-1) >= 0:
                __statistic_matrix[(tmp_y)][(tmp_x-1)] -= 20
            
                __statistic_matrix[(tmp_y)][(tmp_x+1)] -= 20
                __statistic_matrix[(tmp_y)][(tmp_x+2)] -= 10
                __statistic_matrix[(tmp_y)][(tmp_x+3)] -= 4
                __statistic_matrix[(tmp_y)][(tmp_x+4)] -= 1
        
        return [chr(tmp_x+97),tmp_y+1]
