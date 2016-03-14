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
  print "|| ", board[0], " || ", board[1], " || ", board[2]; 
  print "|| ", board[3], " || ", board[4], " || ", board[5]; 
  print "|| ", board[6], " || ", board[7], " || ", board[8]; 


def init_board():
  tmp_list = [2, 2, 2, 2, 2, 2, 2, 2, 2];
  return tmp_list;


class player():
  def __init__(self):
    print "initializing player";

  


board = init_board();
print_board(board);
print eval_game(board);

import random as rnd;
player = 0;
tiles = range(0,9);
while (eval_game(board) == 2):
  rv = rnd.randint(0,len(tiles) - 1);
  tile_chosen = tiles[rv];
  tiles.pop(rv);
  board[tile_chosen] = player;
  print_board(board);
  player = (player + 1) % 2;
print "player ", eval_game(board), " won!";
