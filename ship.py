import pygame


class Ship:

    def __init__(self, screen, ai_settings):
        self.screen = screen
        self.settings = ai_settings

        self.image = pygame.image.load_extended("images/space-invaders.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom-10
        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.settings.ship_seed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= self.settings.ship_seed_factor

        self.rect.centerx = self.center

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx
