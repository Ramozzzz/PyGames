import math
import pygame as pg
from random import randint, choice

RES = W, H = 1000, 680
MVOL = 0.5
SVOL = 0.5
FPS = 60

pg.init()
surface = pg.display.set_mode(RES)
pg.display.set_caption('Asteroids')
clock = pg.time.Clock()

#класс игрок
class Player(pg.sprite.Sprite):
    
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.img_orig = ship_image
        self.moving_img_orig = moving_ship_image
        self.image = self.img_orig
        self.image.set_colorkey('BLACK')
        self.rect = self.image.get_rect()
        self.rect.center = (W // 2, H // 2)
        self.speed = 0
        self.standard_acceleration = 0.2
        self.acceleration = 0.2
        self.bonus_acceleration = 0.3
        self.stopping = -0.04
        self.standard_max_speed = 6
        self.max_speed = 6
        self.bonus_max_speed = 9
        self.angle = 0
        self.standard_rot_speed = 3
        self.rot_speed = 3
        self.bonus_rot_speed = 6
        self.resistance_time = 120
        self.resistance_timer = 0
        self.flicker_time = 2
        self.flicker_timer = 0
        self.speed_bonus_time = 600
        self.speed_bonus_timer = self.speed_bonus_time
        self.gets_life = False

    #проверка столкновений, таймера неуязвимости и мерцания, прорисовка корабля    
    def update(self):
        self.check()
        if self.resistance_timer < self.resistance_time:
            self.resistance_timer += 1
            if self.flicker_timer < self.flicker_time:
                self.flicker_timer += 1
            else:
                self.flicker_timer = 0
                surface.blit(self.image, self.rect)
        else:
            surface.blit(self.image, self.rect)

    #вычисление вектора движения и само движение, реализация тороидальной геометрии        
    def move(self):
        
        self.rect.x -= (self.speed * math.sin(math.radians(self.angle)))
        self.rect.y -= (self.speed * math.cos(math.radians(self.angle)))
        if (self.rect.topleft[1] <= 0) and (self.rect.topright[1] <= 0) and (self.rect.bottomleft[1] <= 0) and (self.rect.bottomright[1] <= 0):
            self.rect.y = H
        elif (self.rect.topleft[1] >= H) and (self.rect.topright[1] >= H) and (self.rect.bottomleft[1] >= H) and (self.rect.bottomright[1] >= H):
            self.rect.y = -70
        elif (self.rect.topleft[0] <= 0) and (self.rect.topright[0] <= 0) and (self.rect.bottomleft[0] <= 0) and (self.rect.bottomright[0] <= 0):
            self.rect.x = W
        elif (self.rect.topleft[0] >= W) and (self.rect.topright[0] >= W) and (self.rect.bottomleft[0] >= W) and (self.rect.bottomright[0] >= W):
            self.rect.x = -70

        if self.speed < self.max_speed:
            self.speed += self.acceleration

    #замедление корабля после выключения двигателей, stop_angle - угол вектора последнего ускорения  
    def slowdown(self, stop_angle):
        
        self.rect.x -= (self.speed * math.sin(math.radians(stop_angle)))
        self.rect.y -= (self.speed * math.cos(math.radians(stop_angle)))
        if (self.rect.topleft[1] <= 0) and (self.rect.topright[1] <= 0) and (self.rect.bottomleft[1] <= 0) and (self.rect.bottomright[1] <= 0):
            self.rect.y = H
        elif (self.rect.topleft[1] >= H) and (self.rect.topright[1] >= H) and (self.rect.bottomleft[1] >= H) and (self.rect.bottomright[1] >= H):
            self.rect.y = -70
        elif (self.rect.topleft[0] <= 0) and (self.rect.topright[0] <= 0) and (self.rect.bottomleft[0] <= 0) and (self.rect.bottomright[0] <= 0):
            self.rect.x = W
        elif (self.rect.topleft[0] >= W) and (self.rect.topright[0] >= W) and (self.rect.bottomleft[0] >= W) and (self.rect.bottomright[0] >= W):
            self.rect.x = -70

        if self.speed > 0:
            self.speed += self.stopping

    #вращение корабля    
    def rotate(self, side):
        if side == 'right':
            self.angle = (360 + (self.angle - self.rot_speed)) % 360
        elif side == 'left':
            self.angle = (self.angle + self.rot_speed) % 360
        new_img = pg.transform.rotate(self.img_orig, self.angle)
        center = self.rect.center
        self.image = new_img
        self.image.set_colorkey('BLACK')
        self.rect = self.image.get_rect()
        self.rect.center = center

    #прорисовка включения и выключения двигателей в зависимости от параметра trigger 
    def engines(self, trigger):
        if trigger:
            new_img = pg.transform.rotate(self.moving_img_orig, self.angle)
        else:
            new_img = pg.transform.rotate(self.img_orig, self.angle)
        center = self.rect.center
        self.image = new_img
        self.image.set_colorkey('BLACK')
        self.rect = self.image.get_rect()
        self.rect.center = center

    #этот метод находит координаты носа корабля
    def top_find(self):
        cx, cy = self.rect.center[0], self.rect.center[1]
        d = self.rect.h / 2
        angle = self.angle
        dx = d * math.sin(math.radians(angle))
        dy = d * math.cos(math.radians(angle))
        x, y = cx - dx, cy - dy

        return x, y

    #проверка таймера действия бонуса скорости, проверка на столкновение с астероидами и подбор бонусов
    def check(self):
        if self.speed_bonus_timer == self.speed_bonus_time:
            self.acceleration = self.standard_acceleration
            self.max_speed = self.standard_max_speed
            self.rot_speed = self.standard_rot_speed
        else:
            self.speed_bonus_timer += 1
        hits = pg.sprite.spritecollide(self, asteroids, False)
        if hits:
            if self.resistance_timer < self.resistance_time:
                for asteroid in hits:
                    asteroid_killed.play()
                    explosion = Explosion(asteroid.rect.center, False, False)
                    explosions.add(explosion)
                    asteroid.kill()
            else:
                for asteroid in hits:
                    asteroid.kill()
                explosion = Explosion(self.rect.center, False, True)
                explosions.add(explosion)
                crash.play()
                self.kill()

        else:
            hits = pg.sprite.spritecollide(self, bonuses, False)
            if hits:
                for bonus in hits:
                    bonus_pickup.play()
                    if bonus.effect == 'life':
                        self.gets_life = True
                    elif bonus.effect == 'resistance':
                        self.resistance_time = 600
                        self.resistance_timer = 0
                    elif bonus.effect == 'speed':
                        self.speed_bonus_timer = 0
                        self.acceleration = self.bonus_acceleration
                        self.max_speed = self.bonus_max_speed
                        self.rot_speed = self.bonus_rot_speed
                    bonus.kill()
                
#класс пуля
class Bullet(pg.sprite.Sprite):

    def __init__(self, top):
        pg.sprite.Sprite.__init__(self)
        self.img_orig = pg.Surface((5,5))
        self.image = self.img_orig
        self.image.fill('yellow')
        self.rect = self.image.get_rect()
        self.rect.center = top
        self.speed = 9
        self.angle = 0
        self.timer = 0
        self.lifetime = 60

    #обновление таймера жизни, проверка на столкновение и истечение времени жизни, прорисовка пули     
    def update(self):
        self.timer += 1
        self.check()
        self.move()
        surface.blit(self.image, self.rect)

    #вычисление вектора движения пули, само движение, реализация тороидальной геометрии
    def move(self):
        
        self.rect.x -= (self.speed * math.sin(math.radians(self.angle)))
        self.rect.y -= (self.speed * math.cos(math.radians(self.angle)))
        if (self.rect.topleft[1] <= 0) and (self.rect.topright[1] <= 0) and (self.rect.bottomleft[1] <= 0) and (self.rect.bottomright[1] <= 0):
            self.rect.y = H
        elif (self.rect.topleft[1] >= H) and (self.rect.topright[1] >= H) and (self.rect.bottomleft[1] >= H) and (self.rect.bottomright[1] >= H):
            self.rect.y = -10
        elif (self.rect.topleft[0] <= 0) and (self.rect.topright[0] <= 0) and (self.rect.bottomleft[0] <= 0) and (self.rect.bottomright[0] <= 0):
            self.rect.x = W
        elif (self.rect.topleft[0] >= W) and (self.rect.topright[0] >= W) and (self.rect.bottomleft[0] >= W) and (self.rect.bottomright[0] >= W):
            self.rect.x = -10

    #пуля поворачивается под нужным углом (это угол, на который повернут корабль, он передается во внутреннем цикле игры) 
    def rotate(self, angle):
        self.angle = angle
        new_img = pg.transform.rotate(self.img_orig, angle)
        center = self.rect.center
        self.image = new_img
        self.rect = self.image.get_rect()
        self.rect.center = center

    #проверка на истечение времени жизни
    def check(self):
        if self.timer > self.lifetime:
            self.kill()

#класс астероид
class Asteroid(pg.sprite.Sprite):
    
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.img_orig = asteroid_image
        self.image = self.img_orig
        self.image.set_colorkey('WHITE')
        self.rect = self.image.get_rect()
        self.rect.center = (randint(0,W), randint(0,H))
        self.speed = randint(2, 6)
        self.angle = randint(0, 360)
        self.rot_angle = 0
        self.rot_speed = randint(1, 4)
        self.rot_dir = choice(['left', 'right'])

    #проверка на столкновения, вращение, движение и прорисовка астероида 
    def update(self):
        self.check()
        self.rotate()
        self.move()
        surface.blit(self.image, self.rect)

    #расчет вектора движения по случайно сгенерированным данным, тороидальная геометрия
    def move(self):
        self.rect.x -= (self.speed * math.sin(math.radians(self.angle)))
        self.rect.y -= (self.speed * math.cos(math.radians(self.angle)))
        if (self.rect.topleft[1] <= 0) and (self.rect.topright[1] <= 0) and (self.rect.bottomleft[1] <= 0) and (self.rect.bottomright[1] <= 0):
            self.rect.y = H
        elif (self.rect.topleft[1] >= H) and (self.rect.topright[1] >= H) and (self.rect.bottomleft[1] >= H) and (self.rect.bottomright[1] >= H):
            self.rect.y = -50
        elif (self.rect.topleft[0] <= 0) and (self.rect.topright[0] <= 0) and (self.rect.bottomleft[0] <= 0) and (self.rect.bottomright[0] <= 0):
            self.rect.x = W
        elif (self.rect.topleft[0] >= W) and (self.rect.topright[0] >= W) and (self.rect.bottomleft[0] >= W) and (self.rect.bottomright[0] >= W):
            self.rect.x = -50

    #вращение астероида (оно постоянно) 
    def rotate(self):
        if self.rot_dir == 'right':
            self.rot_angle = (360 + (self.rot_angle - self.rot_speed)) % 360
        elif self.rot_dir == 'left':
            self.rot_angle = (self.rot_angle + self.rot_speed) % 360
        new_img = pg.transform.rotate(self.img_orig, self.rot_angle)
        center = self.rect.center
        self.image = new_img
        self.image.set_colorkey('WHITE')
        self.rect = self.image.get_rect()
        self.rect.center = center

    #проверка на столкновение с пулями
    def check(self):
        hits = pg.sprite.spritecollide(self, bullets, False)
        if hits:
            asteroid_killed.play()
            for bullet in hits:
                bullet.kill()
            explosion = Explosion(self.rect.center, True, False)
            explosions.add(explosion)
            self.kill()

#класс взрыв (реализует анимацию из нескольких картинок)
class Explosion(pg.sprite.Sprite):
    
    def __init__(self, xy, add_score, minus_life):
        pg.sprite.Sprite.__init__(self)
        self.images = [exp1, exp2, exp3, exp4, exp5, exp6]
        self.index = 0
        self.image = self.images[self.index]
        self.image.set_colorkey('WHITE')
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.timer = 0
        self.speed = 5
        self.add_score = add_score
        self.minus_life = minus_life

    #смена кадров анимации, проверка на то, не закончились ли кадры
    def update(self):
        surface.blit(self.image, self.rect)
        if self.timer < self.speed:
            self.timer +=1
        else:
            self.timer = 0
            self.index +=1
            if self.index <= len(self.images) - 1:
                center = self.rect.center
                self.image = self.images[self.index]
                self.image.set_colorkey('WHITE')
                self.rect = self.image.get_rect()
                self.rect.center = center
            else:
                self.kill()

#бонус - дополнительная жизнь
class LifeBonus(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = life_bonus_image
        self.rect = self.image.get_rect()
        self.rect.center = (randint(20, W - 20), randint(20, H - 20))
        self.effect = 'life'

    #прорисовка
    def update(self):
        surface.blit(self.image, self.rect)

#бонус - защита на 10 секунд
class ResistanceBonus(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = resistance_bonus_image
        self.rect = self.image.get_rect()
        self.rect.center = (randint(20, W - 20), randint(20, H - 20))
        self.effect = 'resistance'

    #прорисовка
    def update(self):
        surface.blit(self.image, self.rect)

#бонус - увеличение скорости на 10 секунд
class SpeedBonus(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = speed_bonus_image
        self.rect = self.image.get_rect()
        self.rect.center = (randint(20, W - 20), randint(20, H - 20))
        self.effect = 'speed'

    #прорисовка
    def update(self):
        surface.blit(self.image, self.rect)

#класс для всех кнопок на экране
class Button(pg.sprite.Sprite):

    def __init__(self, cxy, xy, text):
        pg.sprite.Sprite.__init__(self)
        self.size = xy
        self.image = pg.Surface(self.size)
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.rect.center = cxy
        self.text = text
        self.text_place = text.get_rect(center = self.rect.center)
        self.murk = False

    #проверка на наведение курсора, прорисовка и обводка, прорисовка текста
    def update(self):
        self.cursor_check()
        surface.blit(self.image, self.rect)
        pg.draw.rect(surface, 'black', (self.rect.center[0] - (self.size[0] / 2), self.rect.center[1] - (self.size[1] / 2), self.size[0], self.size[1]), 2)
        surface.blit(self.text, self.text_place)

    #проверка на наведение курсора
    def is_clicked(self):
        mpos = pg.mouse.get_pos()
        if self.rect.collidepoint(mpos):
            return True
        else:
            return False

    #смена цвета в зависимости от того, наведен ли на кнопку курсор, и от параметра self.murk (он нужен для того, чтобы кнопка оставалась темной без наведения курсора) 
    def cursor_check(self):
        if self.murk:
            self.image.fill('brown')
        else:
            if self.is_clicked():
                self.image.fill('brown')
            else:
                self.image.fill('red')

#звуковые эффекты
asteroid_killed = pg.mixer.Sound('AsteroidExplosion.mp3')
crash = pg.mixer.Sound('Crash.mp3')
shot = pg.mixer.Sound('Shot.mp3')
pause = pg.mixer.Sound('Pause.mp3')
button_click = pg.mixer.Sound('ButtonClick.mp3')
settings_button_click = pg.mixer.Sound('LittleButtonClick.mp3')
bonus_pickup = pg.mixer.Sound('BonusPickup.mp3')
all_sounds = (shot, crash, pause, button_click, settings_button_click, bonus_pickup, asteroid_killed)

#картинки, надписи, спрайт группы
ship_image = pg.image.load('Spaceship.png')
moving_ship_image = pg.image.load('MovingSpaceship.png')
asteroid_image = pg.image.load('Asteroid.png')
exp1 = pg.image.load('Explosion1.png')
exp2 = pg.image.load('Explosion2.png')
exp3 = pg.image.load('Explosion3.png')
exp4 = pg.image.load('Explosion4.png')
exp5 = pg.image.load('Explosion5.png')
exp6 = pg.image.load('Explosion6.png')
background = pg.image.load('Background.jpeg')
bg_place = background.get_rect()
start_screen_background = pg.image.load('StartScreen.png')
ssb_place = start_screen_background.get_rect()
life_bonus_image = pg.image.load('Heart.png')
resistance_bonus_image = pg.image.load('Shield.png')
speed_bonus_image = pg.image.load('Speed.png')
bullets = pg.sprite.Group()
asteroids = pg.sprite.Group()
bonuses = pg.sprite.Group()
explosions = pg.sprite.Group()
main_menu_buttons = pg.sprite.Group()
settings_buttons = pg.sprite.Group()
ships = pg.sprite.Group()
gameplay_font = pg.font.Font(None, 48)
lives_sign = gameplay_font.render('Lives: ', False, 'green')
lives_sign_place = lives_sign.get_rect(center = (75, 50))
score_sign = gameplay_font.render('Score: ', False, 'green')
score_sign_place = score_sign.get_rect(center = (75, 100))
pause_sign = gameplay_font.render('PAUSE', False, 'cyan')
pause_sign_place = pause_sign.get_rect(center = (W // 2, H // 2))
game_over_sign = gameplay_font.render('GAME OVER', False, 'cyan')
gos_place = game_over_sign.get_rect(center = (W // 2, H // 2 - 25))
go_instruction = gameplay_font.render('press R to restart or Q to quit', True, 'orange')
goi_place = go_instruction.get_rect(center = (W // 2, H // 2 + 25))                

difficulty = 'medium' #уровень сложности по умолчанию

#заголовки экранов и шрифты
main_title_font = pg.font.SysFont('arial', 48)
main_title = main_title_font.render('ASTEROIDS', True, 'black')
main_title_place = main_title.get_rect(center = (W // 2, H // 2 - 160))
title_font = pg.font.Font(None, 48)
settings_title = title_font.render('SETTINGS', True, 'black')
settings_title_place = settings_title.get_rect(center = (W // 2, H // 2 - 160))
buttons_font = pg.font.Font(None, 36)
controls_title = title_font.render('CONTROLS', True, 'black')
controls_title_place = controls_title.get_rect(center = (W // 2, H // 2 - 160))

#надписи в настройках
sign_font = pg.font.Font(None, 42)
difficulty_sign = sign_font.render('Difficulty:', True, 'black')
difficulty_sign_place = difficulty_sign.get_rect(center = (W // 2 - 100, H // 2 - 100))
music_volume_sign = sign_font.render('Music volume:', True, 'black')
mv_sign_place = music_volume_sign.get_rect(center = (W // 2 - 130, H // 2 - 30))
sound_volume_sign = sign_font.render('Sound volume:', True, 'black')
sv_sign_place = sound_volume_sign.get_rect(center = (W // 2 - 130, H // 2 + 40))
easy_sign = sign_font.render('Easy', True, 'black')
medium_sign = sign_font.render('Medium', True, 'black')
hard_sign = sign_font.render('Hard', True, 'black')
extreme_sign = sign_font.render('Extreme', True, 'black')
sign_plus = sign_font.render('+', True, 'black')
sign_minus = sign_font.render('-', True, 'black')
#два изменяемых параметра mv_swap и sv_swap - цифры будут меняться при нажатии на соответствующие кнопки
mv_swap = sign_font.render(str(MVOL), True, 'black')
mv_swap_place = mv_swap.get_rect(center = (W // 2 + 100, H // 2 - 30))
sv_swap = sign_font.render(str(SVOL), True, 'black')
sv_swap_place = sv_swap.get_rect(center = (W // 2 + 100, H // 2 + 40))

#надписи на экране инструкции к управлению
instruction1 = sign_font.render('UP     -     Accelerate', True, 'black')
instruction1_place = instruction1.get_rect(center = (W // 2, H // 2 - 100))
instruction2 = sign_font.render('RIGHT, LEFT     -     Rotate', True, 'black')
instruction2_place = instruction2.get_rect(center = (W // 2, H // 2 - 50))
instruction3 = sign_font.render('A     -     Shoot', True, 'black')
instruction3_place = instruction3.get_rect(center = (W // 2, H // 2))
instruction4 = sign_font.render('ESCAPE     -     Pause', True, 'black')
instruction4_place = instruction4.get_rect(center = (W // 2, H // 2 + 50))

#кнопки главного меню
play_button_text = buttons_font.render('Play', True, 'black')
play_button = Button((W // 2, H // 2 - 90), (100, 50), play_button_text)
main_menu_buttons.add(play_button)
settings_button_text = buttons_font.render('Settings', True, 'black')
settings_button = Button((W // 2, H // 2 - 20), (160, 50), settings_button_text)
main_menu_buttons.add(settings_button)
controls_button_text = buttons_font.render('Controls', True, 'black')
controls_button = Button((W // 2, H // 2 + 50), (160, 50), controls_button_text)
main_menu_buttons.add(controls_button)
quit_button_text = buttons_font.render('Quit', True, 'black')
quit_button = Button((W // 2, H // 2 + 120), (100, 50), quit_button_text)
main_menu_buttons.add(quit_button)

#кнопки в настройках
settings_quit_button = Button((W // 2, H // 2 + 120), (100, 50), quit_button_text)
settings_buttons.add(settings_quit_button)
difficulty_swap_button = Button((W // 2 + 100, H // 2 - 100), (130, 50), medium_sign)
settings_buttons.add(difficulty_swap_button)
mv_plus_button = Button((W // 2 + 150, H // 2 - 30), (30, 30), sign_plus)
settings_buttons.add(mv_plus_button)
mv_minus_button = Button((W // 2 + 50, H // 2 - 30), (30, 30), sign_minus)
settings_buttons.add(mv_minus_button)
sv_plus_button = Button((W // 2 + 150, H // 2 + 40), (30, 30), sign_plus)
settings_buttons.add(sv_plus_button)
sv_minus_button = Button((W // 2 + 50, H // 2 + 40), (30, 30), sign_minus)
settings_buttons.add(sv_minus_button)

#кнопки на экране controls
controls_quit_button = Button((W // 2, H // 2 + 120), (100, 50), quit_button_text)
