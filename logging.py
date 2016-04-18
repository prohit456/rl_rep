class logging:
  
  """ higher verbosity prints everything. Lower nothing;"""
  def __init__(self):
    self.verbosity = 2;
  
  def Logm (self, msg, msg_verbosity, TAG="DEFAULT_TAG:"):
    TAG = TAG + ":";
    if (self.verbosity >= msg_verbosity):
      print TAG , msg;
    else:
      return;

  def set_verbosity(self, val):
    self.verbosity = val;



