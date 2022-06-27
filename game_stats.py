
class GameStats:

    def __init__(self, settings):
        self.settings = settings
        self.game_active = False
        self.reset_stats()
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.powerful_bullets = self.settings.powerful_bullets_available

    def reset_stats(self):
        """ Resets all the game statistics """
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.powerful_bullets = self.settings.powerful_bullets_available
