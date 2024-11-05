import sys
from .fontMods import TimeFonts
from .mylogger import logger
from time import sleep
from datetime import datetime as dt



class TimeGenerator:
    nums = ["zero", "one", "two", "three", "four",
            "five", "six", "seven", "eight", "nine",
            "ten", "eleven", "twelve", "thirteen",
            "fourteen", "fifteen", "sixteen", 
            "seventeen", "eighteen", "nineteen", 
            "twenty", "twenty one", "twenty two", 
            "twenty three", "twenty four", 
            "twenty five", "twenty six", "twenty seven",
            "twenty eight", "twenty nine"]

    def __init__(self,case='lower',format='12'):
        logger.debug(f'Case set as {case}')
        logger.debug(f'Format set as {format}')
        self.case = case
        self.format = format

    def get_words_from_time(self,h=None,m=None):
        """
        Returns a sentence giving the time based on hour and minute

        Parameter
        ---------
        h: hour as integer 12 or 24-hour format
        m: minute as integer 0<=m<60
        """
        if h is None:
            logger.debug(f'Fetching current hour')
            h = self.get_current_hour()
        if m is None:
            logger.debug(f'Fetching current minute')
            m = self.get_approximate_minute()
        
        if self.format=='12':
            logger.debug(f'Converting to 12-hour format')
            if h > 12: h = h - 12

        if   m==0:              time_sentence = f"{self.nums[h]} o'clock"
        elif m>=1 and m<15:     time_sentence = f"ten minutes past {self.nums[h]}"
        elif m>=15 and m<19:    time_sentence = f"quarter minutes past {self.nums[h]}"
        elif m>=20 and m<29:    time_sentence = f"twenty minutes past {self.nums[h]}"
        elif m==30:             time_sentence = f"half past {self.nums[h]}"
        elif m>30 and m<=35:    time_sentence = f"twenty five minutes to {self.nums[(h % 12) + 1]}"
        elif m>35 and m<45:     time_sentence = f"twenty minutes to {self.nums[(h % 12) + 1]}"
        elif m==45:             time_sentence = f"quarter minutes to {self.nums[(h % 12) + 1]}"
        elif m>45 and m<=50:    time_sentence = f"ten minutes to {self.nums[(h % 12) + 1]}"
        elif m>=51 and m<59:    time_sentence = f"five minutes to {self.nums[(h % 12) + 1]}"


        # time_sentence = "ten minutes past five"
        if self.case != 'lower':
            return ("it is "+time_sentence).upper()
        
        return ("it is "+time_sentence)

    def get_current_hour(self):
        return int(dt.now().hour)

    def get_approximate_minute(self):
        return int(dt.now().minute/5)*5

    def get_current_minute(self):
        return int(dt.now().minute)

    def print_time(self):
        print(TimeFonts.BOLD + self.get_words_from_time() + TimeFonts.END)

    def print_time_matrix(self):
        matrix = TimeFonts(time_sentence=self.get_words_from_time())
        matrix.show()