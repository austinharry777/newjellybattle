import pygame as pg

def dialogue_print(text, font, color, x,y, display):
    current_time = pg.time.get_ticks()
    font = pg.font.Font('img/MMRock9.ttf', 22)
    for i in range(len(text)):
        display.blit(font.render(text[i], True, color), (x, y))
        x += font.size(text[i])[0]
        if current_time - pg.time.get_ticks() > 100:
            pg.display.update()
            current_time = pg.time.get_ticks()
        
        
