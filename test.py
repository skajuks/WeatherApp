import re
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
    elif re.findall("sun",x):
        status = "Sunny"
        return status
    elif re.findall("ligh",x) or re.findall("thun",x) or re.findall("sto",x): 
        status = "Lightning"
        return status
    

print(cloudCheck("Stormy"))
