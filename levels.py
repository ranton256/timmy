from random import randint

class Level:
    """
    rows is count of rows of aliens
    mobs is a dict keyed by string the type of mobs besides bats.
    it is key='mobname string' to value 'int frequency of mob out of 10000 chances'
    """
    def __init__(self, rows=1, mobs={}):
        self.rows = rows
        self.mobs = mobs

    # TODO: this or its calling code isn't working.
    def roll_for_mob(self, mob_name):
        if mob_name in self.mobs:
            chances = int(self.mobs[mob_name]) or 0
            return randint(chances, 10000) == 0
        return False
