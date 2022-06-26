import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):

    def __init__(self, settings, screen, stats, origin_object):
        super().__init__()
        self.screen = screen

        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.centerx = origin_object.rect.centerx
        self.rect.top = origin_object.rect.top

        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

        self.colour = settings.bullet_colour
        self.speed_factor = settings.bullet_speed_factor

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.colour, self.rect)


class AlienBullet(Bullet):
    def __init__(self, settings, screen, stats, origin_object):
        super().__init__(settings, screen, stats, origin_object)

        self.colour = settings.alien_bullet_colour
        self.speed_factor = settings.alien_bullet_speed_factor

    def update(self):
        self.y += self.speed_factor
        self.rect.y = self.y


class RightSideBullet(Bullet):
    def __init__(self, settings, screen, stats, origin_object):
        super().__init__(settings, screen, stats, origin_object)

        self.rect = pygame.Rect(0, 0, settings.sidebullet_size, settings.sidebullet_size)
        self.rect.right = origin_object.rect.right
        self.rect.top = origin_object.rect.centery
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y
        self.x += self.speed_factor
        self.rect.x = self.x


class LeftSideBullet(Bullet):
    def __init__(self, settings, screen, stats, origin_object):
        super().__init__(settings, screen, stats, origin_object)

        self.rect = pygame.Rect(0, 0, settings.sidebullet_size, settings.sidebullet_size)
        self.rect.left = origin_object.rect.left
        self.rect.top = origin_object.rect.centery
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y
        self.x -= self.speed_factor
        self.rect.x = self.x


class PowerfulBullet(Bullet):

    def __init__(self, settings, screen, stats, origin_object):
        super().__init__(settings, screen, stats, origin_object)

        self.rect = pygame.Rect(0, 0, settings.screen_width * 2, settings.bullet_height)
        self.colour = settings.powerful_bullet_colour
        stats.powerful_bullets -= 1
