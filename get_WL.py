def get_WL():

	'''
	Takes no argument

	Returns: nothing

	Downloads all WELLSxx.TXT files from the first of the previous month to the current date
	Directory C:\\1AER
	'''
	import traceback
	try:
			
		print('-------Updating-------')
		import requests, bs4, webbrowser, sys, urllib
		import re
		import os

		res = requests.get('http://www.aer.ca/data/well-lic/st1.html')
		res.raise_for_status()

		links = []

		soup = bs4.BeautifulSoup(res.text, "lxml")
		for link in soup.find_all("a", attrs = {'href': re.compile("http://")}):
			links.append(link.get('href'))


		import datetime

		Year = datetime.date.today().strftime("%Y")
		Month = datetime.date.today().strftime("%m")
		day = datetime.date.today().strftime("%d")

		date = str(Month+day)
		refDATE = datetime.datetime(int(Year), int(Month)-1, 1)

		URL = 'http://www.aer.ca/data/well-lic/WELLS' + date + '.TXT'

		if int(Month) in (1,3,5,7,8,10,12):
			X = 31
		elif int(Month) in (4,6,9,11):
			X = 30
		else: X = 28 

		for i in range(1,X+1):
			num = "{0:02d}".format(int(Month)-1) + "{0:02d}".format(i)
			links.append('http://www.aer.ca/data/well-lic/WELLS' + num + '.TXT') 

		Folder = 'C:\\1AER\\' + Year
		if not os.path.exists(Folder):
			os.makedirs(Folder)


		for n, line in enumerate(links):
			res = requests.get(line)
			res.raise_for_status()
			file = open(Folder + '\\' + links[n][-13:] , "wb")
			for chunk in res.iter_content(100000):
				file.write(chunk)
			file.close

		print('-------Finished-------')
		path_cwd = os.getcwd()
		with open(os.path.join(path_cwd,'update.txt'), 'a+') as f:
			sys.stdout = f
			print('Finished 1AER Update: '+str(datetime.datetime.now()))
		sys.stdout = sys.__stdout__
		os.startfile(os.path.join(path_cwd,'update.txt'))
		
	except Exception as err:
		with open('err_log.txt', 'a') as f:
			f.write(str(err))
			f.write(traceback.format_exc())
			f.write('\n')
			f.write('############# END #############')
			f.write('\n')


if __name__ == '__main__':
	get_WL()