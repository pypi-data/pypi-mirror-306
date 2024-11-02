import logging
import os

class Logger:
    DF=False
    @staticmethod
    def get_logger(name="App", level=logging.INFO, log_file=None):
        """
        Initializes and returns a logger instance.

        Parameters:
        - name (str): Name of the logger. If None, the root logger is used.
        - level (int): Logging level (e.g., logging.DEBUG, logging.INFO).
        - log_file (str): If provided, logs will also be written to this file.

        Returns:
        - logger (logging.Logger): Configured logger instance.
        """

    
        # Get the logger instance
        logger = logging.getLogger(name)
        #Set the early flag
        logger.DF=level<=logging.DEBUG

        # Check if handlers are already added to prevent duplicate logs
        if not logger.handlers:
            logger.setLevel(level)
            # Create a formatter
            formatter = logging.Formatter(
                fmt='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
                datefmt='%Y-%m-%d-%H:%M:%S'
            )

            # Create a console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            # If a log file is specified, add a file handler
            if log_file:
                # Ensure the directory exists
                os.makedirs(os.path.dirname(log_file), exist_ok=True)

                file_handler = logging.FileHandler(log_file)
                file_handler.setLevel(level)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)

        return logger
