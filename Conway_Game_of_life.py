################################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~                                                                            ~#
#~  This is the conway game of life. It simulates the game using correlation  ~#
#~  matrix.                                                                   ~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
################################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~ Project : Conway Game of Life                                              ~#
#~ Creator : Anurag Dhungel                                                   ~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
################################################################################

################################################################################
################################################################################
##                          User Manuel                                       ##
##____________________________________________________________________________##
## pass the row and column of the inital board and an arbiriary number to     ##
## to create a class                                                          ##
## game=conway_game_of_life(row,col,some_number( default=1))                  ##
## Then , pass the timer between each evolution                               ##
## game.play_game(time between evolution)                                     ##
################################################################################
################################################################################

################################################################################
#importing necessary documents

import time # Time is needed for sleep function
import numpy as np # general calculation lirary
import matplotlib.pyplot as plt # for plotting
import matplotlib.animation as animation# for plotting
################################################################################

# Creating a class for the game of life
class conway_game_of_life:
  ##############################################################################
  ## class varialbes                                                          ##
  ## _________________________________________________________________________##
  ## self.n                   : Board column                                  ##
  ## self.m                   : Board row                                     ##                               
  ## self.fig                 : state figure                                  ##
  ## self.state               : present state of board                        ##
  ## self.play                : logical varialbe to continue game             ##
  ## self.eigen_value         : random number that is base of                 ##
  ##                             correlation_matrix                           ##
  ## self.correlation_matrix  : The correaltion matrix that provides          ##
  ##                             scores for next state caclulations           ##
  ## self.eigen_solution      : Solutions of correlation_matrix               ##
  ##                             that decides the fate of the cell            ##
  ##############################################################################
  ## class methods                                                            ##
  ## _________________________________________________________________________##
  ## correlation_matrix_creator() : Creates the correaltion matrix based on   ##
  ##                                 self.eigen_value                         ##
  ## create_board()               : Creates the initial board                 ##
  ##                                 i.e initial state                        ## 
  ## correlation_slice(slice)     : provides the correaltion value to certain ##
  ##                              : cell looking at its neighbout             ##
  ## conway_next_state()          : Decides the fate of cell and calculates   ##
  ##                                next state                                ##
  ## play_game(sellp_time)        : plays the game                            ##
  ##############################################################################

  ##############################################################################
  # class initializer

  # inputs 

  # board_size_x    = integer representing the total rows of the board
  # board_size_y    = integer representing the total cols of the board
  # matrix_constant = any real number (but integer is better)
  def __init__(self,board_size_x,board_size_y,matrix_constant=1):

    self.m=board_size_x#rows
    self.n=board_size_y#columns
    self.fig=plt.figure()#figure

    self.state=self.create_board()#creating board and this is the initial state
    self.play=True# for play_game module

    self.eigen_value=matrix_constant# the constant that defines 
                                    # correlation matrix and the solution to it

    self.correlation_matrix_creator() # creating correlating matrix 
                                      # and its solution
  ##############################################################################
  # correlation matrix creator
  def correlation_matrix_creator(self):

    # initializing the 3*3 matrix 
    # assigning the weights to neighbours
    self.correlation_matrix=np.zeros((3,3),dtype='uint8')+self.eigen_value

    # correcting the weights for self i.e. (7* weights of neighbout)
    # 1. y= 7*x =8*x -x = x<<3 -x
    self.correlation_matrix[1,1]=(self.eigen_value<<3)-self.eigen_value
    
    # assigning the solution of the correlation matrix
    # 1. x*3  = x*2+x = x<<1+x
    # 2. x*9  = x*8+x = x<<3+x 
    # 2. x*10 = x*8+x*2 = x<<3+x<<1
    self.eigen_solution=np.array([(self.eigen_value<<1)+self.eigen_value ,\
                                  (self.eigen_value<<3)+self.eigen_value,\
                                  (self.eigen_value<<3)+(self.eigen_value<<1)\
                                  ],dtype='int8')
  ##############################################################################
  # module that returns the initial state or the board
  def create_board(self):
    return np.random.randint(0, 2, size=(self.m,self.n), dtype='uint8')
  ##############################################################################
  # correlated the passed slice with the correlation_matrix
  def correlation_slice(self,slice):
    return np.sum(np.multiply(slice,self.correlation_matrix))
  ##############################################################################
  # module that calculates the next state
  def conway_next_state(self):

    # adding padding of 0 allround the current state
    # as these are not see in the visual they are considered dead
    state_pad=np.pad(self.state, ((1, 1), (1, 1)), 'constant')

    # temporary next state
    next_state=np.zeros((self.m,self.n),dtype='uint8')

    #looping throught the board to see what it's next state is
    for x in range(self.m):
      for y in range(self.n):
        #looking at the current neighbout of state[x+a,y+1]
        state_pad_slice=state_pad[x:x+3,y:y+3]
        # calculating its correlation score
        next_state[x,y]=self.correlation_slice(state_pad_slice)
    # updating the next state by looking at the correlation score    
    self.state=np.array((next_state==self.eigen_solution[0])\
                        +(next_state==self.eigen_solution[1])\
                        +(next_state==self.eigen_solution[2])\
                        ,dtype='int8')
  ##############################################################################
  # module that runs the simulation
  # Input
  # sleep : gap in seconds between two state simulation
  # This modules play game untill all cell are dead
  def play_game(self,sleep):

    # creating the image for the numbers
    im = plt.imshow(self.state*255, animated=True)
    plt.title("Initial State")
    #plt.grid(color='black', linestyle='-', linewidth=2)
    plt.axis('off')
    i=0
    plt.show()
    while self.play:
      i=i+1
      self.conway_next_state()
      time.sleep(sleep)
      im = plt.imshow(self.state*255, animated=True)
      plt.title("Evolution:"+str(i))
      #plt.grid(color='black', linestyle='-', linewidth=2)
      plt.axis('off')
      plt.show()
      if np.sum(self.state)==0:
        self.play=False
  ##############################################################################

################################################################################
#                                 The End                                      #
################################################################################      
if __name__ == '__main__':
  row=5
  col=5
  number=1
  time_difference_between_evolution=1
  game=conway_game_of_life(row,col,number)
  game.play_game(time_difference_between_evolution)
