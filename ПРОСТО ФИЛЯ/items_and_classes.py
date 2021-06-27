import pygame as pg
from layouts import *

RES = WIDTH, HEIGHT = 1200, 680
TX = 60
TY = 34
W, H = WIDTH // TX, HEIGHT // TY
FPS = 60
MVOL = 1
SVOL = 1

pg.init()
surface = pg.display.set_mode(RES)
pg.display.set_caption('Just Filya')
clock = pg.time.Clock()

class Player(pg.sprite.Sprite):

    def __init__(self, topleft):
        pg.sprite.Sprite.__init__(self)
        self.move_animation = [filya_img, filya_move1_img, filya_img, filya_move2_img]
        self.rmove_animation = []
        for image in self.move_animation:
            new_image = pg.transform.flip(image, True, False)
            new_image.set_colorkey('white')
            self.rmove_animation.append(new_image)
        self.imch_time = 2
        self.imch_timer = 0
        self.image_index = 0
        self.img_state = 'forward'
        self.image = filya_img
        self.rect = self.image.get_rect(topleft = topleft)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.move_speed = 5
        self.run_speed = 10
        self.speedx = 0
        self.running = False
        self.speedy = 0
        self.dy = 0
        self.jumpower = -15
        self.max_speedy = 10
        self.fall_acceleration = 1
        self.mid_air = False
        self.fell = False
        self.moving = False #starts move() method
        self.platform_col = 15

    def update(self):
        self.dy = 0
        self.gravity()
        self.y_collision_check()
        self.rect.y += self.dy
        self.fall_img_check()
        surface.blit(self.image, self.rect)

    def move(self, direction):
        if not self.mid_air:
            if self.imch_timer < self.imch_time:
                self.imch_timer += 1
            else:
                self.image_index += 1
                try:
                    if direction == 'forward':
                        self.image = self.move_animation[self.image_index]
                    elif direction == 'back':
                        self.image = self.rmove_animation[self.image_index]
                except IndexError:
                    self.image_index = 0
                    if direction == 'forward':
                        self.image = self.move_animation[self.image_index]
                    elif direction == 'back':
                        self.image = self.rmove_animation[self.image_index]
                finally:
                    self.imch_timer = 0
        else:
            if direction != self.img_state:
                if direction == 'forward':
                    self.image = filya_fall_img
                elif direction == 'back':
                    self.image = rfilya_fall_img

        self.img_state = direction

        if self.running:
            self.speedx = self.run_speed
        else:
            self.speedx = self.move_speed

        if direction == 'back':
            self.speedx = -self.speedx

        self.x_collision_check()
            
        if direction == 'forward':
            for gift in gifts:
                pass
            if self.rect.right < 500:
                self.rect.x += self.speedx
            elif gift.rect.right <= WIDTH:
                if self.rect.right < WIDTH:
                    self.rect.x += self.speedx
            else:
                for block in blocks:
                    if not isinstance(block, MovingPlatform):
                        block.rect.x -= self.speedx
                    else:
                        block.left_border -= self.speedx
                        block.right_border -= self.speedx
                        block.rect.x -= self.speedx
                for gift in gifts:
                    gift.rect.x -= self.speedx
                for bad_block in bad_blocks:
                    bad_block.rect.x -= self.speedx
        elif direction == 'back':
            if self.rect.left > 0:
                self.rect.x += self.speedx

    def jump(self):
        if not self.mid_air:
            jump_sound.play()
            self.speedy = self.jumpower

    def gravity(self):        
        if self.speedy < self.max_speedy:
            self.speedy += self.fall_acceleration
        self.dy += self.speedy

    def y_collision_check(self):
        on = False
        for block in blocks:
            if isinstance(block, MovingPlatform):
                if block.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.width, self.height):
                    if abs((self.rect.top + self.dy) - block.rect.bottom) < self.platform_col:
                        self.dy = block.rect.bottom - self.rect.top
                    elif abs((self.rect.bottom + self.dy) - block.rect.top) < self.platform_col:
                        self.rect.bottom = block.rect.top
                        self.dy = 0
                        on = True
                    self.speedy = 0
                    if on:
                        if self.rect.x >= 500 and (not self.moving or self.img_state == 'back') and block.direction == 'forward':
                            for block2 in blocks:
                                if not isinstance(block2, MovingPlatform):
                                    block2.rect.x -= block.speed
                                else:
                                    block2.left_border -= block.speed
                                    block2.right_border -= block.speed
                                    block2.rect.x -= block.speed
                            for gift in gifts:
                                gift.rect.x -= block.speed
                            for bad_block in bad_blocks:
                                bad_block.rect.x -= block.speed
                        else:
                            self.rect.x += block.speed

            else:
                if block.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.width, self.height):
                    if self.speedy < 0:
                        self.dy = block.rect.bottom - self.rect.top
                    else:
                        self.dy = block.rect.top - self.rect.bottom
                        on = True
                        if isinstance(block, DisappearingPlatform):
                            block.destruction = True
                    self.speedy = 0
        self.mid_air = not on

    def x_collision_check(self):
        for block in blocks:
            if isinstance(block, MovingPlatform):
                if block.rect.colliderect(self.rect.x + self.speedx - block.speed, self.rect.y, self.width, self.height):
                    self.speedx = 0
                    self.rect.x += block.speed
            else:
                if block.rect.colliderect(self.rect.x + self.speedx, self.rect.y, self.width, self.height):
                    self.speedx = 0
                    

    def fall_img_check(self):
        if self.mid_air and not self.fell:
            if self.img_state == 'forward':
                self.image = filya_fall_img
            elif self.img_state == 'back':
                self.image = rfilya_fall_img
            self.fell = True
        elif not self.mid_air and self.fell:
            if self.img_state == 'forward':
                self.image = self.move_animation[self.image_index]
            elif self.img_state == 'back':
                self.image = self.rmove_animation[self.image_index]
            self.fell = False

