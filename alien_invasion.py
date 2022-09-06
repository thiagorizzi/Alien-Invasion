import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create resources."""
        pygame.init()

        # Create instance of Settings
        self.settings = Settings()

        # Set the background color

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)


        # Create instance of Ship
        # The self argument refers to the current instance of AlienInvasion. 
        self.ship = Ship(self)
        
        # create a group in AlienInvasion to store all the live bullets so we can manage the bullets that have already been fired. 
        # This group will be an instance of the pygame.sprite.Group class
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet_()


    def _check_events_(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:   
                    self._check_KEYDOWN_(event)      
                elif event.type == pygame.KEYUP:
                    self._check_KEYUP_(event)

    def _fire_bullet_(self):
        """Create a new bullet and add it to the bullets group."""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _create_fleet_(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                                (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):    
            for alien_number in range(number_aliens_x):
                # Create an alien and place it in the row.
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)


    def _check_KEYDOWN_(self, event):
        """Check for key right and left presses"""
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right
            self.ship.moving_right = True
            self.ship.update()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet_()

        if event.key == pygame.K_LEFT:
            # Move the ship to the left
            self.ship.moving_left = True
            self.ship.update()

    def _check_KEYUP_(self, event):
        """Check for the moment the user stops holding the key"""
        if event.key == pygame.K_RIGHT:
            # Stop the ship from moving
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            # Stop the ship from moving
            self.ship.moving_left = False

    def _update_aliens(self):
        """Check if the fleet is at an edge,
        then update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()


    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 1:
            # Decrement ships_left.
            self.stats.ships_left -= 1
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and center the ship.
            self._create_fleet_()
            self.ship.center_ship()
            # Pause.
            sleep(0.5)

        else:
            self.stats.game_active = False

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
                    
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events_()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens() 
                self._update_screen()
              
            
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()

        if not self.aliens:
        # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet_()

        
    def _check_bullet_alien_collision(self):
        """Check for any bullets that have hit aliens.
        If so, get rid of the bullet and the alien."""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        # Draw the ship on the screen
        self.ship.blitme()

        # Draw all the bullets to the screen for every loop interation
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        self.aliens.draw(self.screen)

        # Make the most recently drawn screen visible
        pygame.display.flip()
           

if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()
