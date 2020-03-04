
from selenium import webdriver
from time import sleep
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome.options import Options 
import requests, re, random
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify



#todo

#animated loading while getting data
#switch celsius / f 
#my contacts
#add auto refresh for weather


def cloudCheck(status):
    x = status.lower()
    print(x)
    if re.findall("clo",x):
        status = "Cloudy"
        return status
    elif re.findall("sno",x):
        status = "Snow"
        return status
    elif re.findall("rain",x) or re.findall("sho",x):
        status = "Rain"
        return status    
    elif re.findall("sun",x) or re.findall("fai",x):
        status = "Sunny"
        return status
    elif re.findall("ligh",x) or re.findall("thun",x) or re.findall("sto",x): 
        status = "Lightning"
        return status
    else:
        status = "Cloudy"
        return status    

def picCheck(status):
    x = status.lower()
    print(x)
    if re.findall("clo",x):
        status = "cloud"
        return status
    elif re.findall("sno",x):
        status = "snow"
        return status
    elif re.findall("rain",x) or re.findall("sho",x):
        status = "rain"
        return status    
    elif re.findall("sun",x):
        status = "sun"
        return status
    elif re.findall("ligh",x) or re.findall("thun",x) or re.findall("sto",x): 
        status = "lightning"
        return status
    else:
        status = "Cloudy"
        return status




