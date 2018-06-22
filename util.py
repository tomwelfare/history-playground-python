from matplotlib import pyplot as plt

def plotSeries(series,**kwargs):
	if series != None:
		display = kwargs.pop('display','rank')
		ylabel = __getYLabel(display)
		dates = series[display].keys()
		values = series[display].values()
		fig = plt.plot(dates, values, label=series['term'] + ' (' + series['corpus'] + ')')
		plt.xticks(rotation=45) # rotate date labels
		plt.legend(loc='upper left')
		plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0)) # use scientific notation
		plt.gca().set_xticklabels(__everyNth(dates,10))
		plt.setp(fig, linewidth=2.0) # make the lines thicker
		plt.xlabel('Year')
		plt.ylabel(ylabel)
		plt.show()

def plotAllSeries(series,**kwargs):
	if series != None:
		display = kwargs.pop('display','rank')
		ylabel = __getYLabel(display)
		for s in series:
			dates = s[display].keys()
			values = s[display].values()
			fig = plt.plot(dates, values, label=s['term'] + ' (' + s['corpus'] + ')')
			plt.setp(fig, linewidth=2.0) # make the lines thicker
		plt.xticks(rotation=45) # rotate date labels
		plt.legend(loc='upper left')
		plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0)) # use scientific notation
		plt.gca().set_xticklabels(__everyNth(dates,10))
		plt.xlabel('Year')
		plt.ylabel(ylabel)
		plt.show()

def __everyNth(dates,n):
	labels = list(dates)
	for i, l in enumerate(labels):
		val = int(l)
		if val % n != 0:
			labels[i] = ''
	return labels

def __getYLabel(display):
	ylabel = 'Work Rank Score'
	if display != 'rank':
		ylabel = 'Relative Frequency'
	return ylabel