import subprocess
import toml
import os
import shutil
import time
import logging

LOG_FILE_NAME = 'mover.log'
SOURCE = 'source'
DESTINATION = 'destination'
FILE_NAME = 'filename'
CREDENTIALS = 'credentials.toml'
CONFIG = 'config.toml'
NETWORK_PATH ='networkPath'

def validate(config):
    if os.path.isdir(config[SOURCE]) == False:
        logging.error("Source folder doest exists")
        print("Source folder doest exists")
        return False

    if os.path.isdir(config[DESTINATION]) == False:
        print("Destination folder doest exists")
        logging.error("Destination folder doest exists")
        return False
    return True

def read_config(filename):
    if os.path.isfile(filename) == False:
        print("config file " + filename + " doest exists")
        logging.error("config file " + filename + " doest exists")
        os._exit(2)
    configfile = os.path.expanduser(filename)

    if os.path.isfile(configfile):
        with open(configfile, 'r') as f:
            config = toml.loads(f.read())
            return config


def connect(config):
    networkPath = config[NETWORK_PATH]
    user = config['user']
    password = config['password']
    winCMD = 'NET USE ' + networkPath + ' /User:' + user + ' ' + password
    try:
        subprocess.Popen(winCMD, stdout=subprocess.PIPE, shell=True)
        print(subprocess.check_output(winCMD))
        logging.info(subprocess.check_output(winCMD))
    except Exception as ex:
        logging.error(ex)
        print(ex)
        os._exit(1)


def mover(src,dest,filename):
    listOfFiles = getListOfFiles(src)

    if len(listOfFiles) == 0:
        return

# only moves first file
    try:
        print("moving file " + src+'\\'+listOfFiles[0] + " to " +dest+'\\'+filename)
        logging.info("moving file " + src+'\\'+listOfFiles[0] + " to " +dest+'\\'+filename)
        shutil.move(src+'\\'+listOfFiles[0],dest+'\\'+filename)
    except Exception as ex:
        logging.info(ex)
        print(ex)


def getListOfFiles(src):
    return os.listdir(src)

def setLogger():
    # logging.basicConfig(filename = LOG_FILE_NAME , level = logging.INFO)
    logging.basicConfig(filename = LOG_FILE_NAME, level = logging.INFO,\
    format="%(asctime)s - %(name)s - %(message)s")

if __name__ == "__main__":
    setLogger()
    print( "initializing program")
    logging.info( "initializing program")
    credentials = read_config(CREDENTIALS)
    config = read_config(CONFIG)
    
    print("connecting to remote " + credentials[NETWORK_PATH]) 
    logging.info("connecting to remote " + credentials[NETWORK_PATH]) 
    connect(credentials)

    print("validating" )
    logging.info("validating" )
    if validate(config) == False:
        print("program exiting")
        logging.info("program exiting")
        os._exit(1)

    print('waiting for files')
    logging.info('waiting for files')
    while True:
        mover(config[SOURCE],config[DESTINATION],config[FILE_NAME])
        time.sleep(10)

    raw_input('press enter button to exit\n')

