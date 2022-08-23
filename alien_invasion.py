import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet

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

        # Create instance of Ship
        # The self argument refers to the current instance of AlienInvasion. 
        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()


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
                    
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events_()
            self._update_screen()
            self.ship.update()
            self.bullets.update()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        # Draw the ship on the screen
        self.ship.blitme()

        # Draw the bullets on the screen
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Make the most recently drawn screen visible
        pygame.display.flip()
           

if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()
