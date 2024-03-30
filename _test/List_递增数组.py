import numpy as np
import json
arr = np.arange(40000, 50001, 40)
print(arr)
print(json.dumps(arr.tolist()))