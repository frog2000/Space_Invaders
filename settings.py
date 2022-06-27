import pygame


class Settings:

    def __init__(self):
        # Settings of the screen
        self.screen_width = 1200
        self.screen_height = 800
        self.background = pygame.image.load("images/space.jpg")

        self.ship_seed_factor = 10
        self.ship_limit = 3

        self.bullet_speed_factor = 15
        self.alien_bullet_speed_factor = 5
        self.bullet_width = 3
        self.bullet_height = 15
        self.sidebullet_size = 7
        self.bullet_colour = 0, 231, 252
        self.alien_bullet_colour = 255, 0, 0
        self.powerful_bullet_colour = 250, 254, 0

        self.bullets_allowed = 3
        self.powerful_bullets_available = 3

        self.alien_speed_factor = 5
        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        self.frame_time = 0.016

        self.speed_up_scale = 1.1
        self.initialise_dynamic_settings()

        self.alien_points = 50

        self.alien_probability_shooting = 4000

        self.loot_drop_speed = 3
        self.loot_probability = 100

    def initialise_dynamic_settings(self):
        self.ship_seed_factor = 10
        self.bullet_speed_factor = 15
        self.alien_speed_factor = 5
        self.fleet_direction = 1
        self.alien_probability_shooting = 4000

    def increase_speed(self):
        self.ship_seed_factor *= self.speed_up_scale
        self.bullet_speed_factor *= self.speed_up_scale
        self.alien_speed_factor *= self.speed_up_scale
        self.alien_probability_shooting /= self.speed_up_scale
