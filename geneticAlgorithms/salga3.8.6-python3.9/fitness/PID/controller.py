# PID controller

# interface with system model
import motor_v0_2_4 as model

import math
# pid
class PID:
	def __init__ (self, T):
		self.T = T
		self.utmax = 1
		self.utmin = 0
		self.reset()

	def reset (self):
		self.P = 0.0 # en rigor no hace falta guardarlo porque no se usa en t+1
		self.I = 0.0
		self.D = 0.0
		self.error1 = 0.0

	def step (self, setpoint, output, Kp, Ki, Kd, u):
		error = setpoint - output

		self.P = error
		self.I += error * self.T
		self.D = (error - self.error1) / self.T

		self.error1 = error # error in t-1
		ut = Kp * self.P + Ki * self.I + Kd * self.D + u

		if ut>self.utmax: ut=self.utmax # anti-windup strategy
		elif ut<self.utmin: ut=self.utmin
		return ut


class controller: # controlador PID clásico
	def __init__(self, pars): # pars: T, energy_weight, mass, radious
		self.pid = PID(pars[0]) # si el periodo es muy largo puede que el número de iteraciones (K) se quede corto
		self.pid.utmax = 24 # voltaje máximo
		self.pid.utmin = -24

		self.w = (3., .6, 6., 10.) # weight of ts, d, overshot, ess - w = [15., .4, 3., 10.] # paper #1 (cruise control)

		self.setpars(pars)

		self.reset()

	def setpars (self, pars): # parameters to set after init
		self.model = model.DC_Motor(pars[0], pars[1], pars[2]) # Masa del volante de inercia, radio del volante
		self.set_energy_weight(pars[3]) # relative weight of energy in %

	def reset (self):
		self.outputs = [] # evolución de la salida del sistema
		self.controls = [] # evolución de la señal de control
		self.setpoints = []
		self.energies = []
		self.accels = []
		self.total_energy = 0.0
		self.total_recovered = 0.0

		self.disturbances = [] # aceleración debida a la pendiente

		self.output = 0.0 # salida actual
		self.o1 = 0.0 # salida en t-1

		self.pid.reset()
		self.model.reset() # resetea el motor

	def system (self, ut): # model the system to control
		self.model.set_input_voltage(ut) # maximum voltage = 12v
		self.model.exec_cycle()
		res = self.model.get_angular_speed()
		if math.isnan(res):
			print('La velocidad angular es nan: baje el periodo de muestreo')
			res = 0.0
		return res

	def control (self, params, setpoint, disturbances=None): # ejecuta el control hasta una consigna
		# disturbances allow set additional params as for example, slopes in a road segment
		Kp = params[0]
		Ki = params[1]
		Kd = params[2]
		u = 0.0
		if len(params)>3:
			u = params[3]

		# calcula los parámetros ts, d, overshoot, ess que miden la bondad de una regulación
		self.disturbances = disturbances # inicializa para el step la aceleración debida a la pendiente
		origen = self.output
		over = self.output
		tsok = False
		ts = 1.0
		maxerror = 0.0002 # máximo error permitido en estabilización
		K = 350 # número de iteraciones para estabilización
		sign = math.copysign(1,setpoint-self.o1)
		cambiosign = 0
		oldchangesign = 0
		e = [] # vector de errores
		self.model.reset_energy()
		for ite in range(K):
			ut = self.pid.step(setpoint,self.output,Kp,Ki,Kd,u)
			self.controls.append(ut)
			self.setpoints.append(setpoint)
			self.o1 = self.output # output in t-1
			self.output = self.system(ut) # send to the model

			if setpoint>=origen and self.output>over: over=self.output
			if setpoint<origen and self.output<over: over=self.output
			if (self.output-self.o1)*sign<0: # hay un cambio de signo
				if oldchangesign==0:
					oldchangesign = self.output
				cambiosign += abs(self.output-oldchangesign)
				sign = math.copysign(1,self.output-self.o1)
				oldchangesign = self.output # guarda el valor en el que hubo un cambio
				#print('cambio')
			if not tsok and ite>1 and abs(self.output-self.o1)<self.o1*maxerror: # ite>1 es importante para que no salga en la primera iteración
				ts = float(ite)/K
				tsok = True
			self.outputs.append(self.output) # almacena para pintar en phenotype
			self.energies.append(self.model.step_energy) # almacena energía instantánea ***
			self.accels.append((self.output-self.o1)/self.pid.T) # aceleración instantánea
			e.append(abs(setpoint-self.output))
		ess = abs(setpoint-self.output) # error estacionario
		overshoot = abs(over-self.output)
		d = cambiosign
		#print [ts, d, overshoot, ess]

		#print(self.pid.P, self.pid.I, self.pid.D)
		#IAE = list(map(abs,e))
		#self.todo = [ts, d, overshoot, ess, sum(IAE)/len(e)]

		self.total_energy += self.model.get_total_energy() # w x seg que es lo mismo que kNm ***
		self.total_recovered += self.model.get_recovered_energy() # ***

		#return IAE
		return [self.w[0]*ts, self.w[1]*d, self.w[2]*overshoot, self.w[3]*ess, self.energy_weight*self.total_energy/1000.0 ] # 15.*ts, 0.4*d, 3.*overshoot, 5.*ess, , 5.*(sum(IAE)/len(e))

	def set_energy_weight (self, percent): # solve p = w/(w+s) * 100.0 for w -> w = - sp / (p-100)
		self.energy_weight = -percent * sum(self.w) / (percent - 100)
		self.energy_weight_percent = percent
		print(f'Energy weight defined to {self.energy_weight:.3f}')

	def sequence (self, chromosome, targets): # calcula los errores de una secuencia de consignas y los devuelve en una lista
		self.reset() # inicializa parámetros del pid
		e = []
		for target in targets: # para cada target
			e += self.control(chromosome, target)
		return e

