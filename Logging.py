#### TODO:
#    - look to see how the logging module has changed since 2.5.3,
#    especially the hard-coded, version-dependent hack (look for
#    CHECK_MEs)
#    - make the location of the configuration file configurable by
#    client code
#    - update module docstring as needed
#######################################

"""
This module sets up the Python logging module for use by the DataCollector
system. The goal is to have an easily configured subsystem that allows each
module to have its own logging facility. We will use the various levels defined
by the logging module, DEBUG, INFO, WARNING, ERROR and CRITICAL, to control
which messages get displayed at any given time. We will also route certain
messages to a console display as appropriate. (In principle, it would be
possible to route log messages to the status bar on the main window frame, but
this is not currently being done.)

We use rotating files based on file size to capture log output.

We also want to catch otherwise uncaught exceptions and log those specially -
they represent surprises we had not anticipated.

sys.excepthook( type, value, traceback) 

This function prints out a given traceback and exception to sys.stderr.  When an
exception is raised and uncaught, the interpreter calls sys.excepthook with
three arguments, the exception class, exception instance, and a traceback
object. In an interactive session this happens just before control is returned
to the prompt; in a Python program this happens just before the program
exits. The handling of such top-level exceptions can be customized by assigning
another three-argument function to sys.excepthook.

We will attach to the main unhandled exception hook and use that to funnel
uncaught exceptions to a logger at CRITICAL level (possibly attaching these to
an email handler!)

The above functionality is implemented by DCErrorTrap in DataCollector.py
"""

########### RECENT CHANGES
## $Log: Logging.py,v $
## Revision 1.11  2010/12/17 19:25:16  hank
## Added some notes in preparation for moving past Python 2.5.4.
##
## Revision 1.10  2010/01/17 18:20:23  hank
## Add 'root' to imports from logging module.
##
## Revision 1.9  2010/01/13 12:37:34  godzilla
## consolidate imports in one place
##
## Revision 1.8  2010/01/13 11:58:44  godzilla
## py 2.6 doesnt like from logging import *, so start importing specific objects by name.
## py 2.6 wants string explicitly imported
##
## Revision 1.7  2007/07/08 01:30:52  hank
## If we are running from the .zip file in C:\DataCollector, we need to be sure the
## configuration file is set to C:\DataCollector\CONFIG_FILE_NAME. Fixed.
##
## Revision 1.6  2007/06/25 02:54:38  hank
## Clean up some docstrings.
##
## Revision 1.5  2006/12/21 15:44:23  hank
## The Logging module now configures itself via Src/DCLogs.conf on startup.
## It should be imported before any other system modules. (If not, there will be
## an unimportant exception on program exit.)
##
## Revision 1.4  2006/12/21 04:48:50  hank
## Do a minimal logging setup for cases where we don't do full setup via DCLogs.conf.
##
## Revision 1.3  2006/12/18 18:03:39  hank
## Modified LogFileHandler to buffer output until the file is actually opened, then
## send the buffered output immediately to the file.
##
## Revision 1.2  2006/12/18 03:18:53  hank
## Fix problem where the logging system does a shutdown and closes
## its output files before all modules that use loggers have shutdown -
## We will miss some output in the log files this way, but we were missing
## it anyway - this cleans up the error message.
##
## Revision 1.1  2006/12/13 21:54:36  hank
## Added a module to set up the Python logging facilities for DataCollector.
## Each module is set up with its own logger via the DCLogs.conf configuration file.
## The log level for each module can be set appropriately as we work, from
## DEBUG, INFO, WARN up to CRITICAL.
## Output is sent both to stdout and a log file (if set up by the main DataCollector.py module).
## Output format can be tweaked as desired.
##

class LoggingError(Exception):
    pass

#from logging import * # done this way so the logging module namespace can be gotten at from Logging
from logging import getLogger, Handler, root  # needed for python 2.6 CHECK_ME
import logging.handlers
import logging.config
import os.path
import string

