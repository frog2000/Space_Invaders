# Adrian Krzyzanowski - PUW 2022
# Game inspired by the Space Invaders
# This a modification and expansion of the code originally
# written by Eric Matthes in the book "Python Crash Course"
# No Starch Press, San Francisco, 2016
#
# All images are used through the open license
# Sprite images were taken from:
# https://www.flaticon.com/free-icons/space-invaders - Space invaders icon created by Smashicons - Flaticon
# https://www.flaticon.com/free-icons/alien - Alien icon created by smalllikeart - Flaticon
# https://www.flaticon.com/free-icons/hearth - Hearth icon created by Andrean Prabowo - Flaticon
# https://www.flaticon.com/free-icons/bullet - Bullet icon created by Smashicons - Flaticon

import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    pygame.init()
    settings = Settings()

    # set up the screen
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    # set up caption and the icon
    pygame.display.set_caption("Space Invaders - PUW")
    program_icon = pygame.image.load('images/space-invaders.png')
    pygame.display.set_icon(program_icon)

    play_button = Button(screen, "Play")
    stats = GameStats(settings)
    sb = Scoreboard(screen, stats)
    ship = Ship(screen, settings)

    # create groups for multiple sprites on the screen
    bullets = Group()
    alien_bullets = Group()
    aliens = Group()
    loots = Group()

    # create alien fleet
    gf.create_fleet(settings, screen, ship, aliens)
    # initialise the game clock
    clock = pygame.time.Clock()

    while True:
        # clock the game to the specific fps
        clock.tick(settings.fps)

        # check for the mouse and keyboard events
        gf.check_events(settings, screen, stats, sb, play_button, ship, aliens, bullets, alien_bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, loots)
            gf.update_alien_bullets(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)
            gf.update_aliens(settings, stats, sb, screen, ship, aliens, bullets, alien_bullets)
            gf.update_loots(settings, ship, loots, stats, sb)

        gf.update_screen(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, loots, play_button)


if __name__ == '__main__':
    run_game()