class Block(pg.sprite.Sprite):

    def __init__(self, block_type, topleft):
        pg.sprite.Sprite.__init__(self)
        self.image = img_dict[block_type]
        self.rect = self.image.get_rect(topleft = topleft)

    def update(self):
        surface.blit(self.image, self.rect)

class MovingPlatform(pg.sprite.Sprite):

    def __init__(self, block_type, topleft):
        pg.sprite.Sprite.__init__(self)
        self.image = img_dict[block_type]
        self.rect = self.image.get_rect(topleft = topleft)
        self.left_border = self.rect.left
        self.right_border = self.left_border + 6 * TX
        self.speed = 4
        self.direction = 'forward'

    def update(self):
        self.move()
        surface.blit(self.image, self.rect)

    def move(self):
        if self.direction == 'forward':
            if self.rect.right < self.right_border:
                self.rect.x += self.speed
            else:
                self.speed = -self.speed
                self.direction = 'back'
        elif self.direction == 'back':
            if self.rect.left > self.left_border:
                self.rect.x += self.speed
            else:
                self.speed = -self.speed
                self.direction = 'forward'

class DisappearingPlatform(pg.sprite.Sprite):

    def __init__(self, block_type, topleft):
        pg.sprite.Sprite.__init__(self)
        self.image = img_dict[block_type]
        self.rect = self.image.get_rect(topleft = topleft)
        self.time = 20
        self.timer = 0
        self.destruction = False

    def update(self):
        self.timer_control()
        surface.blit(self.image, self.rect)

    def timer_control(self):
        if self.destruction:
            if self.timer < self.time:
                self.timer += 1
            else:
                self.kill()

class Gift(pg.sprite.Sprite):

    def __init__(self, color, topleft):
        pg.sprite.Sprite.__init__(self)
        self.image = gift_img_dict[color]
        self.rect = self.image.get_rect(topleft = topleft)

    def update(self, player):
        if self.collected(player):
            self.kill()
        else:
            surface.blit(self.image, self.rect)

    def collected(self, player):
        if self.rect.colliderect(player.rect.x, player.rect.y, player.width, player.height):
            return True
        else:
            return False

class BadBlock(pg.sprite.Sprite):

    def __init__(self, block_type, topleft):
        pg.sprite.Sprite.__init__(self)
        self.image = bad_img_dict[block_type]
        self.rect = self.image.get_rect(topleft = topleft)

    def update(self, player):
        surface.blit(self.image, self.rect)

    def touched(self, player):
        if self.rect.colliderect(player.rect.x, player.rect.y, player.width, player.height):
            return True
        else:
            return False

