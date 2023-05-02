#pylint: disable=C
#pylint: disable=W0212

import unittest
from unittest.mock import patch
from DTO.player import Player

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player("Mario", 1)
        self.opponent = Player("Yannick", 2)

    def test_init(self):
        self.assertEqual(self.player.name, "Mario")
        self.assertEqual(self.player.playerid, 1)

    def test_validate_coordinate(self):
        #check coordinates for validation
        self.assertEqual(self.player.validate_coordinate("A1"), ("A", "1"))
        self.assertEqual(self.player.validate_coordinate("B2"), ("B", "2"))
        self.assertEqual(self.player.validate_coordinate("J10"), ("J", "10"))
        self.assertEqual(self.player.validate_coordinate("A10"), ("A", "10"))
        self.assertEqual(self.player.validate_coordinate("J1"), ("J", "1"))
        #check coordinates out of playground
        self.assertFalse(self.player.validate_coordinate("C11"))
        self.assertFalse(self.player.validate_coordinate("Z10"))
        self.assertFalse(self.player.validate_coordinate("Test"))

    def test_validate_orientation(self):
        #check orientations
        self.assertEqual(self.player._validate_orientation("N"), "N")
        self.assertEqual(self.player._validate_orientation("S"), "S")
        self.assertEqual(self.player._validate_orientation("O"), "O")
        self.assertEqual(self.player._validate_orientation("W"), "W")
        self.assertFalse(self.player._validate_orientation("w"))
        self.assertFalse(self.player._validate_orientation("E"))
        self.assertFalse(self.player._validate_orientation("123"))

    def test_shoot_field(self):
        self.opponent.map.fields[0][0].shiponfield = True
        self.opponent.map.fields[0][0].fieldhit = False
        self.opponent.map.ship_tiles = 1
        with patch("builtins.input", return_value="A1"):
            self.assertTrue(self.player.shoot_field(self.opponent))
        self.assertTrue(self.opponent.map.fields[0][0].fieldhit)
        self.assertEqual(self.opponent.map.ship_tiles, 0)

    def test_place_ships(self):
        with patch('builtins.input', side_effect=["A1", "S", "C5", "N", "E5", "O", "C10", "O", "D7", "O", "J1", "S", "J10", "N",
                                          "A8", "O", "J7", "W", "F2", "O"]):
            self.player.place_ships()
        #check ship is set on field
        self.assertTrue(self.player.map.fields[0][0].shiponfield)
        # fieldhit must be 0
        self.assertFalse(self.player.map.fields[0][0].fieldhit)
        #check ship_tiles after set
        self.assertEqual(self.player.map.ship_tiles, 30)
