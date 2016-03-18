import json;
from gi.repository import Gtk;
import random as rnd;

def eval_game(board):
  hor_list = [0, 3, 6];
  if ((board[0] == board[4]) and (board[4] == board[8]) and (board[0] != 2)):
    return (board[0]);
  elif ((board[2] == board[4]) and (board[4] == board[6]) and (board[2] != 2)):
    return (board[2]);
  else:
    for i in range(3):
      if ((board[i] == board[i + 3]) and (board[i] == board[i + 6]) and (board[i] != 2)):
        return (board[i]);
  for item in hor_list:      
    if ((board[item] == board[item + 1]) and (board[item] == board[item + 2]) and (board[item] != 2)):
      return (board[item]);
  return(2);


def print_board(board):
  print "";
  print "======================";
  print "|| ", board[0], " || ", board[1], " || ", board[2]; 
  print "|| ", board[3], " || ", board[4], " || ", board[5]; 
  print "|| ", board[6], " || ", board[7], " || ", board[8]; 


def init_board():
  tmp_list = [2, 2, 2, 2, 2, 2, 2, 2, 2];
  return tmp_list;
 

with open('train.txt') as jsonfile:
  statespace = json.load(jsonfile);

space = {int(k):v for k,v in statespace.items()};
print space;

def decode_board(board):
    dop = 0;
    iter_count = 0;
    while (iter_count < 9):
      dop = dop + ((3 ** iter_count) * board[iter_count]);
      iter_count = iter_count + 1;
    return dop;


def play(board):
  board_val = decode_board(board);
  avail_pos = [i for i, x in enumerate(board) if x == 2];
  reward = -1;
  print "++++++ BANNER ++++++++";
  for pos in avail_pos:
    board[pos] = 0;
    board_val = decode_board(board);
    print_board(board);
    if (board_val in space):
      print "reward is ", space[board_val], "bv:", board_val;
      if (space[board_val] > reward):
        final_pos = pos;
        reward = space[board_val];
      elif (space[board_val] == reward):
        if (rnd.random() > 0.5):
          final_pos = pos;

    board[pos] = 2;
  print reward;
  if (reward != -1):
    return final_pos;
  else:
    return avail_pos[0];

#count = 0;
#while (eval_game(board) == 2 and count < 9):
#  if (count % 2 == 0):
#    pl0.exploit(board);
#  else:
#    ip = raw_input("turn");
#    board[int(ip)] = 1;
#  print_board(board);
#  count = count + 1;

  

class ext_button(Gtk.Button):
  
  def __init__(self, bid):
    Gtk.Button.__init__(self);
    self.bid = bid;
    self.player = 3;
        

  def set_bid(self, bid):
   self.bid = bid;

  def set_player(self, player):
    self.player = player;

  def get_player(self):
    return self.player;

  def get_bid(self):
    return self.bid;

 

class ourwindow(Gtk.Window):

  def __init__(self):
    Gtk.Window.__init__(self, title="Hello World");
    Gtk.Window.set_default_size(self, 400, 325);
    Gtk.Window.set_position(self, Gtk.WindowPosition.CENTER);
    self.player_n = 0;
    self.row_sel = 0;
    self.col_sel = 0;
    self.zero_cnt = 0;
    self.one_cnt = 0;
    self.board = [2,2,2,2,2,2,2,2,2];

    grid = Gtk.Grid();
    grid.set_row_spacing(5);
    grid.set_column_spacing(5);

    #self.add(button);
    self.button_list = [];
    for row_count in range(0,3):
        for col_count in range(0,3):
          frm = Gtk.Frame();
          bid = col_count + (3 * row_count);
          self.button_list.append(ext_button(bid));
          self.button_list[bid].set_size_request(25, 25);
          self.button_list[bid].connect("clicked", self.button_clk);
          frm.add(self.button_list[bid]);
          grid.attach(frm, col_count, row_count, 1, 1);
    self.add(grid);
    pos = play(self.board);
    self.board[pos] = 0;
    self.button_list[pos].set_label("0");


  def button_clk(self, button):
    print button.get_bid();
    if (button.get_label() == None or (button.get_label() == "")):
      button.set_label("1");
    self.board[button.get_bid()] = 1;
    pos = play(self.board);
    self.board[pos] = 0;
    self.button_list[pos].set_label("0");


window = ourwindow();
window.connect("delete-event", Gtk.main_quit);
window.show_all();
Gtk.main()