class FallingBadBlock(pg.sprite.Sprite):

    def __init__(self, block_type, topleft):
        pg.sprite.Sprite.__init__(self)
        self.image = bad_img_dict[block_type]
        self.rect = self.image.get_rect(topleft = topleft)
        self.fell = False
        self.speed = 0
        self.max_speed = 10
        self.acceleration = 1

    def update(self, player):
        if self.fell:
            self.fall()
        else:
            self.check(player)
        surface.blit(self.image, self.rect)

    def touched(self, player):
        if self.rect.colliderect(player.rect.x, player.rect.y, player.width, player.height):
            return True
        else:
            return False

    def check(self, player):
        if self.rect.x <= player.rect.right:
            item_fall_sound.play()
            self.fell = True
    
    def fall(self):
        if self.speed < self.max_speed:
            self.speed += self.acceleration
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

class JumpingEnemy(pg.sprite.Sprite):

    def __init__(self, enemy_images, topleft):
        pg.sprite.Sprite.__init__(self)
        self.image_keys = enemy_images
        self.images = [bad_img_dict[self.image_keys[0]], bad_img_dict[self.image_keys[1]]]
        self.rimages = []
        for image in self.images:
            new_image = pg.transform.flip(image, True, False)
            new_image.set_colorkey('white')
            self.rimages.append(new_image)
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = topleft)
        self.jump_timer = 0
        self.jump_time = 60
        self.jumpower = -20
        self.speed = 0
        self.max_speed = 16
        self.acceleration = 1
        self.mid_air = False
        self.bottom_border = self.rect.bottom

    def update(self, player):
        if self.mid_air:
            self.fall()
        else:
            self.timer_check()
        self.img_check(player)
        if self.rect.right < 0:
            self.kill()
        surface.blit(self.image, self.rect)

    def jump(self):
        self.speed = self.jumpower
        self.image = self.images[1]
        self.mid_air = True

    def fall(self):
        if self.speed < self.max_speed:
            self.speed += self.acceleration
        if self.rect.bottom + self.speed >= self.bottom_border:
            self.speed = 0
            self.rect.bottom = self.bottom_border
            self.image = self.images[0]
            self.mid_air = False
        self.rect.y += self.speed

    def timer_check(self):
        if self.jump_timer < self.jump_time:
            self.jump_timer += 1
        else:
            self.jump_timer = 0
            self.jump()

    def img_check(self, player):
        if self.rect.x >= player.rect.x:
            if self.mid_air:
                if self.image != self.images[1]:
                    self.image = self.images[1]
            else:
                if self.image != self.images[0]:
                    self.image = self.images[0]
        else:
            if self.mid_air:
                if self.image != self.rimages[1]:
                    self.image = self.rimages[1]
            else:
                if self.image != self.rimages[0]:
                    self.image = self.rimages[0]

    def touched(self, player):
        if self.rect.colliderect(player.rect.x, player.rect.y, player.width, player.height):
            return True
        else:
            return False

class Level():

    def __init__(self, layout, background, type_codes, gift_color, gameover_sign, win_sign, welcome_screen):
        self.layout = layout
        self.background = background
        self.type_codes = type_codes
        self.gift_color = gift_color
        self.gameover_sign = gameover_sign
        self.win_sign = win_sign
        self.welcome_screen = welcome_screen

    def generate(self):
        y = 0
        for layer in self.layout:
            x = 0
            for item in layer:
                if item == 9:
                    gift = Gift(self.gift_color, (x * TX, y * TY))
                    gift.add(gifts)
                elif item >= 1 and item <= 3:
                    block = Block(self.type_codes[item], (x * TX, y * TY))
                    block.add(blocks)
                elif item == 4:
                    moving_platform = MovingPlatform(self.type_codes[item], (x * TX, y * TY))
                    moving_platform.add(blocks)
                elif item == 5:
                    disappearing_platform = DisappearingPlatform(self.type_codes[item], (x * TX, y * TY))
                    disappearing_platform.add(blocks)
                elif item == 6:
                    bad_block = BadBlock(self.type_codes[item], (x * TX, y * TY))
                    bad_block.add(bad_blocks)
                elif item == 7:
                    falling_bad_block = FallingBadBlock(self.type_codes[item], (x * TX, y * TY))
                    falling_bad_block.add(bad_blocks)
                elif item == 8:
                    jumping_enemy = JumpingEnemy(self.type_codes[item], (x * TX, y * TY))
                    jumping_enemy.add(bad_blocks)

                x += 1

            y += 1

