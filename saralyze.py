import os
import sys

def process_lines(lines):

	firstline = lines.pop(0)
	system = firstline.split()[2][1:-1]
	date = firstline.split()[3]
	cpudata = ''
	memdata = ''
	loaddata = ''
	cpuindex = 0
	memindex = 0
	loadindex = 0

	for index, data in enumerate(lines):
		tokens = data.split()
		if len(tokens) > 2:
			if tokens[2] == 'CPU':
				cpuindex = index
			if tokens[2] == 'kbmemfree':
				memindex = index
			if tokens[2] == 'runq-sz':
				loadindex = index
	print cpuindex,memindex,loadindex

	cpudata = process_data(date, lines[cpuindex + 1:])
	memdata = process_data(date, lines[memindex + 1:])
	loaddata = process_data(date, lines[loadindex + 1:])

	return (cpudata, memdata, loaddata, system)

def process_data(date, lines):

	data = ''
	for line in lines:
		print line
		tokens = line.split()
		print tokens
		if len(line) < 2:
			continue
		if tokens[0] == 'Average:':
			break
		data = data + date + ',' + tokens[0] + ' ' + tokens[1] + ',' + ','.join(tokens[2:]) + '\n'
	return data


def main():

	cpudata = 'Date,Time,CPU,%user,%nice,%system,%iowait,%steal,%idle\n'
	memdata = 'Date,Time,kbmemfree,kbmemused,%memused,kbbuffers,kbcached,kbswapfree,kbswpused,%swpused,kbswpcad\n'
	loaddata = 'Date,Time,runq-sz,plist-sz,ldavg-1,ldavg-5,ldavg-15\n'

	directory = os.path.dirname(os.path.realpath(__file__))
	for item in os.listdir(directory):
		full_path = os.path.join(directory, item)
		if os.path.isfile(full_path) and item != __file__:
			with open(full_path) as f:
				lines = f.read().splitlines()
				results = process_lines(lines)
				cpudata = cpudata + results[0]
				memdata = memdata + results[1]
				loaddata = loaddata + results[2]


	with open(os.path.join(directory, results[3] + '-cpu.csv'), 'w') as f:
		f.write(cpudata)
	with open(os.path.join(directory, results[3] + '-mem.csv'), 'w') as f:
		f.write(memdata)
	with open(os.path.join(directory, results[3] + '-load.csv'), 'w') as f:
		f.write(loaddata)


if __name__ == '__main__':
	main()