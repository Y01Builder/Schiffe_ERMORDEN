class Field:
    def __init__(self, fieldHit, shipOnField):
        self.fieldHit = fieldHit
        self.shipOnField = shipOnField

    def isHit(self):
        return self.fieldHit

    def isShip(self):
        return self.shipOnField