class Button(pg.sprite.Sprite):

    def __init__(self, cxy, text, white_text):
        pg.sprite.Sprite.__init__(self)
        self.image = button_img
        self.rect = self.image.get_rect(center = cxy)
        self.text = text
        self.usual_text = text
        self.white_text = white_text
        self.text_place = text.get_rect(center = self.rect.center)
        self.whited = False

    def update(self):
        self.cursor_check()
        surface.blit(self.image, self.rect)
        surface.blit(self.text, self.text_place)

    def is_clicked(self):
        mpos = pg.mouse.get_pos()
        if self.rect.collidepoint(mpos):
            return True
        else:
            return False
 
    def cursor_check(self):
        if self.whited:
            self.text = self.white_text
        else:
            if self.is_clicked():
                self.text = self.white_text
            else:
                self.text = self.usual_text

#fonts and signs
font = pg.font.Font(None, 48)

play_sign = font.render('Play', True, 'purple')
white_play_sign = font.render('Play', True, 'white')
controls_sign = font.render('Controls', True, 'purple')
white_controls_sign = font.render('Controls', True, 'white')
quit_sign = font.render('Quit', True, 'purple')
white_quit_sign = font.render('Quit', True, 'white')

lvl_1_sign = font.render('Flower Meadow', True, 'purple')
white_lvl_1_sign = font.render('Flower Meadow', True, 'white')
lvl_2_sign = font.render('Hot Desert', True, 'purple')
white_lvl_2_sign = font.render('Hot Desert', True, 'white')
lvl_3_sign = font.render('Polar Night', True, 'purple')
white_lvl_3_sign = font.render('Polar Night', True, 'white')
lvl_4_sign = font.render('Deadly Cave', True, 'purple')
white_lvl_4_sign = font.render('Deadly Cave', True, 'white')

