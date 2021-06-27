import pygame as pg
from random import randint
from copy import deepcopy

RES = WIDTH, HEIGHT = 1000, 680
TILE = 20
W, H = WIDTH // TILE, HEIGHT // TILE
START_FPS = 5
MVOL = 0.3
SVOL = 0.3
    
pg.init()
pickup = pg.mixer.Sound('Pickup.mp3')
pickup.set_volume(SVOL)
gameover = pg.mixer.Sound('Gameover.mp3')
gameover.set_volume(SVOL)
pause = pg.mixer.Sound('Pause.mp3')
pause.set_volume(SVOL)
surface = pg.display.set_mode(RES)
pg.display.set_caption("Snake")
clock = pg.time.Clock()

start_screen = pg.image.load('StartScreen.png')
ctrls_screen = pg.image.load('Controls.png')
start_screen_place = start_screen.get_rect()
ctrls_screen_place = ctrls_screen.get_rect()
font = pg.font.Font(None, 64)
play = font.render('Play', True, (190, 0, 255))
play_place = play.get_rect(center = (WIDTH // 2, HEIGHT // 2 - 125))
controls = font.render('Controls', True, (190, 0, 255))
controls_place = controls.get_rect(center = (WIDTH // 2, HEIGHT // 2 - 25))
quit_ = font.render('Quit', True, (190, 0, 255))
quit_place = quit_.get_rect(center = (WIDTH // 2, HEIGHT // 2 + 75))

def move(pos, fpos, movement, score):

    next_field = [[0 for i in range(W)] for j in range(H)]
        
    if movement=='up':
        if pos[0][0]-1>=0:
            pos.insert(0,[pos[0][0]-1,pos[0][1]])
        else:
            pos.insert(0,[H-1+pos[0][0],pos[0][1]])
    elif movement=='down':
        if pos[0][0]+1<=H-1:
            pos.insert(0,[pos[0][0]+1,pos[0][1]])
        else:
            pos.insert(0,[H-1-pos[0][0],pos[0][1]])
    elif movement=='right':
        if pos[0][1]+1<=W-1:
            pos.insert(0,[pos[0][0],pos[0][1]+1])
        else:
            pos.insert(0,[pos[0][0],W-1-pos[0][1]])
    elif movement=='left':
        if pos[0][1]>=0: 
            pos.insert(0,[pos[0][0],pos[0][1]-1])
        else:
            pos.insert(0,[pos[0][0],W-1+pos[0][1]])
                
    next_field[pos[0][0]][pos[0][1]]=2
    if [pos[0][0],pos[0][1]]==fpos:
        pickup.play()
        score+=1
        while True:
            fx=randint(1,W-2)
            fy=randint(1,H-2)
            if next_field[fy][fx]==0:
                fpos=[fy,fx]
                break
    else:
        pos=pos[:len(pos)-1]
            
    for i in pos[1:]:
        next_field[i[0]][i[1]]=1
        
    return next_field, pos, fpos, score

main = False #отображение всей игры

while not main:

    surface.blit(start_screen, start_screen_place)
    play_button = pg.draw.rect(surface, pg.Color('black'), (WIDTH // 2 - 50, HEIGHT // 2 - 150, 100, 50))
    surface.blit(play, play_place)
    controls_button = pg.draw.rect(surface, pg.Color('black'), (WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50))
    surface.blit(controls, controls_place)
    quit_button = pg.draw.rect(surface, pg.Color('black'), (WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50))
    surface.blit(quit_, quit_place)
    pg.display.update()
    
    started = False #главное меню
    q = False #игровой цикл
    ctrls = True #экран с инструкцией к управлению

    pg.mixer.music.load('MainMenu.mp3')
    pg.mixer.music.set_volume(MVOL)
    pg.mixer.music.play(-1)
    
    while not started:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mpos = pg.mouse.get_pos()
                if play_button.collidepoint(mpos):
                    started = True
                elif controls_button.collidepoint(mpos):
                    ctrls = False
                    started = True
                    surface.blit(ctrls_screen, ctrls_screen_place)
                    pg.display.update()                    
                    pg.mixer.music.load('Controls.mp3')
                    pg.mixer.music.set_volume(MVOL)
                    pg.mixer.music.play(-1)
                elif quit_button.collidepoint(mpos):
                    main = True
                    q = True
                    started = True

    while not ctrls:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    ctrls = True
                    q = True
                    
    #game cycle
    while not q:

        next_field = [[0 for i in range(W)] for j in range(H)]
        current_field = [[0 for i in range(W)] for j in range(H)]
        current_field[18][25],current_field[19][25],current_field[20][25]=2,1,1
        pos = [[18,25],[19,25],[20,25]]

        while True:
            fx=randint(1,W-2)
            fy=randint(1,H-2)
            if current_field[fy][fx]==0:
                fpos=[fy,fx]
                break

        movement = 'up'    

        game_over = False
        score = 0

        pg.mixer.music.load('Music.mp3')
        pg.mixer.music.set_volume(MVOL)
        pg.mixer.music.play(-1)
        
        paused = False
        font = pg.font.Font(None, 36)
        pause_sign = font.render('PAUSE', True, (0,255,0))
        pause_place = pause_sign.get_rect(center = (WIDTH // 2, HEIGHT // 2))
        
        while True:
            
            surface.fill(pg.Color('black'))
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                elif event.type == pg.KEYDOWN:
                    if movement=='up' or movement=='down':
                        if event.key == pg.K_RIGHT or event.key == pg.K_d:
                            movement = 'right'
                        elif event.key == pg.K_LEFT or event.key == pg.K_a:
                            movement = 'left'
                    elif movement=='right' or movement=='left':
                        if event.key == pg.K_UP or event.key == pg.K_w:
                            movement = 'up'
                        elif event.key == pg.K_DOWN or event.key == pg.K_s:
                            movement = 'down'
                    if event.key == pg.K_ESCAPE:
                        if paused:
                            paused = False
                            pg.mixer.music.unpause()
                        else:
                            paused = True
                            pg.mixer.music.pause()
                            surface.blit(pause_sign, pause_place)
                            pg.display.update()
                            pause.play()
                    elif event.key == pg.K_SPACE:
                        game_over = True
                            
            if paused:
                continue
            
            [pg.draw.line(surface, pg.Color('black'), (x, 0), (x, HEIGHT)) for x in range(0, WIDTH, TILE)]
            [pg.draw.line(surface, pg.Color('black'), (0, y), (WIDTH, y)) for y in range(0, HEIGHT, TILE)]

            current_field[fpos[0]][fpos[1]]=3
                        
            for x in range(0, W):
                for y in range(0, H):
                    if current_field[y][x]==3:
                        pg.draw.rect(surface, pg.Color('red'), (x * TILE + 2, y * TILE + 2, TILE - 2, TILE - 2))
                    elif current_field[y][x]==1:
                        pg.draw.rect(surface, pg.Color('white'), (x * TILE + 2, y * TILE + 2, TILE - 2, TILE - 2))
                    elif current_field[y][x]==2:
                        pg.draw.rect(surface, pg.Color('yellow'), (x * TILE + 2, y * TILE + 2, TILE - 2, TILE - 2))

            next_field, pos, fpos, score = move(pos, fpos, movement, score)
            current_field = deepcopy(next_field)

            pg.display.flip()
            FPS = START_FPS + (score // 3)
            clock.tick(FPS)

            for i in pos[1:]:
                if pos[0]==i:
                    game_over = True
                    break

            if game_over:
                pg.mixer.music.pause()
                surface.fill(pg.Color('black'))
                gameover.play()
                font = pg.font.Font(None, 72)
                text1 = font.render('GAME OVER', True, (0,255,0))
                text2 = font.render('Score: ' + str(score), True, (0,190,255))
                text3 = font.render('quit', True, (190,0,255))
                text4 = font.render('restart', True, (190,0,255))
                place1 = text1.get_rect(center = (WIDTH // 2, HEIGHT // 2 - 50))
                place2 = text2.get_rect(center = (WIDTH // 2, HEIGHT // 2 + 30))
                place3 = text3.get_rect(center = (WIDTH // 2 + 100, HEIGHT // 2 + 100))
                place4 = text3.get_rect(center = (WIDTH // 2 - 100, HEIGHT // 2 + 100))
                surface.blit(text1, place1)
                surface.blit(text2, place2)
                rect2 = pg.draw.rect(surface, pg.Color('black'), (WIDTH // 2 + 50, HEIGHT // 2 + 75, 105, 55))
                surface.blit(text3, place3)
                rect1 = pg.draw.rect(surface, pg.Color('black'), (WIDTH // 2 - 150, HEIGHT // 2 + 75, 165, 55))
                surface.blit(text4, place4)
                pg.display.update()
                
                sub_q = False #game over цикл
                
                while True:
                    for event in pg.event.get():
                        if event.type == pg.MOUSEBUTTONDOWN:
                            mpos = pg.mouse.get_pos()
                            if rect1.collidepoint(mpos):
                                sub_q = True
                            elif rect2.collidepoint(mpos):
                                q = True
                                sub_q = True

                    if sub_q:
                        break
                                
                break

pg.quit()