def pullWeatherFromSource(cityname):    
    chrome_options = Options() 
    chrome_options.add_argument("--headless") 
    driver = webdriver.Chrome(r'C:\Users\roberts\Documents\chromedriver.exe', chrome_options=chrome_options)
    driver.get("https://weather.com")
    sleep(2)
    driver.find_element_by_xpath(r'/html/body/div[1]/div/div/div[7]/div[1]/div/div/div/div[2]/div/div/div[1]/div/input')\
    .click()
    sleep(1)
    driver.find_element_by_xpath(r'/html/body/div[1]/div/div/div[7]/div[1]/div/div/div/div[2]/div/div/div[1]/div/input')\
    .send_keys(cityname)
    sleep(1)
    driver.find_element_by_xpath(r'//a[@class="styles__item__sCSPm"]')\
    .click()
    sleep(1)

    page = driver.page_source.encode('utf-8')
        
    soup = BeautifulSoup(page, 'html.parser')
    #filter values from class with same name
    c_list = []
    for c in soup.find_all(class_="today-daypart-temp"):
        c_list.append(c.text)
    print(c_list)

    #gathers information from div classes/ main weather info
    city = soup.find(class_="h4 today_nowcard-location").get_text()
    farenh = soup.find(class_="today_nowcard-temp").get_text()
    celsius = re.sub("°", '', farenh)
    celsius = round(((int(celsius)- 32) * 5/9),1)
    as_of = soup.find(class_="today_nowcard-timestamp").get_text()
    clouds = soup.find(class_="today_nowcard-phrase").get_text()
    temperaturec = (str(celsius))
    

    real_feel_f = soup.find(class_="today_nowcard-feels").get_text()
    real_feel_c = re.sub("Feels Like ", '', real_feel_f)
    real_feel_c = re.sub("°", '', real_feel_c)
    real_feel_c = round(((int(real_feel_c)- 32) * 5/9),1)
    real_feel_c = (str(real_feel_c))

    sun_down = soup.find(id="dp0-details-sunset").get_text()
    sun_up = soup.find(id="dp0-details-sunrise").get_text()
    description = soup.find(id="dp0-details-narrative").get_text()
    uv_index = soup.find(id="dp0-details-uvIndex").get_text()
    humidity = soup.find(class_="wx-detail-value").get_text()
    #----------------------------------------------------------------#
    tonight_clouds = soup.find(id="dp0-phrase").get_text()
    print(tonight_clouds)
    tonight_clouds = cloudCheck(tonight_clouds)
    print(tonight_clouds)
    tonight_highlow = soup.find(id="dp0-highLow").get_text()
    tonight_temperaturec = re.sub("°", '', c_list[0])
    tonight_temperaturec = round(((int(tonight_temperaturec)- 32) * 5/9),1)
    tonight_temperaturec = (str(tonight_temperaturec))
    #--------------------------------------------------------------#
    tomorrow_clouds = soup.find(id="dp1-phrase").get_text()
    tomorrow_clouds = cloudCheck(tomorrow_clouds)
    tomorrow_highlow = soup.find(id="dp1-highLow").get_text()
    tomorrow_temperaturec = re.sub("°", '', c_list[1])
    tomorrow_temperaturec = round(((int(tomorrow_temperaturec)- 32) * 5/9),1)
    tomorrow_temperaturec = (str(tomorrow_temperaturec))
    #---------------------------------------------------------------#
    tn_clouds = soup.find(id="dp2-phrase").get_text()
    tn_clouds = cloudCheck(tn_clouds)
    tn_hl = soup.find(id="dp2-highLow").get_text() 
    tn_t = re.sub("°", '', c_list[2])
    tn_t = round(((int(tn_t)- 32) * 5/9),1)
    tn_t = (str(tn_t))






    driver.close()

    background_list_cloud = ['clouds.jpg', 'clouds2.jpg','clouds3.jpg','clouds4.jpg','clouds5.jpg']
    background_list_snow = ['snow.jpg', 'snow2.jpg', 'snow3.jpg', 'snow4.jpg']
    background_list_sun = ['sun.jpg', 'sun2.jpg', 'sun3.jpg', 'sun4.jpg', 'sun5.png']
    background_list_rain = ['rain.jpg', 'rain2.jpg', 'rain3.jpg']

    
    img = 'default'
    bck_link = ''
    x = clouds.lower()
    if re.findall("clo",x):
        clouds = "Cloudy"
        img = 'cloud'
        bck_link = random.choice(background_list_cloud)
    elif re.findall("sno",x):
        clouds = "Snow"
        img = 'snow'
        bck_link = random.choice(background_list_snow)
    elif re.findall("rain",x) or re.findall("sho",x):
        clouds = "Rain"
        img = 'rain'
        bck_link = random.choice(background_list_rain)
    elif re.findall("sun",x):
        clouds = "Sunny"
        img = 'sun'
        bck_link = random.choice(background_list_sun)
    elif re.findall("ligh",x) or re.findall("thun",x) or re.findall("sto",x): 
        clouds = "Lightning"
        img = 'lightning'
        bck_link = 'lightning.jpg'
    else:
        clouds = "Cloudy"
        img = 'cloud'
        bck_link = random.choice(background_list_cloud)   
    
            
    img_link = r'../static/weather_images/' + img + r'.png'
    bck_link = r'background-image: url(../static/' + bck_link + r'?252552);'
    tn_img_link = r'../static/weather_images/' + picCheck(tonight_clouds) + r'.png'
    tm_img_link = r'../static/weather_images/' + picCheck(tomorrow_clouds) + r'.png'
    tmn_img_link = r'../static/weather_images/' + picCheck(tn_clouds) + r'.png'
    print(tn_img_link)

    weatherData = {
        "currcity": city,
        "image": img_link,
        "asof": as_of,
        "weather": clouds,
        "temperaturece": temperaturec + "°C",
        "temperaturefa": farenh,
        "realfeel": "Feels Like " + real_feel_c + "°C",
        "sunrise": sun_up,
        "sunset": sun_down,
        "description": description,
        "uvindex": uv_index,
        "humidity": humidity,
        "currbcg": bck_link,
        "tonighttemp": tonight_temperaturec + "°C",
        "tonighthl": tonight_highlow,
        "tonightclouds": tonight_clouds,
        "tonightimg": tn_img_link,
        "tomorrowtemp": tomorrow_temperaturec + "°C",
        "tomorrowhl": tomorrow_highlow,
        "tomorrowclouds": tomorrow_clouds,
        "tomorrowimg": tm_img_link,
        "tnt": tn_t + "°C",
        "tnhl": tn_hl,
        "tnclouds": tn_clouds,
        "tnimage": tmn_img_link
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