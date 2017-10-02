import pygame

class Graph:
    def __init__(self, graphData, w, h, scale=1, dataHeight=1, dataOffset=0):
        self.__graphData = graphData
        self.w = w
        self.h = h
        self.scale = scale
        self.dataHeight = (2**15)*dataHeight
        self.dataOffset = 0

    def SetScale(scale):
        self.scale = scale

    # Use self.scale to scale data horizontally to match box
    def Render(self, background, x, y, ):
        pygame.draw.line(background, 0xFF0000, (x, y), (x+self.w, y+self.h))
        pygame.draw.line(background, 0xFF0000, (x+self.w, y), (x, y+self.h))
        dataIterator = self.dataOffset+1
        startTime = self.__graphData[self.dataOffset].time
        dataYZero = y+(self.h)/2
        while (self.__graphData[self.dataOffset+dataIterator+1].time-startTime)*self.scale < self.w:
            """Zero-line"""
            pygame.draw.line(background, 0xFFFF00, (
                  (self.__graphData[self.dataOffset+dataIterator].time-startTime)*self.scale+x    
                , dataYZero)                                                                               
                , ((self.__graphData[self.dataOffset+dataIterator].time-startTime+x)*self.scale+x
                , dataYZero)
                , 2)
            """small box at data-point"""
            pygame.draw.line(background, 0x00FFFF, 
                ((self.__graphData[self.dataOffset+dataIterator].time-startTime)*self.scale+x    , 
                  self.__graphData[self.dataOffset+dataIterator].z/self.dataHeight*(self.h/2)+dataYZero)   , 
                ((self.__graphData[self.dataOffset+dataIterator].time-startTime+x)*self.scale+x, 
                  self.__graphData[self.dataOffset+dataIterator].z/self.dataHeight*(self.h/2)+dataYZero) , 2)
            """Data-line"""
            pygame.draw.line(background, 0x00FFFF, 
                ((self.__graphData[self.dataOffset+dataIterator-1].time-startTime)*self.scale+x  , 
                  self.__graphData[self.dataOffset+dataIterator-1].z/self.dataHeight*(self.h/2)+dataYZero) ,
                ((self.__graphData[self.dataOffset+dataIterator].time-startTime+x)*self.scale+x, 
                  self.__graphData[self.dataOffset+dataIterator].z/self.dataHeight*(self.h/2)+dataYZero) , 1)
            dataIterator += 1

        if dataIterator == self.dataOffset+1:
            print "NO GRAPHDATA SHOWN"
