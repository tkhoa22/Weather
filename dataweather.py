import sys

import json
import requests
from datetime import datetime
from dataDay import dataDay
import time

class dataWeather():
    def __init__(self, API_key  = "06c921750b9a82d8f5d1294e1586276f" , namecity = "united"):
        if namecity == "united":
            self.dataLocation = self.latlon_location()
        else: 
            self.dataLocation = self.namecity_to_latlon(namecity)
        self.lat = self.dataLocation[0]["lat"]
        self.lon = self.dataLocation[0]["lon"]
        data = self.get_data(API_key)
        self.weather = data["current"]
        self.forecasts = data["daily"]
        self.hourly = data["hourly"]
        data = {}
    def get_data(self,API_key):
        url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=daily.pop&appid={}"
        url = url.format(self.lat,self.lon,API_key)
        response = requests.get(url)
        return response.json()
    def latlon_location(self):
        query = "http://ip-api.com/json/"
        resp_json_payload = requests.post(query).json()
        return [{"lat":resp_json_payload["lat"], "lon":resp_json_payload["lon"],"city":resp_json_payload["regionName"],
                "country":resp_json_payload["country"]}]
    def namecity_to_latlon(self, namecity:str):
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
        response.close()
        resp_json_payload = response.json()
        if len(resp_json_payload) == 0:
            raise NameError
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
    def reset_data(self,API_key):
        data = self.get_data_current(API_key)
        self.weather = data["current"]
        self.forecasts = data["daily"]
        self.hourly = data["hourly"]
        self.alerts = data["alerts"]
        data = {}