win_sign1 = font.render('YOU WIN!', True, 'green')
win_sign2 = font.render('YOU WIN!', True, 'blue')
win_sign3 = font.render('YOU WIN!', True, 'red')
win_sign4 = font.render('YOU WIN!', True, 'yellow')
win_sign_place = win_sign1.get_rect(center = (WIDTH // 2, HEIGHT // 2))

gameover_sign1 = font.render('Game Over :(', True, 'green')
gameover_sign2 = font.render('Game Over :(', True, 'blue')
gameover_sign3 = font.render('Game Over :(', True, 'red')
gameover_sign4 = font.render('Game Over :(', True, 'yellow')
gameover_sign_place = gameover_sign1.get_rect(center = (WIDTH // 2, HEIGHT // 2))

#IMAGES
#backgrounds and welcome screens
mm_bg = pg.image.load('images/StartScreens/MainBackground.png')
controls_screen = pg.image.load('images/StartScreens/ControlsScreen.png')
levels_screen = pg.image.load('images/StartScreens/LevelsScreen.png')
welcome_screen1 = pg.image.load('images/set1/WelcomeScreen1.png')
welcome_screen2 = pg.image.load('images/set2/WelcomeScreen2.png')
welcome_screen3 = pg.image.load('images/set3/WelcomeScreen3.png')
welcome_screen4 = pg.image.load('images/set4/WelcomeScreen4.png')
bg1 = pg.image.load('images/set1/Background1.png')
bg2 = pg.image.load('images/set2/Background2.png')
bg3 = pg.image.load('images/set3/Background3.png')
bg4 = pg.image.load('images/set4/Background4.png')
bg_place = mm_bg.get_rect()

#button image
button_img = pg.image.load('images/StartScreens/Button.png')
button_img.set_colorkey('white')

#gifts
green_gift_img = pg.image.load('images/set1/GreenGift.png')
green_gift_img.set_colorkey('white')
blue_gift_img = pg.image.load('images/set2/BlueGift.png')
blue_gift_img.set_colorkey('white')
red_gift_img = pg.image.load('images/set3/RedGift.png')
red_gift_img.set_colorkey('white')
yellow_gift_img = pg.image.load('images/set4/YellowGift.png')
yellow_gift_img.set_colorkey('white')

#set 1
dirt_block_img = pg.image.load('images/set1/DirtBlock.png')
grass_block_img = pg.image.load('images/set1/GrassBlock.png')
wheat_block_img = pg.image.load('images/set1/WheatBlock.png')
wheat_block_img.set_colorkey('white')
carrot_img = pg.image.load('images/set1/Carrot.png')
carrot_img.set_colorkey('white')
flower_img = pg.image.load('images/set1/Flower.png')
flower_img.set_colorkey('white')
thorny_bush_img = pg.image.load('images/set1/ThornyBush.png')
thorny_bush_img.set_colorkey('white')
hive_img = pg.image.load('images/set1/Hive.png')
hive_img.set_colorkey('white')
frog_img = pg.image.load('images/set1/Frog.png')
frog_img.set_colorkey('white')
air_frog_img = pg.image.load('images/set1/AirFrog.png')
air_frog_img.set_colorkey('white')

#set 2
deep_sand_img = pg.image.load('images/set2/DeepSand.png')
sand_block_img = pg.image.load('images/set2/SandBlock.png')
sand_block_img.set_colorkey('white')
sandstone_img = pg.image.load('images/set2/Sandstone.png')
melon_img = pg.image.load('images/set2/Melon.png')
melon_img.set_colorkey('white')
cloud_img = pg.image.load('images/set2/Cloud.png')
cloud_img.set_colorkey('white')
cactus_img = pg.image.load('images/set2/Cactus.png')
cactus_img.set_colorkey('white')
jug_img = pg.image.load('images/set2/Jug.png')
jug_img.set_colorkey('white')
desertfox_img = pg.image.load('images/set2/DesertFox.png')
desertfox_img.set_colorkey('white')
air_desertfox_img = pg.image.load('images/set2/AirDesertFox.png')
air_desertfox_img.set_colorkey('white')

#set 3
deep_snow_img = pg.image.load('images/set3/DeepSnow.png')
snow_block_img = pg.image.load('images/set3/SnowBlock.png')
snow_block_img.set_colorkey('white')
ice_block_img = pg.image.load('images/set3/IceBlock.png')
ice_block_img.set_colorkey('white')
candy_img = pg.image.load('images/set3/Candy.png')
candy_img.set_colorkey('white')
scarf_img = pg.image.load('images/set3/Scarf.png')
scarf_img.set_colorkey('white')
yellow_snow_img = pg.image.load('images/set3/YellowSnow.png')
yellow_snow_img.set_colorkey('white')
icicle_img = pg.image.load('images/set3/Icicle.png')
icicle_img.set_colorkey('white')
penguin_img = pg.image.load('images/set3/Penguin.png')
penguin_img.set_colorkey('white')
air_penguin_img = pg.image.load('images/set3/AirPenguin.png')
air_penguin_img.set_colorkey('white')

#set 4
deep_stone_img = pg.image.load('images/set4/DeepStone.png')
stone_block_img = pg.image.load('images/set4/StoneBlock.png')
stone_block_img.set_colorkey('white')
cobblestone_img = pg.image.load('images/set4/Cobblestone.png')
hamburger_img = pg.image.load('images/set4/Hamburger.png')
hamburger_img.set_colorkey('white')
bone_img = pg.image.load('images/set4/Bone.png')
bone_img.set_colorkey('white')
lava_img = pg.image.load('images/set4/Lava.png')
lava_img.set_colorkey('white')
spikes_img = pg.image.load('images/set4/Spikes.png')
spikes_img.set_colorkey('white')
jol_img = pg.image.load('images/set4/Jack-o-lantern.png')
jol_img.set_colorkey('white')
air_jol_img = pg.image.load('images/set4/AirJack-o-lantern.png')
air_jol_img.set_colorkey('white')

#player images
filya_img = pg.image.load('images/Filya.png')
filya_img.set_colorkey('white')
filya_move1_img = pg.image.load('images/FilyaMove1.png')
filya_move1_img.set_colorkey('white')
filya_move2_img = pg.image.load('images/FilyaMove2.png')
filya_move2_img.set_colorkey('white')
filya_fall_img = pg.image.load('images/FilyaFall.png')
filya_fall_img.set_colorkey('white')
rfilya_fall_img = pg.transform.flip(filya_fall_img, True, False)
rfilya_fall_img.set_colorkey('white')

#sprite groups
mm_buttons = pg.sprite.Group()
lvl_buttons = pg.sprite.Group()
blocks = pg.sprite.Group()
gifts = pg.sprite.Group()
bad_blocks = pg.sprite.Group()

#dicts getting images from names
img_dict = {'grass':grass_block_img, 'dirt':dirt_block_img, 'wheat':wheat_block_img, 'carrot':carrot_img, 'flower':flower_img, 'deep sand':deep_sand_img, 'sand':sand_block_img, 'sandstone':sandstone_img, 'melon':melon_img, 'cloud':cloud_img, 'deep snow':deep_snow_img, 'snow':snow_block_img, 'ice':ice_block_img, 'candy':candy_img, 'scarf':scarf_img, 'deep stone':deep_stone_img, 'stone':stone_block_img, 'cobblestone':cobblestone_img, 'hamburger':hamburger_img, 'bone':bone_img}
gift_img_dict = {'green':green_gift_img, 'blue':blue_gift_img, 'red':red_gift_img, 'yellow':yellow_gift_img}
bad_img_dict = {'thorny bush':thorny_bush_img, 'hive':hive_img, 'frog':frog_img, 'air frog':air_frog_img, 'cactus':cactus_img, 'jug':jug_img, 'desert fox':desertfox_img, 'air desert fox':air_desertfox_img, 'yellow snow':yellow_snow_img, 'icicle':icicle_img, 'penguin':penguin_img, 'air penguin':air_penguin_img, 'spikes':spikes_img, 'lava':lava_img, 'jack-o-lantern':jol_img, 'air jack-o-lantern':air_jol_img}

#dicts getting names from numbers (same numbers mean different for different levels)
type_codes1 = {1:'dirt', 2:'grass', 3:'wheat', 4:'carrot', 5:'flower', 6:'thorny bush',7:'hive',8:['frog', 'air frog']}
type_codes2 = {1:'deep sand', 2:'sand', 3:'sandstone', 4:'melon', 5:'cloud', 6:'cactus',7:'jug',8:['desert fox', 'air desert fox']}
type_codes3 = {1:'deep snow', 2:'snow', 3:'ice', 4:'candy', 5:'scarf', 6:'yellow snow',7:'icicle',8:['penguin', 'air penguin']}
type_codes4 = {1:'deep stone', 2:'stone', 3:'cobblestone', 4:'hamburger', 5:'bone', 6:'lava',7:'spikes',8:['jack-o-lantern', 'air jack-o-lantern']}

#levels
level_1 = Level(lvl_1_layout, bg1, type_codes1, 'green', gameover_sign1, win_sign1, welcome_screen1)
level_2 = Level(lvl_2_layout, bg2, type_codes2, 'blue', gameover_sign2, win_sign2, welcome_screen2)
level_3 = Level(lvl_3_layout, bg3, type_codes3, 'red', gameover_sign3, win_sign3, welcome_screen3)
level_4 = Level(lvl_4_layout, bg4, type_codes4, 'yellow', gameover_sign4, win_sign4, welcome_screen4)

#dict getting level from its number
lvl_dict = {1:level_1, 2:level_2, 3:level_3, 4:level_4}

#creating buttons
play_button = Button((WIDTH // 2, HEIGHT // 2 + 70), play_sign, white_play_sign)
play_button.add(mm_buttons)
controls_button = Button((WIDTH // 2, HEIGHT // 2 + 170), controls_sign, white_controls_sign)
controls_button.add(mm_buttons)
quit_button = Button((WIDTH // 2, HEIGHT // 2 + 270), quit_sign, white_quit_sign)
quit_button.add(mm_buttons)

lvl_1_button = Button((WIDTH // 2, HEIGHT // 2 - 135), lvl_1_sign, white_lvl_1_sign)
lvl_1_button.add(lvl_buttons)
lvl_2_button = Button((WIDTH // 2, HEIGHT // 2 - 35), lvl_2_sign, white_lvl_2_sign)
lvl_2_button.add(lvl_buttons)
lvl_3_button = Button((WIDTH // 2, HEIGHT // 2 + 65), lvl_3_sign, white_lvl_3_sign)
lvl_3_button.add(lvl_buttons)
lvl_4_button = Button((WIDTH // 2, HEIGHT // 2 + 165), lvl_4_sign, white_lvl_4_sign)
lvl_4_button.add(lvl_buttons)
qls_button = Button((WIDTH // 2, HEIGHT // 2 + 265), quit_sign, white_quit_sign)
qls_button.add(lvl_buttons)

#sounds
jump_sound = pg.mixer.Sound('audio/Jump.mp3')
jump_sound.set_volume(SVOL)
button_press_sound = pg.mixer.Sound('audio/ButtonPress.mp3')
button_press_sound.set_volume(SVOL)
item_fall_sound = pg.mixer.Sound('audio/ItemFall.mp3')
item_fall_sound.set_volume(SVOL)
gameover_sound = pg.mixer.Sound('audio/GameOver.mp3')
gameover_sound.set_volume(SVOL)
win_sound = pg.mixer.Sound('audio/Win.mp3')
win_sound.set_volume(SVOL)
