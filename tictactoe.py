# added to git
"""we need to first assign probabilities to the state. The states where we are won have a probability of one
The states where we lost have probability of zero and rest of them have a probability of 0.5
The formula we use is V(s[n]) = V(s[n]) + alpha * (V(s[n+2]) - V(s[n]))"""
import random as rnd;
import json;
def eval_game(board):
  hor_list = [0, 3, 6];
  if ((board[0] == board[4]) and (board[4] == board[8]) and (board[0] != 2)):
    #print "enter 0";
    return (board[0]);
  elif ((board[2] == board[4]) and (board[4] == board[6]) and (board[2] != 2)):
    #print "enter 1";
    return (board[2]);
  else:
    for i in range(3):
      if ((board[i] == board[i + 3]) and (board[i] == board[i + 6]) and (board[i] != 2)):
        #print "enter 2 and ", i;
        return (board[i]);
  for item in hor_list:      
    if ((board[item] == board[item + 1]) and (board[item] == board[item + 2]) and (board[item] != 2)):
      #print "enter 3 and ", item;
      return (board[item]);
  return(2);


def print_board(board):
  pass;
  #print "";
  #print "======================";
  #print "|| ", board[0], " || ", board[1], " || ", board[2]; 
  #print "|| ", board[3], " || ", board[4], " || ", board[5]; 
  #print "|| ", board[6], " || ", board[7], " || ", board[8]; 


def init_board():
  tmp_list = [2, 2, 2, 2, 2, 2, 2, 2, 2];
  return tmp_list;


class player():

  player_id = 0;
  def __init__(self, pid):
    #print "initializing player";
    self.epsilon = 0.1;
    self.player_id = pid;
    self.state_space = {};
    self.prev_state = self.decode_board([2,2,2,2,2,2,2,2,2]);
    self.state_space[self.prev_state] = 0.5;
    self.prev_stateval = 0;
  

  def decode_board(self, board):
    dop = 0;
    ##print "======== DECODING =========";
    #print_board(board);
    iter_count = 0;
    while (iter_count < 9):
      ##print board[iter_count];
      dop = dop + ((3 ** iter_count) * board[iter_count]);
      ##print dop, ",iter", iter_count, ",brdv", board[iter_count], ",pwr", 2**iter_count ;
      iter_count = iter_count + 1;
    ##print "DOP = ", dop;
    ##print "====END DECODING===="
    return dop;

  def explore(self, board):
    #print "Exploring";
    board_val = self.decode_board(board);
    #print "present state for player", self.player_id, " is ", board_val;
    self.update_state_space(board);
    reward = -1;
    self.prev_state = board_val; #to update the state value in the next iteration
    avail_pos = [i for i, x in enumerate(board) if x == 2];
    if (board_val in self.state_space.keys()):
      self.prev_stateval = self.state_space[board_val];
    else:
      self.prev_stateval = 0.5;
      self.state_space[board_val] = 0.5;
    if (len(avail_pos) == 1):
      board[avail_pos[0]] = self.player_id;
      final_pos = avail_pos[0];
    else:
      final_pos = rnd.randint(0, len(avail_pos) - 1);
    board[final_pos] = self.player_id;  



  def set_player_id(self, player_id):
    self.player_id = player_id;

  def exploit(self, board):
    #print "Exploiting";
    board_val = self.decode_board(board);
    #print "present state for player", self.player_id, " is ", board_val;
    self.update_state_space(board);
    if (board_val in self.state_space.keys()):
      self.prev_stateval = self.state_space[board_val];
    else:
      self.prev_stateval = 0.5;
      self.state_space[board_val] = 0.5;
    reward = -1;
    self.prev_state = board_val;
    avail_pos = [i for i, x in enumerate(board) if x == 2];
    for pos in avail_pos:
      board[pos] = self.player_id;
      board_val = self.decode_board(board);
      if (board_val in self.state_space.keys()):
        if (reward  < self.state_space[board_val]):
          final_pos = pos;
          reward = self.state_space[board_val];
        elif (reward == self.state_space[board_val]):
          if (rnd.random() > 0.5):
            final_pos = pos; # idea is to switch to one of the states randomly when both the states have equal reward
      else:
        if (eval_game(board) == self.player_id):
          self.state_space[board_val] = 1;
          return;
        self.state_space[board_val] = 0.5;
        if (reward  < self.state_space[board_val]):
          final_pos = pos;
          reward = self.state_space[board_val];
        elif (reward == self.state_space[board_val]):
          if (rnd.random() > 0.5):
            final_pos = pos; # idea is to switch to one of the states randomly when both the states have equal reward
      board[pos] = 2;
    board[final_pos] = self.player_id;  
    ##print "FINAL POS";
    #print_board(board);

  def update_state_space(self, board):
    #print "updating state space for player", self.player_id;
    #print "prev pos ", self.prev_state; 
    #print_board(board);
    board_val = self.decode_board(board);
    if (board_val in self.state_space.keys()):
      ##print "present in keys";
      if (self.state_space[board_val] != 0):
        self.state_space[self.prev_state] =  self.state_space[self.prev_state] + (0.1 * (self.state_space[board_val] - self.prev_stateval));  
      else:
        self.state_space[self.prev_state] =  0;
      #print self.prev_state, ":", self.state_space[self.prev_state];
    else:
      ##print "not present in keys";
      self.state_space[self.prev_state] =  self.state_space[self.prev_state] + (0.1 * (0.5 - self.prev_stateval));  
      #print self.prev_state, ":", self.state_space[self.prev_state];

  def update_state_with_zero(self, board):
    board_val = self.decode_board(board);
    #print "updating with 0 ", self.player_id;
    print_board(board);
    self.state_space[board_val] = 0;
    self.update_state_space(board);
  
  def update_state_with_one(self, board):
    board_val = self.decode_board(board);
    #print "updating with 1 ", self.player_id;
    print_board(board);
    self.state_space[board_val] = 1;
    self.update_state_space(board);

  def store_to_json(self):
    json_obj = json.dumps(self.state_space);
    #print "json is :", json_obj;
    with open('train.txt', 'w') as outfile:
      json.dump(self.state_space, outfile);


