#pylint: disable=C
#pylint: disable=W0212
import unittest
import pickle
import os
import sys
from unittest.mock import patch
from DTO.player import Player
from DTO.game import Game


class TestGame(unittest.TestCase):

    def setUp(self):
        self.path=os.path.dirname(os.path.abspath(__file__))
        self.game = Game(f"{self.path}")
        if sys.platform== 'win32':
            self.seperator='\\'
        else:
            self.seperator='/'

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
            #ship A1
            self.assertTrue(self.game._Game__set_ships(player))
            self.assertTrue(player.map.fields[0][0].shiponfield)
            self.assertTrue(player.map.fields[0][1].shiponfield)
            self.assertTrue(player.map.fields[0][2].shiponfield)
            self.assertTrue(player.map.fields[0][3].shiponfield)
            #ship E5
            self.assertTrue(player.map.fields[4][4].shiponfield)
            self.assertTrue(player.map.fields[7][4].shiponfield)

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

    def test_startscreen(self):
        with patch('builtins.input', side_effect=['4','1','4','1','4','J','\n']):
            init_bot,difficulty=self.game._Game__startscreen()
        self.assertEqual(init_bot,True)
        self.assertEqual(difficulty,0)
        with patch('builtins.input', side_effect=['1','1','N']):
            init_bot,difficulty=self.game._Game__startscreen()
        self.assertEqual(init_bot,True)
        self.assertEqual(difficulty,0)
        with patch('builtins.input', side_effect=['1','2','J','\n']):
            init_bot,difficulty=self.game._Game__startscreen()
        self.assertEqual(init_bot,True)
        self.assertEqual(difficulty,1)
        with patch('builtins.input', side_effect=['1','3','J','\n']):
            init_bot,difficulty=self.game._Game__startscreen()
        self.assertEqual(init_bot,True)
        self.assertEqual(difficulty,2)
        with patch('builtins.input', side_effect=['2','J','\n']):
            init_bot,difficulty=self.game._Game__startscreen()
        self.assertEqual(init_bot,False)
        self.assertEqual(difficulty,1)

    def test_load_game(self):
        player = Player('Mario', 0)
        with open('mapPlayer1.pickle', 'wb') as file:
            pickle.dump(player, file)
        loaded_player = self.game._Game__load_game(player)
        self.assertEqual(player.name, loaded_player.name)

    def test_start_game(self):
        #test complete game with all ships player vs player
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
            self.game.start_game()

    def test_end_game(self):
        with open(f"{self.path}{self.seperator}mapPlayer1.pickle", "w", encoding="utf-8") as file:
            file.write("test")
        with open(f"{self.path}{self.seperator}mapPlayer2.pickle", "w", encoding="utf-8") as file:
            file.write("test")
        testPlayer = Player('Mario', 0)
        with patch('builtins.input', side_effect=['\n']):
            self.game.end_game(testPlayer)
        self.assertFalse(os.path.exists(f"{self.path}{self.seperator}mapPlayer1.pickle"))
        self.assertFalse(os.path.exists(f"{self.path}{self.seperator}mapPlayer2.pickle"))

    def test_start_game_with_corruptfile(self):
        # save the player object into the mapPlayerX.pickle file
        with open("mapPlayer1.pickle", "w", encoding="utf-8") as file:
            file.write("test")
        player = Player('Mario', 0)
        player.map.fields[0][0].shiponfield = True
        player2 = Player('Yannick', 1)
        player2.map.fields[0][0].shiponfield = True

        #test complete game with all ships player vs player
        with patch('builtins.input', side_effect=[
        "2", "N",
        "Mario",
        "A1", "S", "C5", "N", "E5", "O", "C10", "O", "D7", "O", "J1","S", "J10", "N", "A8", "O", "J7", "W", "F2", "O",
        "Jan",
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
            self.game.start_game()
            self.assertEqual(self.game.player1.name, "Mario")
            self.assertEqual(self.game.player2.name, "Jan")

if __name__ == "__main__":
    unittest.main()
