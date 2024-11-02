import gifnoc
from gifnoc.config import time
from gifnoc.std.time import FrozenTime

for i in range(10):
    with gifnoc.use({"time": FrozenTime(sleep_beat=0.1)}):
        time.sleep(100)
        print("coucou!")
    time.sleep(1)
    # print("!")
    # time.sleep(1)
