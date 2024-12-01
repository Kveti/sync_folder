import os
import shutil
from datetime import datetime


log_path = r"C:\log.txt"


def set_log_path(path: str) -> None:
    global log_path
    log_path = path 


def log(entry: str) -> None:
    global log_path

    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%Y.%m.%d %H:%M:%S")
    log_entry = "[" + formatted_date + "] " + entry

    with open(log_path, 'a') as file:
        file.write("\n" + log_entry)
    print(log_entry)


def ls(dir: str) -> tuple:
    items = os.listdir(dir)
    files = [item for item in items if os.path.isfile(os.path.join(dir, item))]
    dirs = [item for item in items if os.path.isdir(os.path.join(dir, item))]

    return files, dirs
    

def cmp(src_file: str, dest_file: str) -> bool:
    try:
        with open(src_file, 'rb') as sf, open(dest_file, 'rb') as df:
            while True:
                s_chunk = sf.read(1024)
                d_chunk = df.read(1024)
                
                if s_chunk != d_chunk:
                    return False
                
                if not s_chunk and not d_chunk:
                    return True
    except Exception as e:
        print(f"During CMP an error occurred: {e}")
        return False



def cp(src_file: str, dest_file: str) -> None:
    try:
        shutil.copy2(src_file, dest_file)
        log(f"COPY file {src_file} to {dest_file}")
    except FileNotFoundError:
        print(f"In CP Source file {src_file} not found.")
    except Exception as e:
        print(f"During CP an error occurred: {e}")



def sync_file(src_file: str, dest_file: str) -> None:
    rm(dest_file)
    cp(src_file, dest_file)
    log(f"Syncing {src_file} to {dest_file}")


def rm(path: str) -> None:
    try:
        os.remove(path)
    except Exception as e:
        print(f"Duritng RM an error occurred: {e}")


def rmdir(path: str) -> None:
    try:
        shutil.rmtree(path)
    except Exception as e:
        print(f"Duritng RMDIR an error occurred: {e}")


def mkdir(path: str) -> None:
    try:
        os.mkdir(path)
    except FileExistsError:
        print(f"The directory {path} already exists. Therefore can not be created.")
    except Exception as e:
        print(f"During MKDIR an error occurred: {e}") 




def sync_folder(src_path: str, dest_path: str) -> None:
    src_files, src_dirs = ls(src_path)
    dest_files, dest_dirs = ls(dest_path)

    # the loop will go through the files.
    # The ones that are in the destination folder but not present in the source folder,
    # which I need to delete.
    for file in dest_files:
        if file not in src_files:
            path = os.path.join(dest_path, file)
            rm(path)
            log(f"REMOVED file: {path}")


    # the loop will go through files
    # in source folder
    for file in src_files:
        s_p = os.path.join(src_path, file)
        d_p = os.path.join(dest_path, file)
        
        # if folder is missing in destination folder
        # it will copy the missing folder
        if file not in dest_files:    
            cp(s_p, d_p)
        else:
            # if the file is present in destination folder, but is not same it will sync it
            if not cmp(s_p, d_p):
                sync_file(s_p, d_p)

    # The loop will go through the Directories.
    # The ones that are in the destination folder but not present in the source folder,
    # it will delete.
    for dir in dest_dirs:
        if dir not in src_dirs:
            # zmazem priečinok
            # zalogujem to
            # vymazem z dest_files
            path = os.path.join(dest_path, dir)
            rmdir(path)
            log(f"REMOVED directory: {path}")
        

    # the loop will check if the destination directory has all the folders
    # the source directory has. If not, the missing directory will be created
    for dir in src_dirs:
        if dir not in dest_dirs:
            path = os.path.join(dest_path, dir)
            mkdir(path)
            log(f"CREATED {path} directory")


    # the loop will run sync for all subdirectories
    for dir in src_dirs:
        s_p = os.path.join(src_path, dir)
        d_p = os.path.join(dest_path, dir)
        sync_folder(s_p, d_p)


