import pygame.font


class Button:

    def __init__(self, ai_settings, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # choose the button dimensions, button and text colours and text font
        self.width, self.height = 200, 50
        self.button_colour = (255, 255, 255)
        self.text_colour = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center  # centre the button in the screen
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """ Prepares the button text """
        self.msg_image = self.font.render(msg, True, self.text_colour, self.button_colour)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
