from attributes_and_classes import *

for sound in all_sounds:
    sound.set_volume(SVOL)

game_opened = True #триггер основного цикла
ran = True #триггер для непрерывности музыки и фона

#основной цикл программы
while game_opened:

    start_screen = True #триггер начального экрана
    running = True #триггер внешнего игрового цикла
    settings = False #триггер экрана с настройками
    controls = False #триггер экрана с инструкцией управления

    if ran:
        for i in range(10):
                
            asteroid = Asteroid()
            asteroid.add(asteroids)
            asteroid.angle = 150
            asteroid.speed = 5

        pg.mixer.music.load('StartScreen.mp3')
        pg.mixer.music.set_volume(MVOL)
        pg.mixer.music.play(-1)
        
        ran = False

    #цикл начального экрана        
    while start_screen:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                start_screen = False
                running = False
                game_opened = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if play_button.is_clicked():
                    button_click.play()
                    start_screen = False
                elif settings_button.is_clicked():
                    button_click.play()
                    start_screen = False
                    settings = True
                elif controls_button.is_clicked():
                    button_click.play()
                    start_screen = False
                    controls = True
                elif quit_button.is_clicked():
                    button_click.play()
                    start_screen = False
                    running = False
                    game_opened = False

        surface.blit(start_screen_background, ssb_place)

        asteroids.update()

        menu = pg.Surface((600, 380))
        menu_place = menu.get_rect(center = (W // 2, H // 2))
        menu.fill('red')
        menu.set_alpha(100)

        surface.blit(menu, menu_place)
        pg.draw.rect(surface, 'brown', (200, 150, 600, 380), 3)
        surface.blit(main_title, main_title_place)
        main_menu_buttons.update()
            
        pg.display.flip()
        clock.tick(FPS)

    #цикл настроек
    while settings:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                settings = False
                running = False
                game_opened = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if settings_quit_button.is_clicked():
                    button_click.play()
                    settings = False
                    running = False
                elif difficulty_swap_button.is_clicked():
                    settings_button_click.play()
                    if difficulty == 'easy':
                        difficulty = 'medium'
                        difficulty_swap_button.text = medium_sign
                    elif difficulty == 'medium':
                        difficulty = 'hard'
                        difficulty_swap_button.text = hard_sign
                    elif difficulty == 'hard':
                        difficulty = 'extreme'
                        difficulty_swap_button.text = extreme_sign
                    elif difficulty == 'extreme':
                        difficulty = 'easy'
                        difficulty_swap_button.text = easy_sign

                elif mv_plus_button.is_clicked():
                    settings_button_click.play()
                    if MVOL < 1:
                        MVOL += 0.1
                        MVOL = round(MVOL, 1)
                        pg.mixer.music.set_volume(MVOL)
                        mv_swap = sign_font.render(str(MVOL), True, 'black')

                elif mv_minus_button.is_clicked():
                    settings_button_click.play()
                    if MVOL > 0:
                        MVOL -= 0.1
                        MVOL = round(MVOL, 1)
                        pg.mixer.music.set_volume(MVOL)
                        mv_swap = sign_font.render(str(MVOL), True, 'black')

                elif sv_plus_button.is_clicked():
                    settings_button_click.play()
                    if SVOL < 1:
                        SVOL += 0.1
                        SVOL = round(SVOL, 1)
                        for sound in all_sounds:
                            sound.set_volume(SVOL)
                        sv_swap = sign_font.render(str(SVOL), True, 'black')

                elif sv_minus_button.is_clicked():
                    settings_button_click.play()
                    if SVOL > 0:
                        SVOL -= 0.1
                        SVOL = round(SVOL, 1)
                        for sound in all_sounds:
                            sound.set_volume(SVOL)
                        sv_swap = sign_font.render(str(SVOL), True, 'black')

        surface.blit(start_screen_background, ssb_place)

        asteroids.update()

        menu = pg.Surface((600, 380))
        menu_place = menu.get_rect(center = (W // 2, H // 2))
        menu.fill('red')
        menu.set_alpha(100)

        surface.blit(menu, menu_place)
        pg.draw.rect(surface, 'brown', (200, 150, 600, 380), 3)
        surface.blit(settings_title, settings_title_place)
        surface.blit(difficulty_sign, difficulty_sign_place)
        surface.blit(music_volume_sign, mv_sign_place)
        surface.blit(mv_swap, mv_swap_place)
        surface.blit(sound_volume_sign, sv_sign_place)
        surface.blit(sv_swap, sv_swap_place)

        if MVOL == 1:
            mv_plus_button.murk = True
        elif mv_plus_button.murk:
            mv_plus_button.murk = False

        if MVOL == 0:
            mv_minus_button.murk = True
        elif mv_minus_button.murk:
            mv_minus_button.murk = False

        if SVOL == 1:
            sv_plus_button.murk = True
        elif sv_plus_button.murk:
            sv_plus_button.murk = False

        if SVOL == 0:
            sv_minus_button.murk = True
        elif sv_minus_button.murk:
            sv_minus_button.murk = False
        
        settings_buttons.update()
            
        pg.display.flip()
        clock.tick(FPS)

    #цикл экрана с инструкцией
    while controls:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                start_screen = False
                running = False
                game_opened = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if controls_quit_button.is_clicked():
                    button_click.play()
                    controls = False
                    running = False

        surface.blit(start_screen_background, ssb_place)

        asteroids.update()

        menu = pg.Surface((600, 380))
        menu_place = menu.get_rect(center = (W // 2, H // 2))
        menu.fill('red')
        menu.set_alpha(100)

        surface.blit(menu, menu_place)
        pg.draw.rect(surface, 'brown', (200, 150, 600, 380), 3)
        surface.blit(controls_title, controls_title_place)
        surface.blit(instruction1, instruction1_place)
        surface.blit(instruction2, instruction2_place)
        surface.blit(instruction3, instruction3_place)
        surface.blit(instruction4, instruction4_place)
        controls_quit_button.update()
            
        pg.display.flip()
        clock.tick(FPS)
        
    #внешний цикл игры        
    while running:

        pg.mixer.music.load('Gameplay.mp3')
        pg.mixer.music.set_volume(MVOL)
        pg.mixer.music.play(-1)

        for asteroid in asteroids:
            asteroid.kill()

        ran = True

        #настройки в соответствии с уровнем сложности
        if difficulty == 'easy':
            ammount = 3
            asteroid_spawn_frequency = 210
            resistance_bonus_spawntime = 1200
            life_bonus_spawntime = 1800
            speed_bonus_spawntime = 900

        elif difficulty == 'medium':
            ammount = 5
            asteroid_spawn_frequency = 150
            resistance_bonus_spawntime = 1500
            life_bonus_spawntime = 1800 #не будет появляться
            speed_bonus_spawntime = 1200

        elif difficulty == 'hard':
            ammount = 7
            asteroid_spawn_frequency = 90
            resistance_bonus_spawntime = 1500 #не будет появляться
            life_bonus_spawntime = 1800 #не будет появляться
            speed_bonus_spawntime = 1200

        elif difficulty == 'extreme':
            ammount = 10
            asteroid_spawn_frequency = 30
            resistance_bonus_spawntime = 1500 #не будет появляться
            life_bonus_spawntime = 1800 #не будет появляться
            speed_bonus_spawntime = 1200 #не будет появляться

        asteroid_spawn_timer = 0 #таймер появления нового астероида
        resistance_bonus_spawntimer = 0 #таймер появления бонуса защиты
        life_bonus_spawntimer = 0 #таймер появления бонуса доп жизни
        speed_bonus_spawntimer = 0 #таймер появления бонуса скорости
        respawn_timer = 0 #таймер респауна игрока
        respawn_time = 120 #время до респауна после смерти
        
        #спаун игрока и нескольких астероидов в начале
        ship = Player()
        ships.add(ship)
        for i in range(ammount):
            asteroid = Asteroid()
            asteroids.add(asteroid)

        #количество жизней и очков и их отображение
        lives = 3
        lives_num = gameplay_font.render(str(lives), False, 'green')
        lives_num_place = lives_num.get_rect(center = (140, 50))
        score = 0
        score_num = gameplay_font.render(str(score), False, 'green')
        score_num_place = score_num.get_rect(center = (150, 100))

        #триггеры для игрового процесса
        playing = True #триггер внутреннего игрового цикла
        rotating = False
        moving = False
        paused = False
        game_over = False

        #внутренний цикл игры
        while playing:

            surface.blit(background, bg_place)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    playing = False
                    running = False
                    game_opened = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_a and len(ships) == 1:
                        bullet = Bullet(ship.top_find())
                        bullets.add(bullet)
                        bullet.rotate(ship.angle)
                        shot.play()
                    elif event.key == pg.K_ESCAPE:
                        paused = True
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_RIGHT:
                        rotating = False
                    elif event.key == pg.K_LEFT:
                        rotating = False
                    elif event.key == pg.K_UP:
                        stop_angle = ship.angle
                        moving = False
                        ship.engines(moving)
                if not moving:
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_RIGHT:
                            side = 'right'
                            rotating = True
                        elif event.key == pg.K_LEFT:
                            side = 'left'
                            rotating = True
                if not rotating:
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_UP:
                            moving = True
                            ship.engines(moving)
                            
            if moving:
                ship.move()
            else:
                if ship.speed > 0:
                    ship.slowdown(stop_angle)
                
            if rotating:
                ship.rotate(side)

            if asteroid_spawn_timer >= asteroid_spawn_frequency:
                asteroid_spawn_timer = 0
                asteroid = Asteroid()
                asteroids.add(asteroid)
            else:
                asteroid_spawn_timer += 1

            bullets.update()
            asteroids.update()
            explosions.update()

            if difficulty == 'easy':
                
                if resistance_bonus_spawntimer < resistance_bonus_spawntime:
                    resistance_bonus_spawntimer += 1
                else:
                    bonus = ResistanceBonus()
                    bonuses.add(bonus)
                    resistance_bonus_spawntimer = 0

                if life_bonus_spawntimer < life_bonus_spawntime:
                    life_bonus_spawntimer += 1
                else:
                    bonus = LifeBonus()
                    bonuses.add(bonus)
                    life_bonus_spawntimer = 0

                if speed_bonus_spawntimer < speed_bonus_spawntime:
                    speed_bonus_spawntimer += 1
                else:
                    bonus = SpeedBonus()
                    bonuses.add(bonus)
                    speed_bonus_spawntimer = 0
                    
            elif difficulty == 'medium':
                
                if resistance_bonus_spawntimer < resistance_bonus_spawntime:
                    resistance_bonus_spawntimer += 1
                else:
                    bonus = ResistanceBonus()
                    bonuses.add(bonus)
                    resistance_bonus_spawntimer = 0

                if speed_bonus_spawntimer < speed_bonus_spawntime:
                    speed_bonus_spawntimer += 1
                else:
                    bonus = SpeedBonus()
                    bonuses.add(bonus)
                    speed_bonus_spawntimer = 0

            elif difficulty == 'hard':

                if speed_bonus_spawntimer < speed_bonus_spawntime:
                    speed_bonus_spawntimer += 1
                else:
                    bonus = SpeedBonus()
                    bonuses.add(bonus)
                    speed_bonus_spawntimer = 0
                
            bonuses.update()

            for explosion in explosions:
                if explosion.add_score:
                    score += 1
                    score_num = gameplay_font.render(str(score), False, 'green')
                    explosion.add_score = False
                elif explosion.minus_life:
                    lives -= 1
                    if lives == 0:
                        game_over = True
                    lives_num = gameplay_font.render(str(lives), False, 'green')
                    explosion.minus_life = False
            
            if len(ships) == 1:
                ships.update()
                if ship.gets_life:
                    lives += 1
                    lives_num = gameplay_font.render(str(lives), False, 'green')
                    ship.gets_life = False
            elif not game_over:
                if respawn_timer < respawn_time:
                    respawn_timer += 1
                else:
                    respawn_timer = 0
                    ship = Player()
                    ships.add(ship)

            surface.blit(lives_sign, lives_sign_place)
            surface.blit(lives_num, lives_num_place)
            surface.blit(score_sign, score_sign_place)
            surface.blit(score_num, score_num_place)        

            if paused and (game_over == False):
                surface.blit(pause_sign, pause_sign_place)
                moving = False
                stop_angle = ship.angle
                ship.engines(moving)
                rotating = False
                
            pg.display.flip()
            
            if paused and (game_over == False):
                pg.mixer.music.pause()
                pause.play()
                while paused:
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            playing = False
                            running = False
                            paused = False
                            game_opened = False
                        elif event.type == pg.KEYDOWN:
                            if event.key == pg.K_ESCAPE:
                                pg.mixer.music.unpause()
                                paused = False

            if game_over:
                
                if respawn_timer < respawn_time:
                    respawn_timer += 1
                    clock.tick(FPS)
                    continue

                else:
                    pg.mixer.music.load('GameOver.mp3')
                    pg.mixer.music.set_volume(MVOL)
                    pg.mixer.music.play(-1)
                    for asteroid in asteroids:
                        asteroid.kill()
                    for bonus in bonuses:
                        bonus.kill()
                    surface.blit(background, bg_place)
                    surface.blit(lives_sign, lives_sign_place)
                    surface.blit(lives_num, lives_num_place)
                    surface.blit(score_sign, score_sign_place)
                    surface.blit(score_num, score_num_place)
                    surface.blit(game_over_sign, gos_place)
                    surface.blit(go_instruction, goi_place)
                    pg.display.flip()

                while playing:
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            playing = False
                            running = False
                            game_opened = False
                        elif event.type == pg.KEYDOWN:
                            if event.key == pg.K_r:
                                playing = False
                            elif event.key == pg.K_q:
                                playing = False
                                running = False
                                
            clock.tick(FPS)

pg.quit()


