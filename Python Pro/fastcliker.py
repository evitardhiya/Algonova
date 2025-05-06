import pygame
from random import randint
import time
pygame.init()

#RGB colorcode
babypink = (255, 230, 255)
hotpink = (255, 26, 198)
skyblue = (153, 204, 255)
darkblue = (0, 49, 102)
lightred = (255, 204, 204)
lightgreen = (230, 255, 230)

width = 600
height  = 500
window = pygame.display.set_mode((width, height))
window.fill(babypink)
clock = pygame.time.Clock()

class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height) 
        self.fill_color = color
    def color(self, new_color):
        self.fill_color = new_color
    def fill(self):
        pygame.draw.rect(window, self.fill_color, self.rect)
    def outline(self, frame_color, thickness):  #garis besar persegi panjang yang ada
        pygame.draw.rect(window, frame_color, self.rect, thickness)   
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y) 

class Label(Area):
    def set_text(self, text, fsize=12, text_color=darkblue):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)
    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

start_time = time.time()
cur_time = start_time

time_text = Label(0,0,50,50, babypink)
time_text.set_text('Time:',25, hotpink)
time_text.draw(20, 20)

timer = Label(50,55,50,40,babypink)
timer.set_text('0', 20, hotpink)
timer.draw(0,0)

score_text = Label(380,0,50,50,babypink)
score_text.set_text('Count:',25, hotpink)
score_text.draw(20,20)

score = Label(430,55,50,40,babypink)
score.set_text('0', 20, hotpink)
score.draw(0,0)

cards = []
num_cards = 4
x = 70

for i in range(num_cards):
    new_card = Label(x, 170, 70, 100, skyblue)
    new_card.outline(darkblue, 40)
    new_card.set_text('CLICK', 20)
    cards.append(new_card)
    x = x + 100

wait = 0
points = 0
play = True
finish = False

while play:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            play = False
    "Menggambar kartu dan menampilkan klik"
    if wait == 0:
        wait = 20 #begitu banyak kutu label akan berada di satu tempat
        click = randint(1, num_cards)
        for i in range(num_cards):
            cards[i].color(skyblue)
            if (i + 1) == click:
                cards[i].draw(10, 40)
            else:
                cards[i].fill()
    else:
        wait -= 1
    '''Menangani klik pada kartu'''
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            for i in range(num_cards):
                if cards[i].collidepoint(x,y):
                    if i + 1 == click:# jika ada label pada kartu, kita beri warna hijau, tambahkan titik 
                        cards[i].color(lightgreen)
                        points += 1
                    else: #jika tidak, warnai merah, kurangi satu poin
                        cards[i].color(lightred)
                        points -= 1
                    cards[i].fill()
                    score.set_text(str(points),25, hotpink)
                    score.draw(0,0)
    "Menang dan kalah"
    new_time = time.time()

    if new_time - start_time  >= 5:
        win = Label(0, 0, width, height, babypink)
        win.set_text("Waktunya sudah habis!!!", 30, hotpink)
        win.draw(110, 180)
        break
        #play = False
    
    if int(new_time) - int(cur_time) == 1: #periksa apakah ada perbedaan 1 detik antara waktu lama dan baru
        timer.set_text(str(int(new_time - start_time)),30, hotpink)
        timer.draw(0,0)
        cur_time = new_time

    if points >= 5:
        win = Label(0, 0, width, height, babypink)
        win.set_text("Anda menang!!!", 30, hotpink)
        win.draw(140, 180)
        resul_time = Label(90, 230, 250, 250, babypink)
        resul_time.set_text("Waktu untuk menyelesaikan: " + str (int(new_time - start_time)) + " сек", 15, hotpink)
        resul_time.draw(0, 0)
        break
        #play = False


    pygame.display.update()
    clock.tick(40)


pygame.display.update() 