import pygame


class Ship:

    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.screen_rect = screen.get_rect()

        # set up the ship image and the rectangle
        self.image = pygame.image.load_extended("images/space-invaders.png")
        self.rect = self.image.get_rect()

        # set up the ship position
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.bottom-40
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        # set the movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """ Allows for the ship movement in two dimensions"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.centerx -= self.settings.ship_speed_factor
        if self.moving_up and self.rect.top > self.screen_rect.bottom*0.8:
            self.centery -= self.settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.settings.ship_speed_factor

        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def blitme(self):
        """ Draws the ship image """
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """ Places the ship image in the middle of x-axis near the bottom of the screen """
        self.centerx = self.screen_rect.centerx
        self.centery = self.screen_rect.bottom-40
