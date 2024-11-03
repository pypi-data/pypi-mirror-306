from phmd import datasets

#datasets.describe('CMAPSS')

#datasets.search()

datasets.search(domain="drive", nature='time-series')

print(datasets.search(domain="drive", nature='time-series', return_names=True))

datasets.describe('CWRU')