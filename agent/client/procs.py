import os
import re
import subprocess


class Procs():
	def _cpu_count(self):
		# General
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
		# BSD
		try:
			sysctl = subprocess.Popen(['sysctl', '-n', 'hw.ncpu'],stdout=subprocess.PIPE)
			scStdout = sysctl.communicate()[0]
			res = int(scStdout)
			if res > 0:
				return res
		except (OSError, ValueError):
			pass
		# Linux
		try:
			res = open('/proc/cpuinfo').read().count('processor\t:')
			if res > 0:
				return res
		except IOError:
			pass
	
	def _mem_size(self):
		meminfo = open('/proc/meminfo').read()
		matched = re.search(r'^MemTotal:\s+(\d+)', meminfo)
		if matched: 
			return float(matched.groups()[0])/(1024*1024) - 1
		return 0
