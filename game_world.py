import os, pygame
from state import State
from player import Player 
from pygame import mixer 
from jelly import Jelly
import constants 
from world import World
import csv 
from fades import Cutscene_Fadein
from castlebattle import CastleBattle


#from pause_menu import PauseMenu

class Game_World(State):
    def __init__(self, game, player_name, gender):
        State.__init__(self, game)
        self.player_name = player_name 
        self.gender = gender
        self.cutscene_fadein = Cutscene_Fadein(self.game, 1, 0,0)
        #load tilemap images
        self.tile_list = []
        self.level = 0
        for x in range(constants.TILE_TYPES):
            self.tile_image = pygame.image.load(f"maps/dungeon_tiles/{x}.png").convert_alpha()
            self.tile_image = pygame.transform.scale(self.tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
            self.tile_list.append(self.tile_image)
        #create empty tile list
        self.world_data = []
        for row in range(constants.ROWS):
            r = [-1] * constants.COLS
            self.world_data.append(r)
        #load in level data and create world
        with open(f"maps/dungeon_tiles/level{self.level}_data.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter= ",") 
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    self.world_data[x][y] = int(tile)
        self.castle_music = pygame.mixer.Sound("music/Escape From Jelly Castle.wav")
        self.castle_music.set_volume(0.3)
        self.world = World(self.game)
        self.player = self.world.player 
        self.enemy_list = self.world.character_list
        self.world.process_data(self.world_data, self.tile_list)
        screen_scroll = [0,0]
        
    
    
    def update(self, delta_time, actions):
        self.cutscene_fadein.update(delta_time, actions)
        # Check if the game was paused 
        if actions["start"]:
            pass 
        
            #new_state = PauseMenu(self.game)
            #new_state.enter_state()
        screen_scroll = self.world.player.update(delta_time, actions, self.world.obstacle_tiles)
        for enemy in self.enemy_list:
            enemy.update(delta_time, self.world.player, screen_scroll)
        self.world.update(screen_scroll)

        
    def draw(self, display):
        display.fill((0,0,0))
        self.world.draw(display)
        self.world.player.draw(display)
        for enemy in self.enemy_list:
            enemy.draw(display)
        self.cutscene_fadein.draw(display)
        if self.cutscene_fadein.fade_complete == True:
            self.castle_music.play(-1)
            
        

