import argparse
import os
import time
from folder_sync import *
import re


def parse_time_period(time_period: str) -> int:
    # Regular expression to capture the number and the unit (seconds, minutes, hours, days)
    match = re.match(r'^(\d+)(s|min|h|d)$', time_period)
    
    value = int(match.group(1))  # Numeric part
    unit = match.group(2)        # Unit part ('s', 'min', or 'h')
    
    # Convert the time to seconds based on the unit
    if unit == "s":
        return value  # Seconds remain the same
    elif unit == "min":
        return value * 60  # Convert minutes to seconds
    elif unit == "h":
        return value * 3600  # Convert hours to seconds
    elif unit == "d":
        return value * 86400 # Convert days to seconds



def sleep(time_period) -> None:
    t = parse_time_period(time_period)
    time.sleep(t)



def read_parameters() -> tuple[str, str, str]:
    parser = argparse.ArgumentParser(description="Script that synchronizes two folders")
    parser.add_argument('--src_path', type=str, required=True, help="Source path")
    parser.add_argument('--dest_path', type=str, required=True, help="Destination path")
    parser.add_argument('--log_path', type=str, required=True, help="log path")
    parser.add_argument('--sync_period', type=str, required=True, help="The time period during which synchronization is performed. which synchronization is performed. It can be specified in seconds (s), minutes (min), hours (h), or days (d).")
    args = parser.parse_args()

    return args.src_path, args.dest_path, args.log_path, args.sync_period


def check_param(src_path: str = None, dest_path: str = None, log_path: str = None, sync_period: str = None) -> None:
    if src_path != None and not os.path.exists(src_path):
        raise ValueError(f"Error: Source path {src_path} does not exist.")
    
    if dest_path != None and not os.path.exists(dest_path):
        raise ValueError(f"Error: Destination path {dest_path} is not a valid directory.")
        
    if log_path != None and not os.path.isdir(os.path.dirname(log_path)):
        raise ValueError(f"Error: Log directory for {log_path} is invalid.")

    if sync_period != None:
        match = re.match(r'^(\d+)(s|min|h|d)$', sync_period)
    
        if not match:
            raise ValueError(f"Error: Invalid time period format: {sync_period}")


def main() -> int:
    src_path, dest_path, log_path, sync_period = read_parameters()

    try:
        check_param(src_path, dest_path, log_path, sync_period)
    except Exception as e:
        print(e)
        return 1

    set_log_path(log_path)

    try:
        while True:
            log("Syncing in progress ")
            sync_folder(src_path, dest_path)
            sleep(sync_period)
    except KeyboardInterrupt:
        log("Synchronization has finished.")

    return 0


if __name__ == "__main__":
    ec = main()
    exit(ec)



