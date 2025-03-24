#import moduls
from pygame import *

#kelas parents
class GameSprite(sprite.Sprite):
    #kontruktor kelas
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    #metode draw/menampilkan karakter
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#subclass player
class Player(GameSprite):
    #metode pemain - kontrol keyboard
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed 
        self.y_speed = player_y_speed


    def update(self):
        ''' moves the character by applying the current horizontal and vertical speed '''
        # horizontal movement first
        if (packman.rect.x <= win_width - 80 and packman.x_speed > 0) or (packman.rect.x >= 0 and packman.x_speed < 0):
            self.rect.x += self.x_speed
        
        # if we go behind the wall, we'll stand right up to it
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:  # we're going to the right
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:  # we're going to the left
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)

        if (packman.rect.y <= win_height - 80 and packman.y_speed > 0) or (packman.rect.y >= 0 and packman.y_speed < 0):
            self.rect.y += self.y_speed
        
        # if we go behind the wall, we'll stand right up to it
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:  # going down
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:  # going up
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)

    #untuk menembakkan peluru  
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)

#subclass musuh
class Enemy(GameSprite):
    side = 'left'
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    
    #pergerakan musuh 
    def update(self):
        if self.rect.x <= 420:
            self.side = 'right'
        if self. rect.x >= win_width - 85:
            self.side = 'left'
        
        if self.side == 'left':
            self.rect.x -= self.speed
        if self.side == 'right':
            self.rect.x += self.speed

#subclass peluru/bullet
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed 
    
    #movement of an enemy
    def update(self):
        self.rect.x += self.speed
        # disappears after reaching the edge of the screen
        if self.rect.x > win_width+10:
            self.kill()


#================================================================================================================================


#Creating a window
win_width = 700
win_height = 500
display.set_caption("Maze")
window = display.set_mode((win_width, win_height))
back = (119, 210, 223)#setting the color according to the RGB color scheme

#creating a group
barriers = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()

#creating wall pictures
w1 = GameSprite('platform2.png',win_width / 2 - win_width / 3, win_height / 2, 300, 50)
w2 = GameSprite('platform2_v.png', 370, 100, 50, 400)

#adding walls to the group
barriers.add(w1)
barriers.add(w2)

#creating sprites
packman = Player('hero.png', 5, win_height - 80, 80, 80, 0, 0)
monster1 = Enemy('cyborg.png', win_width - 80, 150, 80, 80, 5)
monster2 = Enemy('cyborg.png', win_width - 80, 230, 80, 80, 5)
final_sprite = GameSprite('pac-1.png', win_width - 85, win_height - 100, 80, 80)

#adding a monster to the group
monsters.add(monster1)
monsters.add(monster2)

# the variable responsible for how the game has ended
finish = False
# game loop
run = True
while run:
    # the loop is triggered every 0.05 seconds
    time.delay(50)

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -10
            elif e.key == K_RIGHT:
                packman.x_speed = 10
            elif e.key == K_UP:
                packman.y_speed = -10
            elif e.key == K_DOWN:
                packman.y_speed = 10
            #klik spasi dan peluru muncul
            elif e.key == K_SPACE:
                packman.fire()

        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0
    
    if not finish:
        window.fill(back)  # fill the window with color
        packman.update()
        bullets.update()
        packman.reset()
        bullets.draw(window)
        barriers.draw(window)
        final_sprite.reset()
        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)

        
        # Checking the character's collision with the enemy and walls
        if sprite.spritecollide(packman, monsters, False):
            finish = True
            img = image.load('game-over_1.png')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))

        if sprite.collide_rect(packman, final_sprite):
            finish = True
            img = image.load('thumb.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))

    display.update()
