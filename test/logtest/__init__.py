from selfusepy.log import Logger


def log_test():
    log = Logger().logger
    log.debug("debug")
    log.info('info')
    log.warning("warning")
    log.error("error")
    log.critical("critical")


def log_time_test():
    log_12 = Logger(time_offset = -12).logger
    log_12.info("UTC-12:00")
    log_11 = Logger(time_offset = -11).logger
    log_11.info("UTC-11:00")
    log_10 = Logger(time_offset = -10).logger
    log_10.info("UTC-10:00")
    log_9 = Logger(time_offset = -9).logger
    log_9.info("UTC-09:00")
    log_8 = Logger(time_offset = -8).logger
    log_8.info("UTC-08:00")
    log_7 = Logger(time_offset = -7).logger
    log_7.info("UTC-07:00")
    log_6 = Logger(time_offset = -6).logger
    log_6.info("UTC-06:00")
    log_5 = Logger(time_offset = -5).logger
    log_5.info("UTC-05:00")
    log_4 = Logger(time_offset = -4).logger
    log_4.info("UTC-04:00")
    log_3 = Logger(time_offset = -3).logger
    log_3.info("UTC-03:00")
    log_2 = Logger(time_offset = -2).logger
    log_2.info("UTC-02:00")
    log_1 = Logger(time_offset = -1).logger
    log_1.info("UTC-01:00")
    log0 = Logger(time_offset = 0).logger
    log0.info("UTC")
    log1 = Logger(time_offset = 1).logger
    log1.info("UTC+01:00")
    log2 = Logger(time_offset = 2).logger
    log2.info("UTC+02:00")
    log3 = Logger(time_offset = 3).logger
    log3.info("UTC+03:00")
    log4 = Logger(time_offset = 4).logger
    log4.info("UTC+04:00")
    log5 = Logger(time_offset = 5).logger
    log5.info("UTC+05:00")
    log6 = Logger(time_offset = 6).logger
    log6.info("UTC+06:00")
    log7 = Logger(time_offset = 7).logger
    log7.info("UTC+07:00")
    log8 = Logger(time_offset = 8).logger
    log8.info("UTC+08:00")
    log9 = Logger(time_offset = 9).logger
    log9.info("UTC+09:00")
    log10 = Logger(time_offset = 10).logger
    log10.info("UTC+10:00")
    log11 = Logger(time_offset = 11).logger
    log11.info("UTC+11:00")
    log12 = Logger(time_offset = 12).logger
    log12.info("UTC+12:00")
