#!/usr/bin/env python3

import os, sys
from cyber.python.cyber_py3 import cyber
# from cyber.proto.unit_test_pb2 import  LatencyStats
# from modules.control1.proto.unit_test_pb2                import  LatencyStats
# from modules.control1.proto.unit_test_pb2                import  ChacheFlodderTrigger

# from modules.common_msgs.control_msgs.control_cmd_py_pb2 import  ControlCommand
# import modules.common_msgs.control_msgs.control_cmd_py_pb2 
from modules.common_msgs.control_msgs import control_cmd_pb2
ControlCommand = control_cmd_pb2.ControlCommand

# from modules.control1.proto.control_cmd_py_pb2 import  LatencyStats

import time
import numpy as np
import matplotlib,sys
from itertools import count
import os
from os.path import join

index = count()
# CHANNEL = "/apollo/control_flodded"
CHANNEL = "/apollo/control"

MODE=sys.argv[1]

NPURGE    = 1000

TONSET = time.time()
directory=join("modules","control","evaluations","results",MODE)
directory="/apollo/"+directory
if not os.path.exists(directory):
    os.makedirs(directory)


class Listen2Channels(object):
    def __init__(self):
        """

        """

        self.start_time  = np.zeros([NPURGE])
        self.end_time    = np.zeros([NPURGE])
        self.id_buffer   = 0
        self.id_file     = 0
        self.directory   = directory



    def monitor_control(self,data):
        """
        Original (normal) module
        """
        self.id_buffer+=1
        self.start_time[self.id_buffer] = data.start_time
        self.end_time[self.id_buffer]   = data.end_time
        print(self.id_buffer,self.start_time[self.id_buffer],self.end_time[self.id_buffer])
        os.system("clear")
        if self.id_buffer>NPURGE-5:
            outpath=join(self.directory,"outdata_"+str(self.id_file)+".npz")
            np.savez(outpath,
                start_time=self.start_time,
                end_time=self.end_time,
                )

            print("Wrote to file ",outpath,"at t=",time.time()-TONSET)
            self.id_buffer=0
            self.id_file+=1




    def run(self):
        cyber.init()
        test_node = cyber.Node("listen2Control")
        test_node.create_reader(CHANNEL, ControlCommand, self.monitor_control)
        test_node.spin()
        cyber.shutdown()


if __name__ == '__main__':
    app=Listen2Channels()
    app.run()
