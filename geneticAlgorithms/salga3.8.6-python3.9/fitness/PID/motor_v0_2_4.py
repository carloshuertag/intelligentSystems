#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 21:58:17 2020

@author: norberto
"""

class DC_Motor(object):

    # Init a DC motor (RE-36 with planetary gearbox reduction 26:1)
    # Period is the sampling interval.
    # M is the mass of the inertia wheel (zero for no inertia wheel)
    # radius is the radius of the inertia wheel
    def __init__(self, Period, M, radius):
        self.inertia_wheel_moment = 0.5 * M * radius**2
        self.T = Period
        self.reset()

    def reset (self):
        self.R = 1.11
        self.L = 0.0002
        self.K = 0.0634

        self.J_2 = 9.1e-7 # planetary gearbox and output shaft inertia moment

        self.J_2 += self.inertia_wheel_moment
        self.J_1 = 6.77e-6 # motor shaft inertia moment

        self.f_v_1 = 1.66e-5 # motor shaft viscous friction
        self.f_v_2 = 1.0e-6 # gearbox and output shaft viscous friction
        self.n = 26 # 26:1

        self.i_k = 0.0
        self.i_k_1 = 0.0
        self.ea = 0.0
        self.eb = 0.0
        self.Tau_1 = 0.0
        self.Tau_2 = 0.0

        self.w_1 = 0.0
        self.w_2_k = 0.0
        self.w_2_k_1 = 0.0

        self.step_energy = 0.0
        self.total_energy = 0.0
        self.recovered_energy = 0.0

    def set_input_voltage(self, voltage):
        self.ea = voltage

    def exec_cycle(self):
        self.i_k = ((self.T/self.L)*(self.ea-self.eb) + self.i_k_1)\
        /(1+self.T*self.R/self.L)

        self.Tau_1 = self.K*self.i_k

        self.w_2_k = (self.Tau_1 + (self.n*(self.J_2 + self.J_1))/self.T\
                      *self.w_2_k_1)/((self.n*(self.J_2 +self.J_1))/self.T\
                                     + self.n*(self.f_v_2 + self.f_v_1))

        self.w_1 = self.n*self.w_2_k
        self.eb = self.K * self.w_1

        self.Tau_2 = self.n * self.Tau_1

        # Save current state k as k-1 for next iteration
        self.i_k_1 = self.i_k
        self.w_2_k_1 = self.w_2_k

        self.step_energy = self.ea * self.i_k * self.T # input_voltage * current * period
        self.total_energy += self.step_energy
        if self.step_energy < 0: # si es energía recuperada
            self.recovered_energy -= self.step_energy

    def reset_energy(self):
        self.total_energy = 0.0
        self.recovered_energy = 0.0

    def get_total_energy(self):
        return self.total_energy

    def get_recovered_energy(self):
        return self.recovered_energy

    def get_current(self):
        return self.i_k

    def get_torque(self):
        return self.Tau_2

    def get_angular_speed(self):
        return self.w_2_k