board = init_board();
prev_state0 = [];
prev_state1 = [];
prev_reward0 = 0;
prev_reward1 = 0;
print_board(board);
#print eval_game(board);

#player = 0;
curr_reward = 0;
tiles = range(0,9);
epsilon = 0.2;
init_board = board;
count = 0;
pl0 = player(0);
pl1 = player(1);
for game_idx in range(100000):
  board = [2, 2, 2, 2, 2, 2, 2, 2, 2];
  count = 0;
  if (game_idx == 50000):
    epsilon = 1;
  while (eval_game(board) == 2 and count < 9):
    # Let us start the game here
    policy = rnd.random();
    #print "policy:", policy;
    if (count % 2 == 0):
      if (policy < epsilon):
        pl0.exploit(board);
      else:
        pl0.explore(board);
    else:
      if (policy < epsilon):
        pl1.exploit(board);
      else:
        pl1.explore(board);
      #random
      #avail_pos = [i for i, x in enumerate(board) if x == 2];
      #if (len(avail_pos) != 1):
      #  pos = rnd.randint(0, len(avail_pos) - 1);
      #else:
      #  pos = 0;
      #board[avail_pos[pos]] = 1;

    #print_board(board);
    count = count + 1;
  
  if (eval_game(board) == 0):
    pl1.update_state_with_zero(board);
    pl0.update_state_with_one(board);
  elif(eval_game(board) == 1):
    pl0.update_state_with_zero(board);
    pl1.update_state_with_one(board);

##print pl0.state_space;
pl0.store_to_json();

#print "single player mode"

board = [2, 2, 2, 2, 2, 2, 2, 2, 2];
count = 0;
print_board(board);
while (eval_game(board) == 2 and count < 9):
  if (count % 2 == 0):
    pl0.exploit(board);
  else:
    ip = raw_input("turn");
    board[int(ip)] = 1;
  print_board(board);
  count = count + 1;
   
#while (eval_game(board) == 2 and count < 9):
#  if (len(tiles) > 1):
#    rv = rnd.randint(0,len(tiles) - 1);
#  else:
#    rv = 0;
#  #print tiles, "\n", rv, "\n", count;
#  tile_chosen = tiles[rv];
#  tiles.pop(rv);
#  board[tile_chosen] = player;
#  print_board(board);
#  player = (player + 1) % 2;
#  count = count + 1;
##print "player ", eval_game(board), " won!";
#print_board(init_board);
