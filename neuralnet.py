from logging import logging;
import numpy as np;
import random as rnd;
class neuron:

  def __init__(self):
    print "created neuron";
    self.Logclass = logging();
    self.Logclass.set_verbosity(0);
    self.bias = 0;
    self.z_ip = 0.0;
    self.a_op = 0.0;# ouput of sigmoid needs to go here

  def set_bias(self, bias):
    self.bias = bias;

  @staticmethod
  def eval_out (inp, bias):
    Logclass = logging();
    Logclass.set_verbosity(0);
    ip = np.multiply(-1 , np.add(inp, bias));
    a_op =1 / (1 + np.exp(np.multiply(-1, np.add(inp, bias))));# ouput of sigmoid needs to go here
    diff_op = np.power(a_op, 2) * (np.exp(np.multiply(-1, np.add(inp, bias))));# ouput of sigmoid needs to go here
    Logclass.Logm(diff_op, 1, "DIFF");
    Logclass.Logm(a_op, 1, "ACT");
    return [diff_op, a_op];

  def logv(self, msg, val, TAG="DEFAULT_TAG"):
    self.Logclass.Logm(msg, val, TAG);

class neural_net:

  """ define number of layers
  define number of neurons in each layer
  create weights """

  def __init__(self, nn_inp, nn_op):
    self.Logclass = logging();
    self.Logclass.set_verbosity(0);
    self.num_layers = 2;
    self.num_neurons = [2,  1,  1];
    self.z_vector = np.array([[0 for index in xrange(self.num_neurons[list_idx])] for list_idx in xrange(len(self.num_neurons))]); # these are the inputs to neurons
    self.act_vector = np.array([[0 for index in xrange(self.num_neurons[list_idx])] for list_idx in xrange(len(self.num_neurons))]);
    self.err_vector = np.array([[0 for index in xrange(self.num_neurons[list_idx])] for list_idx in xrange(len(self.num_neurons))]);
    self.bias_vector = np.array([[0 for index in xrange(self.num_neurons[list_idx])] for list_idx in xrange(len(self.num_neurons))]);
    self.diff_vector = np.array([[0 for index in xrange(self.num_neurons[list_idx])] for list_idx in xrange(len(self.num_neurons))]);
    self.weights = []
    self.out = [3];
    self.wt_gradient = []
    for count in xrange(len(self.num_neurons) - 1):
      self.weights.append(self.rand_matrix(self.num_neurons[count + 1], self.num_neurons[count])); 
      self.wt_gradient.append(self.rand_matrix(self.num_neurons[count + 1], self.num_neurons[count])); 
    self.logv(self.weights, 1);
    for iter_count in xrange(1000):
      for elem_idx in range(len(nn_inp)):
        self.update_nn(nn_inp[elem_idx]);
        self.out = nn_op[elem_idx];
        self.calc_errors();
        self.update_weights();
    pass;

  def logv(self, msg, val, TAG="DEFAULT_TAG"):
    self.Logclass.Logm(msg, val, TAG);

  def update_nn(self, inp):
    """ do a matrix multiplication """
    for element in xrange(len(self.act_vector[0])):
      self.z_vector[0][element] = inp[element]; """ calculation of output for first layer"""
      #[self.diff_vector[0], self.act_vector[0]]= neuron.eval_out(self.z_vector[0], self.bias_vector[0]);
      #[self.diff_vector[0], self.act_vector[0]]= [np.add(self.z_vector[0] , self.bias_vector[0]), np.add(self.z_vector[0] , self.bias_vector[0])];
      [self.diff_vector[0], self.act_vector[0]]= [self.z_vector[0], self.z_vector[0] ];
    self.logv(self.weights[0], 1, "WT0");#], 
    self.logv(self.act_vector[1 - 1], 1, "ACT0");
    for idx in range(1, len(self.num_neurons)):
      self.z_vector[idx] = np.dot(self.weights[idx - 1], self.act_vector[idx - 1]);
      for act_vect_idx in xrange(len(self.act_vector[idx])):
        print self.act_vector[idx];
        #self.act_vector[idx] = self.neural_net[idx][0].eval_out(self.z_vector[idx]);
        [self.diff_vector[idx], self.act_vector[idx]] = neuron.eval_out(self.z_vector[idx], self.bias_vector[idx]);
    self.logv(self.act_vector, 1, "ACTIVATION");
    self.logv(self.z_vector, 0, "ZINPUT");
    self.logv(np.exp([1,2]), 1, "EXP");

  def update_weights(self):
    for wt_idx in xrange(len(self.weights)):
      for i in xrange(len(self.weights[wt_idx])):
        self.wt_gradient[wt_idx][i] = np.multiply(self.weights[wt_idx][i], 0.01 * self.err_vector[wt_idx + 1][i]);
        #print "i:", i;
        #print len(self.err_vector);
        #print "wts", self.weights[wt_idx];
        #print "errs", self.err_vector[wt_idx + 1];
      self.weights[wt_idx] = np.subtract(self.weights[wt_idx] ,  self.wt_gradient[wt_idx]);
      self.bias_vector[wt_idx] = np.subtract(self.bias_vector[wt_idx] ,  np.multiply(0.01, self.err_vector[wt_idx]));
    self.logv(self.wt_gradient, 1, "GRADIENT");
    self.logv(self.weights, 1, "WEIGHTS");
    self.logv(self.bias_vector, 0, "BIAS");
    pass;

  def calc_errors(self):
    #self.err_vector[-1] = [1 for i in xrange(len(self.err_vector[-1]))]
    self.err_vector[-1] = np.subtract(self.act_vector[-1], self.out) * self.diff_vector[-1];
    self.logv(np.power(np.subtract(self.act_vector[-1], self.out), 2), 0, "COST");
    for count in range(len(self.num_neurons) - 2, -1, -1):   # count corresponds to layer, len(err) is num layers
      """ weights[count] is a weight matrix and column corresponds to all weights going outward of a neuron"""
      tmp_weight_vector = [np.transpose(self.weights[count])[err_vect_idx] for err_vect_idx in xrange(self.num_neurons[count])]; # each element of weights is a row, pick up the neuron weights corresponding to each row
      self.err_vector[count]= np.dot(tmp_weight_vector, self.err_vector[count + 1]); 
      self.err_vector[count] = self.err_vector[count] * self.diff_vector[count];
    self.logv(self.err_vector, 0, "ERROR");
    pass;

  def rand_matrix(self, num_rows, num_cols):
    return ([[rnd.random() for cols in xrange(num_cols)] for rows in xrange(num_rows)])

nn = neural_net([[1,1], [1, 0], [0, 1], [0, 0]], [0, 1 ,1, 1]);
