import numpy as np
import matplotlib.pyplot as plt

class gameManager :


    def __init__(self):
        self.board = ["black","black","black","black","white","white","white","white","empty"]
        #self.board = ["black","black","empty","black","white","white","white","white","black"]
        self.round = "black"
        self.possibleActions = [0,1,2,3,4,5,6,7,8]
        self.terminated = False

    def step(self, action):
        reward = -10
        #test si l'action est possible
        self.possibleAction()
        for i in self.possibleActions:
            if(i==action):
                reward = 0
                # si action possible, on inverse la position du pion selectioné et du vide
                empty = self.board.index("empty")
                self.board[action]="empty"
                self.board[empty] = self.round
                if(self.round == "black"):
                    self.round = "white"
                else :
                    self.round = "black"

        #test if terminated
        self.possibleAction()
        if (self.possibleActions) == []:
            self.terminated = True
            reward = 1000

        #return state,reward,done,info
        return self.board,reward,self.terminated,None





    def getPositionPayer(self,player):
        position=[]

        for i in self.board :
            if(i==player):
                position.append(1)
            else :
                position.append(0)
        return position

    def removeCircledPawn(self,listE):
        notCicledList=[]
        index = 0
        #créer la liste = 8123456781
        listEcircle=listE.copy()
        listEcircle.insert(0,listE[7])
        listEcircle[9]=listEcircle[1]
        for i in listE[:8] :
            if(i==1):
                if(listEcircle[index]==1 and listEcircle[index+2]==1):
                    notCicledList.append(0)
                else : notCicledList.append(1)
            else : notCicledList.append(0)
            index = index +1
        return notCicledList


    def transformPossibleAction(self,list):
        possibleAction = []
        i = 0
        for elem in list :
            if (elem == 1):
                possibleAction.append(i)
            i = i +1



        self.possibleActions = possibleAction

    def possibleAction(self):
        #millieu dispo
        if(self.board[8]=="empty"):
            self.transformPossibleAction(self.removeCircledPawn(self.getPositionPayer(self.round)))
        else :
            possibleAction = [0,0,0,0,0,0,0,0,0]
            if(self.board[0]=="empty"):
                if (self.board[1] == self.round):
                    possibleAction[1]=1
                if (self.board[7] == self.round):
                    possibleAction[7]=1
                if (self.board[8] == self.round):
                    possibleAction[8]=1

            elif(self.board[7]=="empty"):
                if (self.board[0] == self.round):
                    possibleAction[0]=1
                if (self.board[6] == self.round):
                    possibleAction[6]=1
                if (self.board[8] == self.round):
                    possibleAction[8] = 1
            else :
                index = self.board.index("empty")
                if (self.board[index-1] == self.round):
                    possibleAction[index-1]=1
                if (self.board[index+1] == self.round):
                    possibleAction[index+1]=1
                if (self.board[8] == self.round):
                    possibleAction[8] = 1
            self.transformPossibleAction(possibleAction)

    def actionSpaceSample(self):
        #choisit une action au hasard parmi celles possibles
        self.possibleAction()
        if (self.possibleActions)==[]:
            self.terminated = True
            return
        return np.random.choice(self.possibleActions)

    def render(self):
        print('------------------------------------------')
        print(gameManager.board)
        print('tour : '+self.round)
        print('------------------------------------------')
        print('            '+self.board[2])
        print('      ' + self.board[1] + '        ' +  self.board[3])
        print(''+ self.board[0]+'       '+self.board[8]+'       '+self.board[4])
        print('      ' + self.board[7] + '        ' + self.board[5])
        print('            ' + self.board[6])
        print('------------------------------------------')

def maxAction(Q, state, actions):

    values = np.array([Q[state,a] for a in actions])

    action = np.argmax(values)

    return actions[action]


def playGameRandomly():
    i = 0
    while gameManager.terminated == False:
        i = i + 1
        gameManager.step(gameManager.actionSpaceSample())
        gameManager.render()
    print('round n : '+str(i))
    print('looser : ' + gameManager.round)


def playQLearningBlack(n):
    whiteC, blackC = 0, 0
    state_size = 86
    action_size = 9


    #create Q learning table
    Q = {}
    possibleActions = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    from more_itertools import distinct_permutations

    for p in distinct_permutations('111122223'):
        for action in possibleActions :
            Q[''.join(p), action] = 0

    print(Q)




    # model hyperparameters
    ALPHA = 0.15 #Learning Rate
    GAMMA = 0.80 #discount factor

    EPS = 1

    for gameNumber in range(n):
        print(EPS)
        print('game :',gameNumber)

        gameManager.__init__()
        observation = gameManager.board
        observationInt = ''
        a=0
        for i in observation:
            if i == "black":
                observationInt = str(observationInt)+str(1)
            if i == "white":
                observationInt = str(observationInt) + str(2)
            if i == "empty":
                observationInt = str(observationInt)+str(3)
            a = a+1
        iteration = 0


        while gameManager.terminated == False :
            iteration = iteration +1
            rand = np.random.random()

            if gameManager.round == "black" :
                #play with Q learning
                action = maxAction(Q, observationInt, possibleActions) if rand < (1 - EPS) else gameManager.actionSpaceSample()

                observation_, reward, done, info = gameManager.step(action)
                observation_Int = ''
                a = 0
                for i in observation:
                    if i == "black":
                        observation_Int = str(observation_Int) + str(1)
                    if i == "white":
                        observation_Int = str(observation_Int) + str(2)
                    if i == "empty":
                        observation_Int = str(observation_Int) + str(3)
                    a = a + 1

                action_ = maxAction(Q, observation_Int,possibleActions)






                Q[observationInt, action] = Q[observationInt, action] + ALPHA * (reward + GAMMA * Q[observation_Int, action_] - Q[observationInt, action])
                observationInt = observation_Int

            if gameManager.round == "white":
                #play randomly
                gameManager.step(gameManager.actionSpaceSample())

        #print('looser : ' + gameManager.round)
        #print('in ',iteration,' round')

       # EPS = 1 / (gameNumber+1)
       # print(EPS)

        if gameNumber > 3000 :
            EPS = 0.5

        if gameNumber > 5000:
            EPS = 0.3

        if gameNumber > 7000:
            EPS = 0.2

        if gameNumber > 9000 :
            EPS = 0
            if gameManager.round == "white" :
                blackC = blackC + 1
            else :
                whiteC = whiteC + 1


    print('white win :', whiteC, 'black win :', blackC, '%for black :',blackC/(whiteC+blackC))
    #print(Q)


if __name__ == "__main__":

    gameManager = gameManager()

    #playGameRandomly()
    playQLearningBlack(10000)






