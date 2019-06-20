import random
from collections import deque
from BaseAI_3 import BaseAI
import Displayer_3
from sys import exit

class PlayerAI(BaseAI):
    def getMove(self, grid):
        dirAr = ["Up","Down","Left","Right"]
        
        # Selects a random move and returns it
        moveset = grid.getAvailableMoves()
        print(moveset)
        
    
        '''
        self.ourGridDisplay(grid)
        currScore = self.gridWeight(grid)
        
        print("Current score: ", currScore)
        
        print("---------------------------------------")
        print("---------------------------------------")
        score,direction = self.minimax(grid, 2)
        
        
        self.ourGridDisplay(moveset[direction][1])
        
        print("Next Score: ", score)
        print("Direction: ", dirAr[direction])
        
        exit()
        '''
        score,direction = self.minimax(grid, 2)
        print("Next Score: ", score)
        print("Direction: ", dirAr[direction])
        
        chosenMove = direction
        
        return chosenMove if moveset else None

        
    def gridWeight(self, grid):
        weightedGrid = [[6,5,4,3],
                        [5,4,3,2],
                        [4,3,2,1],
                        [3,2,1,0]]
        

        
        totalWeight = 0
        for row,rowVal in enumerate(weightedGrid):
            for col,value in enumerate(weightedGrid[row]):
                
                totalWeight = grid.getCellValue((row,col)) * weightedGrid[row][col] + totalWeight
                
        return self.squarePenalty(grid, totalWeight)
                
                
    def squarePenalty(self, grid, totalWeight):
        numFilledSquares = 16 - len(grid.getAvailableCells())
        totalWeight = totalWeight / (numFilledSquares*numFilledSquares)
        return totalWeight
    
    def minimax(self,grid,maxDepth):
        score, direction = self.maxValue(grid,maxDepth)
        return score,direction
    
    def maxValue(self, grid, maxDepth):
        moveset = grid.getAvailableMoves()
        maxScore = float("-inf")
    
        if maxDepth == 0 or len(moveset) == 0:
            return self.gridWeight(grid), None
        
        maxDirection = None
        
        for moveTup in moveset:
            direction = moveTup[0]
            nextGrid = moveTup[1]
            #print("moveTup: ",moveTup)
            score, _ = self.minValue(nextGrid, maxDepth - 1)
    
            if score > maxScore:
                maxScore = score
                maxDirection = direction
        return maxScore, maxDirection
    
    def minValue(self, grid, maxDepth):
        moveset = grid.getAvailableMoves()
        minScore = float("inf")
        
        
        if maxDepth == 0 or len(moveset) == 0:
            return self.gridWeight(grid), None
        
        minDirection = None

        
        for moveTup in moveset:
            direction = moveTup[0]
            nextGrid = moveTup[1]
            
            score, _ = self.maxValue(nextGrid, maxDepth - 1)
            if score < minScore:
                minScore = score
                minDirection = direction 
        return minScore, minDirection
    
    
    
    def ourGridDisplay(self, grid):
        cTemp = "\x1b[%dm%7s\x1b[0m "
        colorMap = Displayer_3.colorMap
        for i in range(3 * grid.size):
            for j in range(grid.size):
                v = grid.map[int(i / 3)][j]

                if i % 3 == 1:
                    string = str(v).center(7, " ")
                else:
                    string = " "

                print(cTemp %  (colorMap[v], string), end="")
            print("")

            if i % 3 == 2:
                print("")
    
