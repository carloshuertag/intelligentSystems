import numpy as np 
class MLP:
    def __init__(self, ninput, nhidden_list, noutput):
        self.ninput = ninput # número de entradas
        self.nhidden_list = nhidden_list # lista de número de neuronas en cada capa oculta
        self.noutput = noutput # número de salidas

        self.weights = []
        self.biases = []
        self.n_layers = len(nhidden_list) + 1
        
        # iniciar pesos y bias para cada capa
        #!primera
        self.weights.append(np.random.rand(ninput,nhidden_list[0]) - 0.5)
        self.biases.append(np.random.rand(nhidden_list[0]) - 0.5)
        #!resto
        for i in range(1, len(nhidden_list)):
            self.weights.append(np.random.rand(nhidden_list[i-1],nhidden_list[i]) - 0.5)
            self.biases.append(np.random.rand(nhidden_list[i]) - 0.5)
        #!ultima
        self.weights.append(np.random.rand(nhidden_list[-1],noutput) - 0.5)
        self.biases.append(np.random.rand(noutput) - 0.5)
        
        self.lRMS = [] # contiene la lista de RMSs para pintarlos luego
        self.laccuracy = [] # contiene la lista de accuracy para pintar luego

    def sigm (self, neta): # función sigmoidal
        return 1.0 / (1.0 + np.exp(-neta))
    
    def forward (self, x): # propaga un vector x y devuelve la salida
        input_layer = x
        for i in range(self.n_layers-1):
            output_layer = self.sigm(np.dot(input_layer, self.weights[i]) + self.biases[i])
            input_layer = output_layer
        output_layer = self.sigm(np.dot(input_layer, self.weights[-1]) + self.biases[-1])
        return output_layer, input_layer
    
    def update (self, x, d, alpha): # realiza una iteración de entrenamiento
        output_layer, hidden_layers = self.forward(x)
            
        deltas = []
        delta = (d - output_layer) * output_layer * (1 - output_layer)
        deltas.append(delta)
        for i in range(self.n_layers-2, -1, -1):
            delta = np.dot(deltas[-1], self.weights[i+1].T) * hidden_layers * (1 - hidden_layers)
            deltas.append(delta)
        deltas = deltas[::-1]
        
        for i in range(self.n_layers-1):
            self.weights[i] += alpha * np.outer(hidden_layers[i], deltas[i])
            self.biases[i] += alpha * deltas[i]
    
    def RMS (self, X, D): # error RMS
        S,_ = self.forward(X)
        return np.mean(np.sqrt(np.mean(np.square(S-D),axis=1)))
        
    def accuracy (self, X, D): # calcula ratio de aciertos
        S,_ = self.forward(X)
        S = np.round(S)
        errors = np.mean(np.abs(D-S))
        return 1.0 - errors
    
    def info (self, X, D): # escribe traza
        self.lRMS.append(self.RMS(X,D))
        self.laccuracy.append(self.accuracy(X,D))
        print('     RMS: %6.5f' % self.lRMS[-1])
        print('Accuracy: %6.5f' % self.laccuracy[-1])
        
    def train(self, X, D, alpha, epochs, batch_size=None, trace=0):
      self.lRMS = [] # guarda lista de RMSs para pintarlos
      self.laccuracy = [] # guarda lista de accuracy

      if batch_size is None:
          batch_size = len(X)

      for e in range(1,epochs+1):
          for i in range(0, len(X), batch_size):
              X_batch = X[i:i+batch_size]
              D_batch = D[i:i+batch_size]

              for j in range(len(X_batch)):
                  self.update(X_batch[j], D_batch[j], alpha)

          if trace != 0 and e % trace == 0:
              print('\n   Epoch: %d' % e)
              self.info(X, D)
    def test(self, X_test, D_test):
      print('\n-------- TESTING --------')
      rms_test = self.RMS(X_test, D_test)
      acc_test = self.accuracy(X_test, D_test)
      print('  Test RMS: %6.5f' % rms_test)
      print('Test Acc.: %6.5f' % acc_test)
      print('------------------------\n')