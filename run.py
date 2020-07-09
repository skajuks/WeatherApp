from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re, random
from flask import Flask, render_template, request, jsonify

def picCheck(status):
    x = status.lower()
    print(x)
    if re.findall("clo", x):
        return "cloud"
    elif re.findall("sno", x):
        return "snow"
    elif re.findall("rain", x) or re.findall("sho", x):
        return "rain"
    elif re.findall("sun", x):
        return "sun"
    elif re.findall("ligh", x) or re.findall("thun", x) or re.findall("sto", x):
        return "lightning"
    else:
        return "Cloudy"

def cloudCheck(status):
    x = status.lower()
    print(x)
    if re.findall("sno", x):
        return "Snow"
    elif re.findall("rain", x) or re.findall("sho", x):
        return "Rain"
    elif re.findall("sun", x) or re.findall("fai", x):
        return "Sunny"
    elif re.findall("ligh", x) or re.findall("thun", x) or re.findall("sto", x):
        return "Lightning"
    else:
        return "Cloudy"

def driverf():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://weather.com")
    return driver
def find_city(driver, cityname):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "LocationSearch_input"))).click()   
    driver.find_element_by_id("LocationSearch_input").send_keys(cityname)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "LocationSearch_listbox-0"))).click()

def farenh_to_celsius(farenh):
    celsius = re.sub("°", "", farenh)
    #celsius = round(((int(celsius) - 32) * 5 / 9), 1)
    return str(celsius)      

def pull_data(driver):    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, r"/html/body/div[1]/div[3]/div[2]/div/div/div/div[1]/div[1]/div/div[1]/a[2]/span[1]")))  
    city = driver.find_element_by_xpath(r"/html/body/div[1]/div[3]/div[2]/div/div/div/div[1]/div[1]/div/div[1]/a[2]/span[1]").text
    farenh = driver.find_element_by_xpath(r"/html/body/div[1]/main/div[2]/div[2]/div[1]/div/section/div/div[2]/div[1]/span").text
    celsius = farenh_to_celsius(farenh) 
    as_of = driver.find_element_by_xpath(r"/html/body/div[1]/main/div[2]/div[2]/div[1]/div/section/div/div[1]/div").text
    clouds = driver.find_element_by_xpath(r"/html/body/div[1]/main/div[2]/div[2]/div[1]/div/section/div/div[2]/div[1]/div").text
    real_feel = driver.find_element_by_xpath(r"/html/body/div[1]/main/div[2]/div[2]/div[5]/section/div[1]/div[1]/span[1]").text
    sun_down = driver.find_element_by_xpath(r"/html/body/div[1]/main/div[2]/div[2]/div[5]/section/div[1]/div[2]/div/div/div/div[2]/p").text
    sun_up = driver.find_element_by_xpath(r"/html/body/div[1]/main/div[2]/div[2]/div[5]/section/div[1]/div[2]/div/div/div/div[1]/p").text
    uv_index = driver.find_element_by_xpath(r"/html/body/div[1]/main/div[2]/div[2]/div[5]/section/div[2]/div[6]/div[2]/span").text
    humidity = driver.find_element_by_xpath(r"/html/body/div[1]/main/div[2]/div[2]/div[5]/section/div[2]/div[3]/div[2]/span").text
    return city,celsius,as_of,clouds,real_feel,sun_down,sun_up,uv_index,humidity

def switch_to_10day(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, r"/html/body/div[1]/div[3]/div[3]/nav/div/div[1]/a[3]/span"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, r"/html/body/div[1]/main/div[2]/div[2]/div[1]/section/div[2]/details[1]/div/div/p")))
    description = driver.find_element_by_xpath(r"/html/body/div[1]/main/div[2]/div[2]/div[1]/section/div[2]/details[1]/div/div/p").text

    tonight_clouds = driver.find_element_by_xpath(r"/html/body/div[1]/main/div[2]/div[2]/div[1]/section/div[2]/details[1]/summary/div/div/div[2]/span").text
    tonight_clouds = cloudCheck(tonight_clouds)
    tonight_temperature = driver.find_element_by_xpath(r"/html/body/div[1]/main/div[2]/div[2]/div[1]/section/div[2]/details[1]/summary/div/div/div[1]/span[2]/span").text
    tonight_humidity = driver.find_element_by_xpath(r"/html/body/div[1]/main/div[2]/div[2]/div[1]/section/div[2]/details[1]/summary/div/div/div[3]/span").text

    tomorrow_clouds = driver.find_element_by_xpath(r"/html/body/div[1]/main/div[2]/div[2]/div[1]/section/div[2]/details[2]/summary/div/div/div[2]/span").text
    tomorrow_clouds = cloudCheck(tomorrow_clouds)
    tomorrow_temperature = driver.find_element_by_xpath(r"/html/body/div[1]/main/div[2]/div[2]/div[1]/section/div[2]/details[2]/summary/div/div/div[1]/span[2]/span").text
    tomorrow_humidity = driver.find_element_by_xpath(r"/html/body/div[1]/main/div[2]/div[2]/div[1]/section/div[2]/details[2]/summary/div/div/div[3]/span").text

    tomorrow_clouds2 = driver.find_element_by_xpath(r"/html/body/div[1]/main/div[2]/div[2]/div[1]/section/div[2]/details[3]/summary/div/div/div[2]/span").text
    tomorrow_clouds2 = cloudCheck(tomorrow_clouds2)
    tomorrow_temperature2 = driver.find_element_by_xpath(r"/html/body/div[1]/main/div[2]/div[2]/div[1]/section/div[2]/details[3]/summary/div/div/div[1]/span[2]/span").text
    tomorrow_humidity2 = driver.find_element_by_xpath(r"/html/body/div[1]/main/div[2]/div[2]/div[1]/section/div[2]/details[3]/summary/div/div/div[3]/span").text

    driver.close()
    return description,tonight_clouds,tonight_temperature,tonight_humidity,tomorrow_clouds,tomorrow_temperature,tomorrow_humidity,tomorrow_clouds2,tomorrow_temperature2,tomorrow_humidity2

