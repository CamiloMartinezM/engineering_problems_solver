# -*- coding: utf-8 -*-
"""
Created on December 13, 2019.

@author: Camilo Martínez
"""
import time
from datetime import datetime
from os.path import isfile

import main

# Name of the log file.
LOG_FILE = "log.txt"

# Datetime format
FORMAT = "%d %b %Y %I:%M:%S %p %Z"


class ParentException(Exception):
    """ Parent exception of all exceptions.

        When an exception is raised, the error message gets
        stored inside a log file, which contains all errors.
    """

    def __init__(self, message: str, filename: str = None, error_code: int = 0) -> None:
        """        
        Args:
            message (str): Exception message.
        """
        self.message = message
        self.filename = filename
        self.error_code = error_code
        self.log()

    def utc2local(self, utc: datetime) -> datetime:
        """ Converts UTC date to local date.
        
        Args:
            utc (datetime): Current date in UTC.
        
        Returns:
            datetime: Current date in GMT-5.
        """
        epoch = time.mktime(utc.timetuple())
        offset = datetime.fromtimestamp(
            epoch) - datetime.utcfromtimestamp(epoch)
        return utc + offset

    def log(self) -> None:
        """ Writes a log entry to the log file. 
        """
        if not main.TITLE_EXISTS:  # Checks if title has already been written.
            # This creates a proper title.
            with open(LOG_FILE, "a") as log:
                current_date = datetime.utcnow()
                gmt5_date = self.utc2local(current_date).strftime(FORMAT)
                day = datetime.now().strftime("%A")

                log.write("-" * 111)
                log.write('\n')
                log.write("Log created on {}, {} GMT+5".format(day, gmt5_date))
                log.write('\n')
                log.write("-" * 111)
                log.write('\n')

                main.TITLE_EXISTS = True

        with open(LOG_FILE, "a") as log:
            current_date = datetime.utcnow()
            gmt5_date = self.utc2local(current_date).strftime(FORMAT)
            day = datetime.now().strftime("%A")

            
            # Writes entry.
            extra = ""
            if self.filename is not None:
                extra = ". Error occurred in: " + self.filename
            
            log.write(day + ", " + gmt5_date + " GMT+5 (Error code: " + str(self.error_code) + \
                 "): " + self.message + extra + '\n')
