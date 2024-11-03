from phmd import download
from phmd import datasets

#X = download.download('JNUB', force=True)

#X = datasets.load('JNUB', 'fault', force_download=True)

#print(X.shape)

#datasets.Dataset.search(task="detection")

ds = datasets.Dataset("CWRU")
print(ds.describe())
task = ds['fault']
fold = task[0]

print(fold.keys())
