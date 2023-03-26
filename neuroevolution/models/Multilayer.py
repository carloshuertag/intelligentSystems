import numpy as np
class Multilayer:
    def __init__(self, ninput, nhidden, noutput):
        self.ninput = ninput # número de entradas
        self.nhidden = nhidden # número de neuronas en capa oculta
        self.noutput = noutput # número de salidas

        self.w1 = np.random.rand(ninput,nhidden)-0.5
        self.b1 = np.random.rand(nhidden)-0.5
        self.w2 = np.random.rand(nhidden,noutput)-0.5
        self.b2 = np.random.rand(noutput)-0.5
        
        self.lRMS = [] # contiene la lista de RMSs para pintarlos luego
        self.laccuracy = [] # contiene la lista de accuracy para pintar luego

    def sigm (self, neta): # función sigmoidal
        return 1.0 / (1.0 + np.exp(-neta))
    
    def forward (self, x): # propaga un vector x y devuelve la salida
        layer_1 = self.sigm(np.dot(x, self.w1) + self.b1)
        layer_2 = self.sigm(np.dot(layer_1, self.w2) + self.b2)
        return layer_2,layer_1
    
    def update (self, x, d, alpha): # realiza una iteración de entrenamiento
        layer_2,layer_1 = self.forward(x)
            
        delta2 = (d - layer_2) * layer_2 * (1 - layer_2)
        delta1 = np.dot(delta2, self.w2.T) * layer_1 * (1 - layer_1)
            
        self.w2 += alpha * np.outer(layer_1, delta2)
        self.b2 += alpha * delta2
        self.w1 += alpha * np.outer(x, delta1)
        self.b1 += alpha * delta1
    
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
        
    def train (self, X, D, alpha, epochs, trace=0): # entrena usando update
        self.lRMS = [] # guarda lista de RMSs para pintarlos
        self.laccuracy = [] # guarda lista de accuracy

        for e in range(1,epochs+1):
            for i in range(len(X)):
                self.update(X[i],D[i], alpha)
            if trace!=0 and e%trace == 0:
                print('\n   Epoch: %d' % e)
                self.info(X,D)
    def test(self, X_test, D_test):
        print('\n-------- TESTING --------')
        rms_test = self.RMS(X_test, D_test)
        acc_test = self.accuracy(X_test, D_test)
        print('  Test RMS: %6.5f' % rms_test)
        print('Test Acc.: %6.5f' % acc_test)
        print('------------------------\n')
    def to_chromosome(self):
        return np.concatenate((self.w1.flatten(), self.b1.flatten(), self.w2.flatten(), self.b2.flatten()))
    def from_chromosome(self, chromosome):
        self.w1 = chromosome[:self.ninput*self.nhidden].reshape(self.ninput, self.nhidden)
        chromosome = chromosome[self.ninput*self.nhidden:]
        self.b1 = chromosome[:self.nhidden]
        chromosome = chromosome[self.nhidden:]
        self.w2 = chromosome[:self.nhidden*self.noutput].reshape(self.nhidden, self.noutput)
        chromosome = chromosome[self.nhidden*self.noutput:]
        self.b2 = chromosome[:self.noutput]

def one_hot (d): # codificación one_hot
    num_classes = len(set(d))
    rows = d.shape[0]
    labels = np.zeros((rows, num_classes), dtype='float32')
    labels[np.arange(rows),d.T] = 1
    return labels

M = Multilayer(3, 4, 2)