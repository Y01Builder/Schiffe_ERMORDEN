import unittest
from unittest.mock import patch
from DTO.player import Player

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player("Mario", 1)
        self.opponent = Player("Yannick", 2)

    def test_init(self):
        self.assertEqual(self.player.name, "Mario")
        self.assertEqual(self.player.id, 1)

    def test_validate_coordinate(self):
        #Alle Ecken des Spielfelds pruefen und verschiedene Werte
        self.assertEqual(self.player._validateCoordinate("A1"), ("A", "1"))
        self.assertEqual(self.player._validateCoordinate("B2"), ("B", "2"))
        self.assertEqual(self.player._validateCoordinate("J10"), ("J", "10"))
        self.assertEqual(self.player._validateCoordinate("A10"), ("A", "10"))
        self.assertEqual(self.player._validateCoordinate("J1"), ("J", "1"))
        #Ausserhalb des Spielfelds pruefen
        self.assertFalse(self.player._validateCoordinate("C11"))
        self.assertFalse(self.player._validateCoordinate("Z10"))
        self.assertFalse(self.player._validateCoordinate("Test"))

    def test_validate_orientation(self):
        #Richtungen pruefen (aktuelle ohne Kleinbuchstaben)
        self.assertEqual(self.player._validateOrientation("N"), "N")
        self.assertEqual(self.player._validateOrientation("S"), "S")
        self.assertEqual(self.player._validateOrientation("O"), "O")
        self.assertEqual(self.player._validateOrientation("W"), "W")
        self.assertFalse(self.player._validateOrientation("w"))
        self.assertFalse(self.player._validateOrientation("E"))
        self.assertFalse(self.player._validateOrientation("123"))

    def test_shoot_field(self):
        self.opponent._map.fields[0][0].shiponfield = True
        self.opponent._map.fields[0][0].fieldhit = False
        self.opponent._map.shipTiles = 1
        with patch("builtins.input", return_value="A1"):
            self.assertTrue(self.player.shootField(self.opponent))
        self.assertTrue(self.opponent._map.fields[0][0].fieldhit)
        self.assertEqual(self.opponent._map.shipTiles, 0)

    @patch("builtins.input", side_effect=["A1", "S", "C5", "N", "E5", "O", "C10", "O", "D7", "O", "J1", "S", "J10", "N",
                                          "A8", "O", "J7", "W", "F2", "O"])
    def test_place_ships(self, mock_input):
        self.player.placeShips()
        #Pruefen ob Schiff auf Feld gesetzt
        self.assertTrue(self.player._map.fields[0][0].shiponfield)
        # Fieldhit muss nach setzen auf 0 bleiben
        self.assertFalse(self.player._map.fields[0][0].fieldhit)
        #ShipTiles ist fest auf 30 im Code gesetzt
        self.assertEqual(self.player._map.shipTiles, 30)
