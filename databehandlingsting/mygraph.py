import pygame

class Graph:
    def __init__(self, graphData, w, h, millis, dataHeight):
        self.__graphData = graphData
        self.w = w
        self.h = h
        self.millis = millis
        self.dataHeight = (2**15)*dataHeight

    # Use self.millis to scale data horizontally to match box
    def Render(self, background, x, y, dataOffset):
        iterator = dataOffset+1
        startTime = self.__graphData[dataOffset].time
        dataYZero = y+(self.h)/2

        while self.__graphData[dataOffset+iterator-1].time-startTime < self.w:
            iterator += 1
            pygame.draw.line(background, 0x00FFFF, (self.__graphData[dataOffset+iterator].time-startTime+x    , self.__graphData[dataOffset+iterator].z/self.dataHeight*(self.h/2)+dataYZero)   , (self.__graphData[dataOffset+iterator].time-startTime+x  , self.__graphData[dataOffset+iterator].z/self.dataHeight*(self.h/2)+dataYZero) , 3)
            pygame.draw.line(background, 0xFFFF00, (self.__graphData[dataOffset+iterator].time-startTime+x    , dataYZero)                                                              , (self.__graphData[dataOffset+iterator].time-startTime+x  , dataYZero)                                                            , 3)
            pygame.draw.line(background, 0x00FFFF, (self.__graphData[dataOffset+iterator-1].time-startTime+x  , self.__graphData[dataOffset+iterator-1].z/self.dataHeight*(self.h/2)+dataYZero) , (self.__graphData[dataOffset+iterator].time-startTime+x  , self.__graphData[dataOffset+iterator].z/self.dataHeight*(self.h/2)+dataYZero) , 1)
