from phmd import datasets
import json
md5sum_L = 32

base_code = "68747470733a2f2f66696c65646e2e65752f6c6f58704972546e454a4e7071634d6e5156586578396d2f50686d4461746173657473"

for ds in datasets.search(return_names=True):
    meta = datasets.read_meta(ds)
    jsonfile = json.load(open(f'../datasets/{ds}.json', 'r'))

    for i in range(len(meta['files'])):
        #url = meta['files'][i]['urls'][0]['url']
        if len(meta['files'][i]['md5sum']) <= 32:
            print(ds, len(meta['files'][i]['md5sum']))
        continue

        """
        url = url.replace("https://filedn.eu/loXpIrTnEJNpqcMnQVXex9m/PhmDatasets", "")
        print(url)
        code = ''.join(map((lambda c: hex(ord(c))[2:]), url))

        print(code)

        jsonfile = json.load(open(f'../datasets/{ds}.json', 'r'))
        jsonfile['files'][i]['md5sum'] += code
        json.dump(jsonfile, open(f'../datasets/{ds}.json', 'w'), indent=4)

        code = base_code + code
        decode = ''.join(map((lambda h: chr(int(''.join(h), 16))), zip(code[::2], code[1::2])))

        print(decode)
        print("------------------")
        
        """