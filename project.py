
from selenium import webdriver
from time import sleep
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome.options import Options 
import requests, re
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify



#todo

#animated loading while getting data
#switch celsius / f 
#my contacts
#add auto refresh for weather
#make temperature more stand out



def pullWeatherFromSource(cityname):    
    chrome_options = Options() 
    chrome_options.add_argument("--headless") 
    driver = webdriver.Chrome(r'C:\Users\roberts\Documents\chromedriver.exe', chrome_options=chrome_options)
    driver.get("https://weather.com")
    sleep(2)
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div[8]/div[1]/div/div/div/div[2]/div/div/div[1]/div/input')\
    .click()
    sleep(1)
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div[8]/div[1]/div/div/div/div[2]/div/div/div[1]/div/input')\
    .send_keys(cityname)
    sleep(1)
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div[8]/div[1]/div/div/div/div[2]/div/div/div[2]/div[2]/div/ul/li[1]/a')\
    .click()
    sleep(1)

    page = driver.page_source.encode('utf-8')
        
    soup = BeautifulSoup(page, 'html.parser')
    #gathers information from div classes/ main weather info
    farenh = soup.find(class_="today_nowcard-temp").get_text()
    celsius = re.sub("°", '', farenh)
    celsius = round(((int(celsius)- 32) * 5/9),1)
    as_of = soup.find(class_="today_nowcard-timestamp").get_text()
    clouds = soup.find(class_="today_nowcard-phrase").get_text()
    temperature = (str(celsius))
    

    real_feel = soup.find(class_="today_nowcard-feels").get_text()

    sun_down = soup.find(id="dp0-details-sunset").get_text()
    sun_up = soup.find(id="dp0-details-sunrise").get_text()
    description = soup.find(id="dp0-details-narrative").get_text()
    uv_index = soup.find(id="dp0-details-uvIndex").get_text()
    humidity = soup.find(class_="wx-detail-value").get_text()
    #----------------------------------------------------------------#
    tonight = soup.find(id="dp0-daypartName").get_text()
    tonight_clouds = soup.find(id="dp0-phrase").get_text()
    tonight_highlow = soup.find(id="dp0-highLow").get_text()




    driver.close()

    if 'Clo' in clouds:
        clouds = "Cloudy"    
    elif 'Sno' in clouds:
        clouds = "Snow"
    elif 'Sun' in clouds:
        clouds = "Sunny"
    elif 'Light' in clouds:
        clouds = "Lightning"
    elif 'Rai' in clouds:
        clouds = "Rain"

    weatherData = {
        "asof": as_of,
        "weather": clouds,
        "temperature": temperature + "°C",
        "temperature_f": farenh,
        "realfeel": real_feel,
        "sunrise": sun_up,
        "sunset": sun_down,
        "description": description,
        "uvindex": uv_index,
        "humidity": humidity
    }
    return weatherData

app = Flask(__name__)


@app.route('/')
def asdas():
    return render_template('WeatherApp.html')

@app.route('/city')
def mainpage():
    return "as"


@app.route('/city/<city>', methods=['GET'])
def mainpage_post(city=None):
    city = city
    getdata = pullWeatherFromSource(city)
    return jsonify(getdata)



if __name__ == '__main__':
    app.run(debug = True)    