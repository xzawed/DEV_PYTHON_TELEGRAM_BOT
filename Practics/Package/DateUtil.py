#  Create by NeoDream83

import datetime

from datetime import date, timedelta


class DateUtil:
    def __init__(self, setDate):
        self.result = ""
        format_date = '%Y-%m-%d'
        try:
            self.setDate = datetime.datetime.strptime(setDate, format_date)
        except Exception:
            self.setDate = date.today()


    def getYesterday(self):

        today = self.setDate
        yesterday = self.setDate - timedelta(1)

        self.result = yesterday
        return self.result

    def addDays(self, count):
        targetDate = self.setDate + datetime.timedelta(days=count)
        return targetDate

    def getWeekFirstDate(self):
        tempDate = datetime.datetime(self.setDate.year, self.setDate.month, self.setDate.day)
        weekDayCount = tempDate.weekday()
        targetDate = self.addDays(-weekDayCount)
        return targetDate

    def getWeekLastDate(self):
        tempDate = datetime.datetime(self.setDate.year, self.setDate.month, self.setDate.day)
        weekDayCount = tempDate.weekday()
        targetDate = self.addDays(-weekDayCount + 6)
        return targetDate
