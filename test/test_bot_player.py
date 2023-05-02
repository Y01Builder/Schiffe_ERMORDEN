
import unittest
from unittest.mock import Mock, patch
from DTO.player import Player
from DTO.bot_player import BotPlayer

class TestBotPlayer(unittest.TestCase):


    def setUp(self):
        self.opponent = Player('Opponent', 1)
        self.bot = BotPlayer('Bot', 2)


    def test_init(self):
        self.assertEqual(self.opponent.name, 'Opponent')
        self.assertEqual(self.opponent.playerid, 1)

        self.assertEqual(self.bot.name, 'Bot')
        self.assertEqual(self.bot.playerid, 2)
        self.assertEqual(self.bot.difficulty, 1)

        self.assertEqual(self.bot._BotPlayer__statistic_matrix, [
            [20, 30, 36, 39, 40, 40, 39, 36, 30, 20],
            [30, 40, 46, 49, 50, 50, 49, 46, 40, 30],
            [36, 46, 52, 55, 56, 56, 55, 52, 46, 36],
            [39, 49, 55, 58, 59, 59, 58, 55, 49, 39],
            [40, 50, 56, 59, 60, 60, 59, 56, 50, 40],
            [40, 50, 56, 59, 60, 60, 59, 56, 50, 40],
            [39, 49, 55, 58, 59, 59, 58, 55, 49, 39],
            [36, 46, 52, 55, 56, 56, 55, 52, 46, 36],
            [30, 40, 46, 49, 50, 50, 49, 46, 40, 30],
            [20, 30, 36, 39, 40, 40, 39, 36, 30, 20]])


    def test_set_difficulty(self):
        self.assertTrue(self.bot.set_difficulty(0))
        self.assertEqual(self.bot.difficulty, 0)

        self.assertTrue(self.bot.set_difficulty(1))
        self.assertEqual(self.bot.difficulty, 1)

        self.assertTrue(self.bot.set_difficulty(2))
        self.assertEqual(self.bot.difficulty, 2)

        self.assertFalse(self.bot.set_difficulty(-1))
        self.assertEqual(self.bot.difficulty, 2)

        self.assertFalse(self.bot.set_difficulty(3))
        self.assertEqual(self.bot.difficulty, 2)


    def test_reset_statistic_table(self):
        self.bot._BotPlayer__statistic_matrix = [[0, 0], [0, 0]]
        self.bot.reset_statistic_table()
        self.assertEqual(self.bot._BotPlayer__statistic_matrix, [
        [20, 30, 36, 39, 40, 40, 39, 36, 30, 20],
        [30, 40, 46, 49, 50, 50, 49, 46, 40, 30],
        [36, 46, 52, 55, 56, 56, 55, 52, 46, 36],
        [39, 49, 55, 58, 59, 59, 58, 55, 49, 39],
        [40, 50, 56, 59, 60, 60, 59, 56, 50, 40],
        [40, 50, 56, 59, 60, 60, 59, 56, 50, 40],
        [39, 49, 55, 58, 59, 59, 58, 55, 49, 39],
        [36, 46, 52, 55, 56, 56, 55, 52, 46, 36],
        [30, 40, 46, 49, 50, 50, 49, 46, 40, 30],
        [20, 30, 36, 39, 40, 40, 39, 36, 30, 20]])

    
    def test_place_ships(self):
        with patch.object(BotPlayer, '_BotPlayer__get_placement', side_effect=[('O', ['e', 10]),#5
                                                                              ('S', ['a', 3]),#4
                                                                              ('W', ['j', 1]),#4
                                                                              ('N', ['d', 3]),#3
                                                                              ('O', ['f', 3]),#3
                                                                              ('S', ['j', 6]),#3
                                                                              ('W', ['b', 1]),#2
                                                                              ('N', ['j', 4]),#2
                                                                              ('O', ['a', 8]),#2
                                                                              ('S', ['f', 6])]):#2
            self.bot.place_ships()
        #ShipTiles ist fest auf 30 im Code gesetzt
        self.assertEqual(self.bot.map.ship_tiles, 30)
    

    

    def test_get_placement(self):
        # Test for correct orientation and coordinates
        orientation, coords = self.bot._BotPlayer__get_placement(5, [])
        self.assertIn(orientation, ['N', 'O', 'S', 'W'])
        self.assertGreaterEqual(ord(coords[0]), ord('a'))
        self.assertLessEqual(ord(coords[0]), ord('j'))
        self.assertGreaterEqual(int(coords[1]), 1)
        self.assertLessEqual(int(coords[1]), 10)

        # Test for placement on significant ship fields
        ship_fields = [[2, 3], [4, 3], [4, 4], [4, 5], [4, 6]]
        orientation, coords = self.bot._BotPlayer__get_placement(3, ship_fields)
        # Reset ship_fields, otherwise the coordinates of the placed ship would be contained
        ship_fields = [[2, 3], [4, 3], [4, 4], [4, 5], [4, 6]]
        x, y = ord(coords[0]) - 97, int(coords[1]) - 1
        self.assertNotIn([x, y], ship_fields)
        self.assertNotIn([x, y+1], ship_fields)
        self.assertNotIn([x, y-1], ship_fields)
        self.assertNotIn([x+1, y], ship_fields)
        self.assertNotIn([x+1, y+1], ship_fields)
        self.assertNotIn([x+1, y-1], ship_fields)
        self.assertNotIn([x-1, y], ship_fields)
        self.assertNotIn([x-1, y+1], ship_fields)
        self.assertNotIn([x-1, y-1], ship_fields)

 
    """
    def test_shoot_field(self):        
        self.assertTrue(self.bot.set_difficulty(2))
        opponent = Mock()
        opponent.map.hit_field.return_value = True # Müsste funktionieren
        opponent.map.ship_tiles = 0
        self.assertTrue(self.bot.shoot_field(opponent))
        opponent.map.hit_field.assert_called_once()

        opponent.map.hit_field.return_value = True # Dass auch
        opponent.map.ship_tiles = 1
        self.assertFalse(self.bot.shoot_field(opponent))
        self.assertEqual(opponent.map.hit_field.call_count, 2)

        opponent.map.hit_field.return_value = False # Hier steckt er möglicherweiße im Deathloop
        opponent.map.ship_tiles = 1
        self.assertFalse(self.bot.shoot_field(opponent))
        self.assertEqual(opponent.map.hit_field.call_count, 3)
    """
    
    def test_shoot_cords(self):
        opponent = Mock()
        opponent.map.fields = [[Mock() for _ in range(10)] for _ in range(10)]

        self.assertTrue(self.bot.set_difficulty(0))
        with patch('random.randint', side_effect=[0, 0]):
            opponent.map.fields[0][0].get_field_hit.return_value = False
            self.assertEqual(self.bot._BotPlayer__shoot_cords(opponent), ['a', 1])
            opponent.map.fields[0][0].get_field_hit.assert_called_once()

        self.assertTrue(self.bot.set_difficulty(1))
        with patch.object(BotPlayer, '_BotPlayer__statistical_analysis', return_value=['b', 3]):
            self.assertEqual(self.bot._BotPlayer__shoot_cords(opponent), ['b', 3])

        self.assertTrue(self.bot.set_difficulty(2))
        with patch('random.randint', side_effect=[0, 0, 1, 0, 2, 0]):
            opponent.map.fields[0][0].get_ship_on_field.return_value = False
            opponent.map.fields[0][1].get_ship_on_field.return_value = True
            opponent.map.fields[0][1].get_field_hit.return_value = False
            self.assertEqual(self.bot._BotPlayer__shoot_cords(opponent), ['b', 1])
            opponent.map.fields[0][0].get_ship_on_field.assert_called_once()
            opponent.map.fields[0][1].get_ship_on_field.assert_called_once()

    def test_statistical_analysis(self):
        bot_player = BotPlayer('bot', 2, 1)
        opponent = Player('opponent', 1)
        opponent.map.fields[4][4].shiponfield = False
        opponent.map.fields[5][5].shiponfield = True
        self.assertEqual(bot_player._BotPlayer__statistical_analysis(opponent), ['e', 5])
        self.assertEqual(bot_player._BotPlayer__statistic_matrix[4][4], 0)
        self.assertEqual(bot_player._BotPlayer__statistic_matrix[5][4], 40)
        self.assertEqual(bot_player._BotPlayer__statistic_matrix[4][2], 46)
        self.assertEqual(bot_player._BotPlayer__statistic_matrix[1][4], 46)
        self.assertEqual(bot_player._BotPlayer__statistic_matrix[4][8], 49)
        self.assertEqual(bot_player._BotPlayer__statistic_matrix[9][4], 40)
        self.assertEqual(bot_player._BotPlayer__statistical_analysis(opponent), ['f', 6])
        self.assertEqual(bot_player._BotPlayer__statistic_matrix[5][5], 0)
        self.assertEqual(bot_player._BotPlayer__statistic_matrix[6][6], 0)
        self.assertEqual(bot_player._BotPlayer__statistic_matrix[5][4], 60)
        self.assertEqual(bot_player._BotPlayer__statistic_matrix[6][5], 79)

    def tearDown(self):
        del self.opponent
        del self.bot


