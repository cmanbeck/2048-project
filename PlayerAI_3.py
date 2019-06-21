import random
from collections import deque
from BaseAI_3 import BaseAI
import Displayer_3
from sys import exit
import random


class PlayerAI(BaseAI):
    def getMove(self, grid):
        dirAr = ["Up","Down","Left","Right"]
        
        # Selects a random move and returns it
        moveset = grid.getAvailableMoves()
        print('moveset:', moveset)
        
        alpha = float("-inf")
        beta = float("inf")
        
        score,direction = self.minimax(grid,alpha,beta, 3)
        print("Next Score: ", score)
        print("Direction: ", dirAr[direction])
        
        chosenMove = direction
        
        return chosenMove if moveset else None

        
    def gridWeight(self, grid):
        '''
        weightedGrid = [[6,5,4,3],
                        [5,4,3,2],
                        [4,3,2,1],
                        [3,2,1,0]]
        '''
        
        weightedGrid = [[16,15,14,13],
                        [9,10,11,12],
                        [8,7,6,5],
                        [1,2,3,4]]

        
        totalWeight = 0
        for row,rowVal in enumerate(weightedGrid):
            for col,value in enumerate(weightedGrid[row]):
                
                totalWeight = grid.getCellValue((row,col)) * weightedGrid[row][col] + totalWeight
                
        return self.squarePenalty(grid, totalWeight)
                
                
    def squarePenalty(self, grid, totalWeight):
        numFilledSquares = 16 - len(grid.getAvailableCells())
        #totalWeight = totalWeight / (numFilledSquares)
        return totalWeight
    
    def minimax(self,grid,alpha,beta,maxDepth):
        score, direction = self.maxValue(grid, alpha, beta, maxDepth)
        return score,direction
    
    def maxValue(self, grid, alpha, beta, maxDepth):
        moveset = grid.getAvailableMoves()
        maxScore = float("-inf")
    
        if maxDepth == 0 or len(moveset) == 0:
            return self.gridWeight(grid), None
        
        maxDirection = None
        
        for moveTup in moveset:
            direction = moveTup[0]
            nextGrid = moveTup[1]
            #print("moveTup: ",moveTup)
            score, _ = self.minValue(nextGrid, alpha, beta, maxDepth - 1)
    
            if score > maxScore:
                maxScore = score
                maxDirection = direction
            if score >= beta:
                return maxScore, maxDirection
            alpha = max(alpha, score)
        return maxScore, maxDirection
    
    def minValue(self, grid, alpha, beta, maxDepth):
        posset = grid.getAvailableCells()
        minScore = float("inf")
        
        
        if maxDepth == 0 or len(posset) == 0:
            return self.gridWeight(grid), None
        
        minDirection = None 
        
        minScore = float("inf")
        #minPos = None
        
        probTwo = 0.9
        probFour = 0.1
        
        for pos in posset:
            row,col = pos
            
            tmpGrid = grid.clone()
            
            tmpGrid.setCellValue((row,col),2)
            
            score, _ = self.maxValue(tmpGrid, alpha, beta, maxDepth - 1)
            
            score = score*probTwo
            
            if score < minScore:
                minScore = score
                #minPos = pos
                
            if score <= alpha:
                return minScore, minDirection
            beta = min(beta, score)
                
            
        for pos in posset:
            row,col = pos
            
            tmpGrid = grid.clone()
            tmpGrid.setCellValue((row,col),4)
            
            score, _ = self.maxValue(tmpGrid, alpha, beta, maxDepth - 1)
            
            score = score*probFour
            
            if score < minScore:
                minScore = score
                #minPos = pos
                
            if score <= alpha:
                return minScore, minDirection
            
            beta = min(beta, score)
            
        return minScore, None
            
    
    
    
    
    def oldMinValue(self, grid, alpha, beta, maxDepth):
        moveset = grid.getAvailableMoves()
        minScore = float("inf")
        
        
        if maxDepth == 0 or len(moveset) == 0:
            return self.gridWeight(grid), None
        
        minDirection = None

        
        for moveTup in moveset:
            direction = moveTup[0]
            nextGrid = moveTup[1]
            
            score, _ = self.maxValue(nextGrid, alpha, beta, maxDepth - 1)
            
            randVal = random.uniform(0, 1)
            
            if score < minScore:
                minScore = score
                minDirection = direction 
            if score <= alpha:
                return minScore, minDirection
            beta = min(beta, score)
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
    
