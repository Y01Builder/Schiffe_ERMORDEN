
"""field class defines fieldhit and shiponfield"""
class Field:
    """ init Function"""
    def __init__(self, fieldhit, shiponfield):
        self.fieldhit = fieldhit
        self.shiponfield = shiponfield

    def get_field_hit(self):
        """get fieldhit value"""
        return self.fieldhit

    def get_ship_on_field(self):
        """get shiponfield value"""
        return self.shiponfield
