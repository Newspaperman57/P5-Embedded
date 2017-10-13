import pygame
import math

class Graph:
    def __init__(self, graphData, w, h, scale=1, dataHeight=1, dataOffset=0):
        self.__graphData = graphData
        self.w = w
        self.h = h
        self.scale = scale
        self.dataHeight = (2**15)*dataHeight
        self.dataOffset = dataOffset
        self.lastDrawn = 0

    def SetDataHeight(self, dataheight):
        self.dataHeight /= dataheight

    def SetScale(self, scale, relx):
        drawnPoints = (self.lastDrawn-self.dataOffset)
        self.dataOffset -= ((float(relx)/self.w)/scale)*(drawnPoints-(drawnPoints*scale))
        self.scale *= scale

    # Use self.scale to scale data horizontally to match box
    def Render(self, background, x, y):
        pygame.draw.rect(background, 0x373B3E, (x, y, self.w, self.h))
        if self.dataOffset < 0:
            self.dataOffset = 0
        dataIterator = int(self.dataOffset)+1
        startTime = self.__graphData[dataIterator-1].time
        dataYZero = y+(self.h)/2
        pygame.draw.line(background, 0xE6E6E7, (
              (self.__graphData[dataIterator-1].time-startTime)*self.scale+x    
            , dataYZero)                                                                               
            , ((self.__graphData[dataIterator-1].time-startTime)*self.scale+x
            , dataYZero)
            , 2)


        while dataIterator < len(self.__graphData) and (self.__graphData[dataIterator].time-startTime)*self.scale < self.w:
            # draw a dot for each time we measure data. These dots will look like a line at y=0
            pygame.draw.line(background, 0xE6E6E7, (
                  (self.__graphData[dataIterator].time-startTime)*self.scale+x    
                , dataYZero)                                                                               
                , ((self.__graphData[dataIterator].time-startTime)*self.scale+x
                , dataYZero)
                , 2)

            # print numbers indicating time at given points. Less points are printed when more points are viewed (to avoid overlapping text) by multiplying by the inverse of scale
            iscale = self.scale**(-1)*100
            if dataIterator % max(math.floor(iscale), 1) == 0:
                myfont = pygame.font.SysFont("DejaVu Sans Mono", 15)
                label = myfont.render(("%d" % (self.__graphData[dataIterator].time)), 1, (255, 255, 0))
                background.blit(label, ((self.__graphData[dataIterator].time-startTime)*self.scale+x, dataYZero))

            # variables to print dots at the correct time and position corresponding to time and z-values from data. CHANGE RZ TO Z
            dataY = int(self.__graphData[dataIterator].z/self.dataHeight*(self.h/2))
            if dataY > self.h/2:
                dataY = self.h/2
            if dataY < -self.h/2:
                dataY = -self.h/2

            lastDataY =int(self.__graphData[dataIterator - 1].z/self.dataHeight*(self.h/2))
            if lastDataY > self.h/2:
                lastDataY = self.h/2
            if lastDataY < -self.h/2:
                lastDataY = -self.h/2

            # draw a line from last point to current point, creating a graph
            pygame.draw.line(background, 0x35A4E8, 
                ((self.__graphData[dataIterator-1].time - startTime)*self.scale+x,
                  lastDataY+dataYZero) ,
                ((self.__graphData[dataIterator].time - startTime)*self.scale+x, 
                  dataY+dataYZero) , 2)

            dataIterator += 1
        self.lastDrawn = dataIterator

        if dataIterator == int(self.dataOffset)+1:
            print "NO GRAPHDATA SHOWN"

    def SetDataOffset(self, direction):
        self.dataOffset += direction
        if self.dataOffset < 0:
            self.dataOffset = 0
        