from .complete_logger import get_logger, config_thr_exc_log

# Choose name as filename of logging file. Don't include file-extension
logger = get_logger("logname")

# Captures all raised exceptions and logs it to <filename>.log
# Also prints it to console
config_thr_exc_log()

# Log levels only included in log file
logger.debug("Lowest level of logging. Included in logfile")
logger.info("Second lowest level of logging. Included in logfile")

# Log levels included both in log file, and printed to console
logger.warning("Lowest level that is included both in console and logfile")
logger.error("Middle level log included both in console and logfile")
logger.critical("Highest level log, included in both")
