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


#							d h  m   s                          v
#HEIGHT   |   DATE: Fri_Jan_12_00-53-19_2018   |    VALUE: 460.48159099

print "start read data" 

p_list = sorted_pressure.pressure_list

print "end read data"




converted_data = p_list


print "sort_converted data (only for pressure)"

last_t = -1
sorted_data = []

for pel in p_list:
	c_t  = pel[0]
	if (last_t != c_t):
		sorted_data.append(pel)
		last_t = c_t


p_list = sorted_data
sorted_data = []
index = len(p_list) -1
for i in range (1, len(p_list) - 1):
	print "hi"
	sorted_data.append(p_list[index])
	index -= 1


'''
current_smalest_time = -1
current_v = 0
current_smalest_index = -1
sorted_data = []
len_data = len(converted_data)

while len(sorted_data) != len_data:
	print (float(len(sorted_data))/len_data) * 100., " prozent etwa, len(sortet data): ", len(sorted_data)
	i = 0
	for pack in converted_data:
		#print i[0]
		if pack[0] >= current_smalest_time:
			current_smalest_time = pack[0]
			current_smalest_index = i
			current_v = pack[1]  




		i += 1
	#print "cst: ", current_smalest_time, "lst: ", last_smalest_time

	sorted_data.append((current_smalest_time, current_v))

	last_smalest_time = current_smalest_time
	del converted_data[current_smalest_index]
	current_smalest_time = -1
	current_smalest_index = -1
	i= 0	


converted_data = sorted_data
'''
print sorted_data
file = open('repair.txt','w')

for i in sorted_data: 
	file.write(str((i[0], i[1]))) 
	file.write("\n")

file.close()
