import pygame.font


class Scoreboard:

    def __init__(self, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats

        # set up the tex colour and font of the scoreboard
        self.text_colour = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 40)

        # create the original scoreboard text
        self.prep_score()
        self.prep_level()
        self.prep_lives()
        self.prep_powerful_bullets()

    def prep_score(self):
        """ Prepares the game score text """
        self.score_image = self._render_text_image("Score: ", self.stats.score)
        # text image orientation
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right -20
        self.score_rect.top = 20

    def prep_level(self):
        """ Prepares the game level text """
        self.level_image = self._render_text_image("Level: ", self.stats.level)
        # text image orientation
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right -20
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_lives(self):
        """ Prepares the text describing how many lives are left"""
        self.life_image = self._render_text_image("Starships Left: ", self.stats.ships_left)
        # text image orientation
        self.life_rect = self.life_image.get_rect()
        self.life_rect.centerx = self.screen_rect.centerx
        self.life_rect.top = 20

    def prep_powerful_bullets(self):
        """ Prepares the text describing how many bullet pulses/powerful bullets are left"""
        self.power_bullet_image = self._render_text_image("Pulses Left: ", self.stats.powerful_bullets)
        # text image orientation
        self.power_bullet_rect = self.power_bullet_image.get_rect()
        self.power_bullet_rect.left = 10
        self.power_bullet_rect.top = 20

    def show_info(self):
        """ Shows the scoreboard text on the screen """
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.life_image, self.life_rect)
        self.screen.blit(self.power_bullet_image, self.power_bullet_rect)

    def _render_text_image(self, title, stat):
        """ Renders text """
        msg = title + str(stat)
        return self.font.render(msg, True, self.text_colour)
