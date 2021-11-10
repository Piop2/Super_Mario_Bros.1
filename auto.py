# 69 70
# 86 87 88
# 153 154

import clipboard

data = {}
for i in range(0, 210):
    if not i in [69, 70, 86, 87, 88, 153, 154]:
        data[f"{i}.{13}"] = [0, 0]
        data[f"{i}.{14}"] = [0, 0]

clipboard.copy(str(data)[1:-1].replace("'", '"'))