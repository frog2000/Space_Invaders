import pygame.font


class Scoreboard:

    def __init__(self, settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings

        self.stats = stats

        self.text_colour = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 40)
        self.prep_score()
        self.prep_level()
        self.prep_lives()
        self.prep_powerful_bullets()

    def prep_score(self):
        msg = "Score: " + str(self.stats.score)
        self.score_image = self.font.render(msg, True, self.text_colour)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right -20
        self.score_rect.top = 20

    def prep_level(self):
        msg = "Level: " + str(self.stats.level)
        self.level_image = self.font.render(msg, True, self.text_colour)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right -20
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_lives(self):
        msg = "Starships Left: " + str(self.stats.ships_left)
        self.life_image = self.font.render(msg, True, self.text_colour)
        self.life_rect = self.life_image.get_rect()
        self.life_rect.centerx = self.screen_rect.centerx
        self.life_rect.top = 20

    def prep_powerful_bullets(self):
        msg = "Pulses Left: " + str(self.stats.powerful_bullets)
        self.power_bullet_image = self.font.render(msg, True, self.text_colour)
        self.power_bullet_rect = self.power_bullet_image.get_rect()
        self.power_bullet_rect.left = 10
        self.power_bullet_rect.top = 20

    def show_info(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.life_image, self.life_rect)
        self.screen.blit(self.power_bullet_image, self.power_bullet_rect)
