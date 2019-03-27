#!/usr/bin/python

'''
Description: 
    1).This script will get CPU and Memory of particular process and print stats in Graphite fomat if argument is -p or --process_name
    2). This script can kill process by name if argument is -k or --kill_process
Author: AdilM 20181024
Version: 1.0
'''

import psutil
import platform
import datetime
import json
import argparse
import time
import sys

class getcpu:
 os, name, version, _, _, _ = platform.uname()
 
 # kill process 
 def kill_process(self,pid):
    try:
        parent = psutil.Process(pid)
        for child in parent.children(recursive=True): 
            print "Killing child process if any....",
            child.kill()
        print "Killing process having ID: ",pid," Name: ",parent.name(),"......"
        print parent
        parent.kill()
    except Exception as ex:
        print ("Ops! Error Occur while killing process", str(ex))
        sys.exit(1)
 
 
 def tell_system_status(self):
        os, name, version, _, _, _ = platform.uname()
        version = version.split('-')[0]
        cores = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory()[2]
        disk_percent = psutil.disk_usage('/')[3]
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        running_since = boot_time.strftime("%A %d. %B %Y")
        response = "I am currently running on %s version %s.  " % (os, version)
        response += "This system is named %s and has %s CPU cores.  " % (name, cores)
        response += "Current disk_percent is %s percent.  " % disk_percent
        response += "Current CPU utilization is %s percent.  " % cpu_percent
        response += "Current memory utilization is %s percent. "
        p = psutil.Process(1191)
        # p = p.cpu_percent / psutil.cpu_count()
        print "process is", p.cpu_percent()
        # response += "it's running since %s." % p
        return response
 def pids_active(self,pids_computer):
    pid_valid = {}
    for pid in pids_computer:
        data = None
        try:
            process = psutil.Process(pid)
            data = {"pid": process.pid,
                    "status": process.status(),
                    "percent_cpu_used": process.cpu_percent(interval=0.0),
                    "percent_memory_used": process.memory_percent()}

        except (psutil.ZombieProcess, psutil.AccessDenied, psutil.NoSuchProcess):
            data = None

        if data is not None:
            pid_valid[process.name()] = data
    return pid_valid 

 def find_process(self,process_name):
    print "Searching process having name ", process_name
    for proc in psutil.process_iter():
        cmdline = proc.cmdline(); 
        if process_name in cmdline and "/usr/bin/python" not in cmdline and "grep" not in cmdline: 
            return proc.pid
        
        
        # print "Process not found"

 def grep_pro(self,process_name):
    process_found = {}
    data = None
    for proc in psutil.process_iter():
        cmdline = proc.cmdline()
        if process_name in cmdline and "/usr/bin/python" not in cmdline and "grep" not in cmdline: 
            data =  {"pid": proc.pid,
                    "status": proc.status(),
                    "percent_cpu_used": proc.cpu_percent(interval=0.2),
                    "percent_memory_used": proc.memory_percent()}
    if data is not None:
         process_found = data
         return process_found
    else:
        return "Not Found"
        
myobj=getcpu()

parser = argparse.ArgumentParser(description='Process CPU usage and memory Monitor')
parser.add_argument("-p", "--process_name", metavar='process_name', help="Process Name or part of cmd", type=str, required=False)
parser.add_argument("-k", "--kill_process_name", metavar='kill_process_name', help="Process Name which need to kill", type=str, required=False)
parser.add_argument("-kid", "--kill_process_id", metavar='kill_process_id', help="Process ID which need to kill", type=int, required=False)
parser.add_argument("-pid", "--process_id", required=False) 
args = parser.parse_args()
kill_process_name=args.kill_process_name


if args.process_name is not None:
    proc_info=myobj.grep_pro(args.process_name)
    if proc_info != "Not Found":
        dictionaryToJson = json.dumps(proc_info)
        jsonToPython = json.loads(dictionaryToJson)
        print "stats.cpu."+args.process_name.split("/")[-1]+"."+myobj.name+"cpu", jsonToPython['percent_cpu_used'], int(time.time())
        print "stats.memory."+args.process_name.split("/")[-1]+"."+myobj.name+"mem", jsonToPython['percent_memory_used'], int(time.time())
        print "pid."+myobj.name, jsonToPython['pid'], int(time.time())
    else:
        print "Process Not Found"
elif args.kill_process_id is not None:
    print "Kill process by id", args.kill_process_id
    parent_pid = args.kill_process_id
    myobj.kill_process(args.kill_process_id)
elif kill_process_name is not None and "logagent" in kill_process_name:
    print "Kill process by name", kill_process_name
    get_process_id=myobj.find_process(kill_process_name)
    if get_process_id is not None:
        myobj.kill_process(get_process_id)
        exit(0)
    else:
        print "Process Not Found"
        exit(1)
elif kill_process_name is not None:
    if "logagent" not in kill_process_name:
        print "You cant kill other process now like #",kill_process_name,".  please contact devops"
        exit(1)
else:
    parser.print_help(sys.stderr)
