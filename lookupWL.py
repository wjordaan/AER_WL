###########################################################################################################################################

def open_DSWfolder(operator_log, province_log, field_log, job_num_log):
	import os
	
	#os.chdir()

	field_string = os.path.join(r"\\","BHICalres01","Groups2","Inteq","Drilling Systems Well Files",province_log,field_log)
	
	#os.chdir(string)
	for filename in os.listdir(field_string):
		if filename.lower() in operator_log.lower():
			client = filename

	client_string = os.path.join(field_string, client)

	well_list = []
	for filename in os.listdir(client_string):
		well_list.append(filename)
		if str(job_num_log) in filename:
			well = filename
			well_string = os.path.join(client_string, well)
	
	os.startfile(well_string)
###########################################################################################################################################
def read_WL(WL, searchlines):

	'''
	Reads AER ST1 daily las file

	Takes WL, searchlines

	Return the
	'''
	import re
	import os
	import sys

	#with open("C:\\1Remote\\" + "0485418 WELLS0913.TXT", "r") as f:
	#	searchlines = f.readlines()
	lic_lines=[]
	x=0
	for i, line in enumerate(searchlines):
		if str(WL) in line:
			for l in searchlines[i+1:i+30]:
				if not re.search(r'(\d{7})',l):
					x +=1
					lic_lines = searchlines[i:i+x]
				else:
					break

	path_cwd = os.getcwd()
	if len(lic_lines) > 0:
		with open(path_cwd + "\\WL_" + WL + '.txt', 'a+') as f:
			sys.stdout = f
			#print('########################################################################################')
			#print('###########################    Well License:'+ WL +'    ###################################')
			#print('########################################################################################')
			#print('\n')
			for line in lic_lines:
				if len(line) >2:
					print(line)
			print('############################################################')
			#print('\n')

	sys.stdout = sys.__stdout__
	return
###########################################################################################################################################
def main(WL):
	import os
	import datetime
	from distutils.util import strtobool

	Year = datetime.date.today().strftime("%Y")
	pYear = str(int(Year)-1)

	Folder = os.path.join(r"\\","BHICalres01","Groups2","Inteq","Shared","1AER", Year)
	#tFolder = 'C:\\1AER\\' + Year
	if os.path.isdir(Folder):
		tmod = os.path.getmtime(Folder)
		dtmod = datetime.datetime.fromtimestamp(tmod)

		tnow = datetime.datetime.now()
		diff = tnow - dtmod
		#if diff > datetime.datetime(0,0,1):
		if diff > datetime.timedelta(days=10):
			print('Warning Last updated: ',diff)

		print('One Moment...')
		for root, dirs, files in os.walk(Folder, topdown=False):
			for name in files:
				#print(os.path.join(root, name))
				if '.txt'.lower() in name.lower():
					if 'WL'.lower() in name.lower() or 'WELL'.lower() in name.lower():
						with open(os.path.join(root,name),'r') as f:
							searchlines = f.readlines()
							read_WL(WL,searchlines)
	else:
		print('No 1AER directory found')
		print(Folder)

		with open('err_log.txt', "a+") as f:
			f.write('\n')
			f.write('Missing 1AER Directory, please check:')
			f.write(Folder)
			f.write('\n')
			f.write('############# END #############')
			f.write('\n')

		
		

	return
###########################################################################################################################################
	
def input_WL():
	import os
	import sys
	WL = input("Please enter Alberta Well License: ")
	WL_filename = 'WL_'+str(WL)+'.txt'
	if os.path.isfile(WL_filename):
		os.remove(WL_filename)

	with open(WL_filename, "a+") as f:
		sys.stdout = f
		print('#######################    Well License:'+ str(WL) +'    #######################')
		print('\n')
		sys.stdout = sys.__stdout__

	return WL	
###########################################################################################################################################

if __name__ == "__main__":
	import traceback
	import os
	try:
		import os
		
		WL=input_WL()
		main(WL)
		path_cwd = os.getcwd()		
		os.startfile(os.path.join(path_cwd,'WL_'+WL+'.txt'))
	
	except Exception as err:
		with open('err_log.txt', 'a') as f:
			f.write(str(err))
			f.write(traceback.format_exc())
			f.write('\n')
			f.write('############# END #############')
			f.write('\n')
		path_cwd = os.getcwd()				
		os.startfile(os.path.join(path_cwd,'err_log.txt'))