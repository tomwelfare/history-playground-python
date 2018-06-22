from playground import histplygrd
import util

# Login to the playground (once)
plygrd = histplygrd.Playground()
plygrd.login('email','password')

# Select some queries and datasets
queries = ['dog','cat']
datasets = plygrd.available_datasets()

# Query the playground
series = plygrd.query(queries, datasets)

## (Optional) Plot the results
util.plot_all_series(series)