def backgrounds(today_clouds, tonight_clouds, tomorrow_clouds, tomorrow_clouds2):
    background_list_cloud = [
        "clouds.jpg",
        "clouds2.jpg",
        "clouds3.jpg",
        "clouds4.jpg",
        "clouds5.jpg",
    ]
    background_list_snow = ["snow.jpg", "snow2.jpg", "snow3.jpg", "snow4.jpg"]
    background_list_sun = ["sun.jpg", "sun2.jpg", "sun3.jpg", "sun4.jpg", "sun5.jpg"]
    background_list_rain = ["rain.jpg", "rain2.jpg", "rain3.jpg"]
    img = "default"
    bck_link = ""
    x = today_clouds.lower()
    if re.findall("clo", x):
        clouds = "Cloudy"
        img = "cloud"
        bck_link = random.choice(background_list_cloud)
    elif re.findall("sno", x):
        clouds = "Snow"
        img = "snow"
        bck_link = random.choice(background_list_snow)
    elif re.findall("rain", x) or re.findall("sho", x):
        clouds = "Rain"
        img = "rain"
        bck_link = random.choice(background_list_rain)
    elif re.findall("sun", x):
        clouds = "Sunny"
        img = "sun"
        bck_link = random.choice(background_list_sun)
    elif re.findall("ligh", x) or re.findall("thun", x) or re.findall("sto", x):
        clouds = "Lightning"
        img = "lightning"
        bck_link = "lightning.jpg"
    else:
        clouds = "Cloudy"
        img = "cloud"
        bck_link = random.choice(background_list_cloud)

    img_link = r"../static/weather_images/" + img + r".png"
    bck_link = r"background-image: url(../static/" + bck_link + r"?252552);"
    tn_img_link = r"../static/weather_images/" + picCheck(tonight_clouds) + r".png"
    tm_img_link = r"../static/weather_images/" + picCheck(tomorrow_clouds) + r".png"
    tmn_img_link = r"../static/weather_images/" + picCheck(tomorrow_clouds2) + r".png"
    return img_link,bck_link,tn_img_link,tm_img_link,tmn_img_link

def runthisbitch(city):
    driver = driverf()
    find_city(driver,city)
    city2,celsius,as_of,clouds,real_feel,sun_down,sun_up,uv_index,humidity = pull_data(driver)
    description,tonight_clouds,tonight_temperature,tonight_humidity,tomorrow_clouds,tomorrow_temperature,tomorrow_humidity,tomorrow_clouds2,tomorrow_temperature2,tomorrow_humidity2 = switch_to_10day(driver) 
    img_link,bck_link,tn_img_link,tm_img_link,tmn_img_link = backgrounds(clouds, tonight_clouds, tomorrow_clouds,tomorrow_clouds2)
    weatherData = {
        "currcity": city2,
        "image": img_link,
        "asof": as_of,
        "weather": clouds,
        "temperaturece": celsius,
        "realfeel": "Feels Like " + real_feel + "°C",
        "sunrise": sun_up,
        "sunset": sun_down,
        "description": description,
        "uvindex": uv_index,
        "humidity": humidity,
        "currbcg": bck_link,
        "tonighttemp": tonight_temperature + "°C",
        "tonighthl": tonight_humidity,
        "tonightclouds": tonight_clouds,
        "tonightimg": tn_img_link,
        "tomorrowtemp": tomorrow_temperature + "°C",
        "tomorrowhl": tomorrow_humidity,
        "tomorrowclouds": tomorrow_clouds,
        "tomorrowimg": tm_img_link,
        "tnt": tomorrow_temperature2 + "°C",
        "tnhl": tomorrow_humidity2,
        "tnclouds": tomorrow_clouds2,
        "tnimage": tmn_img_link,
    }
    return weatherData     
app = Flask(__name__)

@app.route("/")
def asdas():
    return render_template("WeatherApp.html")

@app.route("/city")
def mainpage():
    return "as"

@app.route("/city/<city>", methods=["GET"])
def mainpage_post(city=None):
    city = city
    getdata = runthisbitch(city)
    return jsonify(getdata)

if __name__ == "__main__":
    app.run(debug=True)