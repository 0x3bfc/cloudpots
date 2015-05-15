import os
import re
import subprocess


class Procs():

	# get count of CPUs on Host
	def _cpu_count(self):
		# anything
		try:
			m = re.search(r'(?m)^Cpus_allowed:\s*(.*)$',
			open('/proc/self/status').read())
			if m:
				res = bin(int(m.group(1).replace(',', ''), 16)).count('1')
				if res > 0:
					return res
		except IOError:
			pass
		# Python 2.6+
		try:
			import multiprocessing
			return multiprocessing.cpu_count()
		except (ImportError, NotImplementedError):
			pass
		# BSD distributions
		try:
			sysctl = subprocess.Popen(['sysctl', '-n', 'hw.ncpu'],stdout=subprocess.PIPE)
			scStdout = sysctl.communicate()[0]
			res = int(scStdout)
			if res > 0:
				return res
		except (OSError, ValueError):
			pass
		# Other Linux distributions
		try:
			res = open('/proc/cpuinfo').read().count('processor\t:')
			if res > 0:
				return res
		except IOError:
			pass

	# get memory size of current host
	def _mem_size(self):
		meminfo = open('/proc/meminfo').read()
		matched = re.search(r'^MemTotal:\s+(\d+)', meminfo)
		if matched: 
			return float(matched.groups()[0])/(1024*1024) - 1
		return 0

	# execute command line
	def _exec(self, command, option=None):
		pipe = subprocess.PIPE
		p = subprocess.Popen(command,stdout=pipe,stderr=pipe,shell=True)
		if option == 'wait':
			p.wait()
		return p.stdout.read()+"\n"+p.stderr.read()
