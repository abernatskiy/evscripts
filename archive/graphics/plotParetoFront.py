#!/usr/bin/python2

def connectionCost(netDesc):
	return sum([0.0 if x==0.0 else 1.0 for x in netDesc])

def rightLadder(x, y):
	N = len(x)
	if len(y) != N:
		raise ValueError('ladder() takes two arrays of equal size')
	xp = []
	yp = []
	for i in xrange(N-1):
		xp.append(x[i])
		yp.append(y[i])
		xp.append(x[i])
		yp.append(y[i+1])
	xp.append(x[N-1])
	yp.append(y[N-1])
	return xp, yp

class ParetoPlotter(object):
	def __init__(self, filename):
		self.filename = filename
		self.paretoFront = {}
		with open(filename, 'r') as file:
			for line in file:
				self._parseLine(line)

	def _parseLine(self, line):
		if line[0] == '#' or line == '':
			return
		fvals = map(float, line.split())
		objpair = (fvals[0], connectionCost(fvals[2:]))
		indiv = (int(fvals[1]), fvals[2:])
		if not self.paretoFront.has_key(objpair):
			self.paretoFront[objpair] = []
		self.paretoFront[objpair].append(indiv)

	def __str__(self):
		return '{' + ',\n\n '.join(map(str, sorted(self.paretoFront.iteritems()))) + '}'

	def dataForPlot(self):
		fit = []
		cc = []
		size = []
		for key in sorted(self.paretoFront.keys()):
			fit.append(-1.0*key[0])
			cc.append(key[1])
			size.append(32*len(self.paretoFront[key]))
		return fit, cc, size

	def _plot(self):
		f,c,s = self.dataForPlot()

		fp, cp = rightLadder(f, c)
		plt.plot(fp, cp, color='b', lw=3, zorder=1)

		plt.scatter(f, c, marker='o', c='r', s=s, label='Pareto front', lw=0, zorder=2)

		plt.grid()

		plt.xlabel('-1.0*fitness')
		plt.ylabel('connection cost')
		plt.title('Pareto front from file ' + self.filename)

	def savePlot(self, figname):
		self._plot()
		plt.savefig(figname)

	def showPlot(self):
		self._plot()
		plt.show()

if __name__ == '__main__':
	import argparse
	cliParser = argparse.ArgumentParser(description='Pareto front plotter')
	cliParser.add_argument('filename', metavar='filename', type=str, help='name of the log file to plot')
	cliParser.add_argument('-i', dest='interactive', action='store_const', const=True, default=False, help='only show interactive Matplotlib plot window')
	cliParser.add_argument('-V', dest='view', action='store_const', const=True, default=False, help='open Gwenview when done with plotting')
	cliArgs = cliParser.parse_args()

	import matplotlib
	p = ParetoPlotter(cliArgs.filename)
	if cliArgs.interactive:
		import matplotlib.pyplot as plt
		p.showPlot()
	else:
		matplotlib.use('Agg')
		import matplotlib.pyplot as plt
		outfilename = cliArgs.filename + '.png'
		p.savePlot(outfilename)
		if cliArgs.view:
			import subprocess
			subprocess.call(['gwenview', outfilename])
