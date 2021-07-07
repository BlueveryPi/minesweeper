import pygame, math, random
import numpy as np
pygame.init()

size=6
w=61 - int(math.log(size))*10
d=9 #out of 10
screen = pygame.display.set_mode([size*w+30+(size-1)*5, size*w+30+(size-1)*5])
gridlist=[]

def translate(a):
    if a==-1:
        return 0
    elif a==2:
        return 1
    elif a==1:
        return 2
    elif a==-2:
        return 3

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
                else:
                    pass #boom
    
    def checkaround(self, skip=0):
        tmp=[0, 1, 0, -1]
        self.revealed=True
        if skip==0:
            for _ in range(4):
                if self.x+tmp[_]>-1 and self.x+tmp[_]<size and self.y+tmp[3-_]>-1 and self.y+tmp[3-_]<size:
                    if gridlist[self.x+tmp[_]][self.y+tmp[3-_]].nearmines==0 and gridlist[self.x+tmp[_]][self.y+tmp[3-_]].mine==False:
                        gridlist[self.x+tmp[_]][self.y+tmp[3-_]].revealed=True
                        gridlist[self.x+tmp[_]][self.y+tmp[3-_]].checkaround(1)

                    elif gridlist[self.x+tmp[_]][self.y+tmp[3-_]].nearmines!=0 and gridlist[self.x+tmp[_]][self.y+tmp[3-_]].mine==False:
                        gridlist[self.x+tmp[_]][self.y+tmp[3-_]].revealed=True

        else:
            for _ in range(4):
                if self.x+tmp[_]>-1 and self.x+tmp[_]<size and self.y+tmp[3-_]>-1 and self.y+tmp[3-_]<size and gridlist[self.x+tmp[_]][self.y+tmp[3-_]].mine==False:
                    if gridlist[self.x+tmp[_]][self.y+tmp[3-_]].revealed!=True and gridlist[self.x+tmp[_]][self.y+tmp[3-_]].nearmines==0: #nightmare yesn't
                        gridlist[self.x+tmp[_]][self.y+tmp[3-_]].revealed=True
                        gridlist[self.x+tmp[_]][self.y+tmp[3-_]].checkaround(1)
                    elif gridlist[self.x+tmp[_]][self.y+tmp[3-_]].nearmines!=0 and gridlist[self.x+tmp[_]][self.y+tmp[3-_]].mine==False:
                        gridlist[self.x+tmp[_]][self.y+tmp[3-_]].revealed=True

for p in range(size):
    gridlist.append([])

for p in range(size):
    for q in range(size):
        gridlist[p].append(mine())
        gridlist[p][q].x=p
        gridlist[p][q].y=q

for _ in range(int(size**2/4)):
    if random.randint(0, 10)<d:
        a=random.randint(0, size-1)
        b=random.randint(0, size-1)
        gridlist[a][b].mine=True

tmpx=[0, 1, 1, 1, 0, -1, -1, -1]
tmpy=[-1, -1, 0, 1, 1, 1, 0, -1] #no problem! no it wasn't. maybe? yes it is.
for x in range(size):
    for y in range(size):
            for _ in range(8):
                if not(x+tmpx[_]<0 or x+tmpx[_]>size-1 or y+tmpy[_]<0 or y+tmpy[_]>size-1):
                    if gridlist[x+tmpx[_]][y+tmpy[_]].mine:
                        gridlist[x][y].nearmines += 1
                else:
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