class LogFileHandler(logging.handlers.RotatingFileHandler):
    """
    This is a slightly enhanced version of the library RotatingFileHandler that
    allows you to open the file AFTER creating the handler. It is very dependent
    on the logging module code, so if that module changes, expect problems!
    """
    def __init__(self,idStr,filename='',mode='a',maxBytes=0,backupCount=0,encoding=None):
        """
        Mimic the RotatingFileHandler signature with added idStr to identify handler later.
        if filename is empty, then delay the __init__ until later!
        """
        self.ID=idStr # so we can update this handler later
        if filename:
            logging.handlers.RotatingFileHandler.__init__(self,filename,mode,maxBytes,backupCount,encoding)
        else:
            # do the base classes initialisation but hold the file part til later
            Handler.__init__(self) 
            self._filename=None
            self.stream=None
            self.mode,self.maxBytes,self.backupCount,self.encoding=mode,maxBytes,backupCount,encoding
            self._buffer=[]

    def emit(self,record):
        """Only log when file has been opened."""
        if self.stream:
            logging.handlers.RotatingFileHandler.emit(self,record)
        else:
            # save messages pending an open file
            self._buffer.append(self.format(record))

    def openLog(self,filename):
        if self._filename:
            raise LoggingError,"I don't know how to open a LogFileHandler more than once! (%s)"%self.ID
        del self._filename
        # WARNING - ugly hacks, prone to error....
        # because we are calling the base Handler. (and Filterer.) __init__ again,
        # ... we have to save previous stuff
        fmt,level,filters=self.formatter,self.level,self.filters
        logging.handlers.RotatingFileHandler.__init__(self,filename,self.mode,self.maxBytes,self.backupCount,self.encoding)
        # ... and we need to remove ourselves from the logging._handlerList; see Handler.__init__()...
        del logging._handlerList[0] # NOTE this requires Python 2.4.3 (or maybe 2.4.2?) or later!!
        # ... and finally, restore previous stuff
        self.formatter,self.level,self.filters=fmt,level,filters
        #(either we do it this way, or we copy over the __init__ stuff up to the StreamHandler level....)
        # finally, dump pending messages to the file
        for msg in self._buffer:
            self.stream.write("%s\n"%msg)
        self._buffer=[]

    def flush(self):
        """protected stream flush..."""
        if self.stream:
            logging.handlers.RotatingFileHandler.flush(self)

    def close(self):
        """protected stream closing"""
        if self.stream:
            logging.handlers.RotatingFileHandler.close(self)
            # we do this in case the log file gets closed before all modules are closed...
            self.stream=None

# make this available to the logging configuration file which can
#    access the logging namespace:
# CHECK_ME is there something like this in the library now?
logging.handlers.LogFileHandler=LogFileHandler 
# set up the DC logging configuration:
CONFIG_FILE_NAME="DCLogs.conf"
modulePath=os.path.dirname(os.path.abspath(__file__))
# we need to look to the containing directory if we are running from the .zip file
if modulePath.lower().endswith('.zip'):
    modulePath=os.path.dirname(modulePath)
configFile=os.path.join(modulePath,CONFIG_FILE_NAME)
logging.config.fileConfig(configFile)

def openLogFile(handlerID,filename):
    """Find the LogFileHandler in logging._handlerList[] with
    handlerID and call its openLog(filename).
    NOTE that handlerID must match the first arg in the list provided
    in the configuration file for a LogFileHandler"""
    for handler in logging._handlerList:
        try:
            if handler.ID==handlerID:
                handler.openLog(filename)
                return # note we can only get 1 this way!
        except AttributeError,e:
            pass
    raise LoggingError,"Couldn't find LogFileHandler with ID %s"%handlerID
        
##############


if __name__ == '__main__':

    print logging._handlers
    logging.getLogger("SQL").warning("Howdy")
    openLogFile("DCLogger","test.log")
    try:
        openLogFile("Chopper","bad.log")
    except Exception,e:
        print e
    
    #print dir(root.manager)
    for name,log in root.manager.loggerDict.items():
        print name
        for h in log.handlers:
            if isinstance(h,logging.handlers.RotatingFileHandler):
                print h
    print
    print logging._handlers
    print logging._handlerList
    print
    #print dir(logging)
    for target in ["","SQL","DataObjects","DB","Encryption","Inputs","InputWidgets","LayoutWidgets",
                   "Machine","QuestionnaireManager","QuestionnaireSpecifiers","Parser","ResourceParser",
                   "WindowsService","USBKey","Tables","SystemManager","Setup"]:
        log=logging.getLogger(target)
        print 'testing logger',target
        log.debug('debug')
        log.info('info')
        log.warning('warning')
        log.critical('critical')
