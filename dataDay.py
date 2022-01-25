from datetime import datetime,timedelta
from LunarSolar import LunarSolar


class dataDay():
    @property
    def now(self):
    	return datetime.now() 
    @property
    def day(self):
        """set day data"""
        weekday = self.now.weekday()
        day = self.now.day
        month = self.now.month
        year = self.now.year
        day = {"weekday":weekday,"day": day,"month":month,"year":year}
        return day
    @property
    def day_moon(self):
        """set day moon data"""
        x = LunarSolar()
        day_moon = x.solar_to_lunar_string(self.now.day,self.now.month,self.now.year)
        return day_moon
    @property
    def time(self):
        time = {"hour": self.now.hour ,"minute":self.now.minute}
        return time
    @property
    def weekday(self):
        weekday = []
        for x in reversed(range(self.day["weekday"] + 1)):
            weekday.append({"day": (datetime.today() - timedelta(days=x)).day, "month" :(datetime.today() - timedelta(days=x)).month})
        for x in range(1,6 - self.day["weekday"] + 1):
            weekday.append({"day": (datetime.today() + timedelta(days=x)).day, "month" :(datetime.today() + timedelta(days=x)).month})
        return weekday

    def weeknum(self, year, month, day ):
        return datetime(year, month, day).isocalendar()[1]


print(dataDay().day_moon)
    
    

