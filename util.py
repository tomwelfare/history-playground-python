from matplotlib import pyplot as plt

def plot_series(series,**kwargs):
	''' Plot a single series returned from the History Playground,
	i.e. plot_series(series[0])
	'''
	if series != None:
		display = kwargs.pop('display','rank')
		ylabel = __get_ylabel(display)
		dates = series[display].keys()
		values = series[display].values()
		fig = plt.plot(dates, values, label=series['term'] + ' (' + series['corpus'] + ')')
		plt.xticks(rotation=45)
		plt.legend(loc='upper left')
		plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
		plt.gca().set_xticklabels(__every_nth(dates,10))
		plt.setp(fig, linewidth=2.0)
		plt.xlabel('Year')
		plt.ylabel(ylabel)
		plt.show()

def plot_all_series(series,**kwargs):
	''' Plot all series returned from the History Playground '''
	if series != None:
		display = kwargs.pop('display','rank')
		ylabel = __get_ylabel(display)
		for s in series:
			dates = s[display].keys()
			values = s[display].values()
			fig = plt.plot(dates, values, label=s['term'] + ' (' + s['corpus'] + ')')
			plt.setp(fig, linewidth=2.0)
		plt.xticks(rotation=45)
		plt.legend(loc='upper left')
		plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
		plt.gca().set_xticklabels(__every_nth(dates,10))
		plt.xlabel('Year')
		plt.ylabel(ylabel)
		plt.show()

def __every_nth(dates,n):
	''' Return every nth label'''
	labels = list(dates)
	for i, l in enumerate(labels):
		val = int(l)
		if val % n != 0:
			labels[i] = ''
	return labels

def __get_ylabel(display):
	''' Set the y axis label depending on the time series display type'''
	ylabel = 'Work Rank Score'
	if display != 'rank':
		ylabel = 'Relative Frequency'
	return ylabel