import pygame
pygame.init()

size=6
screen = pygame.display.set_mode([size*50+30+(size-1)*5, size*50+30+(size-1)*5])
minelist=[]

class mine():
    def __init__(self):
        self.x=0
        self.y=0

for p in range(size):
    minelist.append([])

for p in range(size):
    for q in range(size):
        minelist[p].append(mine())
        minelist[p][q].x=p
        minelist[p][q].x=q

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    for x in range(size):
        for y in range(size):
            pygame.draw.rect(screen, (33, 118, 255), pygame.Rect(15+x*50+5*x, 15+y*50+5*y, 50, 50))
            pygame.draw.rect(screen, (18, 109, 255), pygame.Rect(18+x*50+5*x, 18+y*50+5*y, 44, 44))

    pygame.display.flip()

pygame.quit()