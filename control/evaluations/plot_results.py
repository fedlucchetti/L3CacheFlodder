import numpy as np
import matplotlib.pyplot as plt
import sys, os, glob, json
from os.path import join, split


def get_data(quantity):
    directory  = join(split(os.path.realpath(__file__))[0],"results",quantity)
    start_times,end_times = np.array([0]),np.array([0])
    for path2file in os.listdir(directory):
        if "outdata" in path2file:
            data = np.load(join(directory,path2file))
            start_times = np.concatenate([start_times,data["start_time"]])
            end_times   = np.concatenate([end_times,data["end_time"]])
    start_times = np.concatenate([start_times,start_times])
    end_times   = np.concatenate([end_times,end_times])
    return start_times,end_times



start_withCF, end_withCF = get_data("CFon")
start_noCF  , end_noCF   = get_data("CFoff")
# start_CF    , end_CF     = get_data("cacheflodder")

# start_withCF, end_withCF = a.get_data("withCF")
# start_noCF  , end_noCF   = a.get_data("withoutCF")
# start_CF    , end_CF     = a.get_data("cacheflodder")

delta_withCF = end_withCF - start_withCF
delta_noCF   = end_noCF   - start_noCF
# delta_CF     = end_CF     - start_CF

delta_withCF = delta_withCF[np.where(delta_withCF!=0)[0]]
delta_noCF   = delta_noCF[np.where(delta_noCF!=0)[0]]
np.random.shuffle(delta_withCF)
np.random.shuffle(delta_noCF)
idx = np.min([len(delta_withCF),len(delta_withCF)])
print("Deadline misses:",len(np.where(delta_withCF>10)[0]))
# delta_withCF = delta_withCF[0:idx]
# delta_noCF   = delta_noCF[0:idx]
print("#########################################################")
print("######################## RESULTS ########################")
print("######################################################### \n")
print("################|####### AVG ############################")
print("ET   with    CF\t|", round(delta_withCF.mean(),3)," +-",round(delta_withCF.std(),3),"ms |\t N = ",delta_withCF.shape[0])
print("ET   without CF\t|", round(delta_noCF.mean(),3)," +-"  ,round(delta_noCF.std()  ,3),"ms |\t N = ",delta_noCF.shape[0])
# print("ET           CF\t|", round(delta_CF.mean(),3),"+-"  ,round(delta_CF.std()  ,3)     ,"ms |\t N = ",delta_CF.shape[0])
print("################|####### WCET ###########################")
print("WCET with    CF\t|", round(delta_withCF.max(),8)," ms")
print("WCET without CF\t|", round(delta_noCF.max(),8)  ,"  ms")
# print("WCET         CF\t|", round(delta_CF.max(),8)  ,"  ms")
print("################|####### 99.9 pc ########################")
print("99pc with    CF\t|", round(np.percentile(delta_withCF,99.99),6)," ms")
print("99pc without CF\t|", round(np.percentile(delta_noCF,99.99),6)," ms")
print("#########################################################")


plt.hist(delta_withCF,alpha=1,bins=15,label="with cache flooder",color="k")
plt.hist(delta_noCF,alpha=1,bins=15,label="without cache flooder",color="r")
plt.yscale('log')
plt.xlabel("Execution time [ms]",fontsize=16)
plt.ylabel("Counts",fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.grid(1)
plt.legend(fontsize=16)
plt.show()
