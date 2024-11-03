from pcloud import PyCloud
from datasets import *

from phmd.datasets import load
from phmd.download import download


X = load('CBMv3', task='ptdsc_port', datasets=['data'])


# PRONOSTIA
download('PRONOSTIA', unzip=True)
X_train, X_test = load('PRONOSTIA', task='rul', datasets=['train', 'test'])
X_train.to_csv('/home/dasolma/pronostia_train.csv', index=False)
X_test.to_csv('/home/dasolma/pronostia_test.csv', index=False)

exit()

# CALCE_A123
download('CALCE_A123', unzip=True)
X = load('CALCE_A123', task='soc_estimation', datasets=['data'], params={'soc_estimation_ahead_cycles': 20},  )[0]

print(X.shape)

print("train")
print("Memory usage: ", X.memory_usage(deep=True).sum() * 1e-6, "MB")
print("Memory usage: ", X.memory_usage(deep=True).sum() * 1e-9, "GB")

exit()

# CALCE_CS2
download('CALCE_CX2', unzip=True)
X = load('CALCE_CX2', task='soc_estimation', datasets=['data'], params={'soc_estimation_ahead_cycles': 20},  )[0]

print(X.shape)

print("train")
print("Memory usage: ", X.memory_usage(deep=True).sum() * 1e-6, "MB")
print("Memory usage: ", X.memory_usage(deep=True).sum() * 1e-9, "GB")


exit()

# STEELPLATES
download('STEELPLATES', unzip=True)
X = load('STEELPLATES', task='fault_diagnosis', datasets=['data'],)[0]

print(X.shape)

print("train")
print("Memory usage: ", X.memory_usage(deep=True).sum() * 1e-6, "MB")
print("Memory usage: ", X.memory_usage(deep=True).sum() * 1e-9, "GB")


exit()

download('PHM10CNCMILLING', unzip=True)
Xs = load('PHM10CNCMILLING', task='wear_estimation', datasets=['train', 'test'],)

Xt, Xtest = Xs
print(Xt.head())

print(Xt.shape)
print(Xt.columns)
print(Xt.unit.unique())
print(Xt.unit.unique().shape)

print("train")
print("Memory usage: ", Xt.memory_usage(deep=True).sum() * 1e-6, "MB")
print("Memory usage: ", Xt.memory_usage(deep=True).sum() * 1e-9, "GB")

print("test")
print("Memory usage: ", Xtest.memory_usage(deep=True).sum() * 1e-6, "MB")
print("Memory usage: ", Xtest.memory_usage(deep=True).sum() * 1e-9, "GB")


# NCMAPSS
download('NCMAPSS', unzip=True)
X = load('NCMAPSS', task='RUL', datasets=['data'],)[0]

print(X.shape)

print("train")
print("Memory usage: ", X.memory_usage(deep=True).sum() * 1e-6, "MB")
print("Memory usage: ", X.memory_usage(deep=True).sum() * 1e-9, "GB")


exit()
