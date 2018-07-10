from playground import histplygrd
import util

# Login to the playground (once)
plygrd = histplygrd.Playground()
plygrd.login('email','password')

# Select some queries and datasets
settings = (['dog','cat'], plygrd.available_datasets())

# Query the playground
series = plygrd.query(settings)

## (Optional) Plot the results
util.plot_all_series(series)
