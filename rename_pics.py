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
import all_data

#							d h  m   s                          v
#HEIGHT   |   DATE: Fri_Jan_12_00-53-19_2018   |    VALUE: 460.48159099

print "start read data" 

starttime = 0

c_start_h = 10
c_start_m = 23
c_start_s = 3

#dont account first pic time but first height time to snycronise data, height meassurement starts earlier -> use this 00-53-19 
f_start_h = 0
f_start_m = 53
f_start_s = 19


diff_csh_sh = c_start_h - f_start_h
diff_cdm_sm = c_start_m - f_start_m 
diff_sdm_ss = c_start_s - f_start_s


correct_time_pack = ""

def get_sektime(h,m,s):
	total_time = 0
	total_time += h * 60 * 60
	total_time += m * 60
	total_time += s 


	return total_time

starttime = get_sektime(f_start_h, f_start_m, f_start_s)



def get_runtime(h,m,s):
	sektime = get_sektime(h,m,s)
	return sektime - starttime

runtime = 0
highest_value = -1000999
lowest_value = 10000000

def add_name(h, m, s):
	global correct_time_pack




def get_value(list, time):
	match_count = 0
	value = 0
	for dic in list:
		if dic[0] == time:
			#print "match: dic[0]: ", dic[0], "  time: ", time
			match_count += 1
			value = str(dic[1])


	if match_count > 0:
		#print "match count: ", match_count
		return str(value)
	else:		
		print "WARNING NO DATA PIC"	 
		return "no_data"



def make_data():
	converted_data = [] 
	global runtime
	global starttime
	global highest_value
	global lowest_value



	os.listdir("./pictures")[0]

	highest_runtime = 0
	for fname in os.listdir("./pictures"):
		
		it = 0
		it += 1
		if it%1 == 0:
			c_h = int(fname[11 : 13])
			c_m = int(fname[14 : 16])
			c_s = int(fname[17 : 19])
			runtime = get_runtime(c_h, c_m, c_s)
			print runtime
			#if runtime > highest_runtime: 
			#	print runtime
		    #	highest_runtime = runtime

			a_c_h = c_h + diff_csh_sh
			a_c_m = c_m + diff_cdm_sm
			a_c_s = c_s + diff_sdm_ss

			if a_c_s >= 60:
				a_c_m += a_c_s/60
				a_c_s = a_c_s%60
			if a_c_m >= 60:
				a_c_h += a_c_m/60
				a_c_m = a_c_m%60

			if a_c_s < 0:
				a_c_m -= 1
				a_c_s = 60 + a_c_s
			if a_c_m < 0:
				a_c_h -= 1
				a_c_m = 60 + a_c_m


			if a_c_m < 10:
				a_c_m = "0" + str(a_c_m)
			if a_c_s < 10:
				a_c_s = "0" + str(a_c_s)

			time_str = str(a_c_h) + "-" + str(a_c_m) + "-" + str(a_c_s)
			#print time_str

			h_str = get_value(all_data.aktual_height, runtime)[:8]
			rh_str = get_value(all_data.humidity, runtime)[:5]
			ouT_str = get_value(all_data.outerTemperature, runtime)[:5]
			inT_str = get_value(all_data.innerTemperature, runtime)[:5]
			p_str = get_value(all_data.pressure, runtime)[:7]

			new_name = time_str  + "__h:_" + h_str + "__RH:_" + rh_str + "__out_T:_" + ouT_str + "__in_T:_" + inT_str + "__p:_" + p_str + "__.jpg"
			#print new_name
			#print runtime
			#print new_name
			os.system("cp ./pictures/" + fname + " ./new_name_pics/" +  new_name)
			#add_name()
			


make_data()