from playground import histplygrd
import util

plygrd = histplygrd.Playground()

plygrd.login('email','password')

queries = ['dog','cat']
datasets = plygrd.availableDatasets()

series = plygrd.query(queries, datasets)

## Plot the series
util.plotAllSeries(series)
