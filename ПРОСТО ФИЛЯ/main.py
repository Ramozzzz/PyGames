from items_and_classes import *

running = True
played = False

pg.mixer.music.load('audio/StartScreen.mp3')
pg.mixer.music.set_volume(MVOL)
pg.mixer.music.play(-1)

while running:

    if played:
        for block in blocks:
            block.kill()
        for gift in gifts:
            gift.kill()
        for bad_block in bad_blocks:
            bad_block.kill()
            
        player.kill()

        pg.mixer.music.load('audio/StartScreen.mp3')
        pg.mixer.music.set_volume(MVOL)
        pg.mixer.music.play(-1)

        played = False
    
    in_main_menu = True
    in_levels = False
    in_controls = False
    playing = False
    
    while in_main_menu:

        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                in_main_menu = False
                running = False

            elif event.type == pg.MOUSEBUTTONDOWN:
                if play_button.is_clicked():
                    button_press_sound.play()
                    in_main_menu = False
                    in_levels = True
                elif controls_button.is_clicked():
                    button_press_sound.play()
                    in_main_menu = False
                    in_controls = True
                elif quit_button.is_clicked():
                    button_press_sound.play()
                    in_main_menu = False
                    running = False

        surface.blit(mm_bg, bg_place)

        mm_buttons.update()

        pg.display.flip()
        clock.tick(FPS)

    while in_controls:

        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                in_controls = False
                running = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    in_controls = False

        surface.blit(controls_screen, bg_place)

        pg.display.flip()
        clock.tick(FPS)

    while in_levels:

        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                in_levels = False
                running = False

            elif event.type == pg.MOUSEBUTTONDOWN:
                if lvl_1_button.is_clicked():
                    button_press_sound.play()
                    pg.mixer.music.load('audio/Level1.mp3')
                    lvl_num = 1
                    in_levels = False
                    playing = True
                elif lvl_2_button.is_clicked():
                    button_press_sound.play()
                    pg.mixer.music.load('audio/Level2.mp3')
                    lvl_num = 2
                    in_levels = False
                    playing = True
                elif lvl_3_button.is_clicked():
                    button_press_sound.play()
                    pg.mixer.music.load('audio/Level3.mp3')
                    lvl_num = 3
                    in_levels = False
                    playing = True
                elif lvl_4_button.is_clicked():
                    button_press_sound.play()
                    pg.mixer.music.load('audio/Level4.mp3')
                    lvl_num = 4
                    in_levels = False
                    playing = True
                elif qls_button.is_clicked():
                    button_press_sound.play()
                    in_levels = False

        surface.blit(levels_screen, bg_place)

        lvl_buttons.update()

        pg.display.flip()
        clock.tick(FPS)
        
    if playing:
        
        level = lvl_dict[lvl_num]
        background = level.background
        gameover_sign = level.gameover_sign
        win_sign = level.win_sign
        welcome_screen = level.welcome_screen

        for time in range(3 * FPS):

            for event in pg.event.get():
            
                if event.type == pg.QUIT:
                    playing = False
                    running = False

            surface.blit(welcome_screen, bg_place)

            pg.display.flip()
            clock.tick(FPS)

        level.generate()

        player = Player((TX, 16 * TY))

        pg.mixer.music.set_volume(MVOL)
        pg.mixer.music.play(-1)
        
        win = False
        game_over = False
        direction = 'forward'

        played = True

    while playing:

        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                playing = False
                running = False

            elif event.type == pg.KEYDOWN:
                if not player.moving:
                    if event.key == pg.K_RIGHT:
                        player.moving = True
                        direction = 'forward'
                    elif event.key == pg.K_LEFT:
                        player.moving = True
                        direction = 'back'

                if event.key == pg.K_UP:
                    player.jump()

                if event.key == pg.K_LSHIFT and not player.mid_air:
                    player.running = True

            elif event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT or event.key == pg.K_LEFT:
                    player.speedx = 0
                    player.moving = False
                elif event.key == pg.K_LSHIFT:
                    player.running = False

        if player.moving:
            player.move(direction)
        else:
            if not player.mid_air:
                player.image_index = 0
                if direction == 'forward':
                    player.image = player.move_animation[player.image_index]
                elif direction == 'back':
                    player.image = player.rmove_animation[player.image_index]
                player.img_state = direction

        surface.blit(background, bg_place)

        blocks.update()
        bad_blocks.update(player)
        gifts.update(player)
        
        player.update()

        if len(gifts) == 0:
            win = True

        if win:
            pg.mixer.music.pause()
            win_sound.play()
            quit_pushed = False
            for time in range(3 * FPS):
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        quit_pushed = True

                if quit_pushed:
                    running = False
                    break
                else:
                    surface.blit(win_sign, win_sign_place)

                pg.display.flip()
                clock.tick(FPS)
                
            playing = False

        else:
            if player.rect.top > HEIGHT:
                game_over = True
            else:
                for bad_block in bad_blocks:
                    if bad_block.touched(player):
                        game_over = True

            if game_over:
                pg.mixer.music.pause()
                gameover_sound.play()
                quit_pushed = False
                for time in range(3 * FPS):
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            quit_pushed = True

                    if quit_pushed:
                        running = False
                        break
                    else:
                        surface.blit(gameover_sign, gameover_sign_place)

                    pg.display.flip()
                    clock.tick(FPS)
                    
                playing = False
        
        pg.display.flip()
        clock.tick(FPS)

pg.quit()
