from tkinter import *

HEIGHT = 500
WIDTH = 800
window = Tk()
window.title('Bubble blaster')
c = Canvas(window, width=WIDTH, height=HEIGHT, bg='darkblue')
c.pack()

nave_id = c.create_polygon(5, 5, 5, 25, 30, 15, fill='red')
nave_id2 = c.create_oval(0, 0, 30, 30, outline='red')

NAVE_R = 15
MID_X = WIDTH / 2
MID_Y = HEIGHT / 2
c.move(nave_id, MID_X, MID_Y)
c.move(nave_id2, MID_X, MID_Y)

VELOCITA = 10
def muovi_nave(event):
    if event.keysym == 'Up':
        c.move(nave_id, 0, -VELOCITA)
        c.move(nave_id2, 0, -VELOCITA)
    elif event.keysym == 'Down':
        c.move(nave_id, 0, VELOCITA)
        c.move(nave_id2, 0, VELOCITA)
    elif event.keysym == 'Left':
        c.move(nave_id, -VELOCITA, 0)
        c.move(nave_id2, -VELOCITA, 0)
    elif event.keysym == 'Right':
        c.move(nave_id, VELOCITA, 0)
        c.move(nave_id2, VELOCITA, 0)
c.bind_all('<Key>', muovi_nave)

from random import randint

bub_id = list()
bub_r = list()
bub_speed = list()
MIN_BUB_R = 10
MAX_BUB_R = 30
MAX_BUB_SPEED = 10
GAP = 100

def crea_bubbles():
    x = WIDTH + GAP
    y = randint(0, HEIGHT)
    r = randint(MIN_BUB_R, MAX_BUB_R)
    id1 = c.create_oval(x - r, y - r, x + r, y + r, outline='white')
    bub_id.append(id1)
    bub_r.append(r)
    bub_speed.append(randint(1, MAX_BUB_SPEED))
def move_bubbles():
    for i in range(len(bub_id)):
        c.move(bub_id[i], -bub_speed[i], 0)
        
def hole_koord(id_num):
    pos = c.coords(id_num)
    x = (pos[0] + pos[2])/2
    y = (pos[1] + pos[3])/2
    return x, y
def cancella_bubble(i):
    del bub_r[i]
    del bub_speed[i]
    c.delete(bub_id[i])
    del bub_id[i]
def elim_bubbles():
    for i in range(len(bub_id)-1, -1, -1):
        x, y = hole_koord(bub_id[i])
        if x < -GAP:
            cancella_bubble(i)

from math import sqrt

def distanza(id1, id2):
    x1, y1 = hole_koord(id1)
    x2, y2 = hole_koord(id2)
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)
def collisione():
    score = 0
    for bub in range(len(bub_id)-1, -1, -1):
        if distanza(nave_id2, bub_id[bub]) < (NAVE_R + bub_r[bub]):
            score += (bub_r[bub] + bub_speed[bub])
            cancella_bubble(bub)
    return score

c.create_text(50, 30, text='TIME', fill='white')
c.create_text(150, 30, text='SCORE', fill='white')
time_text = c.create_text(50, 50, fill='white')
points_text = c.create_text(150, 50, fill='white')

def view_points(points):
    c.itemconfig(points_text, text=str(points))
def view_time(time_left):
    c.itemconfig(time_text, text=str(time_left))
    
from time import sleep, time

BUB_CHANCE = 10
TIME_LIMIT = 40
BONUS_SCORE =1000
points = 0
bonus = 0
end = time() + TIME_LIMIT

#Main Loop
while time() < end:
    if randint(1, BUB_CHANCE) == 1:
        crea_bubbles()
    move_bubbles()
    elim_bubbles()
    points += collisione()
    if (int(points / BONUS_SCORE)) > bonus:
        bonus += 1
        end += TIME_LIMIT
    view_points(points)
    view_time(int(end - time()))
    window.update()
    sleep(0.01)

c.create_text(MID_X, MID_Y, \
    text='GAME OVER', fill='white', font=('Helvetica',30))
c.create_text(MID_X, MID_Y + 30, \
    text='Score: '+ str(points), fill='white')
c.create_text(MID_X, MID_Y + 45, \
    text='Bonus time: '+str(bonus*TIME_LIMIT), fill='white')             
