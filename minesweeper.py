import pygame, math, random, asyncio, pickle
from PIL import Image, ImageDraw, ImageFont
from socket import *
import threading 
pygame.init()

size=10
w=61 - int(math.log(size))*10
d=9 #out of 10
screen = pygame.display.set_mode([(size*w+30+(size-1)*5)*2, size*w+30+(size-1)*5])
font=ImageFont.truetype("Rockout-vVaM.ttf", 30)

class mine():
    def __init__(self, board, enabled):
        self.x=0
        self.y=0
        self.flagged=False
        self.mine=False
        self.revealed=False
        self.nearmines=0
        self.mx=board.x
        self.my=board.y
        self.board=board
        self.enabled=enabled
        self.gridlist=board.gridlist
        self.minelist=board.minelist

    def draw(self):
        if self.revealed==True:
            color=(220, 220, 220)
            
        elif self.flagged==True:
            color=(255, 26, 10)

        elif self.mine==True:
            color=(0, 0, 0) #debug mode

        else:
            color=(33, 118, 255)
        

        pygame.draw.rect(screen, color, pygame.Rect(15+self.x*w+5*self.x+self.mx, 15+self.y*w+5*self.y+self.my, w, w)) #draw the thingy
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(18+self.x*w+5*self.x+self.mx, 18+self.y*w+5*self.y+self.my, w-6, w-6))

        if self.mine==True and self.revealed==True: #if boom
            self.board.ongame=False
            pygame.draw.rect(screen, (255, 26, 10), pygame.Rect(15+self.x*w+5*self.x+self.mx, 15+self.y*w+5*self.y+self.my, w, w))
            for i in range(0):
                pass

        elif self.revealed==True and self.nearmines!=0:
            blank=Image.new("RGBA", (w-3, w-3), (220, 220, 220, 0))
            ctx = ImageDraw.Draw(blank)
            ctx.text((10,10), str(self.nearmines), font=font, fill=(33, 118, 255, 255))
            screen.blit(pygame.image.fromstring(blank.tobytes(), blank.size, blank.mode), (self.x*w+15+5*self.x+int(w//4)+self.mx, self.y*w+15+5*self.y-int(w/6)+self.my+3))

    def onclick(self, event):
        if self.enabled:
            if event.pos[0]>15+5*self.x+w*self.x+self.mx and event.pos[0]<15+5*self.x+w*(self.x+1)+self.mx and event.pos[1]>15+5*self.y+w*self.y+self.my and event.pos[1]<15+5*self.y+w*(self.y+1)+self.my:
                if event.button==3:
                    if self.revealed==False:
                        self.flagged ^= True
                        if self.mine==True and self.flagged==True:
                            self.board.remainingmines-=1
                            if self.board.remainingmines==0 and self.board.remaininggrids==0:
                                self.board.ongame=False
                                print('good')
                                pass #endgame
                            
                        elif self.mine==True:
                            self.board.remainingmines+=1
                elif event.button==1:
                    if self.mine==False and self.revealed==False and self.flagged==False:
                        self.checkaround()
                        self.revealed=True
                    elif self.revealed==False and self.flagged==False:
                        self.revealed=True
    
    def checkaround(self, skip=0):
        gridlist=self.gridlist
        tmp=[0, 1, 0, -1]
        self.revealed=True
        self.board.remaininggrids-=1
        if skip==0:
            for _ in range(4):
                if self.x+tmp[_]>-1 and self.x+tmp[_]<size and self.y+tmp[3-_]>-1 and self.y+tmp[3-_]<size:
                    if gridlist[self.x+tmp[_]][self.y+tmp[3-_]].nearmines==0 and gridlist[self.x+tmp[_]][self.y+tmp[3-_]].mine==False and gridlist[self.x+tmp[_]][self.y+tmp[3-_]].flagged==False:
                        gridlist[self.x+tmp[_]][self.y+tmp[3-_]].revealed=True
                        self.board.remaininggrids-=1
                        gridlist[self.x+tmp[_]][self.y+tmp[3-_]].checkaround(1)

                    elif gridlist[self.x+tmp[_]][self.y+tmp[3-_]].nearmines!=0 and gridlist[self.x+tmp[_]][self.y+tmp[3-_]].mine==False and gridlist[self.x+tmp[_]][self.y+tmp[3-_]].flagged==False:
                        gridlist[self.x+tmp[_]][self.y+tmp[3-_]].revealed=True
                        self.board.remaininggrids-=1

        else:
            for _ in range(4):
                if self.x+tmp[_]>-1 and self.x+tmp[_]<size and self.y+tmp[3-_]>-1 and self.y+tmp[3-_]<size and gridlist[self.x+tmp[_]][self.y+tmp[3-_]].mine==False and gridlist[self.x+tmp[_]][self.y+tmp[3-_]].flagged==False:
                    if gridlist[self.x+tmp[_]][self.y+tmp[3-_]].revealed!=True and gridlist[self.x+tmp[_]][self.y+tmp[3-_]].nearmines==0: #nightmare yesn't
                        gridlist[self.x+tmp[_]][self.y+tmp[3-_]].revealed=True
                        self.board.remaininggrids-=1
                        gridlist[self.x+tmp[_]][self.y+tmp[3-_]].checkaround(1)
                    elif gridlist[self.x+tmp[_]][self.y+tmp[3-_]].nearmines!=0 and gridlist[self.x+tmp[_]][self.y+tmp[3-_]].mine==False and gridlist[self.x+tmp[_]][self.y+tmp[3-_]].flagged==False:
                        gridlist[self.x+tmp[_]][self.y+tmp[3-_]].revealed=True
                        self.board.remaininggrids-=1

class gameboard():
    def __init__(self, x, y, enabled):
        self.x=x
        self.y=y
        self.ongame=True
        self.enabled=enabled
        self.gridlist=[]
        self.minelist=[]

    def initalize(self):
        gridlist=self.gridlist
        minelist=self.minelist
        for p in range(size):
            gridlist.append([])

        for p in range(size):
            for q in range(size):
                gridlist[p].append(mine(self, self.enabled))
                gridlist[p][q].x=p
                gridlist[p][q].y=q

        for _ in range(int(size**2/4)):
            if random.randint(0, 10)<d:
                a=random.randint(0, size-1)
                b=random.randint(0, size-1)
                if gridlist[a][b].mine==False:
                    gridlist[a][b].mine=True
                    minelist.append(gridlist[a][b])
        self.remainingmines=len(minelist)
        self.remaininggrids=size**2-self.remainingmines

        tmpx=[0, 1, 1, 1, 0, -1, -1, -1]
        tmpy=[-1, -1, 0, 1, 1, 1, 0, -1] #no problem! no it wasn't. maybe? yes it is.
        for x in range(size):
            for y in range(size):
                    for _ in range(8):
                        if not(x+tmpx[_]<0 or x+tmpx[_]>size-1 or y+tmpy[_]<0 or y+tmpy[_]>size-1):
                            if gridlist[x+tmpx[_]][y+tmpy[_]].mine:
                                gridlist[x][y].nearmines += 1

global updated
updated=False

def send(sock):
    global updated
    while True:
        if updated==True:
            updated=False
            sendData = pickle.dumps(game1)
            sock.send(sendData)

def recv(sock):
    global game2
    while True:
        data = sock.recv(8192)
        game2=pickle.loads(data)

ip = str(input("IP: "))
port = 65432

nick=str(input("닉네임: "))
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect( (ip, port))
clientSocket.send(nick.encode('utf-8'))

print("접속완료")

sender = threading.Thread(target=send, args=(clientSocket, ))
receiver = threading.Thread(target=recv, args = (clientSocket,))

sender.start()
receiver.start()
global game2
game1=gameboard(0, 0, True)
game2=gameboard(size*w+30+(size-1)*5, 0, False)
game1.initalize()
game2.initalize()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP: 
            for x in range(size):
                for y in range(size):
                    game1.gridlist[x][y].onclick(event)
                    updated=True


    screen.fill((255, 255, 255))

    for x in range(size):
        for y in range(size):
            game1.gridlist[x][y].draw()
            game2.gridlist[x][y].draw()

    pygame.display.flip()

pygame.quit()
