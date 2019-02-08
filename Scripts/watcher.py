import os.path as path
import csv
import win32file
import win32con
import logging
import subprocess

path_to_watch = path.abspath(path.join(os.getcwd(), '../../..')) # look at C:/HISHTPService
file_to_watch = path.join(path_to_watch,'data')
log_file = path.join(path_to_watch, 'watcher.log')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handler
handler = logging.FileHandler(log_file, mode='w')
handler.setLevel(logging.INFO)

# Create logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s %(message)s')
handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(handler) 

def SendToPrinter(copies,
                  prtname,
                  filepath,
                  prttype):
  if filepath != "":
    for x in range(int(copies)):
      binpath = path.join(path_to_watch, 'bin')
      progname = path.join(binpath, 'PDFtoPrinter.exe')
      
      subprocess.call([progname ,filepath, prtname])
      #os.system(r'"C:/HISHTPService/bin/PDFtoPrinter.exe %s %s"' % (path, prtname))
  else:
    loggger.warning("File to print not created. Check HISHTP service")
  if copies == "":
    logger.warning("NoCopies is empty.")
  if prtname == "":
    logger.warning("PrinterName is empty.")

# Set up the bits we'll need for output
ACTIONS = {
  1 : "Created",
  2 : "Deleted",
  3 : "Updated",
  4 : "Renamed from something",
  5 : "Renamed to something"
}
FILE_LIST_DIRECTORY = 0x0001
hDir = win32file.CreateFile (
  path_to_watch,
  FILE_LIST_DIRECTORY,
  win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
  None,
  win32con.OPEN_EXISTING,
  win32con.FILE_FLAG_BACKUP_SEMANTICS,
  None
)


try:

  logger.info("PrintWatcher service is started.")

  with open(file_to_watch, "r") as a:
  
    # Throw everything in buffer
    a.read()
    # Wait for new data and call ProcessNewData for each new chunk that's written
    while 1:
      # Wait for a change to occur
      results = win32file.ReadDirectoryChangesW (
        hDir,
        1024,
        False,
        win32con.FILE_NOTIFY_CHANGE_LAST_WRITE,
        None,
        None
      )
    
      # For each change, check to see if it's updating the file we're interested in
      for action, file in results:
        full_filename = path.join (path_to_watch, file)
        #full_filename = PurePath.joinpath(path_to_watch, file)
        logger.info(full_filename, ACTIONS.get (action, "Unknown"))
    
        if full_filename == file_to_watch:
          last_line = a.readline()
          print(last_line)
          if(last_line != ''):
            csv_reader = csv.reader([last_line],skipinitialspace=True, delimiter=',')
            for row in csv_reader:
              
              logger.info("time=%s" % row[0])
              logger.info("noCopies=%s" % row[1])
              logger.info("prtName=%s" % row[2])
              logger.info("filename=%s" % row[3])
              logger.info("prtType=%s" % row[4])
          
            # Ready to process
            SendToPrinter(row[1],row[2],row[3],row[4])
            logger.info("Success printing.")

except FileNotFoundError:
  logger.error("Path to watch :%s" % (path_to_watch))
  logger.error("File to watch :%s" % (file_to_watch))
  logger.error("File named data is missing. Make sure HISHTP service is running.")
  logger.error("PrintWatcher service is exited with error(1).")
  
