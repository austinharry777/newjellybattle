import pygame
import constants    
import math
import random 





class BatPlayer:
    def __init__(self, game, x,y, player_name, max_hp, max_mp, atk=10, defense=5, potions=1, gender = 0, level = 1, xp = 0):
        self.game = game
        self.player_name = player_name
        self.action = 0 #0: idle, 1: attack, 2: hurt, 3: dead, 4: potion, 5: victory
        self.current_frame, self.last_frame_update = 0,0
        self.load_sprites()
        self.rect = self.curr_image.get_rect()
        self.rect.midbottom = x,y
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mp = max_mp
        self.mp = max_mp
        self.atk = atk
        self.defense = defense
        self.potions = potions
        self.level = level
        self.xp = xp
        self.alive = True 
        self.gender = gender  #0 is female, #1 is male 
        self.damage_text_group = pygame.sprite.Group()

    def update(self, delta_time, actions):
        self.animate(delta_time)
        self.damage_text_group.update(delta_time)
        

    def draw(self, display):
        #if self.action == 1 or 4:
            #display.blit(self.curr_image, (self.rect.x, self.rect.y + 47 * 3))

        
        display.blit(self.curr_image, self.rect) 
        self.damage_text_group.draw(display)

    def animate(self, delta_time):
        # Compute how much time has passed since the frame last updated
        self.last_frame_update += delta_time
        # Advance the animation if enough time has elapsed
        if self.last_frame_update > .13:
            self.last_frame_update = 0
            if self.action == 0:
                self.current_frame = (self.current_frame +1) % len(self.animation_list[self.action])
                self.curr_image = self.animation_list[self.action][self.current_frame]
            
            else:
                if self.current_frame >= len(self.animation_list[self.action]) - 1:
                    if self.action == 3 or self.action == 5:
                        self.current_frame = len(self.animation_list[self.action]) - 1
                        self.curr_image = self.animation_list[self.action][self.current_frame]
                    else:
                        self.idle()
                        self.curr_image = self.animation_list[self.action][self.current_frame]
                else:
                    self.current_frame = self.current_frame +1
                    self.curr_image = self.animation_list[self.action][self.current_frame]
                
            
    
    def load_sprites(self):
        self.animation_list = []
        #Turned based sprites
        #load idle images
        temp_list = []
        for i in range (8):
            img = pygame.image.load(f'img/playerfemtattered/idle/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width()*3, img.get_height()*3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load attack images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/playerfemtattered/attack/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load hurt images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/playerfemtattered/hurt/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load dead images
        temp_list = []
        for i in range(12):
            img = pygame.image.load(f'img/playerfemtattered/death/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load potion use images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/playerfemtattered/potion/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load victory images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/playerfemtattered/victory/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.curr_image = self.animation_list[self.action][self.current_frame]

    def idle(self):
        self.action = 0
        self.current_frame = 0
        self.last_frame_update = 0
    
    def attack(self, enemy):
        variance = random.randint(-5,5)
        damage = self.atk + variance
        enemy.hp -= damage 
        enemy.hurt()
        #check if enemy has died
        if enemy.hp < 0: 
            enemy.hp = 0
            enemy.alive = False 
            enemy.dead()
            #self.victory()
        damage_text = DamageText(enemy.rect.centerx, enemy.rect.y + 20, str(damage), constants.RED)
        self.damage_text_group.add(damage_text)
        #set variables to attack animation
        self.action = 1
        self.current_frame = 0
        self.last_frame_update = 0

    def hurt(self):
        self.action = 2
        self.current_frame = 0
        self.last_frame_update = 0

    def dead(self):
        self.action = 3
        self.current_frame = 0
        self.last_frame_update = 0
    
    def use_potion(self):
        if self.max_hp - self.hp >= 30:
            heal = 30
        else:
            heal = self.max_hp - self.hp
        self.hp += heal 
        self.potions -= 1
        heal_text = DamageText(self.rect.centerx, self.rect.y + 50, str(heal), constants.GREEN)
        self.damage_text_group.add(heal_text)
        self.action = 4
        self.current_frame = 0
        self.last_frame_update = 0

    def victory(self):
        self.action = 5
        self.current_frame = 0
        self.last_frame_update = 0

    # def spell(self):
    #     self.action = 6
    #     self.current_frame = 0
    #     self.last_frame_update = 0



class BatJelly:
    def __init__(self, game, x,y, type, max_hp, atk=10, defense=0, potions=0):
        self.game = game
        self.type = type  #0: strawberry, 1: grape, 2: peanut
        self.action = 0 #0: idle, 1: attack, 2: hurt, 3: dead
        self.current_frame, self.last_frame_update = 0,0
        self.load_sprites()
        self.rect = self.curr_image.get_rect()
        self.rect.center = x,y
        self.max_hp = max_hp
        self.hp = max_hp
        self.atk = atk
        self.defense = defense
        self.potions = potions 
        self.alive = True
        self.damage_text_group = pygame.sprite.Group()
        
    def update(self, delta_time, actions):
        self.animate(delta_time)
        self.damage_text_group.update(delta_time)

    def draw(self, display):
        display.blit(self.curr_image, self.rect)
        self.damage_text_group.draw(display)

    def animate(self, delta_time):
        # Compute how much time has passed since the frame last updated
        self.last_frame_update += delta_time
        # Advance the animation if enough time has elapsed
        if self.last_frame_update > .13:
            self.last_frame_update = 0
            if self.action == 0:
                self.current_frame = (self.current_frame +1) % len(self.animation_list[self.type][self.action])
                self.curr_image = self.animation_list[self.type][self.action][self.current_frame]
            
            else:
                if self.current_frame >= len(self.animation_list[self.type][self.action]) - 1:
                    if self.action == 3:
                        self.current_frame = len(self.animation_list[self.type][self.action]) - 1
                        self.curr_image = self.animation_list[self.type][self.action][self.current_frame]
                    else:
                        self.idle()
                        self.curr_image = self.animation_list[self.type][self.action][self.current_frame]
                else:
                    self.current_frame = self.current_frame +1
                    self.curr_image = self.animation_list[self.type][self.action][self.current_frame]
        

    def load_sprites(self):
        self.animation_list = []
        self.strawberry_list, self.grape_list, self.peanut_list = [], [], []
        
        #Turned based sprites for strawberry jelly
        #load idle images
        temp_list = []
        for i in range (8):
            img = pygame.image.load(f'img/jellysprites/strawberry/idle/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width()*3, img.get_height()*3))
            temp_list.append(img)
        self.strawberry_list.append(temp_list)
        #load attack images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/jellysprites/strawberry/attack/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.strawberry_list.append(temp_list)
        #load hurt images
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'img/jellysprites/strawberry/hurt/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.strawberry_list.append(temp_list)
        #load dead images
        temp_list = []
        for i in range(12):
            img = pygame.image.load(f'img/jellysprites/strawberry/death/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.strawberry_list.append(temp_list)
        self.animation_list.append(self.strawberry_list) 
        
        #Turned based sprites for grape jelly
        #load idle images
        temp_list = []
        for i in range (8):
            img = pygame.image.load(f'img/jellysprites/grape/idle/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width()*3, img.get_height()*3))
            temp_list.append(img)
        self.grape_list.append(temp_list)
        #load attack images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/jellysprites/grape/attack/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.grape_list.append(temp_list)
        #load hurt images
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'img/jellysprites/grape/hurt/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.grape_list.append(temp_list)
        #load dead images
        temp_list = []
        for i in range(12):
            img = pygame.image.load(f'img/jellysprites/grape/death/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.grape_list.append(temp_list)
        self.animation_list.append(self.grape_list)

        #Turned based sprites for peanut jelly
        #load idle images
        temp_list = []
        for i in range (8):
            img = pygame.image.load(f'img/jellysprites/peanut/idle/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width()*3, img.get_height()*3))
            temp_list.append(img)
        self.peanut_list.append(temp_list)
        #load attack images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/jellysprites/peanut/attack/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.peanut_list.append(temp_list)
        #load hurt images
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'img/jellysprites/peanut/hurt/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.peanut_list.append(temp_list)
        #load dead images
        temp_list = []
        for i in range(12):
            img = pygame.image.load(f'img/jellysprites/peanut/death/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.peanut_list.append(temp_list)
        self.animation_list.append(self.peanut_list)
        self.curr_image = self.animation_list[self.type][self.action][self.current_frame]



    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.last_frame_update = 0
    
    def attack(self, enemy):
        variance = random.randint(-5,5)
        damage = self.atk + variance
        enemy.hp -= damage
        enemy.hurt()
         #check if player has died
        if enemy.hp < 0: 
            enemy.hp = 0
            enemy.alive = False 
            enemy.dead()
        damage_text = DamageText(enemy.rect.centerx - 5, enemy.rect.y, str(damage), constants.RED)
        self.damage_text_group.add(damage_text)
        #set variables to attack animation
        self.action = 1
        self.frame_index = 0
        self.last_frame_update = 0
        

    def hurt(self):
        self.action = 2
        self.frame_index = 0
        self.last_frame_update = 0

    def dead(self):
        self.action = 3
        self.frame_index = 0
        self.last_frame_update = 0

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x,y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font('img/MMRock9.ttf', 22)
        self.image = self.font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0
        self.last_frame_update = 0
        
    def update(self, delta_time):
        self.last_frame_update += delta_time
        #move damage text up
        if self.last_frame_update > 0.05:
            self.rect.y -= 1
            self.last_frame_update = 0
            self.counter += 1
            # delete damage text after 1 second
            if self.counter > 40:
                self.kill()



        
         