class Node() :
    def __init__(self, name, duration, previousNodes, ES = 0, EF = 0, LS = 0, LF = 0, done = False, TF = 0, TD = 0):
        self._name = name
        self._duration = duration
        self._previousNodes = previousNodes
        self._ES = ES
        self._EF = EF
        self._LS = LS
        self._LF = LF
        self._done = done        
        self._TF = TF
        self._TD = TD

graphToTest = [
    Node("A", 10, []),
    Node("B", 20, ["A"]),
    Node("C", 5, ["B"]),
    Node("D", 10, ["C"]),
    Node("E", 20, ["H", "G", "D"]),
    Node("F", 15, ["A"]),
    Node("G", 5, ["F", "C"]),
    Node("H", 15, ["A"])
    ]

class Calculations() :
    def __init__(self, myGraph, firstNode, lastNode):
        self._myGraph = myGraph
        self._firstNode = firstNode
        self._lastNode = lastNode
        self._theCriticalPath = []
    
     
    def findEarlyStartAndFinish(self) :
        node = self._firstNode
        #Calculation firstNode
        for i in range(0, len(self._myGraph)) :
            if self._myGraph[i]._name == node :
                currentNode = self._myGraph[i]
                currentNode._ES = 1
                currentNode._EF = currentNode._ES + currentNode._duration - 1
                currentNode._done = True
        #Calculation nodes with first node as predecessor
        for i in range(0, len(self._myGraph)) :      
            myPredecessors = self._myGraph[i]._previousNodes
            if node in myPredecessors :
                self._myGraph[i]._ES = currentNode._EF + 1
                self._myGraph[i]._EF = self._myGraph[i]._ES +  self._myGraph[i]._duration - 1
                self._myGraph[i]._done = True
                print("Forward walk: ", self._myGraph[i]._name, self._myGraph[i]._duration, self._myGraph[i]._ES , self._myGraph[i]._EF )
        #Calculation rest of the nodes
        for i in range(0, len(self._myGraph)) :  
            node = self._myGraph[i]._name          
            for j in range(0, len(self._myGraph)) :
                myPredecessors = self._myGraph[j]._previousNodes
                if node in myPredecessors :
                    # where there are multiple predecessor take the highest value of the predecessor earlier start(ES)
                    if self._myGraph[j]._ES  < self._myGraph[i]._EF :
                        self._myGraph[j]._ES = self._myGraph[i]._EF + 1
                        self._myGraph[j]._EF = self._myGraph[j]._ES +  self._myGraph[j]._duration - 1
                        self._myGraph[j]._done = True
                        print("Forward walk: ", self._myGraph[j]._name, self._myGraph[j]._duration, self._myGraph[j]._ES , self._myGraph[j]._EF ) 
        #Resetting done values so I can calculate the late start and finish after early start and finish is done
        for i in range(0, len(self._myGraph)) :
            self._myGraph[i]._done = False
       
            


    def findLateStartAndFinish(self) :
        node = self._lastNode
        #Calculation lastNode
        for i in range(0, len(self._myGraph)) :
            if self._myGraph[i]._name == node :
                self._myGraph[i]._LF = self._myGraph[i]._EF
                self._myGraph[i]._LS = self._myGraph[i]._LF - self._myGraph[i]._duration + 1
                self._myGraph[i]._done = True
                print("Backwards walk: ", self._myGraph[i]._name, self._myGraph[i]._duration, self._myGraph[i]._ES , self._myGraph[i]._EF,  self._myGraph[i]._LS, self._myGraph[i]._LF)
        #Calculation predecessor of last node(H,G,D) 
        for i in range(0, len(self._myGraph)) : 
            if self._myGraph[i]._name == node :
                for j in range(0, len(self._myGraph)) :
                    if self._myGraph[j]._name in self._myGraph[i]._previousNodes :
                        self._myGraph[j]._LF = self._myGraph[i]._LS - 1
                        self._myGraph[j]._LS = self._myGraph[j]._LF -  self._myGraph[j]._duration + 1
                        self._myGraph[j]._done = True
                        print("Backwards walk walk: ", self._myGraph[j]._name, self._myGraph[j]._duration, self._myGraph[j]._ES , self._myGraph[j]._EF,  self._myGraph[j]._LS, self._myGraph[j]._LF)
        #Calculation rest of the nodes not done only
        for x in range(0, len(self._myGraph)) :  
            if not self._myGraph[x]._done :
                for i in range(0, len(self._myGraph)) :
                    myPredecessors = self._myGraph[i]._previousNodes
                    if self._myGraph[i]._done : 
                        for j in range(1, len(self._myGraph)) :                   
                             if self._myGraph[j]._name in myPredecessors and not self._myGraph[j]._done:
                                    self._myGraph[j]._LF = self._myGraph[i]._LS - 1
                                    self._myGraph[j]._LS = self._myGraph[j]._LF -  self._myGraph[j]._duration + 1
                                    self._myGraph[j]._done = True
                                    print("Backwards walk: ", self._myGraph[j]._name, self._myGraph[j]._duration, self._myGraph[j]._ES , self._myGraph[j]._EF,  self._myGraph[j]._LS, self._myGraph[j]._LF)    
        #Calculation firstNode   
        for i in range(0, len(self._myGraph)) :
            if self._myGraph[i]._done :                
                for j in range(0, 1, len(self._myGraph)) : # we are looking only at the first node
                        if self._myGraph[j]._name in self._myGraph[i]._previousNodes :
                            # conditions to make sure we get the the smallest latest finish from the predecssors
                            if self._myGraph[j]._LF == 0 :
                                self._myGraph[j]._LF = self._myGraph[i]._LS - 1
                                self._myGraph[j]._LS = self._myGraph[j]._LF -  self._myGraph[j]._duration + 1
                                self._myGraph[j]._done = True   
                            elif self._myGraph[i]._LS < self._myGraph[j]._LF :
                                self._myGraph[j]._LF = self._myGraph[i]._LS - 1
                                self._myGraph[j]._LS = self._myGraph[j]._LF -  self._myGraph[j]._duration + 1

    def findFloat(self):
         for i in range(0, len(self._myGraph)) :
             self._myGraph[i]._TF = self._myGraph[i]._LS - self._myGraph[i]._ES

    def findDrag(self):
         firstNode = self._firstNode
         lastNode = self._lastNode
         # this method is not complete, here we only calculated the fisrt node drag and the last node
         for i in range(0, len(self._myGraph)) :
            myPredecessors = self._myGraph[i]._previousNodes
            if self._myGraph[i]._name == firstNode or self._myGraph[i]._name == lastNode :
                self._myGraph[i]._TD = self._myGraph[i]._duration     



    def findCriticalPath(self) :
        currentNode = self._lastNode
        for i in range(0, len(self._myGraph)) :
            if self._myGraph[i]._EF == self._myGraph[i]._LF :
                self._theCriticalPath.append(self._myGraph[i])       

        


    def printGraphToTest(self) :
        print("Name     Duration     ES     EF     LS     LF     Float     Drag     Predecessors")
        print("---------------------------------------------------------------------------------")
        for x in range(0, len(self._myGraph)) :
            current = self._myGraph[x]
            print("{} {:12} {:9} {:6} {:6} {:6} {:6} {:10} {:8} {}".format(current._name, current._duration, current._ES,  current._EF,  current._LS,  current._LF, current._TF, current._TD, str("    "), (str(current._previousNodes))))
        print()   
        print() 
        # check critical path is found and print to test
        criticalPathDuration = 0
        print("Crtical path was found: ", end=" ")
        for x in range(0, len(self._theCriticalPath)) :
            print(self._theCriticalPath[x]._name, end=" ")
            criticalPathDuration += self._theCriticalPath[x]._duration        
        print()   
        print("Critical path duration: ", criticalPathDuration)   
        print()
          


run = Calculations(graphToTest, "A", "E")
run.findEarlyStartAndFinish()
print()
run.findLateStartAndFinish()
print()
run.findCriticalPath()
print()
run.findFloat()
print()
run.findDrag()
print()
run.printGraphToTest()