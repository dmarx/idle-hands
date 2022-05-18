import pandas as pd
import time
from pynvml import (
    nvmlInit, 
    nvmlDeviceGetCount,
    nvmlDeviceGetHandleByIndex,
    nvmlDeviceGetMemoryInfo,
)

try:
    nvmlDeviceGetCount()
except NVMLError:
    nvmlInit()

df_hist = pd.DataFrame()

def probe_gpu_utilization():
    recs = []
    n = nvmlDeviceGetCount()
    for i in range(n):
        handle = nvmlDeviceGetHandleByIndex(i)
        info = nvmlDeviceGetMemoryInfo(handle)
        rec = {k:getattr(info, k) for k in ('free','total','used')}
        rec['ts'] = time.time()
        rec['device_id'] = i
        rec['perc_util'] = rec['used'] / rec['total']
        recs.append(rec)
    return recs

util = probe_gpu_utilization()
df_now = pd.DataFrame(util)
df_hist = pd.concat([df_hist, df_now])
df_hist

class GpuMonitor:
    def __init__(
        self,
        cache_duration = 1800, # 30min
        probe_interval = 300, # 5min
        utilization_threshold = .1,

    ):
        self.cache_duration = cache_duration
        self.probe_interval = probe_interval
        self.df = pd.DataFrame()
    def go(self):
        pass
