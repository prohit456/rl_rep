from logging import logging;
class board:

  def __init__ (self):
    self.Logclass = logging();
    self.Logclass.set_verbosity(0);
    self.avail_pos_dict = {0 : [x for x in xrange(48)], 1: [x for x in xrange(48)]};
    self.state = [[0 for list_idx in xrange(6)] for vert_idx in xrange(8)];
    self.win = 0;
    self.prev_player = -2;
    self.logv(self.avail_pos_dict, 0);

  def logv(self, msg, val, TAG="DEFAULT_TAG"):
    self.Logclass.Logm(msg, val, TAG);

  def avail_pos(self, player, move, force = 0):
    #self.avail_pos_dict = 
    if (move in self.avail_pos_dict[(player + 1) % 2] and (force == 0)):
      self.avail_pos_dict[(player + 1) % 2].remove(move);
    if (force == 1 and (move not in self.avail_pos_dict[player])):
      self.avail_pos_dict[player].append(move);
      self.avail_pos_dict[(player + 1) % 2].delete(move);
    self.logv(self.avail_pos_dict, 0);
    pass;

  def get_neighbors(self, pos):
    neighbors = [];
    row_num = pos//6;
    col_num = pos % 6;
    if (row_num in xrange(1, 7) and (col_num in xrange(1,5))):
      neighbors = [pos - 6, pos -1, pos + 1, pos + 6];
      return neighbors;
    if (pos == 0):
      neighbors = [1, 6];
      return neighbors;
    elif (pos == 5):
      neighbors = [4, 11];
      return neighbors;
    elif (pos == 42):
      neighbors = [36, 43];
      return neighbors;
    elif (pos == 47):
      neighbors = [46, 41];
      return neighbors;
    elif (row_num == 0):
      neighbors = [pos -1, pos + 1, pos + 6];
      return neighbors;
    elif (col_num == 0):
      neighbors = [pos -6, pos + 1, pos + 6];
      return neighbors;
    elif (row_num == 7):
      neighbors = [pos -1, pos + 1, pos - 6];
      return neighbors;
    elif (col_num == 5):
      neighbors = [pos -6, pos - 1, pos + 6];
      return neighbors;


  def modulus (self, value):
    if (value < 0):
      return (-1 * value);
    return value;


  """ Need to make modifications such that it takes care of negative as well as positive signs"""
  def correct_state(self, player, pos):
    col_num = pos % 6;
    row_num = pos // 6;
    neighbors = self.get_neighbors(pos); """ need to write this function which outputs a list"""
    self.state[row_num][col_num] = 0;
    for position in neighbors:
      self.make_move(player, position, 1);
        

  def eval_win(self):
    if (len(self.avail_pos_dict[0]) == 48 and (len(self.avail_pos_dict[1]) < 48)):
      self.win = -1;
      return 1;
    elif (len(self.avail_pos_dict[1]) == 48 and (len(self.avail_pos_dict[0]) < 48)):
      self.win = 1;
      return 1;
    else:
      return 0;


  """ in case of explosion force is set to one. Otherwise its a normal operation"""
  def make_move(self, player, move, force = 0):
    col_num = move % 6;
    row_num = move // 6;
    if (self.prev_player == player and force == 0):
      self.logv("Wrong player", 0);
      return;
    neighbors = self.get_neighbors(move); """ need to write this function which outputs a list"""
    if (move in self.avail_pos_dict[player] and (force == 0)):
      self.state[row_num][col_num] = self.state[row_num][col_num] +  (player * 2) - 1; # this is to make sure 0 gets updated with -ve values, one with +ve ones
      if (self.modulus(self.state[row_num][col_num]) == len(neighbors)):
        self.correct_state(player, move);
    elif (force == 1):
      if (player == 0):
        self.state[row_num][col_num] = -1 * (self.modulus(self.state[row_num][col_num]) + 1);
      else:
        self.state[row_num][col_num] = self.modulus(self.state[row_num][col_num]) + 1;
      if (self.modulus(self.state[row_num][col_num]) == len(neighbors)):
        self.correct_state(player, move);
    self.avail_pos(player, move);
    if (force == 0):
      self.prev_player = player;

    self.logv(self.state, 0, "State");

""" logic of players taking turns must be written in the game, not in the board"""


testb = board();
testb.make_move(0, 4);
testb.make_move(0, 4);
testb.make_move(0, 4);
testb.make_move(1, 7);

