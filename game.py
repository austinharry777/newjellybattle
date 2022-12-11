import os, time, pygame
import constants 
from pygame import mixer
from title import Title

mixer.init()

class Game:
    def __init__(self):
        pygame.init()
        mixer.init()
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.canvas = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.running = True
        self.playing = True  
        self.actions = {'left': False, 'right': False, 'up': False, 'down': False, 'action1': False, 'action2': False, 'start': False}
        self.delt = 0
        self.prev_time = 0
        self.state_stack = []
        self.font = pygame.font.Font('img/MMRock9.ttf', 22)
        self.load_states()
        self.current_time = pygame.time.get_ticks()
        
        
    #game loop
    def game_loop(self):
        while self.playing:
            self.get_delt()
            self.get_events()
            self.update()
            self.draw()
        
#event handler
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                        self.playing = False
                        self.running = False
                if event.key == pygame.K_a:
                    self.actions['left'] = True
                if event.key == pygame.K_d:
                    self.actions['right'] = True
                if event.key == pygame.K_w:
                    self.actions['up'] = True
                if event.key == pygame.K_s:
                    self.actions['down'] = True
                if event.key == pygame.K_p:
                    self.actions['action1'] = True
                if event.key == pygame.K_o:
                    self.actions['action2'] = True    
                if event.key == pygame.K_RETURN:
                    self.actions['start'] = True  
                

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.actions['left'] = False
                if event.key == pygame.K_d:
                    self.actions['right'] = False
                if event.key == pygame.K_w:
                    self.actions['up'] = False
                if event.key == pygame.K_s:
                    self.actions['down'] = False
                if event.key == pygame.K_p:
                    self.actions['action1'] = False
                if event.key == pygame.K_o:
                    self.actions['action2'] = False
                if event.key == pygame.K_RETURN:
                    self.actions['start'] = False  
    def update(self):
        self.state_stack[-1].update(self.delt, self.actions)
    
    def draw(self):
        self.state_stack[-1].draw(self.canvas)
        self.screen.blit(pygame.transform.scale(self.canvas, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)), (0,0))
        pygame.display.flip()

    def get_delt(self):
        now = time.time()
        self.delt = now - self.prev_time
        self.prev_time = now 

    #function for drawing text
    def draw_text(self, surface, text, color, x,y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        surface.blit(text_surface, text_rect)

    #function for drawing text by letter
    def draw_text_by_letter(self, surface, text, color, x,y):
        #
        text_delay = 100 
        # Create an empty list to store the individual letters of the text
        letters = []
        # Loop through each character in the text and create a surface
        # for each letter, with the character as its text
        for char in text:
            letter_surface = self.font.render(char, True, color)
            letters.append(letter_surface)
        
        # Loop through the list of letters
        for letter in letters:
            if pygame.time.get_ticks() - self.current_time > text_delay:
                # Blit the letter onto the screen at the given position
                surface.blit(letter, (x, y))
                # Increment the x position by the width of the letter
                # plus a small gap of 10 pixels
                x += letter.get_width() +1 
                # Reset the current time
                self.current_time = pygame.time.get_ticks()
            
                

    def load_states(self):
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)
    
    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False

if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()














