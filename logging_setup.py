"""
This module sets up the figured-bass extractor system to use the Python logging
facilities. It reads a logging configuration file that initialises one logger
for each module in the system. Each module then imports getLogger from
logging-setup.py to retrieve its own logger object:

LOG=logging-setup.getLogger('moduleName')

When ever you wish to display output, use the LOG object instead of a print
statement to send output to the console and to a logging file (depending on
settings in log.conf), eg:

LOG.info("Something normal happened here")
LOG.critical("Something terrible happened here")
[NOTE logging message syntax: LOG.level("formatted string %s %s %s",arg1, arg2, arg 3)]

We use the logging levels defined by the logging module, DEBUG, INFO, WARNING,
ERROR and CRITICAL, to control which messages get displayed at any given
time.

A default logging configuration file is provided (log.conf-default) that sets up
each module to send log messages to stdout and format them as follows:
FILENAME LINENUMBER LOG-LEVEL log-message
It is configured to send ALL log messages to the console.

The local configuration file, log.conf, can be tailored in a number of ways:
- to send log messages to a file, or multiple destinations
- to adjust the format of log messages
- to adjust the log level that appears in the log output by modifying either the
level in each logger section OR by adjusting the log level of the output
handler.

Adding a new module to the system involves adding a new entry to the local
log.conf and to the system-wide log.conf-default; see log.conf-default for
examples or write me for instructions (hank@music.mcgill.ca).

Local log.conf files should NOT be checked into the repository. The
log.conf-default file is used to initialise the log.conf in each cloned
repository.

For more details about the Python logging facilites, see
http://docs.python.org/library/logging.html#module-logging.
"""
CONF_FILENAME = 'log.conf'
DEFAULT_CONF_FILENAME = 'log.conf-default'


class LoggingError(Exception):
    pass

#from logging import getLogger,root
#import logging./handlers
import logging.config
import os.path
import shutil
import logging
getLogger = logging.getLogger
logging.raiseException = True

# check that we have a configuration file, if not, copy the default template to config file.
conf_filename = os.path.abspath(CONF_FILENAME)
if not os.path.exists(conf_filename):
    print 'copying logging defaults to local file %s' % conf_filename
    shutil.copy(os.path.abspath(DEFAULT_CONF_FILENAME), conf_filename)

# load the configuration
logging.config.fileConfig(conf_filename)
del conf_filename
##############

if __name__ == '__main__':
    for target in ["root", "engine", "evaluation", "extractor", "figured_bass", "rules", "work_browser", "rulesViewer", "figure_extractor"]:
        log = logging.getLogger(target)
        print 'testing logger', target
        log.debug('debug')
        log.info('info')
        log.warning('warning')
        log.critical('critical')