# controladores especializados
class controller_updown (controller):
	def sequence (self, params, targets): # calcula los errores de una secuencia de consignas y los devuelve en una lista
		self.reset() # inicializa parámetros del pid
		e = []

		tar = [0.0] + targets # añade 0 para el primero
		for i in range(1,len(tar)): # para cada target
			r = tar[i]-tar[i-1]
			if  r > 0.0:
				e += self.control(params[:3],tar[i])
			else:
				e += self.control(params[3:],tar[i])

		return e

'''
def errors_salto (chromosome, targets): # calcula el error de una secuencia de consigna en múltiples PIDs por salto
	c.reset()

	max = 100
	salto = max / levels # tamaño de la franja

	e = []
	tar = [0.0] + targets # añade 0 para el primero
	for i in range(1,len(tar)): # para cada target
		r = abs(tar[i]-tar[i-1])

		franja = int(r / salto) # franja en la que estoy
		pos = franja * npars

		e += c.control(chromosome[pos:pos+npars], tar[i])

	return e

def errors_zona (chromosome, targets): # calcula el error de una secuencia de consigna en múltiples PIDs por zonas
	c.reset()

	max = 101
	salto = max / levels # tamaño de la franja

	e = []
	tar = [0.0] + targets # añade 0 para el primero
	for i in range(1,len(tar)): # para cada target
		franja = int(tar[i] / salto) # franja a la que voy
		pos = franja * npars

		e += c.control(chromosome[pos:pos+npars], tar[i])

	return e
'''

# Nota sobre los parámetros:
# we are fine tuned the parameters over a set of different problems, but if you can modify the behaviour of the final control, you can modify these parameters
# in a semantic according with the visual result that you want
# aparece overshot: subir c[2]
# etc
# remember that improve a visual behaviour can empeorar another

# cosillas para Norberto: cuando m=0 y r=0 no va bien
