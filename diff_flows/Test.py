from datetime import datetime
from time import time



timestamp = time()
dt_object = datetime.fromtimestamp(timestamp)

print("dt_object =", dt_object)
