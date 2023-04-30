#pylint: disable=C
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
        with patch('builtins.input', side_effect=['Mario']):
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
        with patch('builtins.input', side_effect=['A1\n']):
            #with patch('sys.stdout', new=StringIO()) as fake_stdout:
            self.assertFalse(self.game._Game__player_turn(player1, player2))
        #self.assertIn('Spielende!', fake_stdout.getvalue())

    def test_save_map(self):
        player = Player('Mario', 0)
        self.game._Game__save_map(player)
        self.assertTrue(os.path.isfile("testPlayer1.pickle"))
        with open('testPlayer1.pickle', 'rb') as file:
            loaded_player = pickle.load(file)
        self.assertEqual(player.name, loaded_player.name)
        self.assertEqual(player.playerid, loaded_player.playerid)

    def test_load_game(self):
        player = Player('Mario', 0)
        with open('testPlayer1.pickle', 'wb') as file:
            pickle.dump(player, file)
        loaded_player = self.game._Game__load_game(player)
        self.assertEqual(player.name, loaded_player.name)

