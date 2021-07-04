import pygame, math, random
import numpy as np
pygame.init()

size=6
w=61 - int(math.log(size))*10
screen = pygame.display.set_mode([size*w+30+(size-1)*5, size*w+30+(size-1)*5])
gridlist=[]

class mine():
    def __init__(self):
        self.x=0
        self.y=0
        self.flagged=False
        self.mine=False
        self.revealed=False
        self.nearmines=0

    def draw(self):
        if self.revealed==True:
            color=(220, 220, 220)
        elif self.flagged==True:
            color=(255, 26, 10)
        elif self.mine==True:
            color=(0,0,0)
        else:
            color=(33, 118, 255)
        

        pygame.draw.rect(screen, color, pygame.Rect(15+self.x*w+5*self.x, 15+self.y*w+5*self.y, w, w)) #draw the thingy
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(18+self.x*w+5*self.x, 18+self.y*w+5*self.y, w-6, w-6))

        if self.mine==True and self.revealed==True: #if boom
            pygame.draw.rect(screen, (255, 26, 10), pygame.Rect(15+self.x*w+5*self.x, 15+self.y*w+5*self.y, w, w)) #color red

    def onclick(self, event):
        if event.pos[0]>15+5*self.x+w*self.x and event.pos[0]<15+5*self.x+w*(self.x+1) and event.pos[1]>15+5*self.y+w*self.y and event.pos[1]<15+5*self.y+w*(self.y+1):
            if event.button==3:
                self.flagged ^= True
                print(self.nearmines)
            elif event.button==1:
                if self.mine == False:
                    self.checkaround()
                    self.revealed=True
    
    def checkaround(self, skip=-1):
        tmp=[0, 1, 0, -1]
        self.revealed=True
        if skip==-1:
            for _ in range(4):
                try:
                    if gridlist[self.x+tmp[_]][self.y+tmp[3-_]].nearmines==0:
                        gridlist[self.x+tmp[_]][self.y+tmp[3-_]].revealed=True
                        gridlist[self.x+tmp[_]][self.y+tmp[3-_]].checkaround(4-_)
                except IndexError:
                    continue

        else:
            for _ in range(4):
                try:
                    if _==skip:
                        break
                    elif gridlist[self.x+tmp[_]][self.y+tmp[3-_]].revealed==True:
                        break
                    elif gridlist[self.x+tmp[_]][self.y+tmp[3-_]].nearmines==0:
                        gridlist[self.x+tmp[_]][self.y+tmp[3-_]].revealed=True
                        gridlist[self.x+tmp[_]][self.y+tmp[3-_]].checkaround(4-_)
                except IndexError:
                    continue

for p in range(size):
    gridlist.append([])

for p in range(size):
    for q in range(size):
        gridlist[p].append(mine())
        gridlist[p][q].x=p
        gridlist[p][q].y=q

for _ in range(int(size**2/4)):
    a=random.randint(0, size-1)
    b=random.randint(0, size-1)
    gridlist[a][b].mine=True

tmpx=[0, 1, 1, 1, 0, -1, -1, -1]
tmpy=[-1, -1, 0, 1, 1, 1, 0, -1]
for x in range(size):
    for y in range(size):
        try:
            for _ in range(8):
                if gridlist[x+tmpx[_]][y+tmpy[_]].mine:
                    gridlist[x][y].nearmines += 1
        except IndexError:
            continue

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP: 
            for x in range(size):
                for y in range(size):
                    gridlist[x][y].onclick(event)

    screen.fill((255, 255, 255))

    for x in range(size):
        for y in range(size):
            gridlist[x][y].draw()

    pygame.display.flip()

pygame.quit()
