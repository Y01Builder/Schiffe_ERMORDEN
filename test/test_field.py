#pylint: disable=C
import unittest
from DTO.field import Field


class TestField(unittest.TestCase):

    def test_get_field_hit(self):
        field = Field(True, False)
        self.assertTrue(field.get_field_hit())
        field.fieldhit = False
        self.assertFalse(field.get_field_hit())

    def test_get_ship_on_field(self):
        field = Field(False, True)
        self.assertTrue(field.get_ship_on_field())
        field.shiponfield = False
        self.assertFalse(field.get_ship_on_field())


if __name__ == "__main__":
    unittest.main()
