import re
import collections

data = collections.defaultdict(list)
pat = re.compile(r'(ov\d+_[0-9A-F]{8}): ; (0x[0-9A-F]{8})')
with open('tmp.s') as fp:
    for line in fp:
        if (m := pat.match(line)) is not None:
            data[int(m[2], 0)].append(m[1])
for addr, labels in data.items():
    if len(labels) == 1:
        print(f's/sub_{addr:08X}/{labels[0]}/g')
