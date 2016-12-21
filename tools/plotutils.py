import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

colors = ['red', 'blue', 'yellow', 'green', 'cyan', 'violet']
                                                                                
def plotAverageTimeSeries(samplesDict, ylabel, outFile, title=None, strips='conf95', xlabel='Time', xlimit=None, disableStrips=False, legendLocation=4, dpi=300):
	'''Plots averages of several random time series. The samples must represented
     as a numpy matrix (each row is a sample) and stored as values in the
	   samplesDict dictionary. The keys of the dictionary will be used to annotate
	   the plot via legend. Error data is provided in the form of strips
	   surrounding each everage plot. What exactly the strip represents is
	   controlled by the strips option:
	     strips='conf95' (default) - 95% confidence interval (gaussian assumption)
	     strips='stderr' - raw standard error of the sum
	  Strips can be disabled by setting disableStrips to true, in which case they
	  are going to be replaced with errorbars around the points. This is useful
	  when the xlimit is low.
		The output is written in PNG format to outFile.
	'''
	import stats
	colorIdx = 0
	for tsname, tssamples in samplesDict.items():
		tsavg = np.mean(tssamples, axis=0)
		tsstderr = stats.timeSeriesStderr(tssamples)
		if strips == 'conf95':
			tsstderr *= 1.96
		elif strips == 'stderr':
			pass
		else:
			raise ValueError('Unsupported strip type {}. Supported types: conf95, stderr'.format(strips))
		lower = tsavg - tsstderr
		upper = tsavg + tsstderr

		time = np.arange(0,len(tsavg))
		if disableStrips:
			plt.errorbar(time, tsavg, color=colors[colorIdx], yerr=tsstderr, label=tsname)
		else:
			plt.plot(time, lower, time, upper, color=colors[colorIdx], alpha=0.5)
			plt.fill_between(time, lower, upper, where=upper>=lower, facecolor=colors[colorIdx], alpha=0.3, interpolate=True)
			plt.plot(time, tsavg, color=colors[colorIdx], label=tsname)

		colorIdx += 1

	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.legend(loc=legendLocation)
	if xlimit:
		plt.xlim(0, xlimit)
	if title:
		plt.title(title)

	plt.savefig(outFile, dpi=300)
	plt.close()
