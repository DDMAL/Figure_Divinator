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
CONF_FILENAME='figured_bass_log.conf'
DEFAULT_CONF_FILENAME='figured_bass_log.conf-default'

class LoggingError(Exception):
    pass

from logging import getLogger,root
#import logging./handlers
import logging.config
import os.path
import shutil

# check that we have a configuration file, if not, copy the default template to config file.
conf_filename=os.path.abspath(CONF_FILENAME)
if not os.path.exists(conf_filename):
    print 'copying logging defaults to local file %s' % conf_filename
    shutil.copy(os.path.abspath(DEFAULT_CONF_FILENAME),conf_filename)

# load the configuration
logging.config.fileConfig(conf_filename)

##############

if __name__ == '__main__':
    pass

##     print dir(root.manager)
##     for name,log in root.manager.loggerDict.items():
##         print name
##         for h in log.handlers:
##             print h
##     print
##     print logging._handlers
##     print logging._handlerList
##     print
##     #print dir(logging)
##     for target in ["","SQL","DataObjects","DB","Encryption","Inputs","InputWidgets","LayoutWidgets",
##                    "Machine","QuestionnaireManager","QuestionnaireSpecifiers","Parser","ResourceParser",
##                    "WindowsService","USBKey","Tables","SystemManager","Setup"]:
##         log=logging.getLogger(target)
##         print 'testing logger',target
##         log.debug('debug')
##         log.info('info')
##         log.warning('warning')
##         log.critical('critical')
