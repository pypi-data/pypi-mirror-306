from phmd import datasets

for ds in datasets.search(return_names=True):
    meta = datasets.read_meta(ds)

    if 'license' not in meta:
        print(ds)