class weather_current(dataWeather):
    def __init__(self,API_key = "06c921750b9a82d8f5d1294e1586276f" , namecity = "united"):
        super(weather_current, self).__init__(API_key,namecity)
        self.pic_sun_time = ""
        self.sunrise = self.weather["sunrise"]
        self.sunset = self.weather["sunset"]
        self.clouds = self.weather["clouds"]
        self.moon_phase = self.forecasts[0]["moon_phase"] 
        self.suntime_loop = self.suntime_loop()
        self.suntime = []
        self.set_suntime()
        self.now = datetime.now()
        self.day = dataDay().day
        self.day_moon = dataDay().day_moon
        self.pic = self.setState()
        print("reset data")
    @property
    def temp_C(self):
        return round(self.weather["temp"] - 273.15)
    @property
    def feels_like_C(self):
        return round(self.weather["feels_like"] - 273.15)

    @property
    def temp_F(self):
        return round(1.8 * (self.weather["temp"] - 273.15) + 32)

    @property
    def feels_like_F(self):
        return round(1.8 * (self.weather["feels_like"] - 273.15) + 32)

    @property
    def city(self):
        return self.dataLocation[0]["city"]

    @property
    def country(self):
        return self.dataLocation[0]["country"]

    @property
    def wind_mps(self):
        return self.weather["wind_speed"]

    @property
    def wind_mph(self):
        return round(self.weather["wind_speed"] * 2.23693629,2) 

    @property
    def uvi(self):
        return self.weather["uvi"]

    @property
    def description(self):
        return self.weather["weather"][0]["description"]

    @property
    def main(self):
        return  self.weather["weather"][0]["main"]

    @property
    def uvi(self):
        return round(self.weather["uvi"],1)

    @property
    def Necessary(self):
        pic = []
        if 3 <= self.uvi < 5:
            pic.append({"pic":"icon/cap.png","tt":"mũ"})
            pic.append({"pic":"icon/sunglasses.png","tt":"kính đen"})
        elif 5 <= self.uvi < 8:
            pic.append({"pic":"icon/cap.png","tt":"mũ"})
            pic.append({"pic":"icon/sunglasses.png","tt":"kính đen"})
            pic.append({"pic":"icon/jacket.png","tt":"áo khoác nắng"})
            pic.append({"pic":"icon/sunscreen.png","tt":"kem chống nắng"})
        if 0 < self.humidity < 40:
            pic.append({"pic":"icon/lipstick.png","tt":"son dưỡng môi"})
        if self.temp_C < 17:
            pic.append({"pic":"icon/winter-jacket.png","tt":"áo ám"})
            pic.append({"pic":"icon/scarf.png","tt":"khăn quang cổ"})
            pic.append({"pic":"icon/hat.png","tt":"mũ len"})
        if 5 - len(pic) < 0:
            return pic 
        for x in range(5-len(pic)):
            pic.append({"pic":"","tt":""})
        return pic


    @property
    def text_day_moon(self):
        if self.day_moon["lunar day"] < 10 and self.day_moon["lunar month"] < 10:
            return "0{}.0{}".format(self.day_moon["lunar day"],self.day_moon["lunar month"])
        elif self.day_moon["lunar day"] >= 10 and self.day_moon["lunar month"] < 10:
            return "{}.0{}".format(self.day_moon["lunar day"],self.day_moon["lunar month"])
        elif self.day_moon["lunar day"] < 10 and self.day_moon["lunar month"] >= 10: 
            return "0{}.{}".format(self.day_moon["lunar day"],self.day_moon["lunar month"])
        else:
            return "{}.{}".format(self.day_moon["lunar day"],self.day_moon["lunar month"])
    @property
    def tooltip_day_moon(self):
        return "Ngày: {}, Tháng: {}, Năm: {}".format(self.day_moon["ngày"],self.day_moon["tháng"],self.day_moon["năm"])

    
    @property
    def day_in_week(self):
        return self.day_moon["day in week"]
    
    @property
    def text_day(self):
        if self.day["day"] < 10 and self.day["month"] < 10:
            return "0{}.0{}".format(self.day["day"],self.day["month"])
        elif self.day["day"] >= 10 and self.day["month"] < 10:
            return "{}.0{}".format(self.day["day"],self.day["month"])
        elif self.day["day"] < 10 and self.day["month"] >=10: 
            return "0{}.{}".format(self.day["day"],self.day["month"])
        else:
            return "{}.{}".format(self.day["day"],self.day["month"])
    @property
    def tooltip_day(self):
        if self.day["month"] == 1:
            month_str = "một"
        elif self.day["month"] == 2:
            month_str = "hai "
        elif self.day["month"] == 3:
            month_str = "ba"
        elif self.day["month"] == 4:
            month_str = "bốn"
        elif self.day["month"] == 5:
            month_str = "năm"
        elif self.day["month"] == 6:
            month_str = "sáu"
        elif self.day["month"] == 7:
            month_str = "bảy"
        elif self.day["month"] == 8:
            month_str = "tám"
        elif self.day["month"] == 9:
            month_str = "chín"
        elif self.day["month"] == 10:
            month_str = "mười"
        elif self.day["month"] == 11:
            month_str = "mười một"
        elif self.day["month"] == 12:
            month_str = "mười hai"
        return "{} Tháng {} {}".format(self.day["day"],month_str,self.day["year"])
    @property
    def humidity(self):
        return self.weather["humidity"]
    @property
    def suntime_text(self):
        n = datetime.fromtimestamp(self.suntime[0])
        if n.hour < 10 and n.minute < 10:
            return "0{}:0{}".format(n.hour,n.minute)
        elif n.hour >= 10 and n.minute < 10:
            return "{}:0{}".format(n.hour,n.minute)
        elif n.hour < 10 and n.minute >=10: 
            return "0{}:{}".format(n.hour,n.minute)
        else:
            return "{}:{}".format(n.hour,n.minute)
    @property
    def tooltip_suntime(self):
        return self.tooltip_suntimea + self.suntime_text
    

    def suntime_loop(self):
        while True:
            yield self.weather["sunrise"]
            yield 2
            yield self.weather["sunset"]
            yield 1
            yield self.forecasts[1]["sunrise"]
            yield 2
    def set_suntime(self,now = datetime.now().timestamp()):
        self.suntime = []
        if self.sunrise <= now < self.sunset:
            self.suntime.append(next(self.suntime_loop))
            self.suntime.append(next(self.suntime_loop))
            self.suntime = []
            self.suntime.append(next(self.suntime_loop))
            self.suntime.append(next(self.suntime_loop))
            self.pic_sun_time = "icon/sunset.png"
            self.tooltip_suntimea = "Hoàng hôn vào lúc "
            #ban ngày 
        elif now < self.sunrise :
            self.suntime.append(next(self.suntime_loop))
            self.suntime.append(next(self.suntime_loop))
            self.suntime.append(next(self.suntime_loop))
            print(self.suntime)
            self.pic_sun_time = "icon/sunrise.png"
            self.tooltip_suntimea = "Bình minh vào lúc "
            #ban đêm 1
        else:
            #ban đêm 
            self.suntime.append(next(self.suntime_loop))
            self.suntime.append(next(self.suntime_loop))
            self.suntime = []
            self.suntime.append(next(self.suntime_loop))
            self.suntime.append(next(self.suntime_loop))
            self.suntime = []
            self.suntime.append(next(self.suntime_loop))
            self.suntime.append(next(self.suntime_loop))
            self.suntime.append(next(self.suntime_loop))
            self.pic_sun_time = "icon/sunrise.png"
            self.tooltip_suntimea = "Bình minh vào lúc "
    def setState(self):
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
                    if 0.70 < self.moon_phase:
                        return json_object[x]["pic2"]
                    else:
                        return json_object[x]["pic2"]
        with open('main_weather.json', 'r') as openfile:
            json_object1 = json.load(openfile)
            openfile.close()
        for x in range(len(json_object1)):
            if self.main ==json_object[x]["des"]:
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


        
if __name__ == "__main__":
    b = dataWeather()
    print(b.lat)