import math
import pygame as pg


# complex math 

boundary = 1e10
countmax = 150

colorc = int(255/countmax)

def getDistance(z):
    return (z.real)**2 + (z.imag)**2

def mapFromTo(x,a,b,c,d):
   y=(x-a)/(b-a)*(d-c)+c
   return y

# def f2(i,j):
#     x = mapFromTo(i,int(-WIDTH/2),int(WIDTH/2),-2,1)
#     y = mapFromTo(j,int(-HEIGHT/2),int(HEIGHT/2),-1.2,1.2)
#     c = complex(x,y)
#     count = 0
#     z = complex(0,0)
#     while count <= countmax-1 and getDistance(z) < boundary**2:
#         count +=1 
#         z = z**2 + c
#     return count

def f2(c):
    count = 0
    z = complex(0,0)
    while count <= countmax-1 and getDistance(z) < boundary**2:
        count +=1 
        z = z**2 + c
    return count


# pygame setup
    
RUN = True

pg.init()
clock = pg.time.Clock()


WIDTH = 300
HEIGHT = 300
window = pg.display.set_mode((WIDTH,HEIGHT))

xz,yz = 0,0
zoomed = False
zoomVar = 5
hasloaded = False

fractalArray = []
fractalsArray = []

zoomCount = 0

xLzoombound = int(-WIDTH/2)
xUzoombound = int(WIDTH/2)

yLzoombound = int(-HEIGHT/2)
yUzoombound = int(HEIGHT/2)

selected = 0

def LoadFractal():
    fractalArray = []
    for i in range(int((-WIDTH/2)),int(WIDTH/2)):
        fractalRow = []
        for j in range(int(-HEIGHT/2),int(HEIGHT/2)):
            pg.event.pump()
            if zoomed:
                x = mapFromTo(i,xLzoombound,xUzoombound, xz-0.1/(2**zoomVar),xz+0.1/(2**zoomVar))
                y = mapFromTo(j,yLzoombound,yUzoombound, yz-0.1/(2**zoomVar),yz+0.1/(2**zoomVar))
            else:
                x = mapFromTo(i,int(-WIDTH/2),int(WIDTH/2),-2,1)
                y = mapFromTo(j,int(-HEIGHT/2),int(HEIGHT/2),-1.2,1.2)
            z = complex(x,y)
            color = f2(z)
            # COlOR MAPPING
            c1 = mapFromTo(color,0,int(countmax/3),0,255)
            c2 = mapFromTo(color,int(countmax/3),int(countmax/3*2),0,255)
            if c2 < 0:
                c2 = 0
            c3 = mapFromTo(color,int(countmax*2/3),int(countmax),0,255)
            if c3 <0:
                c3 = 0
            if c1 > 255:
                c1 = 255
            if c2 > 255:
                c2 = 255
            if c3 > 255:
                c3 = 255
            color = [c1,c2,c3]
            fractalRow.append(color)
            
            # color = f2(i,j)   
            # window.set_at((int(i+WIDTH/2),int(j+HEIGHT/2)),(color*colorc,color*colorc,color*colorc))
        fractalArray.append(fractalRow)
    return fractalArray

while RUN:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            RUN = False
        if event.type == pg.KEYDOWN:
            key = event.unicode
            if key == '1':
                if selected == 0:
                    selected = 0
                else:
                    selected -= 1
            if key == '2':
                if selected == len(fractalsArray) -1 :
                    selected = len(fractalsArray) -1
                else: selected += 1
            if key == '-':
                if zoomVar == 1:
                    zoomVar = 1
                else:
                    zoomVar -= 0.5
                print('zoom: ', zoomVar)
            if key == '=':
                zoomVar += 0.5
                print('zoom: ', zoomVar)

            if key =='p':
                fractalsArray = fractalsArray[:selected+1]
        
        if event.type == pg.MOUSEBUTTONUP:
            print('mouse dowwn')
            mousecoords = pg.mouse.get_pos()
            xz = mapFromTo(mousecoords[0],0,WIDTH,-2,1)
            yz = mapFromTo(mousecoords[1],0,HEIGHT,-1.2,1.2)
            
            zoomCount += 1

            xLzoombound = xz - 0.05
            xUzoombound = xz + 0.05
            yLzoombound = xz - 0.05
            yUzoombound = xz + 0.05
            zoomed = True
            fractalArray = []
            selected += 1
            print(mousecoords[0],mousecoords[1])
            print(xz,yz)
    if fractalArray == []:
        fractalArray = LoadFractal()  
        fractalsArray.append(fractalArray)
        print('loaded')
    for idx,i in enumerate(fractalsArray[selected]):
        for jdx,j in enumerate(i):
            pg.event.pump()            
            window.set_at((idx,jdx),(j[2],j[1],j[0]))
    pg.display.update()
    
    clock.tick(60)
    