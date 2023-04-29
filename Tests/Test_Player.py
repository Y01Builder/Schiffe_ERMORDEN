import unittest
from unittest.mock import patch
from DTO.Map import Map
from DTO.Player import Player

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player("Mario", 1)
        self.opponent = Player("Yannick", 2)

    def test_init(self):
        self.assertEqual(self.player.name, "Yannick")
        self.assertEqual(self.player.id, 1)

    def test_validate_coordinate(self):
        #Alle Ecken des Spielfelds pruefen und verschiedene Werte
        self.assertEqual(self.player._Player__validateCoordinate("A1"), ("A", "1"))
        self.assertEqual(self.player._Player__validateCoordinate("B2"), ("B", "2"))
        self.assertEqual(self.player._Player__validateCoordinate("J10"), ("J", "10"))
        self.assertEqual(self.player._Player__validateCoordinate("A10"), ("A", "10"))
        self.assertEqual(self.player._Player__validateCoordinate("J1"), ("J", "1"))
        #Ausserhalb des Spielfelds pruefen
        self.assertFalse(self.player._Player__validateCoordinate("C11"))
        self.assertFalse(self.player._Player__validateCoordinate("Z10"))
        self.assertFalse(self.player._Player__validateCoordinate("Test"))

    def test_validate_orientation(self):
        #Richtungen pruefen (aktuelle ohne Kleinbuchstaben)
        self.assertEqual(self.player._Player__validateOrientation("N"), "N")
        self.assertEqual(self.player._Player__validateOrientation("S"), "S")
        self.assertEqual(self.player._Player__validateOrientation("O"), "O")
        self.assertEqual(self.player._Player__validateOrientation("W"), "W")
        self.assertFalse(self.player._Player__validateOrientation("w"))
        self.assertFalse(self.player._Player__validateOrientation("E"))
        self.assertFalse(self.player._Player__validateOrientation("123"))

    def test_shoot_field(self):
        self.opponent._Player__map.fields[0][0].shipOnField = True
        self.opponent._Player__map.fields[0][0].fieldHit = False
        self.opponent._Player__map.shipTiles = 1
        with patch("builtins.input", return_value="A1"):
            self.assertTrue(self.player.shootField(self.opponent))
        self.assertTrue(self.opponent._Player__map.fields[0][0].fieldHit)
        self.assertEqual(self.opponent._Player__map.shipTiles, 0)

    @patch("builtins.input", side_effect=["A1", "S", "C5", "N", "E5", "O", "C10", "O", "D7", "O", "J1", "S", "J10", "N",
                                          "A8", "O", "J7", "W", "F2", "O"])
    def test_place_ships(self, mock_input):
        self.player.placeShips()
        #Pruefen ob Schiff auf Feld gesetzt
        self.assertTrue(self.player._Player__map.fields[0][0].shipOnField)
        # Fieldhit muss nach setzen auf 0 bleiben
        self.assertFalse(self.player._Player__map.fields[0][0].fieldHit)
        #ShipTiles ist fest auf 30 im Code gesetzt
        self.assertEqual(self.player._Player__map.shipTiles, 30)