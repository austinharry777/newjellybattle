import pygame
from player import Player
from jelly import Jelly 
from items import Item
import constants

class World():
    def __init__(self, game):
        self.game = game 
        self.map_tiles = []
        self.obstacle_tiles = []
        self.exit_tile = None
        self.item_list = []
        self.player = None
        self.character_list = []
        

    def process_data(self, data, tile_list):
        self.level_length = len(data)
        #iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x * constants.TILE_SIZE
                image_y = y * constants.TILE_SIZE
                image_rect.center = image_x, image_y
                tile_data = [image, image_rect, image_x, image_y]
                
                if tile == 1 or tile == 2 or tile == 6 or tile ==7:
                    self.obstacle_tiles.append(tile_data)
                elif tile == 3:
                    self.exit_tile = tile_data 
                #elif tile == 9:
                    #coin = Item(image_x, image_y, 0, item_images[0])
                    #self.item_list.append(coin)
                    #tile_data[0] = tile_list[0]
                #elif tile == 10:
                    #potion = Item(image_x, image_y, 1, [item_images[1]])
                    #self.item_list.append(potion)
                    #tile_data[0] = tile_list[0]
                elif tile == 11:
                    player = Player(self.game, image_x, image_y)
                    self.player = player
                    tile_data[0] = tile_list[0]
                elif tile >= 12 and tile <= 15:
                    enemy = Jelly(self.game, image_x, image_y, tile - 12)
                    self.character_list.append(enemy)
                    tile_data[0] = tile_list[0]
                
                #add image data to main tiles list
                if tile >= 0:
                    self.map_tiles.append(tile_data)

    def draw(self, display):
        for tile in self.map_tiles:
            display.blit(tile[0], tile[1])

    def update(self, screen_scroll):
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])