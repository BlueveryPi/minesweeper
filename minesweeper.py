import pygame
pygame.init()

size=6
screen = pygame.display.set_mode([size*50+30+(size-1)*5, size*50+30+(size-1)*5])
gridlist=[]

class mine():
    def __init__(self):
        self.x=0
        self.y=0
        self.flagged=False
        self.mine=False
        self.triggered=False

for p in range(size):
    gridlist.append([])

for p in range(size):
    for q in range(size):
        gridlist[p].append(mine())
        gridlist[p][q].x=p
        gridlist[p][q].x=q

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP: 
            if event.button==3: #if left click
                if event.pos[0]>15 and event.pos[0]<size*50+30+(size-1)*5-15 and event.pos[1]>15 and event.pos[1]<size*50+30+(size-1)*5-15: #some nice over-safety
                    gridlist[int((event.pos[0]-2.5)//56)][int((event.pos[1]-2.5)//56)].flagged ^= True #toggle the thingy

    screen.fill((255, 255, 255))

    for x in range(size):
        for y in range(size):
            if gridlist[x][y].flagged==False:
                color=(33, 118, 255)
            else:
                color=(255, 26, 10)

            pygame.draw.rect(screen, color, pygame.Rect(15+x*50+5*x, 15+y*50+5*y, 50, 50)) #draw the thingy
            pygame.draw.rect(screen, (240, 240, 240), pygame.Rect(18+x*50+5*x, 18+y*50+5*y, 44, 44))

            if gridlist[x][y].mine==True and gridlist[x][y].triggered==True: #if boom
                pygame.draw.rect(screen, (255, 26, 10), pygame.Rect(18+x*50+5*x, 18+y*50+5*y, 44, 44)) #color red

    pygame.display.flip()

pygame.quit()
