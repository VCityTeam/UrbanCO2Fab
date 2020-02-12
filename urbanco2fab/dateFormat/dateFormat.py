import sys
import dateutil
import time
import datetime
import re
import logging
logger = logging.getLogger("root")



class DateFormat:
    _wanted_format_only_number = r"(\d{4})-?(\d{2})?-?(\d{2})?T?(\d{2})?:?(\d{2})?:?(\d{2})?\+?(\d{2}:\d{2})?" #regex match for 2001-06-05T15:29:54+02:00
    _wanted_format_month = r"\d{4}-(\w+)" #regex match for 2001-janvier-05T15:29:54+02:00
    _month_dict = {
                "janvier":"01",
                "january":"01",
                "février":"02",
                "february":"02",
                "mars":"03",
                "march":"03",
                "avril":"04",
                "april":"04",
                "mai":"05",
                "may":"05",
                "juin":"06",
                "june":"06",
                "juillet":"07",
                "july":"07",
                "août":"08",
                "august":"08",
                "septembre":"09",
                "september":"09",
                "octobre":"10",
                "october":"10",
                "novembre":"11",
                "november":"11",
                "décembre":"12",
                "december":"12",
                }
    """
    Get a string and convert it to the format 2001-06-05T15:29:54+02:00
    The string has a wanted format. The year is mandatory. The rest not. Any precision can be used (ex 2001, 2001-02, 2001-02-15, 2001-02-15T12...)
    Warning: if time zone is not provided by default the one from the system will be taken
    @Input : date(string)
    @Return : ret(string) with the format 2001-06-05T15:29:54+02:00
    """
    @staticmethod
    def parser(date):
        ret = None
        if type(date) is not str:
            logger.error('Wrong input for Date parser : %s, type:%s', str(date), type(date))
            return ret

        test = re.match(DateFormat._wanted_format_only_number, date)
        logger.debug("Date mathed : %s", test)
        if not test:
            logger.error("Date parser failed : %s", date)
        else:
            list_date = list(test.groups()[:7]) # to be sure of the length
            
            if not list_date[1]: # month was not present at least in a number
                for key in DateFormat._month_dict:
                    if ( date.find(key) != -1 ):
                        list_date[1] = DateFormat._month_dict[key]
                        logger.debug("Month string replace by number : date:%s - key:%s - number:%s", date, key,  DateFormat._month_dict[key])
                        break

            for i in range(len(list_date)-1): # fill the none
                if not list_date[i]:
                    list_date[i] = '01'
            
            time_zone = list_date.pop(-1)
            if not time_zone: # fill the time zone
                time_zone = DateFormat._get_time_zone_from_system()
                logger.warning("Used of the default time zone coming from the systeme: +%s", time_zone)
            
            ret = list_date[0] + "-" + \
                list_date[1] + "-" + \
                list_date[2] + "T" + \
                list_date[3] + ":" + \
                list_date[4] + ":" + \
                list_date[5] + "+" + \
                time_zone

            logger.info("Date parse : From:%s to:%s",date, ret)
            return ret


        

    """
    Get the time zone from the system
    Warning: we only consider complete time zone as 01:00, 02:00, 03:00 ...
    @Return : ret(string) : UTC time zone in the format ii:ii
    """
    @staticmethod
    def _get_time_zone_from_system():
        ret = ""
        time_zone = time.timezone / -(60*60) # int in UTC
        ret = str(round(time_zone)).zfill(2) + ':00'
        
        return ret





if __name__ == "__main__":
    sys.path.append("../") # allow relative import beyond top-level package

    from logger.logger import set_logger

    # 2001-06-05T15:29:54+02:00
    logger = set_logger()
    logger.debug('Start')  
    test = ["2001-06-05T15:29:54+02:00",
            "2001-06-05T15:29:54+02:0",
            "2001-06-05T15:29:5+02:00",
            "2001-06-05T15:29:5402:00",
            "2001-06-05T15:2:54+02:00",
            "2001-06-05T15:",
            "2001",
            "201",
            "2001-06T15:29:54+02:00",
            "toto",
            2001,
            "2001-06-05T15:20:54+02:00 2001-06-05T15:2:54+02:00",
            "2001-janvier-05T15:29:54+02:00",
            "2001-toto-05T15:29:54+02:00",
            "2001-march-05T15:29:54+02:00",
            "2001-06-albertT15:29:54+02:00",
            "2001-06-05Tjanvier29:54+02:00",
            "2001-août-05T15:29:54+02:00",
            ]
    for date in test:
        DateFormat.parser(date)

