import sys
import pygame
import time
import random

from bullet import Bullet, PowerfulBullet, RightSideBullet, LeftSideBullet, AlienBullet
from alien import Alien


def check_keydown_events(event, settings, screen, stats, sb, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, stats, sb, ship, bullets, Bullet)
    elif event.key == pygame.K_x:
        fire_bullet(settings, screen, stats, sb, ship, bullets, RightSideBullet)
    elif event.key == pygame.K_z:
        fire_bullet(settings, screen, stats, sb, ship, bullets, LeftSideBullet)
    elif event.key == pygame.K_LCTRL and stats.powerful_bullets > 0:
        fire_bullet(settings, screen, stats, sb, ship, bullets, PowerfulBullet)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        settings.initialise_dynamic_settings()
        pygame.mouse.set_visible(False)
        
        stats.reset_stats()
        stats.game_active = True

        sb.prep_score()
        sb.prep_level()
        sb.prep_lives()
        sb.prep_powerful_bullets()

        aliens.empty()
        bullets.empty()

        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()


def check_events(settings, screen, stats, sb, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, stats, sb, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def update_screen(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, play_button):
    screen.blit(settings.background, (0, 0))
    sb.show_info()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for alien_bullet in alien_bullets.sprites():
        alien_bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def update_bullets(settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(settings, screen, stats, sb, ship, aliens, bullets)


def update_alien_bullets(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets):

    generate_alien_bullets(settings, aliens, screen, stats, alien_bullets)
    alien_bullets.update()
    for alien_bullet in alien_bullets.copy():
        if alien_bullet.rect.bottom >= settings.screen_height:
            alien_bullets.remove(alien_bullet)
    
    if pygame.sprite.spritecollideany(ship, alien_bullets):
        ship_hit(settings, stats, sb, screen, ship, aliens, bullets, alien_bullets)


def generate_alien_bullets(settings, aliens, screen, stats, alien_bullets):
    for alien in aliens:
        random_int = random.randint(0, int(settings.alien_probability_shooting))
        if 0 == random_int:
            new_alien_bullet = AlienBullet(settings, screen, stats, alien)
            alien_bullets.add(new_alien_bullet)


def check_bullet_alien_collisions(settings, screen, stats, sb, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += settings.alien_points * len(aliens)
            sb.prep_score()

    if len(aliens) == 0:
        bullets.empty()
        create_fleet(settings, screen, ship, aliens)
        settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        time.sleep(0.5)


def ship_hit(settings, stats, sb, screen, ship, aliens, bullets, alien_bullets):
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
    print(stats.ships_left)


def update_aliens(settings, stats, sb, screen, ship, aliens, bullets, alien_bullets):
    check_fleet_edges(settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, stats, sb, screen, ship, aliens, bullets, alien_bullets)
    
    check_aliens_bottom(settings, stats, sb, screen, ship, aliens, bullets, alien_bullets)


def fire_bullet(settings, screen, stats, sb, ship, bullets, bullet_class):
    if len(bullets) < settings.bullets_allowed:
        new_bullet = bullet_class(settings, screen, stats, ship)
        bullets.add(new_bullet)
        sb.prep_powerful_bullets()


def create_fleet(settings, screen, ship, aliens):

    alien = Alien(screen, settings)
    number_aliens_x = get_number_aliens(settings, alien.rect.width)
    number_rows = get_number_rows(settings, ship.rect.height, alien.rect.height)

    for row in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(settings, screen, aliens, alien_number, row)


def get_number_aliens(settings, alien_width):
    available_space_x = settings.screen_width - 2*alien_width
    number_aliens_x = int(available_space_x / (2*alien_width))
    return number_aliens_x


def create_alien(settings, screen, aliens, alien_number, row_number):
    alien = Alien(screen, settings)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_rows(settings, ship_height, alien_height):
    available_space_y = settings.screen_height - 3*alien_height - ship_height
    number_rows = int(available_space_y / (2*alien_height))
    return number_rows


def check_fleet_edges(settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break


def change_fleet_direction(settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1


def check_aliens_bottom(settings, stats, sb, screen, ship, aliens, bullets, alien_bullets):
    
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(settings, stats, sb, screen, ship, aliens, bullets, alien_bullets)
            break
    