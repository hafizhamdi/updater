#!/bin/python

# Script updater.py
# Check update for application to the latest version

import urllib.request as request
import os.path as path
import os
import ctypes
import logging

# define
OK = 1
NOK = 0


htpdir = path.abspath(path.join(os.getcwd(), '../../..'))
log_file = path.join(htpdir + '\\log','updater.log')
os.makedirs(os.path.dirname(log_file), exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handler
handler = logging.FileHandler(log_file, mode='w')
handler.setLevel(logging.INFO)

# Create logging format
formatter = logging.Formatter('%(asctime)s %(levelname)s : %(message)s')
handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(handler) 
    
def remove_dot(input):
  ori = input
  rem = ori.replace('.','')
  return rem

def get_local_version():
  res = ''
  file = path.join(os.getcwd(),'update')
  with open(file,'r') as read:
    res = read.readline()  
  trim = str(res).rstrip('\r\n')
  trunc = trim[15:]
  return remove_dot(trunc)

def compare_version(local,remote):

  logger.info("Current Local version [%s]" % local)
  logger.info("Latest Remote version [%s]" % remote)
  needUpdate = 0
  if(local == remote):
    needUpdate = 0
    logger.info("No update. Application has the latest version")
  if(local < remote):
    needUpdate = 1
    logger.info("Require update to the latest version")

  return needUpdate

def get_remote_version():  
  res = request.urlopen('https://raw.githubusercontent.com/hafizhamdi/updater/master/update.txt')
  line = res.readline()
  sres = str(line, 'utf-8').strip()
  ver = sres[14:]
  return remove_dot(ver)

def confirm(local, remote):
  MessageBox = ctypes.windll.user32.MessageBoxW
  return MessageBox(None, 'Current v%s. Confirm download the latest patches v%s?' % (local, remote ), 'Confirm', 1)  
  
def padzero(version):
  return str(version).zfill(5)

def backup():
  import subprocess as p  
  sts = NOK
  try:
    bindir = path.abspath(path.join(os.getcwd(),'../..'))
    bkpscr = path.join(bindir, 'backup.bat')
    p.call([bkpscr,'/b'])
    logger.info("Backup files... success")
    sts = OK
  except:
    logger.error("Backup files error")
    sts = NOK
  finally:
    return sts

def download(version):
  import requests,zipfile,io
  sts = NOK
  try:
    patch = 'Patches/HFX' + padzero(version) + '/HISHTPService.zip'
    url = 'https://github.com/hafizhamdi/updater/raw/master/' + patch
    logger.info(url)
    r = requests.get(url)
    logger.info("Request return %s" % (r.ok))
    z = zipfile.ZipFile(io.BytesIO(r.content))
    cfolder = path.abspath(path.join(os.getcwd(), '../../../..'))
    
    z.extractall(cfolder)
    
    MessageBoxW = ctypes.windll.user32.MessageBoxW  
    MessageBoxW(None, 'Program has successfully updated', 'HISHTPService Updating...', 1)  
    sts = OK
  except:
    MessageBoxW = ctypes.windll.user32.MessageBoxW  
    MessageBoxW(None, 'Updating Error', 'Updating...', 1)  
    sts = NOK
  finally:
    return sts

def append_dot(version):
  res = ''
  for i in range(len(version)):
    res += version[i] + '.'
  
  return res[:-1]

def update_localv(ver):
  try:
    with open('update','w') as f:
      f.write('CurrentVersion:' + append_dot(ver))
    logger.info("Updating local version %s success" % (ver))
  except:
    logger.error("Updating local version failed.")

def stop_services():
  import subprocess as p  
  sts = NOK
  try:
    bindir = path.abspath(path.join(os.getcwd(),'../..'))
    stopscr = path.join(bindir, 'stop_services.bat')
    p.call([bkpscr])
    logger.info("Stop services... success")
    sts = OK
  except:
    logger.error("Stop services error")
    sts = NOK
  finally:
    return sts

remote = get_remote_version()
local = get_local_version()

if 1 == compare_version(local,remote):
  #print(confirm())
  if 1 == confirm(local,remote):
    ss = stop_services() # Stop running services HISHTP Service and Print Watcher 
    if OK == backup(): # Backup data to bkp under C directory
      if OK == download(remote): # Check downloading
        update_localv(remote) # Sucess, update local version 