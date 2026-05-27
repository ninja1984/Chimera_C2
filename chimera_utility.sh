#!/bin/bash

# Define a function to check if a process is suspicious based on its PPID and command line arguments
check_suspicious_process() {
    local pid=$1
    local ppid=$(ps -o ppid= -p $pid)
    local cmdline=$(ps -o comm=,args= -p $pid | awk '{print $2}')
    
    # Check if the parent process ID (PPID) is 1 or not running (0)
    if [ "$ppid" = "1" ] || [ "$ppid" = "" ]; then
        echo "Suspicious: Process with PID $pid has an unusual parent PPID ($ppid). Command line: $cmdline"
    fi
}

# Define a function to audit processes based on their name or UID
audit_processes() {
    local process_name=$1
    local uid=$2
    
    # Use ps command with options to list all running processes
    ps -eo pid=,ppid=,uid=,comm=,args= | while read line; do
        IFS=' ' read -r pid ppid uid cmdline <<< "$line"
        
        # Check if the process name matches or UID is specified and not 0 (root)
        if [[ $cmdline == *$process_name* ]] || [ "$uid" != "0" ] && [ -n "$uid" ]; then
            echo "Process found: PID=$pid, PPID=$ppid, UID=$uid, Command=$cmdline"
            
            # Check if the process is suspicious
            check_suspicious_process $pid
        fi
    done
}

# Main script execution starts here
if [ "$#" -eq 0 ]; then
    echo "Usage: $0 <process_name> [UID]"
    exit 1
fi

# Get the process name and UID from command line arguments
process_name=$1
uid=${2:-}

# Audit processes based on the provided criteria
audit_processes "$process_name" "$uid"