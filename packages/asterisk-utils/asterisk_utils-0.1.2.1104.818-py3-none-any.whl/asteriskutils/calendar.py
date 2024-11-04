import datetime,chinese_calendar

def is_business_day(somedate: datetime.date=datetime.datetime.now()) -> bool:
    '''
    判断是否是工作日
    Args
        somedate(datetime.date):要判断的日期，默认是今天
    Returns
        bool:是否是工作日
    '''
    return somedate.weekday() in (0,1,2,3,4) and not chinese_calendar.is_holiday(somedate)

