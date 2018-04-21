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
import aktual_height

#							d h  m   s                          v
#HEIGHT   |   DATE: Fri_Jan_12_00-53-19_2018   |    VALUE: 460.48159099

print "start read data" 

starttime = 0

start_h = 10
start_m = 29
start_s = 19
diff_csh_sh = 0


correct_time_pack = ""

def get_sektime(h,m,s):
	total_time = 0
	total_time += h * 60 * 60
	total_time += m * 60
	total_time += s 


	return total_time

def get_runtime(h,m,s):
	sektime = get_sektime(h,m,s)
	return sektime - starttime

runtime = 0
highest_value = -1000999
lowest_value = 10000000

def add_correct_time(h, m, s, v):
	global correct_time_pack




def save_correct_time():
	pass

def make_data(fname, indexPlus):
	converted_data = [] 
	global runtime
	global starttime
	global highest_value
	global lowest_value

	for filename in os.listdir("./raw"):
		if filename.endswith(fname + ".pro"): 
			with open('raw/' + filename, 'r') as f:
				
	 			fline = f.readline()
				#c_d = float(fline[27 + indexPlus :29 + indexPlus])
				c_h = float(fline[30 + indexPlus :32 + indexPlus ])
				c_m = float(fline[33 + indexPlus :35 + indexPlus ])
				c_s = float(fline[36 + indexPlus :38 + indexPlus ])
				starttime = get_sektime(c_h, c_m, c_s)

			with open('raw/' + filename, 'r') as f:
				it = 0
				for line in f.readlines():
					it += 1
					if it%1 == 0:
						#c_d = float(line[27 + indexPlus :29 + indexPlus ])
						c_h = float(line[30 + indexPlus :32 + indexPlus ])
						c_m = float(line[33 + indexPlus :35 + indexPlus ])
						c_s = float(line[36 + indexPlus :38 + indexPlus ])

						runtime = get_runtime(c_h, c_m, c_s)

						c_v = float(line[57 + indexPlus::])

						if c_v > highest_value:
							highest_value = c_v
						elif c_v < lowest_value:
							lowest_value = c_v

						#print "runtime:", get_runtime(c_d, c_h, c_m, c_s), ":::",c_v
						converted_data.append((runtime, c_v))

						#add_correct_time()
						


			return converted_data

height_data = make_data("height", 0)
humidity_data = make_data("humidity" ,2)
inT_data = make_data("innerTemperature", 5)
outT_data = make_data("outerTemperature", 5)

runt_at_max = 0
def get_maxes(data):
	
	global highest_value	
	global lowest_value
	global runtime
	global runt_at_max

	highest_value = -99999999999
	lowest_value = 9999999999

	for pt in data:
		if pt[1] > highest_value:
			highest_value = pt[1]
			runt_at_max = pt[0]
		elif pt[1] < lowest_value:
			lowest_value = pt[1]

		runtime = pt[0]





pressure_data = sorted_pressure.pressure_list
#get_maxes(pressure_data)

aktual_height_data = aktual_height.aktual_height
get_maxes(aktual_height_data)



print "h: ", highest_value, "   l: ", lowest_value
print "end read data"

for t in outT_data:
	if runt_at_max == t[0]:
		print "t at max: ", t[1]


converted_data = aktual_height_data

'''
print "sort_converted data (only for pressure)"

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


file = open('repair.txt','w')

for i in sorted_data: 
	file.write(str((i[0], "  |  ", i[1],))) 
	file.write("\n")

file.close()



print converted_data
'''




file = open('all_data.py','w')
file.write("old_height = [ \n")

for i in height_data: 
	file.write(str((i[0], i[1]))) 
	file.write(",\n")

file.write("]\n\n")


file.write("humidity = [ \n")

for i in humidity_data: 
	file.write(str((i[0], i[1]))) 
	file.write(",\n")

file.write("]\n\n")


file.write("innerTemperature = [ \n")

for i in inT_data: 
	file.write(str((i[0], i[1]))) 
	file.write(",\n")

file.write("]\n\n")


file.write("outerTemperature = [ \n")

for i in outT_data: 
	file.write(str((i[0], i[1]))) 
	file.write(",\n")

file.write("]\n\n")


file.write("pressure = [ \n")

for i in pressure_data: 
	file.write(str((i[0], i[1]))) 
	file.write(",\n")

file.write("]\n\n")


file.write("aktual_height = [ \n")

for i in aktual_height_data: 
	file.write(str((i[0], i[1]))) 
	file.write(",\n")

file.write("]\n\n")



file.close()

class My_Graph(Graph):
	
	def __init__(self, **kwarks):
		super (My_Graph, self).__init__(**kwarks)
		print lowest_value
		self.xmax = runtime
		self.xmin = 0
		self.ymax = highest_value + highest_value * 0.1 
		self.ymin = lowest_value

		self.y_ticks_major =  int(highest_value / 10)


		#print matchcountIn5Line 
		self.hplot = SmoothLinePlot(color=[1, 0, 0, 1])
		self.splot = SmoothLinePlot(color=[0, 1, 0, 1])
		
		self.splot.points = converted_data
		#self.hplot.points = apoints #[(x, sin(x / 10)) for x in range(0, 101)] 
		#print self.splot.points

		self.add_plot(self.hplot)
		self.add_plot(self.splot)


class Control_panel(Widget):
	def __init__(self, **kwarks):
		super (Control_panel, self).__init__(**kwarks)
		#amplitude = self.ids['amplitude']


class main_layout(BoxLayout):

	def __init__(self, **kwarks):
		super(main_layout, self).__init__(**kwarks)
		pass
		#self.graph = self.ids['graph']
		#self.panel = self.ids['panel']

		#valuep = self.panel.amplitude.value

	def on_touch_down(self, touch):
		xmax = self.graph.xmax
		ymax = self.graph.ymax
		touch_pos = touch.pos

		startpoint = (60., 50.)
		startx = startpoint[0]
		starty = startpoint[1]

		touch_pig_x = (touch_pos[0] - startx)
		touch_pig_y = (touch_pos[1] - starty)  
		touch_pig = (touch_pig_x, touch_pig_y)


		print touch_pig

	#def update(self, dt):
	#	print 'hi'




class interfaceApp(App):
	def build(self):
		app = main_layout()
		#Clock.schedule_interval(app.graph.update, 1.0 / 60.0)
		return app
	
interfaceApp().run()

