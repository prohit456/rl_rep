from gi.repository import Gtk;
# 8 x 6 game

class ext_button(Gtk.Button):
  
  def __init__(self, bid):
    Gtk.Button.__init__(self);
    self.bid = bid;
    self.player = 3;
    self.max_bombs = 0;
    self.neighbors = [];
    col_num = bid % 6;
    row_num = (bid - col_num) / 6;
    if (col_num == 0 and row_num == 0):
      self.neighbors = [1, 6];
      self.max_bombs = 2;
    elif (col_num == 0 and row_num == 7):
      self.neighbors = [43, 36];
      self.max_bombs = 2;
    elif (col_num == 5 and row_num == 0):
      self.neighbors = [4, 11];
      self.max_bombs = 2;
    elif (col_num == 5 and row_num == 7):
      self.neighbors = [46, 41];
      self.max_bombs = 2;
    elif (row_num == 0):
      self.neighbors = [bid - 1, bid + 1, bid + 6];
      self.max_bombs = 3;
    elif (row_num == 7):
      self.neighbors = [bid - 1, bid + 1, bid - 6];
      self.max_bombs = 3;
    elif (col_num == 0):
      self.neighbors = [bid - 6, bid + 1, bid + 6];
      self.max_bombs = 3;
    elif (col_num == 5):
      self.neighbors = [bid - 6, bid - 1, bid + 6];
      self.max_bombs = 3;
    else:
      self.neighbors = [bid - 6, bid - 1, bid + 1, bid + 6];
      self.max_bombs = 4;

    

  def get_neighbors(self):
    return self.neighbors;

  def set_bid(self, bid):
    self.bid = bid;

  def set_player(self, player):
    self.player = player;

  def get_player(self):
    return self.player;

  def get_bid(self, bid):
    return self.bid;

  def add_bomb(self, bomb):
    self.set_label(self.get_label() + bomb);
    self.set_player(int(bomb));
    if (len(self.get_label()) == self.max_bombs):
      self.set_label("");
      self.set_player(3);
      return (1);
    return(0);

  def explosive_add(self, bomb):
    if (self.get_label() == None):
      self.set_label(bomb);
      self.set_player(int(bomb));
      return(0);
    self.set_label(bomb * (len(self.get_label())) + bomb);
    self.set_player(int(bomb));
    if (len(self.get_label()) == self.max_bombs):
      self.set_label("");
      self.set_player(3);
      return (1);
    return(0);


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

    grid = Gtk.Grid();
    grid.set_row_spacing(5);
    grid.set_column_spacing(5);

    #self.add(button);
    self.button_list = [];
    #for row_count in range(0,9):
    #    for col_count in range(0,7):
    #      frm = Gtk.Frame();
    #      button = Gtk.Button();
    #      button.set_size_request(25, 25);
    #      button.connect("clicked", self.button_clk);
    #      frm.add(button);
    #      grid.attach(frm, row_count, col_count, 1, 1);
    #self.add(grid);
    for row_count in range(0,8):
        for col_count in range(0,6):
          frm = Gtk.Frame();
          bid = col_count + (6 * row_count);
          self.button_list.append(ext_button(bid));
          #self.button_list[bid].set_bid(bid);
          self.button_list[bid].set_size_request(25, 25);
          self.button_list[bid].connect("clicked", self.button_clk);
          frm.add(self.button_list[bid]);
          grid.attach(frm, col_count, row_count, 1, 1);
    self.add(grid);


  def button_clk(self, button):
    print button.get_bid(self);
    # this part deals with empty tiles
    if (button.get_label() == None or (button.get_label() == "")):
      button.set_label(str(self.player_n));
      if (self.player_n == 0):
        self.zero_cnt = self.zero_cnt + 1;
        button.set_player(0);
      else:
        self.one_cnt = self.one_cnt + 1;
        button.set_player(1);
      self.player_n = (self.player_n + 1 ) % 2;
      return;

    # non empty tiles
    if (str(self.player_n) not in button.get_label()):
      #button.set_label("");
      return;
    else:
      print "adding_bon", self.player_n;
      rv = button.add_bomb(str(self.player_n));
    if (rv != 0):  
      print "Exploded!";
      self.recursive_explode(button);
    self.player_n = (self.player_n + 1 ) % 2;
    self.zero_cnt = 0;
    self.one_cnt = 0;
    for btn in self.button_list:
      if (btn.get_player() == 1):
        self.one_cnt = self.one_cnt + 1;
      if (btn.get_player() == 0):
        self.zero_cnt = self.zero_cnt + 1;

    if (self.zero_cnt >1 and self.one_cnt == 0):
      print "zero:", self.zero_cnt, " one:", self.one_cnt;
      print "player zero won";
    elif (self.one_cnt >1 and self.zero_cnt == 0):
      print "zero:", self.zero_cnt, " one:", self.one_cnt;
      print "player one won";


  def recursive_explode(self, button):
      print "entered rec expl";
      tmp_nbr = button.get_neighbors();
      for nbr in tmp_nbr:
        rv = self.button_list[nbr].explosive_add(str(self.player_n));
        if (rv == 1):
          self.recursive_explode(self.button_list[nbr]);

        self.button_list[nbr].set_player(self.player_n);

  
  def button_clk1(self, button):
    print "Hellow World1!";
    print Gtk.get_major_version();
    print Gtk.get_minor_version();
    print Gtk.get_micro_version();

window = ourwindow();
window.connect("delete-event", Gtk.main_quit);
window.show_all();
Gtk.main()
