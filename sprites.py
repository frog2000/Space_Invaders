import pygame
from pygame.sprite import Sprite
import random
from bullets import AlienBullet


def _check_if_event_happens(probability_factor):
    if 0 == random.randint(0, int(probability_factor)):
        return True
    return False


class Alien(Sprite):

    def __init__(self, screen, settings):
        super().__init__()
        self.screen = screen
        self.settings = settings

        self.image = pygame.image.load_extended("images/alien2.png")
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.x += self.settings.alien_speed_factor * self.settings.fleet_direction
        self.rect.x = self.x

    def update_y(self):
        self.rect.y += self.settings.fleet_drop_speed

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def generate_loot(self, loots):
        if _check_if_event_happens(self.settings.loot_probability):
            loots.add(LootHealth(self.screen, self.settings, self.rect.x, self.rect.y))
        elif _check_if_event_happens(self.settings.loot_probability):
            loots.add(LootPowerfulBullet(self.screen, self.settings, self.rect.x, self.rect.y))

    def generate_alien_bullet(self, alien_bullets):
        if _check_if_event_happens(self.settings.alien_probability_shooting):
            new_alien_bullet = AlienBullet(self.settings, self.screen, self)
            alien_bullets.add(new_alien_bullet)


class LootHealth(Sprite):

    def __init__(self, screen, settings, x, y):
        super().__init__()

        self.screen = screen
        self.settings = settings

        self.image = pygame.image.load_extended("images/hearth.png")
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += self.settings.loot_drop_speed

    def update_ship_stats(self, stats):
        stats.ships_left += 1


class LootPowerfulBullet(LootHealth):

    def __init__(self, screen, settings, x, y):
        super().__init__(screen, settings, x, y)

        self.image = pygame.image.load_extended("images/ammo.png")
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def update_ship_stats(self, stats):
        stats.powerful_bullets += 1
