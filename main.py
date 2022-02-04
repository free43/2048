import pygame as pg
import sys
import math
import random
#TODO: Bug could be inside. Check if Blocks disappear outside the gamefield

def getOppositeDirection(direction):
    if direction == "UP":
        return "DOWN"
    elif direction == "DOWN":
        return "UP"
    elif direction == "LEFT":
        return "RIGHT"
    elif direction == "RIGHT":
        return "LEFT"
class Game:
    emptyBlockList : list
    valueBlockList : list
    blockSize : int
    windowSize : tuple
    direction : str
    numbOfBlocks : int
    newKeyValue : bool
    toCombineBlock : list
    score : int
    losed : bool
    def __init__(self, blockSize : int, windowSize : tuple, numbOfBLocks):
        self.blockSize = blockSize
        self.windowSize = windowSize
        self.numbOfBlocks = numbOfBLocks
        self.emptyBlockList = [EmptyBlock(self.blockSize, x, self.numbOfBlocks) for x in range(self.numbOfBlocks*self.numbOfBlocks)]
        elementIndex = random.randint(0, self.numbOfBlocks*self.numbOfBlocks - 1)
        self.valueBlockList = []
        self.valueBlockList.append( ValueBlock(self.blockSize, elementIndex, value=2, numbOfBlocks=self.numbOfBlocks)) #< for Game
        # For testing: Manipulate here
        #for i in range(0, self.numbOfBlocks**2):
        #    self.valueBlockList.append(ValueBlock(self.blockSize, i, value=i + 10))
        #self.valueBlockList[0] = ValueBlock(self.blockSize, 0, value=2)
        #self.valueBlockList[4] = ValueBlock(self.blockSize, 4, value=2)
        #self.valueBlockList.append( ValueBlock(self.blockSize, 0, value=2))
        #self.valueBlockList.append( ValueBlock(self.blockSize, 1, value=2))
        #self.valueBlockList.append( ValueBlock(self.blockSize, 2, value=4))
        #self.valueBlockList.append( ValueBlock(self.blockSize, 3, value=4))
        #self.valueBlockList.append( ValueBlock(self.blockSize, 4, value=16))
        #self.valueBlockList.append( ValueBlock(self.blockSize, 8, value=32))
        #self.valueBlockList.append( ValueBlock(self.blockSize, 9, value=2))
        #self.valueBlockList.append( ValueBlock(self.blockSize, 10, value=2))
        #self.valueBlockList.append( ValueBlock(self.blockSize, 12, value=4))
        #self.valueBlockList.append( ValueBlock(self.blockSize, 13, value=16))
        #self.valueBlockList.append( ValueBlock(self.blockSize, 14, value=8))
        #self.valueBlockList.append( ValueBlock(self.blockSize, 15, value=4))
        self.direction = None
        self.newKeyValue = False
        self.toCombinBlock = set()
        self.score = 0
        self.losed = False
        pass
    def draw(self, DISP):
        for block in self.emptyBlockList:
            block.draw(DISP)
        for block in self.valueBlockList:
            block.draw(DISP)
        self.drawScore(DISP)
        if self.losed:
            self.drawLose(DISP)
    def drawScore(self, DISP):
        fontSize = 40
        myfont = pg.font.SysFont("Comic Sans MS", fontSize)
        value = "Score: " + str(self.score)
        label = myfont.render(value, True, (0, 0, 0))
        DISP.blit(label, ( 0, self.numbOfBlocks * self.blockSize + fontSize))
    def drawLose(self, DISP):
        fontSize = 40
        myfont = pg.font.SysFont("Comic Sans MS", fontSize)
        value = "Lose"
        label = myfont.render(value, True, (0, 0, 0))
        DISP.blit(label, ( 0, self.numbOfBlocks * self.blockSize + 2*fontSize))
    def keyHandling(self, key):
        if not self.losed:
            self.newKeyValue = True
            if key == pg.K_UP:
                self.direction = "UP" 
                pass
            elif key == pg.K_LEFT:
                self.direction = "LEFT" 
                pass
            elif key == pg.K_RIGHT:
                self.direction = "RIGHT" 
                pass
            elif key == pg.K_DOWN:
                self.direction = "DOWN" 
                pass
            pass
    pass
    def appendValueBlock(self):
        allValues = {x for x in range(self.numbOfBlocks*self.numbOfBlocks)}
        existingValues = set()
        for block in self.valueBlockList:
            x = block.pos[0] //self.blockSize + block.pos[1] // self.blockSize * self.numbOfBlocks
            existingValues.add(x)
        possibleValues = tuple(allValues - existingValues)
        if possibleValues:
            newIndex = random.choice(possibleValues)
            value = random.choice((2,4)) 
            self.valueBlockList.append(ValueBlock(size= self.blockSize, fieldNumber=newIndex, value=value, numbOfBlocks=self.numbOfBlocks))
        else:
            pass
        pass
    def checkCollision(self, valueBlock):
        coolidated = False
        valueBlockRect = pg.Rect(valueBlock.pos[0], valueBlock.pos[1], self.blockSize, self.blockSize)
        for block in self.valueBlockList:
            if block is valueBlock:
                continue
            blockRect = pg.Rect(block.pos[0], block.pos[1], self.blockSize, self.blockSize)
            if blockRect.colliderect(valueBlockRect):
                coolidated = True
                if valueBlock.isSameValue(block):
                    self.toCombinBlock.add((valueBlock, block))
                break
        
        return coolidated

        pass
    def combine(self):
        def toSort(e):
            return (e[0].pos[0] //self.blockSize + e[0].pos[1] // self.blockSize) + (e[1].pos[0] //self.blockSize + e[1].pos[1] // self.blockSize)
        def moveNeighbours(block):
            direction = getOppositeDirection(self.direction)
            neighbour = block.getNeighbour(self.valueBlockList, direction, self.numbOfBlocks)
            if neighbour != None:
                moveNeighbours(neighbour)
                if self.direction == "UP":
                    neighbour.goUp()
                elif self.direction == "DOWN":
                    neighbour.goDown()
                elif self.direction == "LEFT":
                    neighbour.goLeft()
                elif self.direction == "RIGHT":
                    neighbour.goRight()
        
        minValueElements = min(self.toCombinBlock, key=lambda x: x[0].value)
        self.score += minValueElements[0].value + minValueElements[1].value # could be replaced by *2 because the two elements have equal values
        if self.direction == "UP":
            tmp = list(self.toCombinBlock)
            tmp.sort(key = toSort)
            for toCombine in tmp:
                if toCombine[0] in self.valueBlockList and toCombine[1] in self.valueBlockList:
                    if toCombine[0].pos[1] < toCombine[1].pos[1]:
                        toCombine[0].addTogether(toCombine[1])
                        moveNeighbours(toCombine[1])
                        self.valueBlockList.remove(toCombine[1])
                    else:
                        toCombine[1].addTogether(toCombine[0])
                        moveNeighbours(toCombine[0])
                        self.valueBlockList.remove(toCombine[0])
                pass
            pass
        elif self.direction == "DOWN":
            tmp = list(self.toCombinBlock)
            tmp.sort(key = toSort, reverse=True)
            for toCombine in tmp:
                if toCombine[0] in self.valueBlockList and toCombine[1] in self.valueBlockList:
                    if toCombine[0].pos[1] > toCombine[1].pos[1]:
                        toCombine[0].addTogether(toCombine[1])
                        moveNeighbours(toCombine[1])
                        self.valueBlockList.remove(toCombine[1])
                    else:
                        toCombine[1].addTogether(toCombine[0])
                        moveNeighbours(toCombine[0])
                        self.valueBlockList.remove(toCombine[0])
                pass
                pass
            pass
        elif self.direction == "LEFT":
            tmp = list(self.toCombinBlock)
            tmp.sort(key = toSort)
            for toCombine in tmp:
                if toCombine[0] in self.valueBlockList and toCombine[1] in self.valueBlockList:
                    if toCombine[0].pos[0] < toCombine[1].pos[0]:
                        toCombine[0].addTogether(toCombine[1])
                        moveNeighbours(toCombine[1])
                        self.valueBlockList.remove(toCombine[1])
                    else:
                        toCombine[1].addTogether(toCombine[0])
                        moveNeighbours(toCombine[0])
                        self.valueBlockList.remove(toCombine[0])
                pass
            pass         
        elif self.direction == "RIGHT":
            tmp = list(self.toCombinBlock)
            tmp.sort(key = toSort, reverse=True)
            for toCombine in tmp:
                if toCombine[0] in self.valueBlockList and toCombine[1] in self.valueBlockList:
                    if toCombine[0].pos[0] > toCombine[1].pos[0]:
                        toCombine[0].addTogether(toCombine[1])
                        moveNeighbours(toCombine[1])
                        self.valueBlockList.remove(toCombine[1])
                    else:
                        toCombine[1].addTogether(toCombine[0])
                        moveNeighbours(toCombine[0])
                        self.valueBlockList.remove(toCombine[0])
                    pass
            pass
        
        pass
    def updateBlocks(self):
        possibles = len(self.valueBlockList)*[False]
        if self.direction == "UP":
            i = 0
            for block in self.valueBlockList:
                if block.pos[1] > 0:
                    possibles[i] = True
                    block.goUp()
                    collision = self.checkCollision(block)
                    if collision:
                        possibles[i] = False
                        block.goDown()
                    i += 1
        elif self.direction == "DOWN":
            i = 0
            for block in self.valueBlockList:
                if block.pos[1] + self.blockSize < self.numbOfBlocks * self.blockSize:
                    possibles[i] = True
                    block.goDown()
                    collision = self.checkCollision(block)
                    if collision:
                        possibles[i] = False
                        block.goUp()

                    i += 1
        elif self.direction == "LEFT":
            i = 0
            for block in self.valueBlockList:
                if block.pos[0] > 0:
                    possibles[i] = True
                    block.goLeft() 
                    collision = self.checkCollision(block)
                    if collision:
                        possibles[i] = False
                        block.goRight()
                    i += 1
        elif self.direction == "RIGHT":
            i = 0
            for block in self.valueBlockList:
                if block.pos[0] + self.blockSize < self.windowSize[0]:
                    possibles[i] = True
                    block.goRight()
                    collision = self.checkCollision(block)
                    if collision:
                        possibles[i] = False
                        block.goLeft()
                    i += 1
        if not (True in possibles) and self.direction != None and not self.newKeyValue: #< last move is done so append a block. If first key press value is not possible do not add a another Block, this is done with variable self.newKeyValue
            self.appendValueBlock()
        if not (True in possibles): # no block cant move more
            if self.toCombinBlock:
                self.combine()
                self.toCombinBlock.clear()
            self.direction = None
            pass
        self.newKeyValue = False
        pass
    def isLose(self):
        ret = False
        if len(self.valueBlockList) == (self.numbOfBlocks ** 2) : # just need to check if all fields are occupied
            directionList = ["UP", "DOWN", "LEFT" , "RIGHT"]
            haveToBreak = False
            for valueBlock in self.valueBlockList:
                if haveToBreak: break
                for direction in directionList:
                    neighbour = valueBlock.getNeighbour(self.valueBlockList, direction, self.numbOfBlocks)
                    if neighbour != None:
                        if neighbour.value == valueBlock.value: # move possible
                            ret = False
                            haveToBreak = True
                            break 
            if not haveToBreak: ret = True
            pass
        return ret
class Block:
    pos : list
    size : int 
    def __init__(self, size : int, fieldNumber : int, numbOfBlocks : int):
        self.size = size
        self.pos = [(fieldNumber % numbOfBlocks) *self.size, (fieldNumber // numbOfBlocks) *self.size]
        pass

     
class EmptyBlock(Block):
    pos : list
    size : int
    def __init__(self, size : int, fieldNumber : int, numbOfBlocks : int):
        super().__init__(size, fieldNumber, numbOfBlocks)
        pass
    def draw(self, DISP):
        OFFSET = 6
        pg.draw.rect(DISP, color=(127,127,127), rect= pg.Rect(self.pos[0] + OFFSET//2, self.pos[1] + OFFSET // 2, self.size - OFFSET, self.size- OFFSET), border_radius=5)
    
class ValueBlock(Block):
    pos : list
    size : int
    value : int
    def __init__(self, size : int, fieldNumber : int, value : int, numbOfBlocks : int):
        super().__init__(size, fieldNumber, numbOfBlocks)
        self.value = value
        pass
    def draw(self, DISP):
        OFFSET = 6
        pg.draw.rect(DISP, color=(self.value % 256, int(math.sin(self.value)) * 255 , 255* abs(math.cos(self.value))), rect= pg.Rect(self.pos[0] + OFFSET//2, self.pos[1] + OFFSET // 2, self.size - OFFSET, self.size- OFFSET), border_radius=5)
        fontSize = int(self.size * (1/4))
        myfont = pg.font.SysFont("Comic Sans MS", fontSize)
        value = str(self.value)
        label = myfont.render(value, True, (255, 255, 255))
        DISP.blit(label, ((self.pos[0] + self.size//2 - label.get_width()//2 ) ,(self.pos[1] + self.size//2 - label.get_height()//2) ))
        pass
    def goUp(self):
        self.pos[1] -= self.size
        pass
    def goDown(self):
        self.pos[1] += self.size
        pass
    def goLeft(self):
        self.pos[0] -= self.size
        pass
    def goRight(self):
        self.pos[0] += self.size
        pass
    def addTogether(self, valueBLock):
        self.value += valueBLock.value
        pass
    def isSameValue(self, valueBLock):
        return self.value == valueBLock.value
    def getNeighbour(self, valueBlockList : list, direction : str, numbOfBlocks : int):
        posList = [(x.pos[0] // self.size) + (x.pos[1] // self.size)*numbOfBlocks for x in valueBlockList]
        pos = (self.pos[0] // self.size) + (self.pos[1] // self.size)*numbOfBlocks
        ret = None
        if direction == "UP": # checking if block is in a edge is not necessary, because values doesnt pos - numbOfBlocks doesnt exist twice
            tmp = pos - numbOfBlocks
            if tmp in posList:
                ret = valueBlockList[posList.index(tmp)]
        elif direction == "DOWN": # checking if block is in a edge is not necessary, because values doesnt pos + numbOfBlocks doesnt exist twice
            tmp = pos + numbOfBlocks
            if tmp in posList:
                ret = valueBlockList[posList.index(tmp)]
        elif direction == "LEFT":
            if pos % numbOfBlocks == 0: # check if block is in a edge
                ret = None
            else:
                tmp = pos - 1
                if tmp in posList:
                    ret = valueBlockList[posList.index(tmp)]
        elif direction == "RIGHT":
            if (pos + 1) % numbOfBlocks == 0: # check if block is in a edge
                ret = None # edge doesnt have a right neighbour
            else: # block is not in a edge
                tmp = pos + 1
                if tmp in posList:
                    ret = valueBlockList[posList.index(tmp)]
        return ret
def main():
    FPS_CLOCK = pg.time.Clock()
    FPS = 60
    numbOfBlocks = 4
    windowsize = (numbOfBlocks*100,numbOfBlocks*200)
    pg.font.init()
    DISP = pg.display.set_mode(windowsize)
    pg.display.set_caption("2048")
    game = Game(100, windowsize, numbOfBlocks)
    fps_counter = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit(0)
            elif event.type == pg.KEYDOWN:
                key = pg.key.get_pressed()
                if key[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit(0)
                elif key[pg.K_UP]:
                    game.keyHandling(pg.K_UP)
                elif key[pg.K_DOWN]:
                    game.keyHandling(pg.K_DOWN)
                elif key[pg.K_LEFT]:
                    game.keyHandling(pg.K_LEFT)
                elif key[pg.K_RIGHT]:
                    game.keyHandling(pg.K_RIGHT)
        FPS_CLOCK.tick(FPS)
        DISP.fill((255,255,255))
        if not game.losed and fps_counter % 3 == 0:
            game.updateBlocks()
        game.draw(DISP)
        pg.display.update()
        fps_counter = (fps_counter + 1) % (FPS + 1) 
        if not game.losed and game.isLose():
            game.losed = True
    pass


if __name__ == '__main__':
    main()