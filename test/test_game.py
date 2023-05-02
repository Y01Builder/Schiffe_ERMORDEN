#pylint: disable=C
#pylint: disable=W0212
import unittest
import pickle
import os
from unittest.mock import patch
from DTO.player import Player
from DTO.game import Game


class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game("")

    def tearDown(self):
        del self.game

    def test_init(self):
        self.assertIsInstance(self.game.player1, Player)
        self.assertIsInstance(self.game.player2, Player)
        self.assertEqual(self.game.player1.name, 'User1')
        self.assertEqual(self.game.player2.name, 'User2')
        self.assertEqual(self.game.player1.playerid, 0)
        self.assertEqual(self.game.player2.playerid, 1)

    def test_create_player(self):
        with patch('builtins.input', side_effect=['Mario', "A1", "S", "C5", "N", "E5", "O", "C10", "O", "D7", "O", "J1",
                                                  "S", "J10", "N", "A8", "O", "J7", "W", "F2", "O"]):
            player = self.game._Game__create_player(0)
        self.assertIsInstance(player, Player)
        self.assertEqual(player.name, 'Mario')
        self.assertEqual(player.playerid, 0)

    def test_set_ships(self):
        with patch('builtins.input', side_effect=["A1", "S", "C5", "N", "E5", "O", "C10", "O", "D7", "O", "J1", "S", "J10", "N",
                                          "A8", "O", "J7", "W", "F2", "O"]):
            player = Player('Mario', 0)
            self.assertTrue(self.game._Game__set_ships(player))

    def test_player_turn(self):
        player1 = Player('Mario', 0)
        player2 = Player('Yannick', 1)
        player1.turn = True
        player2.map.ship_tiles = 30
        with patch('builtins.input', side_effect=['A1\n', '\n']):
            self.assertFalse(self.game._Game__player_turn(player1, player2))

    def test_save_map(self):
        player = Player('Mario', 0)
        self.game._Game__save_map(player)
        self.assertTrue(os.path.isfile("mapPlayer1.pickle"))
        with open('mapPlayer1.pickle', 'rb') as file:
            loaded_player = pickle.load(file)
        self.assertEqual(player.name, loaded_player.name)
        self.assertEqual(player.playerid, loaded_player.playerid)

    def test_load_game(self):
        player = Player('Mario', 0)
        with open('mapPlayer1.pickle', 'wb') as file:
            pickle.dump(player, file)
        loaded_player = self.game._Game__load_game(player)
        self.assertEqual(player.name, loaded_player.name)

    def test_start_game(self):
        #test complete game
        with patch('builtins.input', side_effect=[
        "2", "N",
        "Mario",
        "A1", "S", "C5", "N", "E5", "O", "C10", "O", "D7", "O", "J1","S", "J10", "N", "A8", "O", "J7", "W", "F2", "O",
        "Yannick",
        "A1", "S", "C5", "N", "E5", "O", "C10", "O", "D7", "O", "J1","S", "J10", "N", "A8", "O", "J7", "W", "F2", "O",
        "\n", "A1", "\n", "\n", "A2", "\n","\n", "A3", "\n","\n", "A4", "\n","\n", "A5", "\n","\n", "C2", "\n","\n", "C3", "\n","\n", "C4", "\n","\n", "C5", "\n","\n",
        "E5", "\n","\n", "F5", "\n","\n", "G5", "\n","\n", "H5", "\n","\n","D7", "\n","\n","E7", "\n","\n", "F7", "\n","\n", "I7", "\n","\n", "J7", "\n","\n",
          "A8", "\n","\n", "B8", "\n","\n", "C10", "\n","\n", "D10", "\n","\n", "E10", "\n","\n", "F2", "\n","\n", "G2", "\n","\n", "J9", "\n","\n", "J10",
          "\n","\n", "J1", "\n","\n", "J2", "\n","\n", "J3",
        "\n","\n", "C1", "\n","\n","A1", "\n","\n", "A2", "\n","\n", "A3", "\n","\n", "A4", "\n","\n", "A5", "\n","\n", "C2", "\n","\n", "C3", "\n","\n", "C4", "\n","\n", "C5",
         "\n","\n" , "E5", "\n","\n", "F5", "\n","\n", "G5", "\n","\n", "H5", "\n","\n","D7", "\n","\n","E7", "\n","\n", "F7", "\n","\n", "I7", "\n","\n", "J7", "\n","\n",
          "A8", "\n","\n", "B8", "\n","\n", "C10", "\n","\n", "D10", "\n","\n", "E10", "\n","\n", "F2", "\n","\n", "G2", "\n","\n", "J9", "\n","\n", "J10",
          "\n","\n", "J1", "\n","\n", "J2", "\n","\n", "J3", "\n"
                                                  ]):
        #with patch('builtins.input', side_effect=["Mario",
        #"A1", "S",
        #"Yannick",
        #"A1", "S",
        #"A1", "A1", "A2", "A2", "A3", "A3", "A4", "A4", "A5", "A5","A1", "A1", "A2", "A2", "A3", "A3", "A4", "A4", "A5", "A5"]):
            self.game.start_game()

