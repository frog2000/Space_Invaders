import sys
import pygame
import time

from bullets import Bullet, PowerfulBullet, RightSideBullet, LeftSideBullet
from sprites import Alien


def check_keydown_events(event, settings, screen, stats, sb, ship, bullets):
    """ Check for the key presses, and reacts appropriately """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, sb, ship, bullets, Bullet)
    elif event.key == pygame.K_x:
        fire_bullet(settings, screen, sb, ship, bullets, RightSideBullet)
    elif event.key == pygame.K_z:
        fire_bullet(settings, screen, sb, ship, bullets, LeftSideBullet)
    elif event.key == pygame.K_LCTRL and stats.powerful_bullets > 0:
        stats.powerful_bullets -= 1
        fire_bullet(settings, screen, sb, ship, bullets, PowerfulBullet)


def check_keyup_events(event, ship):
    """ Check for the key releases, and reacts appropriately """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_play_button(settings, screen, stats, sb, play_button, ship, aliens, bullets, alien_bullets, mouse_x, mouse_y):
    """Registers presses of the play button, and sets-up a new game"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        # return to the initial speed settings
        settings.set_dynamic_settings()

        # set the mouse cursor invisible
        pygame.mouse.set_visible(False)

        # reset the game stats and activate the game
        stats.reset_stats()
        stats.game_active = True

        # clean the scoreboard values
        sb.prep_score()
        sb.prep_level()
        sb.prep_lives()
        sb.prep_powerful_bullets()

        # empty the lists of active aliens and bullets
        aliens.empty()
        bullets.empty()
        alien_bullets.empty()

        # set up a new alien fleet and recenter the ship
        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()


def check_events(settings, screen, stats, sb, play_button, ship, aliens, bullets, alien_bullets):
    """ Checks for the keyboard and mouse events """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats, sb, play_button, ship, aliens, bullets, alien_bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, stats, sb, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def update_screen(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, loots, play_button):
    """ Refreshes the screen and draws the visible screen elements """

    # display the background
    screen.blit(settings.background, (0, 0))

    # display the scoreboard information
    sb.show_info()

    # draw the bullets
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for alien_bullet in alien_bullets.sprites():
        alien_bullet.draw_bullet()
    # draw the ship, aliens and loot
    ship.blitme()
    aliens.draw(screen)
    loots.draw(screen)

    # if the game is not currently active, display the "PLAY" button
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def update_bullets(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, loots):
    """ Updates the status of the ship bullets """
    bullets.update()
    # check if the bullets left the screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            # remove the bullets that left the screen (upper edge)
            bullets.remove(bullet)
    check_bullet_alien_collisions(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, loots)


def update_alien_bullets(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets):
    """ Updates the status of the alien bullets """
    generate_alien_bullets(aliens, alien_bullets)
    alien_bullets.update()
    # check if the bullets left the screen
    for alien_bullet in alien_bullets.copy():
        if alien_bullet.rect.bottom >= settings.screen_height:
            # remove the bullets that left the screen (bottom edge)
            alien_bullets.remove(alien_bullet)

    # check for collision of the bullets with the ship
    if pygame.sprite.spritecollideany(ship, alien_bullets):
        ship_hit(settings, stats, sb, screen, ship, aliens, bullets, alien_bullets)


def generate_alien_bullets(aliens, alien_bullets):
    """ Create new alien bullets with appropriate probability """
    for alien in aliens:
        alien.generate_alien_bullet(alien_bullets)


def check_bullet_alien_collisions(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, loots):
    """ Checks for the collision between ship bullets and the aliens"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            # if collisions are detected, increase the game score
            stats.score += settings.alien_points * len(aliens)
            sb.prep_score()  # refresh the scoreboard game score
            # generate possible loot in place of the hit alien
            for alien in aliens:
                alien.generate_loot(loots)

    # if no more aliens left, move on to the next level
    if len(aliens) == 0:
        bullets.empty()
        alien_bullets.empty()
        create_fleet(settings, screen, ship, aliens)
        settings.increase_difficulty()
        stats.level += 1
        sb.prep_level()
        time.sleep(0.5)


def ship_hit(settings, stats, sb, screen, ship, aliens, bullets, alien_bullets):
    """ Reacts to the ship being hit by resetting the level or by ending the game """
    if stats.ships_left > 0:
        stats.ships_left -= 1
        aliens.empty()
        bullets.empty()
        alien_bullets.empty()
        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()
        time.sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    sb.prep_lives()


def update_aliens(settings, stats, sb, screen, ship, aliens, bullets, alien_bullets):
    """ Updates the status of the aliens """

    check_fleet_edges(settings, aliens)
    aliens.update()

    # check for the collisions between the ship and aliens
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, stats, sb, screen, ship, aliens, bullets, alien_bullets)
    
    check_aliens_bottom(settings, stats, sb, screen, ship, aliens, bullets, alien_bullets)


def update_loots(settings, ship, loots, stats, sb):
    """ Updates the status of the loot """

    loots.update()

    # check for loot collisions with the ship
    collided_loot = pygame.sprite.spritecollideany(ship, loots)
    if collided_loot:
        collided_loot.update_ship_stats(stats)
        loots.remove(collided_loot)
        sb.prep_lives()
        sb.prep_powerful_bullets()

    # remove the loot if beyond the screen
    for loot in loots.copy():
        if loot.rect.top >= settings.screen_height:
            loots.remove(loot)


def fire_bullet(settings, screen, sb, ship, bullets, bullet_class):
    """ Fires new bullets if allowed by the game constraints """
    if len(bullets) < settings.bullets_allowed:
        new_bullet = bullet_class(settings, screen, ship)
        bullets.add(new_bullet)
        sb.prep_powerful_bullets()


def create_fleet(settings, screen, ship, aliens):
    """ Generates a fleet of aliens on the screen in the x- and y-axis """

    # generate one alien to find out its dimensions and how many aliens will fit into rows and columns
    alien = Alien(screen, settings)
    num_aliens_x = get_number_alien_columns(settings, alien.rect.width)
    num_rows = get_number_rows(settings, ship.rect.height, alien.rect.height)

    # generate aliens for the calculated number of rows and columns
    for row in range(num_rows):
        for alien_number in range(num_aliens_x):
            create_alien(settings, screen, aliens, alien_number, row)


def get_number_alien_columns(settings, alien_width):
    """ Finds out how many alien columns will fit on the x-axis """
    available_space_x = settings.screen_width - 2*alien_width
    number_aliens_x = int(available_space_x / (2*alien_width))
    return number_aliens_x


def get_number_rows(settings, ship_height, alien_height):
    """ Finds out how many alien rows will fit into the available space on the y-axis """
    available_space_y = settings.screen_height - 3*alien_height - ship_height
    number_rows = int(available_space_y / (2*alien_height))
    return number_rows


def create_alien(settings, screen, aliens, alien_number, row_number):
    """ Generates new aliens with the appropriate position in the fleet """
    alien = Alien(screen, settings)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def check_fleet_edges(settings, aliens):
    """ Checks if any of the aliens hit the edge of the screen, and if so,
    changes the direction of movement """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break


def change_fleet_direction(settings, aliens):
    """ Changes the direction of the movement for all the aliens """
    for alien in aliens.sprites():
        alien.update_y()
    settings.fleet_direction *= -1


def check_aliens_bottom(settings, stats, sb, screen, ship, aliens, bullets, alien_bullets):
    """ Checks if any of the aliens hit the bottom of the screen, and
    if so causes hit to the ship """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(settings, stats, sb, screen, ship, aliens, bullets, alien_bullets)
            break
    