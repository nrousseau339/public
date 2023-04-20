from ipaddress import IPv4Address, ip_address
import os
from pythonping import *
from datetime import datetime
import time
import pandas as pd
import matplotlib.pyplot as plot
import matplotlib.animation as animation

ip = "8.8.8.8"
path = "C:\\Users\\nrousseau\\Desktop\\" + ip + "_ping.csv"
results = []
i = 0
sts = 'n'

f = open(path, "w")
f.write('Target, SysTime, RespTime\n')
      
while sts != 'y':
    try:
        p_res = ping(ip,timeout=5)
        t =  p_res.rtt_avg_ms
        print(p_res)
        results.append([ip,datetime.now().strftime('%D %H:%M:%S'),t])
        f.write(ip + ', ' + datetime.now().strftime('%D %H:%M:%S') + ', '+str(t) +'\n')
        time.sleep(1)
        i += 1
        
    except KeyboardInterrupt:
        sts = input("quit? (y/n)")
        if sts == 'y':
            i=10

f.close()
print(results)


##pandas matplotlib


df = pd.DataFrame(results,columns=['Target', 'SysDate', 'ResponseTime'])
print(df)
df.plot.line()
plot.show(block=True)



