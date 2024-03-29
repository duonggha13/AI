# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        
        distance = -10000
        foodList = currentGameState.getFood().asList()

        if action == Directions.STOP:
            return -10000
        
        for ghostState in newGhostStates:
            if (ghostState.getPosition() == newPos) and (ghostState.scaredTimer == 0):
                return -10000
        
        for food in foodList:
            if distance < -(manhattanDistance(food, newPos)):
                distance = -manhattanDistance(food, newPos)

        return distance
        """ return successorGameState.getScore() """

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        def minvalue(state, depth, agentindex):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            else:
                value = float('inf')
                for action in state.getLegalActions(agentindex):
                    if agentindex == gameState.getNumAgents() - 1:
                        value = min(value, maxvalue(state.generateSuccessor(agentindex, action), depth + 1))
                    else:
                        value = min(value, minvalue(state.generateSuccessor(agentindex, action), depth, agentindex + 1))
                return value

        def maxvalue(state, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            else:
                value = - float('inf')
                for action in state.getLegalActions(0):
                    value = max(value, minvalue(state.generateSuccessor(0, action), depth, 1))
                return value
        value = - float('inf')
        bestAction = Directions.STOP
        for action in gameState.getLegalActions(0):
            nextValue = minvalue(gameState.generateSuccessor(0, action),0, 1)
            if nextValue > value:
                value = nextValue
                bestAction = action
        return bestAction
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxvalue(state, alpha, beta, depth):
          if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
          else:
            value = - float('inf')
            for action in state.getLegalActions(0):
              value = max(value, minvalue(state.generateSuccessor(0, action), alpha, beta, 1, depth))
              if value > beta:
                return value
              alpha = max(alpha, value)
            return value

        def minvalue(state, alpha, beta, agentindex, depth):
          if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
          else:
            value = float('inf')
            for action in state.getLegalActions(agentindex):
              if agentindex == state.getNumAgents() - 1:
                value = min(value, maxvalue(state.generateSuccessor(agentindex, action), alpha, beta, depth + 1))
              else:
                value = min(value, minvalue(state.generateSuccessor(agentindex, action), alpha, beta,agentindex + 1, depth))
              if value < alpha:
                return value
              beta = min(beta, value)
            return value

        value = - float('inf')
        alpha = - float('inf')
        beta = float('inf')
        bestAction = Directions.STOP
        for action in gameState.getLegalActions(0):
          nextValue = minvalue(gameState.generateSuccessor(0, action), alpha, beta, 1, 0)
          if nextValue > value:
            value = nextValue
            bestAction = action
          alpha = max(alpha, value)
        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def exvalue(state, depth, agentindex):
          if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
          else:
            value = 0
            for action in state.getLegalActions(agentindex):
              if agentindex == state.getNumAgents() - 1:
                value += maxvalue(state.generateSuccessor(agentindex, action), depth + 1)
              else:
                value += exvalue(state.generateSuccessor(agentindex, action), depth, agentindex + 1)
            return value

        def maxvalue(state, depth):
          if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
          else:
            value = - float('inf')
            for action in state.getLegalActions(0):
              value = max(value, exvalue(state.generateSuccessor(0, action), depth, 1))
            return value

        maxValue = - float('inf')
        bestAction = None

        for action in gameState.getLegalActions(0):
          nextValue = exvalue(gameState.generateSuccessor(0, action), 0, 1)
          if nextValue > maxValue:
            maxValue = nextValue
            bestAction = action
        return bestAction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    foodPos = currentGameState.getFood().asList() 
    foodDist = 0
    ghostDist = 0
    ghostStates = currentGameState.getGhostStates()
    currentPos = list(currentGameState.getPacmanPosition()) 

    for ghost in ghostStates:
      if ghost.scaredTimer == 0:
        ghostDist = max(ghostDist, manhattanDistance(ghost.getPosition(), currentPos))
 
    for food in foodPos:
        foodDist = max(foodDist, manhattanDistance(food, currentPos))

    return foodDist - 5*ghostDist + currentGameState.getScore()

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

