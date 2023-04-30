import unittest
from DTO.Map import Map

class MapTests(unittest.TestCase):

    def setUp(self):
        self.map = Map(0)

    def test_placeShips_validPlacement(self):
        # Testet platzieren von Schiffen an Position
        result = self.map.placeShips("A1", "S", 3)
        self.assertTrue(result)
        # Überprueft ob die Felder korrekt mit Schiffen belegt sind
        self.assertTrue(self.map.fields[0][0].shipOnField)
        self.assertTrue(self.map.fields[0][1].shipOnField)
        self.assertTrue(self.map.fields[0][2].shipOnField)

    def test_placeShips_invalidPlacement(self):
        # Fall 1 Testet platzieren von Schiffen an einer ungültigen Position
        self.map.fields[0][0].shipOnField = True
        result = self.map.placeShips("A1", "S", 3)
        self.assertFalse(result)
        # Pruefung damit sich Werte nicht verändert haben
        self.assertTrue(self.map.fields[0][0].shipOnField)
        self.assertFalse(self.map.fields[0][1].shipOnField)
        # Fall 2 Testet ob Schiff neben anderes platziert werden kann
        #Setze E5 Feld auf true
        self.map.fields[4][4].shipOnField = True
        result = self.map.placeShips("D4", "O", 1)
        self.assertFalse(result)
        result = self.map.placeShips("E4", "O", 1)
        self.assertFalse(result)
        result = self.map.placeShips("F4", "O", 1)
        self.assertFalse(result)
        result = self.map.placeShips("D5", "O", 1)
        self.assertFalse(result)
        result = self.map.placeShips("F5", "O", 1)
        self.assertFalse(result)
        result = self.map.placeShips("D6", "O", 1)
        self.assertFalse(result)
        result = self.map.placeShips("E6", "O", 1)
        self.assertFalse(result)
        result = self.map.placeShips("F6", "O", 1)
        self.assertFalse(result)

    def test_hitField_miss(self):
        # Testet, ob ein Feld als "Daneben" markiert wird, wenn kein Schiff darauf platziert ist
        result = self.map.hitField("A1")
        self.assertTrue(result)
        self.assertTrue(self.map.fields[0][0].fieldHit)
        self.assertFalse(self.map.fields[0][0].shipOnField)

    def test_hitField_hit(self):
        # Testet, ob ein Feld als "Schiff wurde getroffen" markiert wird, wenn es ein Schiff darauf gibt
        self.map.fields[0][0].shipOnField = True
        result = self.map.hitField("A1")
        self.assertTrue(result)
        self.assertTrue(self.map.fields[0][0].fieldHit)
        self.assertTrue(self.map.fields[0][0].shipOnField)
        self.assertEqual(self.map.shipTiles, 29)

    def test_hitField_alreadyHit(self):
        # Testet, ob ein bereits getroffenes Feld als "bereits getroffen" markiert wird
        self.map.fields[0][0].fieldHit = True
        result = self.map.hitField("A1")
        self.assertFalse(result)
        self.assertTrue(self.map.fields[0][0].fieldHit)
        self.assertFalse(self.map.fields[0][0].shipOnField)

    def test_validateShipPlacement_valid(self):
        # Testet, ob ein Schiff an einer gültigen Position platziert werden kann
        result = self.map._Map__validateShipPlacement(0, 0, "S", 3)
        self.assertTrue(result)

    def test_validateShipPlacement_invalid(self):
        # Testet, ob ein Schiff an einer ungültigen Position platziert werden kann
        # (Schiff kollidiert mit einem bereits platzierten Schiff)
        self.map.fields[0][0].shipOnField = True
        result = self.map._Map__validateShipPlacement(0, 0, "S", 3)
        self.assertFalse(result)