from pyowm.owm import OWM
from datetime import timezone, datetime
import asyncio
from LunarSolar import LunarSolar
import requests
import time
import json

day_of_week = ["Thứ hai","Thứ ba","Thứ tư","Thứ năm","Thứ sáu","Thứ bảy","Chủ nhật"]
string_month = ["Tháng Một","Tháng Hai","Tháng Ba","Tháng Tư","Tháng Năm","Tháng Sáu","Tháng bảy", "Tháng Tám", "Tháng Chín", "Tháng Mười Một", "Tháng Mười Hai"]
# 1: sun, 2: clouds, 3: moon, 4: halfmoon   
class dataWeather(OWM):
    """docstring for dataWeather"""
    def __init__(self,namecity):
        super(dataWeather, self).__init__("06c921750b9a82d8f5d1294e1586276f")
        self.namecity = namecity
        self.dataLocation = self.namecity_to_latlon(self.namecity)
        self.latitude = float(self.dataLocation[0]["lat"])
        self.longitude = float(self.dataLocation[0]["lon"])
        self.city = self.dataLocation[0]["city"]
        self.country = self.dataLocation[0]["country"]
        self.data = self.weather_manager().weather_at_coords(lat=self.latitude,lon=self.longitude).weather
        self.sunrise = self.data.sunrise_time()
        self.sunset = self.data.sunset_time()
        self.temperature_C = self.data.temperature("celsius")
        self.temperature_F = self.data.temperature("fahrenheit")
        self.wind = self.data.wind()
        self.foresight = self.data
        self.suntime_loop = self.suntime_loop()
        self.visibility_distance = self.data.visibility_distance
        self.description = self.data.detailed_status 
        self.clouds = self.data.clouds
        self.suntime = []
        self.set_suntime()
        self.necessary = []
        self.now = datetime.now()
        self.day = self.set_day()
        self.day_moon = self.set_day_moon()
        self.pic_description =  self.setState(self.data.status)
        self.GMT =datetime.now().hour-datetime.now(timezone.utc).hour
        self.necessary = self.set_necessary()
    def namecity_to_latlon(self, namecity):
        string_input = namecity
        string_input += " " 
        cout = 0 
        string_test = ""
        List_word_demo = [] 
        List_word = []
        while cout < len (string_input):
            if (string_input[cout].isalpha() == True):
                string_test += string_input[cout]
            else:
                List_word_demo.append(string_test)
                string_test=""
            cout += 1
        #filter the twice time (delete space,...)
        List_word = list(filter(lambda a: (a.isalpha() == True) , List_word_demo))
        address=""
        for x in range(len(List_word)):
            if x < len(List_word) - 1:
                address+=List_word[x]+"-"
            else:
                address+=List_word[x]    
        URL = "https://nominatim.openstreetmap.org/?addressdetails=1&q="+address+"&format=json&limit=1"
        response = requests.get(URL)
        resp_json_payload = response.json()
        if len(resp_json_payload) == 0:
            return [{"lat":None,"lon":None,"city":None, "country":None}]
        try:
            return [{"lat":resp_json_payload[0]["lat"], "lon":resp_json_payload[0]["lon"],"city":resp_json_payload[0]["address"]["city"],
                "country":resp_json_payload[0]["address"]["country"]}]
        except KeyError:
            try:
                return [{"lat":resp_json_payload[0]["lat"], "lon":resp_json_payload[0]["lon"],"city":resp_json_payload[0]["address"]["state"],
                "country":resp_json_payload[0]["address"]["country"]}]
            except KeyError:
                return [{"lat":resp_json_payload[0]["lat"], "lon":resp_json_payload[0]["lon"],"city":resp_json_payload[0]["address"]["country"],
                "country":resp_json_payload[0]["address"]["country"]}]
    def run1(self):
        """Run event loop"""
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.display_date(loop,1))
        loop.run_forever()
        loop.stop()
    def reset_Data(self):
        """resetdata"""
        self.data = self.weather_manager().weather_at_coords(lat=self.latitude,lon=self.longitude).weather
        self.temperature_C = self.data.temperature("celsius")
        self.temperature_F = self.data.temperature("fahrenheit")
        self.wind = self.data.wind()
        self.foresight = self.data
        self.visibility_distance = self.data.visibility_distance
        self.description = self.data.detailed_status 
        self.pic_description =  self.setState(self.data.status)
        self.necessary = []
        self.cloud = self.data.clouds
    def set_day(self):
        """set day data"""
        day = self.now.day
        month = self.now.month
        year = self.now.year
        day = {"day": day,"month":month,"year":year}
        return day
    def set_day_moon(self):
        """set day moon data"""
        x = LunarSolar()
        day_moon = x.solar_to_lunar_string(self.now.day,self.now.month,self.now.year)
        return day_moon
    def reset_Data_day(self):
        """reset day day"""
        self.day = self.set_day()
        self.day_moon = self.set_day_moon()
    def reset_Sun_time(self):
        self.data = self.weather_manager().weather_at_coords(lat=self.latitude,lon=self.longitude).weather
        self.sunrise = self.data.sunrise_time()
        self.sunset = self.data.sunset_time()
    def suntime_loop(self):
        while True:
            self.reset_Sun_time()
            yield self.sunrise
            yield 2
            yield self.sunset
            yield 1
            yield 0
            yield 2
    def delay_when_start(self,now):
        """delay time when start app  (0-3-6-9-12-15-18-21-24)"""
        now1=now + self.GMT*3600
        next_time = (int(((now1/3600)/3))+1)*3*3600
        next_time = now + (next_time-now1)
        return next_time 
    def set_suntime(self,now =datetime.now().timestamp()):
        self.suntime = []
        if self.sunrise <= now < self.sunset:
            self.suntime.append(next(self.suntime_loop))
            self.suntime.append(next(self.suntime_loop))
            self.suntime = []
            self.suntime.append(next(self.suntime_loop))
            self.suntime.append(next(self.suntime_loop))
            print("ban ngày")
        elif now < self.sunrise :
            self.suntime.append(next(self.suntime_loop))
            self.suntime.append(next(self.suntime_loop))
            print("ban đêm 1")
        else:
            print("ban đêm")
            self.suntime = [0 , 1]
    def setState(self, status):
        """set picture descriptio"""
        with open('weather_state.json', 'r') as openfile:
            json_object = json.load(openfile)
            openfile.close()
        for x in range(len(json_object)):
            if self.description ==json_object[x]["des"]:
                if self.suntime[1] == 1:
                    if self.clouds <= 25:
                        return json_object[x]["pic0"]
                    else:
                        return json_object[x]["pic1"]
                else:
                    if 11<=self.day_moon["lunar day"]<=18:
                        return json_object[x]["pic2"]
                    else:
                        return json_object[x]["pic2"]
        with open('main_weather.json', 'r') as openfile:
            json_object1 = json.load(openfile)
            openfile.close()
        for x in range(len(json_object1)):
            if status ==json_object[x]["des"]:
                if self.suntime[1] == 1:
                    if self.clouds <= 25:
                        return json_object[x]["pic0"]
                    else:
                        return json_object[x]["pic1"]
                else:
                    if 11<=self.day_moon["lunar day"]<=18:
                        return json_object[x]["pic2"]
                    else:
                        return json_object[x]["pic2"]
        return "united"
    def set_necessary(self):
        pass
    async def display_date(self, loop ,  status): 
        """ status = 1 ->day
            status = 2 ->night"""
        tic = time.perf_counter()
        now = datetime.now().timestamp()
        print(self.pic_description)
        next_time =self.delay_when_start(now)
        hour_begin_ts = next_time 
        hour_end_ts = next_time + 3 * 3600
        hour_begin = datetime.fromtimestamp(hour_begin_ts).hour
        self.set_suntime(now)
        self.reset_Data()
        self.reset_Data_day()
        toc = time.perf_counter()
        if (next_time - now - (toc - tic) >= 0):
            time_daley_1 = 0 
            print(next_time - now - (toc - tic))
            await asyncio.sleep(next_time - now - (toc - tic))
        else:
            time_daley_1 = 0 - (next_time - now - (toc - tic))
            hour_begin_ts = next_time  + 3 * 3600
            hour_end_ts = next_time + 3 * 3600 + 3 * 3600
            hour_begin = datetime.fromtimestamp(hour_begin_ts).hour + 3
        while True:
            tic1=time.perf_counter()
            self.reset_Data()
            hour_begin_ts +=3
            hour_end_ts +=3
            hour_begin = datetime.fromtimestamp(hour_begin_ts).hour
            toc2 = time.perf_counter()
            print(self.visibility_distance)
            
            if hour_begin_ts < self.suntime[0] < hour_end_ts:
                hour_next - next_time[0]
                self.suntime = []
                self.suntime.append(next(self.suntime_loop))
                self.suntime.append(next(self.suntime_loop))
                delay_suntime = self.suntime[0]-hour_begin_ts
                toc1 = time.perf_counter()
                await asyncio(self.suntime[0]-hour_begin_ts)
                tic2 = time.perf_counter()
                self.reset_Data()
            else:
                toc1 = 0
                tic2 = 0
                delay_suntime = 0
            if hour_begin == 00:
                self.reset_Data_day()
                print(self.day)
                self.suntime = []
                self.suntime.append(next(suntime_loop))
                self.suntime.append(next(suntime_loop))
            time_execute=(tic1-toc1)+(tic2-toc2) 
            await asyncio.sleep(3*3600-time_execute - delay_suntime - time_daley_1)



    
if __name__ == "__main__":
    a = LunarSolar()
    n = a.solar_to_lunar_string(22,4,2021)
    print(n)
    a = dataWeather("Tomsk")
    a.run1()