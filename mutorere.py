import numpy as np
import matplotlib.pyplot as plt
import collections

class gameManager :

    # Initialisation
    def __init__(self):
        self.board = ["black","black","black","black","white","white","white","white","empty"]
        self.round = "black"
        self.possibleActions = [0,1,2,3,4,5,6,7,8]
        self.terminated = False

    # Faire un déplacement en parcourant les actions possibles, puis changer de joueur.
    # Attribution des récompenses
    def step(self, action):
        # Récompense négative si l'action passée en paramètre n'est pas possible
        reward = -10
        #test si l'action est possible
        self.possibleAction()
        for i in self.possibleActions:
            if(i==action):
                reward = -1
                # si action possible, on inverse la position du pion selectionné et du vide
                empty = self.board.index("empty")
                self.board[action]="empty"
                self.board[empty] = self.round
                if(self.round == "black"):
                    self.round = "white"
                else :
                    self.round = "black"

        # Mise à jour des actions possibles et détermination si la partie est finie ou non
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

    # Fonction énumérant les actions possibles en fonction de la case vide
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

    # choisis une action au hasard parmi celles possibles
    def actionSpaceSample(self):
        #self.possibleAction()
        possibleActions = [0,1,2,3,4,5,6,7,8]

        return np.random.choice(possibleActions)

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

# Retourne l'action qui a le plus de valeur en fonction de l'état dans lequel on se situe, à partir de la table Q
def maxAction(Q, state, actions):

    values = np.array([Q[state,a] for a in actions])

    action = np.argmax(values)

    return actions[action]

# Jouer la partie aléatoirement
def playGameRandomly():
    i = 0
    while gameManager.terminated == False:
        i = i + 1
        gameManager.step(gameManager.actionSpaceSample())
        gameManager.render()
    print('round n : '+str(i))
    print('looser : ' + gameManager.round)


# Fonction principale : Simulation du jeu du mutorere opposant 1 joueur effectuant des actions aléatoires et 1 joueur intelligent
def playQLearningBlack(n):
    iterationBeforeWin, evolutionWinrate, epsList = [], [], []
    whiteC, blackC = 0, 0
    winrateQ = collections.deque(maxlen=1000)


    # Création de la table de Q learning
    Q = {}
    possibleActions = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    from more_itertools import distinct_permutations

    # Initialisation de toutes les actions possible dans la Q table
    for p in distinct_permutations('111122223'):
        for action in possibleActions :
            Q[''.join(p), action] = 0


    # Hyperparamètres
    ALPHA = 0.15 # Learning Rate
    GAMMA = 0.80 # discount factor
    EPS = 1 # Epsilon

    # On joue le nombre de game passé en paramètre de la fonction
    for gameNumber in range(n):
        print('game :',gameNumber)
        print('EPS :',EPS)
        print('####')
        

        gameManager.__init__()
        observation = gameManager.board
        observationInt = ''

        # Changement de format de la situation du board en une chaîne de caractères pour pouvoir la passer en paramètres de la fonction maxAction
        for i in observation:
            if i == "black":
                observationInt = str(observationInt)+str(1)
            if i == "white":
                observationInt = str(observationInt) + str(2)
            if i == "empty":
                observationInt = str(observationInt)+str(3)

        iteration = 0


        while gameManager.terminated == False :
            iteration = iteration +1
            
            # Tour du joueur noir (intelligent)
            while gameManager.round == "black" :
                #play with Q learning
                rand = np.random.random()
                # Détermination de l'action en fonction d'epsilon
                action = maxAction(Q, observationInt, possibleActions) if rand < (1 - EPS) else gameManager.actionSpaceSample()

                # Récupération de l'état du board après avoir effectué l'action
                observation_, reward, done, info = gameManager.step(action)
                # Etat futur du board par rapport à l'action passée
                observation_Int = ''
                for i in observation:
                    if i == "black":
                        observation_Int = str(observation_Int) + str(1)
                    if i == "white":
                        observation_Int = str(observation_Int) + str(2)
                    if i == "empty":
                        observation_Int = str(observation_Int) + str(3)


                
            # Tour du joueur blanc (aléatoire)
            while gameManager.round == "white" and gameManager.terminated == False:

                observation_, reward1, done, info = gameManager.step(gameManager.actionSpaceSample())

                # Etat futur du board par rapport à l'action passée
                observation_Int = ''
                for i in observation_:
                    if i == "black":
                        observation_Int = str(observation_Int) + str(1)
                    if i == "white":
                        observation_Int = str(observation_Int) + str(2)
                    if i == "empty":
                        observation_Int = str(observation_Int) + str(3)

                # affectation d'une reward négative si victoire du blanc
                if(reward1 == 1000) :
                    reward = -1000


            action_ = maxAction(Q, observation_Int,possibleActions)
            # Equation de Bellman
            Q[observationInt, action] = Q[observationInt, action] + ALPHA * (reward + GAMMA * Q[observation_Int, action_] - Q[observationInt, action])
            observationInt = observation_Int

        # Création des graphes de représentation des résultats

        # Graphe de représentation du nombre d'itérations avant une victoire (pour les 2 joueurs)
        if gameManager.round == "black":
            iteration = -iteration 
        iterationBeforeWin.append(iteration)

        # Graphe du taux de victoire du joueur intelligent (black)
        if gameNumber > n/1.3 :
            EPS = 0
            if gameManager.round == "white" :
                blackC = blackC + 1
            else :
                whiteC = whiteC + 1

        else :
            EPS = 1 - gameNumber/(n/1.3)


        if gameManager.round == "white" :
                winrateQ.append(1)

        else :
                winrateQ.append(0)

        if gameNumber> 9 :
            evolutionWinrate.append(np.mean(winrateQ))
            epsList.append(EPS)





    print('white win :', whiteC, 'black win :', blackC, '%for black :',blackC/(whiteC+blackC))

    plt.figure(1,figsize=(13,6))

    plt.gcf().subplots_adjust(left = 0.1, bottom = 0.2, right = 0.98)
    plt.subplot(1,2,1)
    plt.bar(range(n), iterationBeforeWin, label="number of iterations before victory")
    plt.title("Comparison of the number of moves played \n before a victory between black (positive values) and white (negative values)")
    plt.xlabel("number of games")
    plt.ylabel("number of moves played before victory")

    plt.subplot(1,2,2)
    plt.plot(range(n-10), evolutionWinrate,label="black winrate on last 1000 games")
    plt.plot(range(n-10), epsList, label = "epsilon")
    plt.title("Evolution of winrate and epsilon \n according to the number of games")
    plt.legend(loc="lower left")
    plt.xlabel("number of games")


    plt.show()



if __name__ == "__main__":

    gameManager = gameManager()
    # playGameRandomly()
    playQLearningBlack(5000)
