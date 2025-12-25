
def set_time():
    from machine import RTC
    import plc

    rtc = RTC()

    year = plc.YEAR
    month = plc.MONTH
    day = plc.DAY
    hour = plc.HOURS
    minute = plc.MINS
    second = plc.SECS
    subsecond = 0
    rtc.datetime((year, month, day, 0, hour, minute, second, subsecond))
    print("RTC updated\n")

#End
#time.localtime() --> (2019, 10, 6, 16, 39, 28, 6, 279)
