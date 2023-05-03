#pylint: disable=C
#pylint: disable=W0212
import unittest
from DTO.map import Map

class MapTests(unittest.TestCase):

    def setUp(self):
        self.map = Map(0)

    def test_placeShips_validPlacement(self):
        # test placed ships on position
        result = self.map.place_ships("A1", "S", 3)
        self.assertTrue(result)
        # check if shiponfield is set to true
        self.assertTrue(self.map.fields[0][0].shiponfield)
        self.assertTrue(self.map.fields[0][1].shiponfield)
        self.assertTrue(self.map.fields[0][2].shiponfield)

    def test_placeShips_invalidPlacement(self):
        # case 1 test placing ships valide
        self.map.fields[0][0].shiponfield = True
        result = self.map.place_ships("A1", "S", 3)
        self.assertFalse(result)
        # check values dont change
        self.assertTrue(self.map.fields[0][0].shiponfield)
        self.assertFalse(self.map.fields[0][1].shiponfield)
        # case 2 test ship can be placed next to other ship
        #set E5 field to true
        self.map.fields[4][4].shiponfield = True
        result = self.map.place_ships("D4", "O", 1)
        self.assertFalse(result)
        result = self.map.place_ships("E4", "O", 1)
        self.assertFalse(result)
        result = self.map.place_ships("F4", "O", 1)
        self.assertFalse(result)
        result = self.map.place_ships("D5", "O", 1)
        self.assertFalse(result)
        result = self.map.place_ships("F5", "O", 1)
        self.assertFalse(result)
        result = self.map.place_ships("D6", "O", 1)
        self.assertFalse(result)
        result = self.map.place_ships("E6", "O", 1)
        self.assertFalse(result)
        result = self.map.place_ships("F6", "O", 1)
        self.assertFalse(result)

    def test_hitField_miss(self):
        # test field is missed, if no ship is placed
        result = self.map.hit_field("A1")
        self.assertTrue(result)
        self.assertTrue(self.map.fields[0][0].fieldhit)
        self.assertFalse(self.map.fields[0][0].shiponfield)

    def test_hitField_hit(self):
        # test ship is hitten
        self.map.fields[0][0].shiponfield = True
        result = self.map.hit_field("A1")
        self.assertTrue(result)
        self.assertTrue(self.map.fields[0][0].fieldhit)
        self.assertTrue(self.map.fields[0][0].shiponfield)
        self.assertEqual(self.map.ship_tiles, -1)

    def test_hitField_alreadyHit(self):
        # test already hitten field is marked as fieldhit
        self.map.fields[0][0].fieldhit = True
        result = self.map.hit_field("A1")
        self.assertFalse(result)
        self.assertTrue(self.map.fields[0][0].fieldhit)
        self.assertFalse(self.map.fields[0][0].shiponfield)

    def test_validateShipPlacement_valid(self):
        # tests ship has validate ship coordinates and can be placed
        result = self.map._Map__validate_ship_placement(0, 0, "S", 3)
        self.assertTrue(result)

    def test_validateShipPlacement_invalid(self):
        # tests ship has invalidate ship coordinates and cant be placed
        # ship over ship
        self.map.fields[0][0].shiponfield = True
        result = self.map._Map__validate_ship_placement(0, 0, "S", 3)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
