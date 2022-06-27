# "https://www.flaticon.com/free-icons/space-invaders" "space invaders icons" Space invaders icons created by Smashicons - Flaticon
# "https://www.flaticon.com/free-icons/alien" "alien icons" Alien icons created by smalllikeart - Flaticon
# <a href="https://www.flaticon.com/free-icons/hearth" title="hearth icons">Hearth icons created by Andrean Prabowo - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/bullet" title="bullet icons">Bullet icons created by Smashicons - Flaticon</a>

import sys
import pygame
from pygame.sprite import Group
import time

from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    pygame.init()

    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Space Invaders - PUW")
    program_icon = pygame.image.load('images/space-invaders.png')
    pygame.display.set_icon(program_icon)

    play_button = Button(settings, screen, "Play")

    stats = GameStats(settings)
    sb = Scoreboard(settings, screen, stats)

    ship = Ship(screen, settings)
    bullets = Group()
    alien_bullets = Group()
    aliens = Group()
    loots = Group()

    gf.create_fleet(settings, screen, ship, aliens)

    while True:
        frame_start = time.time()
        gf.check_events(settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(settings, screen, stats, sb, ship, aliens, bullets, loots)
            gf.update_alien_bullets(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)
            gf.update_aliens(settings, stats, sb, screen, ship, aliens, bullets, alien_bullets)
            gf.update_loots(settings, ship, loots, stats, sb)

        gf.update_screen(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, loots, play_button)

        elapsed_time = time.time() - frame_start
        if elapsed_time < settings.frame_time:
            time.sleep(settings.frame_time-elapsed_time)


if __name__ == '__main__':
    run_game()
