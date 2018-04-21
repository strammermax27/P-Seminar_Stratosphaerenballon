from kivy.app import App 
from kivy.uix.widget import Widget 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.properties import ObjectProperty
from kivy.garden.graph import Graph, SmoothLinePlot, MeshLinePlot
from kivy.clock import Clock

from math import sin, cos

import os

import sorted_pressure
import make_graphs
import numpy as np

#							d h  m   s                          v
#HEIGHT   |   DATE: Fri_Jan_12_00-53-19_2018   |    VALUE: 460.48159099

print "start read data" 

p_list = sorted_pressure.pressure_list
t_list = make_graphs.make_data("outerTemperature", 5)
a_h_list = []
print "end read data"

for i in range(0 , len(p_list) - 1):
	runtime = p_list[i][0]
	t_kel = t_list[i][1] + 273.15
	p = p_list[i][1] 

	print "t: ", runtime, "	 |  T_kel: ", t_kel, "  |  p:  ", p

	#old formula
	#m_1 = t_kel/(0.0065) 
	#m_2 = (1. -  (p/1013.)**(1/5.255)       )

	#new formula
	m_1 = (1.381 * 10**-23 * t_kel) / (28.8 * 1.66 * 10**-27 * 9.81)
	m_2 = np.log(1020/p)

	a_height = m_1 * m_2


	a_h_list.append((runtime, a_height))


file = open('aktual_height.py','w')
file.write("aktual_height = [ \n")

for i in a_h_list: 
	file.write(str((i[0], i[1]))) 
	file.write(",\n")

file.write("]")

file.close()

print "end"
