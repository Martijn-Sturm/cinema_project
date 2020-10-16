import logging
import os
import sys
import threading


def dummy_logger():
    logger = logging.getLogger("dummy")
    logger.addHandler(logging.NullHandler())
    return logger


def get_logger(filename, name=__name__, subfolder=None):
    try:
        name = filename
    except NameError:
        filename = name

    folder = "./logs/"
    if subfolder:
        if subfolder[0] == ("." or "/"):
            raise Exception(
                "Subfolder format is not right. Should be 'folder'. No beginning '.' or '/'"
            )
        if subfolder[-1] == "/":
            raise Exception(
                "Subfolder format is not right. Should be 'folder'. No trailing '/'"
            )

        folder = folder + subfolder + "/"
    # if os.path.exists(folder):
    #     overwrite_check = input(
    #         f"You are going to overwrite folder '{folder}'. Proceed? (y/n) "
    #     )
    #     if overwrite_check == "y":
    #         pass
    #     elif overwrite_check == "n":
    #         raise Exception(f"Aborted to not overwrite folder: {folder}")
    #     else:
    #         raise Exception("Invalid input, use 'y' for yes and 'n' for no.")
    os.makedirs(folder, exist_ok=True)

    logger = logging.getLogger(f"{name}_logger")
    logger.setLevel(logging.DEBUG)

    # Handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(f"{folder}{filename}.log")
    c_handler.setLevel(logging.WARNING)
    f_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    c_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger


# Source: https://www.scrygroup.com/tutorial/2018-02-06/python-excepthook-logging/
def config_thr_exc_log(filename="exception", name="exception"):
    """Logs all uncaptured exceptions to <filename>.log with name
    of logger: <name>
    """
    logger = get_logger(filename=filename, name=name)

    def handle_unhandled_exception(
        exc_type, exc_value, exc_traceback, thread_identifier=""
    ):
        """Handler for unhandled exceptions that will write to the logs"""
        if issubclass(exc_type, KeyboardInterrupt):
            # call the default excepthook saved at __excepthook__
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        if not thread_identifier:
            logger.critical(
                "Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback)
            )
        else:
            logger.critical(
                "Unhandled exception (on thread %s)",
                thread_identifier,
                exc_info=(exc_type, exc_value, exc_traceback),
            )

    sys.excepthook = handle_unhandled_exception

    def patch_threading_excepthook():
        """Installs our exception handler into the threading modules Thread object
        Inspired by https://bugs.python.org/issue1230540
        """
        old_init = threading.Thread.__init__

        def new_init(self, *args, **kwargs):
            old_init(self, *args, **kwargs)
            old_run = self.run

            def run_with_our_excepthook(*args, **kwargs):
                try:
                    old_run(*args, **kwargs)
                except (KeyboardInterrupt, SystemExit):
                    raise
                except:
                    sys.excepthook(
                        *sys.exc_info(), thread_identifier=threading.get_ident()
                    )

            self.run = run_with_our_excepthook

        threading.Thread.__init__ = new_init

    patch_threading_excepthook()


class ExceptionFromThread(Exception):
    """An exception type we raise from within a thread"""


class RunsInAThread:
    def __init__(self, error_message):
        self.error_message = error_message

    def run(self):
        raise ExceptionFromThread(self.error_message)
